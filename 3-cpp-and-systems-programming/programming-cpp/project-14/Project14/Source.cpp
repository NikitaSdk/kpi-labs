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
    std::function<void()> func; // Функціональний об'єкт, який виконує завдання
    int id;                      // Ідентифікатор завдання

    Task(const std::function<void()>& f, int i)
    {
        func = f; // Присвоюємо функцію
        id = i;   // Присвоюємо ідентифікатор
    }
};

class TaskQueue {
private:
    std::queue<Task> tasks;      // Черга завдань
    std::mutex queue_mutex;      // Мютекс для синхронізації доступу до черги
    std::condition_variable cond_var; // Умовна змінна для управління доступом до черги
    bool stop = false;           // Флаг для зупинки черги
    bool paused = false;         // Флаг для паузи черги
    int task_id = 0;             // Лічильник завдань

    // Додамо змінну для збереження часу очікування потоку в стані очікування
    std::chrono::steady_clock::time_point start_waiting_time;

public:
    void addTask(const std::function<void()>& task) {
        // Блокуємо м'ютекс для синхронізації доступу до черги завдань
        std::unique_lock<std::mutex> lock(queue_mutex);

        // Перевіряємо, чи пул потоків не зупинено
        if (!stop) {
            // Використовуємо emplace для оптимального додавання нового завдання в кінець черги.
            // std::function<void()> обгортка дозволяє передавати будь-яку викликальну одиницю.
            // task_id - це ідентифікатор завдання, який інкрементується з кожним новим завданням.
            tasks.emplace(task, ++task_id);

            // Виводимо повідомлення про додане завдання, використовуючи поточний ідентифікатор.
            std::cout << "Завдання №" << task_id << " додано в чергу\n";

            // Сповіщаємо один з очікуючих потоків, що нове завдання доступне.
            // Це може розбудити один із сплячих робочих потоків в пулі, який чекає на завдання.
            cond_var.notify_one();
        }
    }

    Task getTask() {
        // Блокуємо м'ютекс для синхронізації доступу до черги завдань
        std::unique_lock<std::mutex> lock(queue_mutex);

        // Отримуємо час початку очікування завдання
        start_waiting_time = std::chrono::steady_clock::now();

        // Чекаємо на зміну умови: зупинка черги, наявність завдань або пауза
        cond_var.wait(lock, [this]() { return stop || !tasks.empty() || paused; });

        // Якщо черга зупинена і завдання відсутні, або робота пулу призупинена, повертаємо пусте завдання
        if ((stop && tasks.empty()) || paused) {
            return Task(nullptr, 0);
        }

        // Вираховуємо час очікування та додаємо його до загального часу очікування потока
        auto end_waiting_time = std::chrono::steady_clock::now();
        double waiting_time = std::chrono::duration<double>(end_waiting_time - start_waiting_time).count();

        // Повертаємо перше завдання з черги
        Task task = tasks.front();

        // Видаляємо завдання з черги
        tasks.pop();

        // Повертаємо завдання для виконання
        return task;
    }

    void pause() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        paused = true; // Встановлюємо паузу
        cond_var.notify_all(); // Сповіщаємо всі потоки
    }

    void resume() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        paused = false; // Знімаємо паузу
        cond_var.notify_all(); // Сповіщаємо всі потоки
    }

    void stopQueue() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true; // Зупиняємо чергу
        tasks = {};  // Очищаємо всі завдання
        cond_var.notify_all(); // Сповіщаємо всі потоки
    }

    bool isStopped() {
        return stop; // Перевіряємо, чи зупинена черга
    }

    bool isPaused() {
        return paused; // Перевіряємо, чи черга на паузі
    }

    std::chrono::steady_clock::time_point getStartWaitingTime() const {
        return start_waiting_time;
    }
};

class ThreadPool {
private:
    std::vector<std::thread> workers; // Вектор робочих потоків, які виконують завдання.
    TaskQueue& queue; // Посилання на чергу завдань, звідки потоки будуть брати завдання для виконання.
    std::vector<double> total_execution_time; // Вектор для зберігання загального часу виконання для кожного потоку.
    std::vector<int> execution_count; // Вектор для зберігання кількості виконаних завдань кожним потоком.
    std::vector<double> total_waiting_time; // Вектор для зберігання загального часу очікування для кожного потоку.

public:
    ThreadPool(TaskQueue& q, int workers_count) : queue(q) {
        total_execution_time.resize(workers_count, 0.0);
        execution_count.resize(workers_count, 0);
        total_waiting_time.resize(workers_count, 0.0);

        for (int i = 0; i < workers_count; ++i) {
            workers.emplace_back([this, i]() { this->worker(i); });
        }
    }

    void worker(int id) {
        while (!queue.isStopped()) {
            Task task = queue.getTask();
            if (task.func) {
                std::cout << "Завдання №" << task.id << " початок виконання\n";

                auto start_time = std::chrono::high_resolution_clock::now();

                task.func();

                auto end_time = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> elapsed = end_time - start_time;

                total_execution_time[id] += elapsed.count();
                execution_count[id]++;

                std::cout << "Завдання №" << task.id << " виконано за " << elapsed.count() << " секунд\n";

                // Зберігаємо час очікування потока
                total_waiting_time[id] += std::chrono::duration<double>(std::chrono::steady_clock::now() - queue.getStartWaitingTime()).count();
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
        double total_waiting = 0; // Додана змінна для обчислення загального часу очікування

        for (size_t i = 0; i < total_execution_time.size(); i++) {
            total_time += total_execution_time[i];
            total_tasks += execution_count[i];
            total_waiting += total_waiting_time[i]; // Додаємо час очікування кожного потоку
        }

        std::cout << "Сумма часу всіх задач: " << total_time << " секунд\n";
        std::cout << "Загальна кількість завдань: " << total_tasks << "\n";
        if (total_tasks > 0) {
            std::cout << "Середній час виконання задачі: " << (total_time / total_tasks) << " секунд\n";
            // Виведемо також середній час очікування
            std::cout << "Середній час очікування потоку: " << (total_waiting / total_tasks) << " секунд\n";
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

    std::thread producer([&queue]() { taskProducer(queue); });

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

    pool.stop();
    pool.printStatistics();

    producer.join();
    return 0;
}
