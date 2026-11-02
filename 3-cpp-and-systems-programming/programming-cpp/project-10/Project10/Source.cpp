#include <iostream>
#include <Windows.h>
#include <thread>
#include <chrono>
#include <random>
#include <vector>

using std::chrono::nanoseconds;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;


int** Alloc_Matrix(int size)
{
    int** matrix = new int* [size];
    for (int i = 0; i < size; i++)
    {
        matrix[i] = new int[size];
    }
    return matrix;
}


void Delete_Matrix(int** matrix, int size)
{
    for (int i = 0; i < size; i++)
    {
        delete[] matrix[i];
    }
    delete[] matrix;
}


void Fill_Matrix(int** matrix, int size)
{
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            matrix[i][j] = rand() % 10;
        }
    }
}

void Compute(int** matrix, int size, int start, int end)
{
    for (int i = start; i < end; i++)
    {
        for (int j = 0; j < size; j++)
        {
            matrix[size - 1 - i][j] = matrix[i][j];
        }
    }
}

void Parallel_Compute(int** matrix, int size, int num_threads)
{
    auto payload_begin = high_resolution_clock::now();
    std::vector<std::thread> threads;
    int segment_matrix = size / num_threads;
    int start = 0;

    for (int i = 0; i < num_threads; i++)
    {
        int end = start + segment_matrix;
        if (i == num_threads - 1) 
        {
            end = size; 
        }
        threads.emplace_back(Compute, matrix, size, start, end);
        start = end;
    }

    for (auto& thread : threads)
    {
        thread.join();
    }

    auto payload_end = high_resolution_clock::now();
    auto elapsed = duration_cast<nanoseconds>(payload_end - payload_begin);
    std::printf("Payload Time: %.3f seconds.\n", elapsed.count() * 1e-9);
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    srand(time(NULL));

    int size;
    std::cout << "¬вед≥ть розм≥р матриц≥: ";
    std::cin >> size;

    int num_threads;
    std::cout << "¬вед≥ть к≥льк≥сть поток≥в: ";
    std::cin >> num_threads;

    int** matrix = Alloc_Matrix(size);

    Fill_Matrix(matrix, size);

    Parallel_Compute(matrix, size, num_threads);
     
    Delete_Matrix(matrix, size);

    return 0;
}