#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <chrono>
#include <windows.h>

class Task {
public:
    std::function<void()> func;
    int id;

    Task(std::function<void()> f, int i) : func(std::move(f)), id(i) {}
};

class TaskQueue {
private:
    std::queue<Task> tasks;
    std::mutex queue_mutex;
    std::condition_variable cond_var;
    bool stop;
    bool paused;
    int task_id;

public:
    TaskQueue() : stop(false), paused(false), task_id(0) {}

    void addTask(const std::function<void()>& task) {
        std::unique_lock<std::mutex> lock(queue_mutex);
        if (stop) return;
        tasks.emplace(task, ++task_id);
        std::cout << "Завдання №" << task_id << " додано в чергу\n";
        cond_var.notify_one();
    }

    Task getTask() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        while (tasks.empty() && !stop && !paused) {
            cond_var.wait(lock);
        }
        if ((stop && tasks.empty()) || paused) {
            return { nullptr, 0 };
        }
        Task task = std::move(tasks.front());
        tasks.pop();
        return task;
    }

    void pause() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        paused = true;
        cond_var.notify_all();
    }

    void resume() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        paused = false;
        cond_var.notify_all();
    }

    void stopQueue(bool finishCurrentTasks = false) {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true;
        if (!finishCurrentTasks) {
            tasks = {};  // Clear all pending tasks
        }
        cond_var.notify_all();
    }

    bool isStopped() const {
        return stop;
    }

    bool isPaused() const {
        return paused;
    }

    void clear() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        while (!tasks.empty()) {
            tasks.pop();
        }
    }

    ~TaskQueue() {
        stopQueue();
        clear();
    }
};

class ThreadPool {
private:
    std::vector<std::thread> workers;
    TaskQueue& queue;
    std::vector<double> total_execution_time;
    std::vector<int> execution_count;

public:
    ThreadPool(TaskQueue& q, int workers_count) : queue(q) {
        total_execution_time.resize(workers_count, 0.0);
        execution_count.resize(workers_count, 0);

        for (int i = 0; i < workers_count; ++i) {
            workers.emplace_back([this, i] { this->worker(i); });
        }
    }

    void worker(int id) {
        while (!queue.isStopped() || !queue.isPaused()) {
            auto task = queue.getTask();
            if (task.func) {
                std::cout << "Завдання №" << task.id << " початок виконання\n";
                auto start_time = std::chrono::high_resolution_clock::now();
                task.func();
                auto end_time = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> elapsed = end_time - start_time;
                total_execution_time[id] += elapsed.count();
                execution_count[id]++;
                std::cout << "Завдання №" << task.id << " виконано за " << elapsed.count() << " секунд\n";
            }
        }
    }

    void printStatistics() {
        double total_time = 0;
        int total_tasks = 0;
        for (size_t i = 0; i < total_execution_time.size(); i++) {
            total_time += total_execution_time[i];
            total_tasks += execution_count[i];
        }
        std::cout << "Загальний час виконання: " << total_time << " секунд\n";
        std::cout << "Загальна кількість завдань: " << total_tasks << "\n";
        if (total_tasks > 0) {
            std::cout << "Середній час виконання задачі: " << (total_time / total_tasks) << " секунд\n";
        }
    }

    void stop(bool finishCurrentTasks = false) {
        queue.stopQueue(finishCurrentTasks);
        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    ~ThreadPool() {
        stop();
    }
};

void taskProducer(TaskQueue& queue) {
    while (!queue.isStopped()) {
        int sleep_time = 10 + rand() % 7;
        if (!queue.isPaused()) {
            queue.addTask([sleep_time] {
                std::this_thread::sleep_for(std::chrono::seconds(sleep_time));
                });
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}

int main() {
    srand(time(NULL));
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    TaskQueue queue;
    ThreadPool pool(queue, 8);

    std::thread producer([&queue] { taskProducer(queue); });

    char command;
    std::cout << "Enter 'p' to pause, 'r' to resume and 'q' to quit:\n";
    while (std::cin >> command && command != 'q') {
        if (command == 'p') {
            queue.pause();
            std::cout << "Execution paused.\n";
        }
        else if (command == 'r') {
            queue.resume();
            std::cout << "Execution resumed.\n";
        }
    }

    pool.stop(true);  // Ensure all threads are stopped before printing statistics
    pool.printStatistics();  // Manually call to print statistics

    producer.join();
    return 0;
}
