#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <mutex>
#include <thread>
#include <atomic>
#include <windows.h>


const int size_vector = 25000000;
const int DIVISOR = 19;

// Функція для заповнення масиву рандомними числами
std::vector<int> generateRandomNumbers(int size_vector) { // Приймаємо розмір вектора як параметр
    std::vector<int> numbers(size_vector);
    for (int i = 0; i < size_vector; i++) 
    { // Використовуємо індексний доступ до елементів вектора
        numbers[i] = rand() % 100000 + 1;  // Заповнюємо вектор випадковими числами
    }
    return numbers;
}

// Функція виводу результатів
void Print(int count, int min) {
    std::cout << "Кількість чисел що ділятся на 19: " << count << std::endl;
    std::cout << "Найменше число: " << min << std::endl;
}

// Однопоточне рішення
void SingleThreadSolution(std::vector<int>& numbers) {
    auto start = std::chrono::high_resolution_clock::now();
    int count = 0;
    int min = INT_MAX;
    // Змінюємо цикл на індексований доступ
    for (int i = 0; i < numbers.size(); i++)
    {
        int num = numbers[i];  // Отримуємо поточне число з вектора
        if (num % DIVISOR == 0)
        {
            count++;  // Інкрементуємо лічильник, якщо число кратне DIVISOR
            if (num < min) 
            {
                min = num;  // Оновлюємо мінімальне значення, якщо поточне число менше поточного мінімуму
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;  // Обчислюємо час виконання

    Print(count, min);  // Виводимо результати
    std::cout << "Пройдений час: " << elapsed.count() << " секунд" << std::endl;
}


// Обробка частини вектора чисел у многопоточному режимі з використанням мютекс

/*
void processPart (std::vector<int>& numbers, int start, int end, int& count, int& min, std::mutex& mtx) {
    
    int local_count = 0;  // Локальний лічильник для зберігання кількості чисел, кратних DIVISOR
    int local_min = INT_MAX;  // Локальна мінімальна змінна для знаходження найменшого числа, кратного DIVISOR

    // Прохід по частині вектора
    for (int i = start; i < end; i++) {
        if (numbers[i] % DIVISOR == 0) {  
            local_count++;  
            if (numbers[i] < local_min) {  // Пошук нового мінімуму
                local_min = numbers[i];
            }
        }
    }
    // Блокування мютексу для безпечного оновлення загальних змінних
    mtx.lock();
    count += local_count;  // Додавання локального лічильника до загального
    if (local_min < min) {  // Оновлення загальної мінімальної змінної, якщо знайдено новий мінімум
        min = local_min;
    }
    mtx.unlock();  // Розблокування мютексу
}
*/


void processPart(std::vector<int>& numbers, int start, int end, int& count, int& min, std::mutex& mtx) {
    for (int i = start; i < end; i++) {
        if (numbers[i] % DIVISOR == 0) {
            mtx.lock();
            count++;
            if (numbers[i] < min) {  // Пошук нового мінімуму
                min = numbers[i];
            }
            mtx.unlock();
        }
    }
}



// Многопоточна обробка вектора чисел із використанням мютексу для синхронізації
void multiThreadedSolutionWithMutex(std::vector<int>& numbers, int num_threads) {
    
    int count = 0;  // Загальний лічильник чисел, кратних DIVISOR
    int min = INT_MAX;  // Загальний мінімум серед чисел, кратних DIVISOR
    std::vector<std::thread> threads;  // Вектор потоків
    std::mutex mtx;  // Мютекс для синхронізації

    int part_size = size_vector / num_threads;  // Розмір частини вектора для кожного потоку
    auto start = std::chrono::high_resolution_clock::now();  // Початок вимірювання часу

    for (int i = 0; i < num_threads; ++i) {
        int start_index = i * part_size;
        int end_index;
        if (i == num_threads - 1) 
        {
            end_index = size_vector;  // Останній потік бере всі решта елементи
        }
        else
        {
            end_index = start_index + part_size;  // Нормальний випадок для інших потоків
        }
        threads.emplace_back(processPart, std::ref(numbers), start_index, end_index, std::ref(count), std::ref(min), std::ref(mtx));
    }

    for (auto& thread : threads)
    {
        thread.join();  // Очікування завершення всіх потоків
    }

    auto end = std::chrono::high_resolution_clock::now();  // Кінець вимірювання часу
    std::chrono::duration<double> elapsed = end - start;  // Обчислення тривалості виконання

    Print(count, min);  // Вивід результатів
    std::cout << "Пройдений час: " << elapsed.count() << " секунд" << std::endl;
}

// Обробка частини вектора чисел у многопоточному режимі з використанням атоміків

/*
void atomicProcessPart(std::vector<int>& numbers, int start, int end, std::atomic<int>& count, std::atomic<int>& min) {
    
    int local_count = 0;
    int local_min = INT_MAX;  

    for (int i = start; i < end; ++i) 
    {
        if (numbers[i] % DIVISOR == 0)
        {
            local_count++;
            int current_min = min.load();
            do {
                if (current_min <= numbers[i]) break;
            } while (!min.compare_exchange_weak(current_min, numbers[i]));
        }
    }

    count.fetch_add(local_count); 
}
*/

/*
void atomicProcessPart(std::vector<int>& numbers, int start, int end, std::atomic<int>& count, std::atomic<int>& min) {
    for (int i = start; i < end; ++i) {
        if (numbers[i] % DIVISOR == 0) {
            ++count;  // Атомарне збільшення лічильника
            int current_min = min.load();
            while (numbers[i] < current_min && !min.compare_exchange_weak(current_min, numbers[i]));
        }
    }
}
*/


void atomicProcessPart(std::vector<int>& numbers, int start, int end, std::atomic<int>& count, std::atomic<int>& min) {
    for (int i = start; i < end; ++i) {
        if (numbers[i] % DIVISOR == 0) 
        {
            count.fetch_add(1);
            int current_min = min.load();
            while (numbers[i] < current_min && !min.compare_exchange_weak(current_min, numbers[i]));
        }
    }
}


// Многопоточна обробка вектора чисел із використанням атомічних змінних
void multiThreadedSolutionWithAtomic(std::vector<int>& numbers, int num_threads) {
    std::atomic<int> count(0);
    std::atomic<int> minimum(INT_MAX);  // Використання INT_MAX для ініціалізації мінімуму
    std::vector<std::thread> threads;

    int part_size = size_vector / num_threads;
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i) {
        int start_index = i * part_size;
        int end_index;
        if (i == num_threads - 1) 
        {
            end_index = size_vector;  // Останній потік бере всі решта елементи
        }
        else 
        {
            end_index = start_index + part_size;  // Нормальний випадок для інших потоків
        }
        threads.emplace_back(atomicProcessPart, std::ref(numbers), start_index, end_index, std::ref(count), std::ref(minimum));
    }

    for (auto& thread : threads) {
        thread.join();  // Очікування завершення всіх потоків
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;  // Обчислення тривалості виконання

    Print(count.load(), minimum.load());  // Вивід результатів
    std::cout << "Пройдений час " << elapsed.count() << " секунд" << std::endl;
}


int main() 
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    srand(time(NULL));

    int thread_count;
    std::cout << "Введіть кількість потоків: ";
    std::cin >> thread_count;

    std::cout << std::endl;

    std::vector<int> numbers = generateRandomNumbers(size_vector);

    std::cout << "Без використання паралелезації: " << std::endl;
    SingleThreadSolution(numbers);

    std::cout << std::endl;

    std::cout << "З використанням мютекса: " << std::endl;
    multiThreadedSolutionWithMutex(numbers, thread_count);

    std::cout << std::endl;

    std::cout << "З використанням атоманрих змінних: " << std::endl;
    multiThreadedSolutionWithAtomic(numbers, thread_count);


    return 0;
}
