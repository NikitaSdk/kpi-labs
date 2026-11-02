#include<iostream>
#include<cmath>
#define epsilon 0.0001
double MyFunction (double x) 
{
    return (1/(3*pow(x,3)))+ pow(x,2)+ 0.33; // для другого пунку: return x * x - 4 * x + 4;
}
void Calculate( int i ) {
    int count = 0;
    double t1 = 2 / (1 + sqrt(5));
    double t2 = 1 - t1;
    double a, b, c, d;
    double F3, F4, D;
    a = 0.5; // 1.5 для другого пункту
    b = 1.5; // 3.5 для другого пункту
    D = b - a;
    c = a + t2 * D;
    d = a + t1 * D;
    F3 = MyFunction(c);
    F4 = MyFunction(d);
    while (D > epsilon)
    {
        count++;
        i++;
        std::cout << "i = " << i << "\t a1 = " << a << "\ta2 = " << b << std::endl;
        if (F4 < F3) 
        {
            a = c;
            c = d;
            D = b - a;
            F3 = F4;
            d = a + t1 * D;
            F4 = MyFunction(d);

        }
        else 
        {
            b = d;
            d = c;
            D = b - a;
            c = a + t2 * D;
            F4 = F3;
            F3 = MyFunction(c);
        }
    }
    double x = (a + b) / 2;
    std::cout << std::endl;
    std::cout << "X(aopt) = " << x << "\tF(x)= " << MyFunction(x)<< std::endl; // round (MyFunction(x)) для другого пункту округлити
}
int main()
{
    int iter = 0;
    Calculate(iter);
}