#include <iostream>
#include <cmath>

double fun(double);

int main()
{
	double x0 = 2;				//початкова точка
	double h = 1;			//початкове значення кроку

	double x1 = x0 - h;
	double x2 = x0 + h;
	double f0 = fun(x0);
	double f1 = fun(x1);
	double f2 = fun(x2);

	double a, b, x3, f3;

	int i_max = 20;

	if ((f1 > f0) && (f2 > f0))
	{
		a = x1;
		b = x2;
	}
	else
	{
		if ((f1 < f0) && (f2 < f0))
		{
			std::cout << " The function is not unimodal on the initial interval.";

			return 1;
		}
	}

	if (f1 <= f2)
	{
		h = -h;
	}
	else
	{
		x1 = x2;
		f1 = f2;
	}

	for (int i = 1; i < i_max; i++)
	{
		h = 2 * h;
		x2 = x1 + h;
		f2 = fun(x2);

		if (f2 <= f1)
		{
			x0 = x1;
			x1 = x2;
			f1 = f2;
		}
		else
		{
			x3 = x2 - h / 2;
			f3 = fun(x3);

			if (f1 > f3)
			{
				a = x1;
				b = x2;
			}
			else
			{
				a = x0;
				b = x3;
			}

			if (a > b)
			{
				std::swap(a, b);
			}

			std::cout
				<< " a = " << a << std::endl
				<< " b = " << b << std::endl
				<< " i = " << i;

			return 0;
		}
	}

	std::cout << " The starting point is too far from the minimum point.";

	return 1;
}

double fun(double x)
{
	return
		(pow(x, 2) - 4 * x + 4); 					  	  //квадратична функція
		//(pow (sin (x), 4) + 6 * pow (x - 1, 2) + 10); //індивідувльно задана функція
}
