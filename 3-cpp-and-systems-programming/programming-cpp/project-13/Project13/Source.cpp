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

        // Чекаємо на зміну умови: зупинка черги, наявність завдань або пауза
        cond_var.wait(lock, [this]() { return stop || !tasks.empty() || paused; });

        // Якщо черга зупинена і завдання відсутні, або робота пулу призупинена, повертаємо пусте завдання
        if ((stop && tasks.empty()) || paused) {
            return Task(nullptr, 0);
        }

        // В іншому випадку, отримуємо перше завдання з черги
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
};

// Клас пулу потоків, який використовується для управління виконанням завдань в багатопоточному режимі.
class ThreadPool {
private:
    std::vector<std::thread> workers; // Вектор робочих потоків, які виконують завдання.
    TaskQueue& queue; // Посилання на чергу завдань, звідки потоки будуть брати завдання для виконання.
    std::vector<double> total_execution_time; // Вектор для зберігання загального часу виконання для кожного потоку.
    std::vector<int> execution_count; // Вектор для зберігання кількості виконаних завдань кожним потоком.
    std::vector<double> total_waiting_time;

public:
    // Конструктор класу ThreadPool
    ThreadPool(TaskQueue& q, int workers_count) : queue(q) {
        // Ініціалізуємо вектор total_execution_time, де кожен елемент встановлюється на початкове значення 0.0.
        // Цей вектор зберігає загальний час виконання завдань для кожного потоку.
        total_execution_time.resize(workers_count, 0.0);

        // Ініціалізуємо вектор execution_count, де кожен елемент встановлюється на 0.
        // Цей вектор зберігає кількість завдань, виконаних кожним потоком.
        execution_count.resize(workers_count, 0);

        // Цикл створює workers_count потоків у пулі.
        for (int i = 0; i < workers_count; ++i) {
            // Для кожного потоку в пулі створюється лямбда-функція, яка викликає метод worker(i),
            // де i - індекс потоку. Ця функція визначена в класі ThreadPool і відповідає за обробку завдань.
            workers.emplace_back([this, i]() { this->worker(i); });
        }
    }

    void worker(int id) {
        while (!queue.isStopped()) {
            auto start_waiting = std::chrono::high_resolution_clock::now(); // Фіксація часу початку очікування
            Task task = queue.getTask(); // Отримання завдання з черги
            auto end_waiting = std::chrono::high_resolution_clock::now(); // Фіксація часу закінчення очікування
            std::chrono::duration<double> elapsed_waiting = end_waiting - start_waiting; // Обчислення тривалості очікування
            total_waiting_time[id] += elapsed_waiting.count(); // Додавання часу очікування до загального часу очікування для цього потоку
            // Решта коду функції
        }
    }

    // Функція зупиняє роботу пулу потоків.
    void stop() {
        queue.stopQueue(); // Зупиняємо чергу завдань, щоб більше не додавались нові завдання і вже додані завдання перестали оброблятись.
        // Проходимось по всім робочим потокам.
        for (auto& worker : workers) {
            // Перевіряємо, чи потік може бути приєднаним (joinable).
            if (worker.joinable()) {
                worker.join(); // Якщо так, то викликаємо join() для цього потоку.
                // Метод join() блокує потік, у якому він викликається, до тих пір, поки потік `worker` не завершить своє виконання.
            }
        }
    }

    void printStatistics() {
        double total_time = 0;
        int total_tasks = 0;
        double total_waiting = 0; // Загальний час очікування для всіх потоків

        for (size_t i = 0; i < total_execution_time.size(); i++) {
            total_time += total_execution_time[i]; // Сумуємо часи виконання
            total_tasks += execution_count[i]; // Сумуємо кількість завдань
            total_waiting += total_waiting_time[i]; // Сумуємо часи очікування
        }

        std::cout << "Сума часу всіх завдань: " << total_time << " секунд\n";
        std::cout << "Загальна кількість завдань: " << total_tasks << "\n";

        if (total_tasks > 0) {
            std::cout << "Середній час виконання завдання: " << (total_time / total_tasks) << " секунд\n";
            std::cout << "Середній час очікування потоку: " << (total_waiting / total_tasks) << " секунд\n";
        }
    }
};


// Функція для додавання завдань до черги. Виконується в окремому потоці.
void taskProducer(TaskQueue& queue) {
    while (!queue.isStopped()) { // Поки черга не зупинена, виконуємо цикл.
        int sleep_time = 10 + rand() % 7; // Генеруємо випадковий час виконання завдання від 10 до 16 секунд.
        if (!queue.isPaused()) { // Якщо черга не на паузі, додаємо завдання.
            // Додаємо завдання до черги. Завдання полягає у затримці на випадковий час.
            queue.addTask([sleep_time] { std::this_thread::sleep_for(std::chrono::seconds(sleep_time)); });
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(2000)); // Призупиняємо потік на 2000 мілісекунд (2 секунди).
    }
}


int main() {
    srand(time(NULL));

    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    TaskQueue queue;
    ThreadPool pool(queue, 8);

    std::thread producer( [&queue]() { taskProducer(queue); });

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

    pool.stop();  // Ensure all threads are stopped before printing statistics
    pool.printStatistics();  // Manually call to print statistics

    producer.join();
    return 0;
}
