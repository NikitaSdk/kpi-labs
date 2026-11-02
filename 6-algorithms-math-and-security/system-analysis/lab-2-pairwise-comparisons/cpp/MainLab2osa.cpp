#include <iostream>
#include <Windows.h>
#include <vector>

using namespace std;

void Method_of_paired_comparisons(std::vector<std::vector<int>>& matrix, int size_matrix) {
	int counter = 0;
	int arr_for_price[4];

	for (int i = 0; i < size_matrix; i++) {
		for (int j = 0; j < size_matrix; j++) {
			if (matrix[i][j] == 1) {
				counter++;
			}
		}
		arr_for_price[i] = counter;
		std::cout << "C" << i + 1 << " = " << counter << std::endl;
		counter = 0;
	}
	std::cout << std::endl;
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
	std::vector<std::vector<int>> matrix (N, std::vector<int>(N));
	// Вводим матрицу построчно
	for (int i = 0; i < N; i++) {
		std::cout << "Введите элементы " << (i + 1) << "-й строки через пробел: ";
		for (int j = 0; j < N; j++) {
			std::cin >> matrix[i][j];
		}
	}
	
	std::cout << "Введенная матрица:\n";
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			std::cout << matrix[i][j] << " ";
		}
		std::cout << std::endl;
	}
	
	Method_of_paired_comparisons( matrix, N );
	return 0;


	//Method_of_successive_comparisons( matrix, N);

	/*
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	int aray[4][4] = {
		{0,1,1,1},
		{0,0,0,0},
		{0,1,0,1},
		{0,1,0,0}
	};
	std::cout << "Задана матриця (з умови):" << std::endl;
	for (int i = 0; i < 4; i++) 
	{
		for (int j = 0; j < 4; j++)
		{
			std::cout << aray[i][j] << " ";
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;

	int counter = 0;
	int arr_for_price[4];

	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (aray[i][j] == 1)
			{
				counter++;
			}
		}
		arr_for_price[i] = counter;
		std::cout << "C" << i+1 << " = " << counter << std::endl;
		counter = 0;
	}
	std::cout << std::endl;

	std::cout << "Нормування : " << std::endl;
	float arr[4];
	for (int i = 0; i < 4; i++)
	{
		std::cout << "Z" << i + 1 << " = " << float(arr_for_price[i]) / 6 << std::endl;
		arr[i] = float(arr_for_price[i]) / 6;
	}
	std::cout << std::endl;
	float sum = 0.0f;
	for (int i = 0; i < 4; i++)
	{
		sum = sum + arr[i];
	}
	std::cout << "Сума Zi = " << sum << std::endl;
	*/
	/*
	int array_of_marks[] = { 125, 10, 60, 40 };
	for (int i = 0; i < 4; i++)
	{
		std::cout <<"p" << i+1 << " = " << array_of_marks[i] << " ";
	}
	std::cout << std::endl;
	std::cout << std::endl;
	int count_sum = 0;
	float iter = 0.0f;
	for (int i = 0; i < 4; i++)
	{
		count_sum = count_sum + array_of_marks[i];
	}
	for (int i = 0; i < 4; i++)
	{
		iter = float(array_of_marks[i]) / count_sum;
		std::cout << "V" << i+1 << " = " << iter << std::endl;
	}
	*/

}