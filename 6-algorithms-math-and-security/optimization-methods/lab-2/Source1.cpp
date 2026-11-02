#include <iostream>
#include <cmath>

double fun(double x)
{
	return  x * x - 4 * x + 4;//квадратична функція
			// (1 / (3 * pow(x, 3))) + pow(x, 2) + 0.33; //індивідувльно задана функція
}

int main()
{
	for (int k = 0; k < 4; k++)
	{
		double x0 = 0.5; //0.5				//початкова точка
		double h[] = { 0.01, 0.1, 1, 2 };		//початкове значення кроку
		double x1 = x0 - h[k];
		double x2 = x0 + h[k];
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
			h[k] = -h[k];
		}
		else
		{
			x1 = x2;
			f1 = f2;
		}

		for (int i = 1; i < i_max; i++)
		{
			h[k] = 2 * h[k];
			x2 = x1 + h[k];
			f2 = fun(x2);

			if (f2 <= f1)
			{
				x0 = x1;
				x1 = x2;
				f1 = f2;
			}
			else
			{
				x3 = x2 - h[k] / 2;
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
				//Пошук мiнiмуму методом золотого перетину:
				double epsilon = 0.001;
				double carrier_a = a;
				double carrier_b = b;

				double l = carrier_b - carrier_a;
				double x1 = carrier_a + 0.382 * l;
				double x2 = carrier_a + 0.618 * l;
				double f1 = fun(x1);
				double f2 = fun(x2);

				int j = 0;

				while (carrier_b - carrier_a > epsilon)
				{
					if (f1 > f2)
					{
						carrier_a = x1;
						l = carrier_b - carrier_a;
						x1 = x2;
						f1 = f2;
						x2 = carrier_a + 0.618 * l;
						f2 = fun(x2);
					}
					else
					{
						carrier_b = x2;
						l = carrier_b - carrier_a;
						x2 = x1;
						f2 = f1;
						x1 = carrier_a + 0.382 * l;
						f1 = fun(x1);
					}

					++j;
				}

				double xopt = (carrier_a + carrier_b) / 2; //мінімум функції
				//Кінець метода золотого перетину
				std::cout << "a = " << a << "  b = " << b << "  i = " << i << "  j = " << j << "  i + j = " << i + j << "  xopt = " << xopt << std::endl;
				break;
			}
		}
	}
	std::cout << " The starting point is too far from the minimum point.";

	return 1;
}