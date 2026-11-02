#include <iostream>
#include <vector>
#include <windows.h>

void Method_of_paired_comparisons(std::vector<std::vector<int>>& matrix, int size_matrix) 
{
    std::cout << std::endl;
    std::cout << "\tМетод парних порівнянь : " << std::endl;
    std::cout << std::endl;
    int counter = 0;
    int counter_two = 0;
    std::vector<int> arr_for_price(size_matrix);

    std::cout << "Ціна кожної мети : " << std::endl;
    for (int i = 0; i < size_matrix; i++) {
        for (int j = 0; j < size_matrix; j++) {
            if (matrix[i][j] == 1) {
                counter++;
                counter_two++;
            }
        }
        arr_for_price[i] = counter;
        std::cout << "C" << i + 1 << " = " << counter << std::endl;
        counter = 0;
    }
    std::cout << std::endl;

    std::cout << "Нормування : " << std::endl;



    float sum = 0.0f;
    for (int i = 0; i < size_matrix; i++) {
        float normalized_value = static_cast<float>(arr_for_price[i]) / counter_two;
        std::cout << "Z" << i + 1 << " = " << normalized_value << std::endl;
        sum += normalized_value;
    }
    std::cout << std::endl;
    std::cout << "Сума Zi = " << sum << std::endl;
}

void Method_of_successive_comparisons(std::vector<std::vector<int>>& matrix, int size_matrix)
{
    std::cout << std::endl;
    std::cout << "\tМетод послідовних порівнянь : " << std::endl;
    std::cout << std::endl;
    std::cout << "Запис оцінок : " << std::endl;
    std::vector <int> array_of_marks; 
    int a = 0;
    for (int i = 0; i < size_matrix; i++ )
    {
        std::cin >> a;
        array_of_marks.push_back(a);
    }
    for (int i = 0; i < size_matrix; i++)
    {
        std::cout << "p" << i+1 << " = " << array_of_marks[i] << " ";
    }
    std::cout << std::endl;
    std::cout << std::endl;
    int count_sum = 0;
    float iter = 0.0f;
    for (int i = 0; i < 4; i++)
    {
        count_sum = count_sum + array_of_marks[i];
    }
    for (int i = 0; i < size_matrix; i++)
    {
        iter = float(array_of_marks[i]) / count_sum;
        std::cout << "V" << i + 1 << " = " << iter << std::endl;
    }

}

int main() 
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    int N;

    // Запрашиваем у пользователя размерность матрицы NxN
    std::cout << "Введите размерность матрицы (N): ";
    std::cin >> N;

    // Создаем матрицу NxN
    std::vector<std::vector<int>> matrix(N, std::vector<int>(N));

    // Вводим матрицу построчно
    for (int i = 0; i < N; i++) {
        std::cout << "Введіть елементи " << (i + 1) << " строки через пробіл: ";
        for (int j = 0; j < N; j++) {
            std::cin >> matrix[i][j];
        }
    }

    std::cout << "Матриця :\n";
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }

    Method_of_paired_comparisons(matrix, N);
    Method_of_successive_comparisons(matrix, N);

    return 0;
}