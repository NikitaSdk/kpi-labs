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

    Task(const std::function<void()>& f, int i)
    {
        func = f;
        id = i;
    }
};

class TaskQueue {
private:
    std::queue<Task> tasks;
    std::mutex queue_mutex;
    std::condition_variable cond_var;
    bool stop = false;
    bool paused = false;
    int task_id = 0;

public:
    void addTask(const std::function<void()>& task) {
        std::unique_lock<std::mutex> lock(queue_mutex);
        if (!stop) {
            tasks.emplace(task, ++task_id);
            std::cout << "Завдання №" << task_id << " додано в чергу" << std::endl;
            cond_var.notify_one();
        }
    }

    Task getTask() {
        std::unique_lock<std::mutex> lock(queue_mutex);

        cond_var.wait(lock, [this]() { return stop || !tasks.empty() || paused; });
        if ((stop && tasks.empty()) || paused) {
            return Task(nullptr, 0);
        }
        Task task = tasks.front();
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

    void stopQueue() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true;
        tasks = {};
        cond_var.notify_all();
    }

    bool isStopped() {
        return stop;
    }

    bool isPaused() {
        return paused;
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
        for (int i = 0; i < workers_count; i++) {
            workers.emplace_back([this, i]() { this->worker(i); });
        }
    }

    void worker(int id) {
        while (!queue.isStopped()) {
            Task task = queue.getTask();
            if (task.func) {
                std::cout << "Завдання №" << task.id << " початок виконання" << std::endl;
                auto start_time = std::chrono::high_resolution_clock::now();
                task.func();
                auto end_time = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> elapsed = end_time - start_time;
                total_execution_time[id] += elapsed.count();
                execution_count[id]++;
                std::cout << "Завдання №" << task.id << " виконано за " << elapsed.count() << " секунд" << std::endl;
            }
        }
    }

    void stop() {
        queue.stopQueue();
        for (auto& worker : workers) {
            if (worker.joinable()) { 
                worker.join();
            }
        }
    }

    void printStatistics() {
        double total_time = 0;
        int total_tasks = 0;

        for (int i = 0; i < total_execution_time.size(); i++) {
            total_time += total_execution_time[i];
            total_tasks += execution_count[i];
        }
        std::cout << "Сумма часу всіх задач: " << total_time << " секунд" << std::endl;
        std::cout << "Загальна кількість виконаних завдань: " << total_tasks << std::endl;
        if (total_tasks > 0) {
            std::cout << "Середній час виконання задачі: " << (total_time / total_tasks) << " секунд" << std::endl;
        }
    }
};

void taskProducer(TaskQueue& queue) {
    while (!queue.isStopped()) {
        int sleep_time = 10 + rand() % 7;
        if (!queue.isPaused()) {
            queue.addTask([sleep_time] { std::this_thread::sleep_for(std::chrono::seconds(sleep_time)); });
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(2000));
    }
}

int main() {
    srand(time(NULL));

    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    TaskQueue queue;
    ThreadPool pool(queue, 8);

    std::thread producer([&queue]() {taskProducer(queue); });

    char command;
    std::cout << "Введіть 'p' для паузи, 'r' для відновлення і 'q' для завершення:" << std::endl;
    while (std::cin >> command && command != 'q') {
        if (command == 'p') {
            queue.pause();
            std::cout << "Роботу зупинено." << std::endl;
        }
        else if (command == 'r') {
            queue.resume();
            std::cout << "Роботу відновлено." << std::endl;
        }
    }

    pool.stop();
    pool.printStatistics();

    producer.join();
    return 0;
}
