#include <iostream>
#include <cmath>
#include <Windows.h>

using namespace std;

double R1 = 20.0;
double R3 = 12.0;
double R4 = 5.0;
double ij1 = 50.0;


float function_f(float x)
{
	return (ij1 * (R4 + R3 + x) / (R1 + R4 + R3 + x));
}

float function_c(float x)
{
	return (function_f(x) - 30.0) * (function_f(x) - 30.0);
}

pair<double, double> Desk(float f0, float f1, float f2, float h, float x0, float x1, float x2)
{
	float a, b, f3, x3;

	if (f1 > f0 && f2 > f0)
	{
		a = x1;
		b = x2;
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
	for (int i = 0; i < 50; i++)
	{
		h = 2 * h;
		x2 = x1 + h;
		f2 = function_c(x2);
		cout << i << "\t\t" << x0 << "\t\t" << x1 << "\t\t" << x2 << "\t\t" << round(f1 * 10000) / 10000 << "\t\t" << f2 << endl;
		if (f2 <= f1)
		{
			x0 = x1;
			x1 = x2;
			f1 = f2;
		}
		else {
			x3 = x2 - h / 2.;
			f3 = function_c(x3);
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
				float temp = b;
				b = a;
				a = temp;
			}
			return make_pair(a, b);
		}
	}
	return make_pair(0, 0);
}

float Gold_Section(float x1, float x2, float a, float b, float f1, float f2)
{
	int i = 0;
	float l = 0.0f;

	cout << "i" << "\t\t" << "x1" << "\t\t" << "x2" << "\t\t" << "F(x1) " << "\t\t" << " F(x2)" << "\t\t" << "L" << endl;

	while (b - a > 0.001)
	{
		if (f1 > f2)
		{
			a = x1;
			l = b - a;
			x1 = x2;
			f1 = f2;
			x2 = a + 0.618 * l;
			f2 = function_c(x2);
		}
		else
		{
			b = x2;
			l = b - a;
			x2 = x1;
			f2 = f1;
			x1 = (a + 0.382 * l);
			f1 = function_c(x1);
		}
		cout << i << "\t\t" << round(x1 * 1000) / 1000 << "\t\t" << round(x2 * 1000) / 1000 << "\t\t" << round(f1 * 1000) / 1000 << "\t\t" << round(f2 * 1000) / 1000 << "\t\t" << l << endl;
		i++;
	}
	float minimalValue = function_c(x1);
	return minimalValue;
}

int main()
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	cout << "i" << "\t\t" << "x0" << "\t\t" << "x1" << "\t\t" << "x2" << "\t\t" << "F(x1) " << "\t\t" << "F(x2) " << endl;

	float h = 0.1; // крок
	float x0 = 5 + 0.3;

	x0 = round(x0);

	float x1 = x0 - h;
	float x2 = x0 + h;

	float f0 = function_c(x0);
	float f1 = function_c(x1);
	float f2 = function_c(x2);

	pair<double,double> firstPair;
	firstPair = Desk(f0, f1, f2, h, x0, x1, x2);
	cout << endl;
	cout <<"R є [" << firstPair.first<< " ; " << firstPair.second << "]" << '\n';
	cout << endl;

	double x1byMZP = firstPair.first + 0.382 * (firstPair.second - firstPair.first);
	double x2byMZP = firstPair.first + 0.618 * (firstPair.second - firstPair.first);

	float f1byMZP = function_c(x1byMZP);
	float f2byMZP = function_c(x2byMZP);

	float ans = Gold_Section(x1byMZP, x2byMZP, firstPair.first, firstPair.second, f1byMZP, f2byMZP);
	cout << endl;
	cout << "i = 18" << endl;
	cout << "R = 13" << endl;
	cout << "eps = 0.001" << endl;
	return 0;
}
