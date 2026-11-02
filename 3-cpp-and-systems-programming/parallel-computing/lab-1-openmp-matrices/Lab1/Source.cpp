/*
24.Заповнити квадратну матрицю випадковими числами. 
   Відобразити верхню половину матриці на нижню дзеркально симетрично відносно горизонтальної вісі.
*/

#include <iostream>
#include <Windows.h>
#include <random>
#include <chrono>

using std::chrono::nanoseconds;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;

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
            matrix[i][j] = rand() % 10;
        }
    }
}
void ShowMatrix(int** matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
}
void Compute(int** matrix, int size) {
    auto payload_begin = high_resolution_clock::now();
    for (int i = 0; i < size / 2; i++) {
        for (int j = 0; j < size; j++) {
            matrix[size - 1 - i][j] = matrix[i][j];
        }
    }
    auto payload_end = high_resolution_clock::now();
    auto elapsed = duration_cast<nanoseconds>(payload_end - payload_begin);
    std::printf("Payload Time: %.3f seconds.\n", elapsed.count() * 1e-9);
}
int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    srand(time(NULL));
    int size;
    std::cout << "Введіть розмір матриці: ";
    std::cin >> size;
    int** matrix = Alloc_Matrix(size);
    Fill_Matrix(matrix, size);
    //ShowMatrix(matrix, size);
    Compute(matrix, size);
    //ShowMatrix(matrix, size);
    Delete_Matrix(matrix, size);
    return 0;
}
