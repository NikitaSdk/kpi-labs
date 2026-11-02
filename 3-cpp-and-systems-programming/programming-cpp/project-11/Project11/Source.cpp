#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <mutex>
#include <thread>
#include <atomic>
#include <windows.h>

const int DIVISOR = 19;

int** Alloc_Matrix(int size) {
    int** matrix = new int* [size];
    for (int i = 0; i < size; i++) {
        matrix[i] = new int[size];
    }
    return matrix;
}

void Delete_Matrix(int** matrix, int size) {
    for (int i = 0; i < size; i++) {
        delete[] matrix[i];
    }
    delete[] matrix;
}

void Fill_Matrix(int** matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            matrix[i][j] = rand() % 100000 + 1;
        }
    }
}

void Print(int count, int min) {
    std::cout << "Кількість чисел що ділятся на 19: " << count << std::endl;
    std::cout << "Найменше число: " << min << std::endl;
}

void SingleThreadSolution(int** matrix, int size) {
    auto start = std::chrono::high_resolution_clock::now();
    int count = 0;
    int min = INT_MAX;

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            int num = matrix[i][j];
            if (num % DIVISOR == 0) {
                count++;
                if (num < min) {
                    min = num;
                }
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    Print(count, min);
    std::cout << "Пройдений час: " << elapsed.count() << " секунд" << std::endl;
}

// не опт
/*
void MutexCompute(int** matrix, int size, int start, int end, int& count, int& min, std::mutex& mtx) {
    for (int i = start; i < end; i++) {
        for (int j = 0; j < size; j++) {
            if (matrix[i][j] % DIVISOR == 0) 
            {
                mtx.lock();
                count++;
                if (matrix[i][j] < min) 
                {
                    min = matrix[i][j];
                }
                mtx.unlock();
            }
        }
    }
}
*/
// опт
void MutexCompute(int** matrix, int size, int start, int end, int& count, int& min, std::mutex& mtx) {
    int local_count = 0;
    int local_min = INT_MAX;
    for (int i = start; i < end; i++) {
        for (int j = 0; j < size; j++) {
            if (matrix[i][j] % DIVISOR == 0) {
                local_count++;
                if (matrix[i][j] < local_min) {
                    local_min = matrix[i][j];
                }
            }
        }
    }
    mtx.lock();
    count += local_count;
    if (local_min < min) {
        min = local_min;
    }
    mtx.unlock();
}

void ParallelComputeMutex(int** matrix, int size, int num_threads) {
    std::vector<std::thread> threads;
    int segment = size / num_threads;
    int count = 0, min = INT_MAX;
    std::mutex mtx;

    auto start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num_threads; i++) {
        int start_index = i * segment;
        int end_index;
        if (i == num_threads - 1) 
        {
            end_index = size; 
        }
        else 
        {
            end_index = start_index + segment; 
        }
        threads.emplace_back(MutexCompute, matrix, size, start_index, end_index, std::ref(count), std::ref(min), std::ref(mtx));
    }

    for (auto& thread : threads) {
        thread.join();
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    Print(count, min);
    std::cout << "Час виконання з мютексами: " << elapsed.count() << " секунд." << std::endl;
}

// не опт 
/*
void AtomicCompute(int** matrix, int size, int start, int end, std::atomic<int>& count, std::atomic<int>& minimum) {
    for (int i = start; i < end; i++) {
        for (int j = 0; j < size; j++) {
            if (matrix[i][j] % DIVISOR == 0) 
            {
                count.fetch_add(1);
                int current_min = minimum.load();
                do {
                    if (matrix[i][j] >= current_min) {
                        break;
                    }
                } while (!minimum.compare_exchange_weak(current_min, matrix[i][j]));
            }
        }
    }
}
*/
// опт
void AtomicCompute(int** matrix, int size, int start, int end, std::atomic<int>& count, std::atomic<int>& minimum) {
    int local_count = 0;

    for (int i = start; i < end; i++) {
        for (int j = 0; j < size; j++) {
            if (matrix[i][j] % DIVISOR == 0) {
                local_count++;
                int current_min = minimum.load();  
                do {
                    if (matrix[i][j] >= current_min) {
                        break;
                    }
                } while (!minimum.compare_exchange_weak(current_min, matrix[i][j])); 
            }
        }
    }
    count.fetch_add(local_count);  
}

void ParallelComputeAtomic(int** matrix, int size, int num_threads) {
    std::vector<std::thread> threads;
    int segment = size / num_threads;
    std::atomic<int> count(0), minimum(INT_MAX);


    auto start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num_threads; i++) {
        int start_index = i * segment;
        int end_index;
        if (i == num_threads - 1)
        {
            end_index = size; 
        }
        else 
        {
            end_index = start_index + segment; 
        }
        threads.emplace_back(AtomicCompute, matrix, size, start_index, end_index, std::ref(count), std::ref(minimum));
    }

    for (auto& thread : threads) {
        thread.join();
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    Print(count.load(), minimum.load());
    std::cout << "Час виконання з атоміками: " << elapsed.count() << " секунд." << std::endl;
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    srand(time(NULL));


    int N;
    std::cout << "Введіть розмір матриці: ";
    std::cin >> N;

    int num_threads;
    std::cout << "Введіть кількість потоків: ";
    std::cin >> num_threads;

    std::cout << std::endl;

    int** matrix = Alloc_Matrix(N);

    Fill_Matrix(matrix, N);


    std::cout << "Без використання паралелезації: " << std::endl;
    SingleThreadSolution(matrix, N);

    std::cout << std::endl;

    std::cout << "З використанням мютекса: " << std::endl;
    ParallelComputeMutex(matrix, N, num_threads);

    std::cout << std::endl;

    std::cout << "З використанням атоманрих змінних: " << std::endl;
    ParallelComputeAtomic(matrix, N, num_threads);

    Delete_Matrix(matrix, N);

    return 0;
}