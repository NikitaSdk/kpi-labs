#include <iostream>
#include <cmath>
#include <windows.h>
#include <ctime>

int main()
{
	srand(time(NULL));
	system("color 3F");
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE); 
	SetConsoleTextAttribute(handle, FOREGROUND_RED);
	setlocale(LC_ALL, "ru");
	long long int a, b, c, d; 
	c = 100;
	//std::cout << "\t" << std::endl;
	int arr[] = { 1,1,1,1,1,1,1,1,1,1};

	std::cout << "ÏÀÏÈ× TV" << std :: endl;

	while (true)
	{
		d = rand() % 10;
		if (c == 100)
		{
			std::cout << "Ââåäèòå ñóììó äåïîçèòà : ";
			std::cin >> a;
			std::cout << "Âàø îáùèé âûèãðûø ñîñòàâëÿåò : ";
			b = c * pow(a, 2) * d;
			std::cout << b << "$  ONLY BIGGG WINNN !!!!" << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << arr[0] << "\t" << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << std::endl;
			std::cout << arr[0] << "\t" << arr[0] << std::endl;
			std::cout << arr[0] << "\t" << arr[0] << std::endl;
			std::cout << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << std::endl;
			std::cout << "\t" << arr[0] << " " << " " << " " << " " << " " << " " << " " << arr[0] << std::endl;
			std::cout << "\t" << arr[0] << " " << " " << " " << " " << " " << " " << " " << arr[0] << std::endl;
			std::cout << "\t" << arr[0] << " " << " " << " " << " " << " " << " " << " " << arr[0] << std::endl;

			std::cout << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << arr[0] << " " << " " << " " << " " << " " << " " << " " << arr[0];
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;

		}
		else
		{
			b = log(c / (a * 10));
			std::cout << "ÂÛ ÏÐÎÅÁÀËÈ !!! " << std::endl;
			std::cout << "ÂÛ ÓØËÈ Â ÌÈÍÓÑ ÍÀ " << b << std::endl;
		}

	}
	return 0;
}