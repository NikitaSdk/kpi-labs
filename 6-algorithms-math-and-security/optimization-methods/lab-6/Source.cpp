#include <iostream>
#include <vector>

using namespace std;

// Функція для знаходження ведучого стовпця
int findPivotColumn(const vector<double>& coefficients) {
    int pivotColumn = 0;
    double minValue = coefficients[0];
    for (int i = 1; i < coefficients.size(); i++) {
        if (coefficients[i] < minValue) {
            minValue = coefficients[i];
            pivotColumn = i;
        }
    }
    return pivotColumn;
}

// Функція для знаходження ведучого рядка
int findPivotRow(const vector<vector<double>>& tableau, int pivotColumn) {
    int pivotRow = 0;
    double minValue = tableau[0][0] / tableau[0][pivotColumn];
    for (int i = 1; i < tableau.size(); i++) {
        double ratio = tableau[i][0] / tableau[i][pivotColumn];
        if (tableau[i][pivotColumn] > 0 && ratio < minValue) {
            minValue = ratio;
            pivotRow = i;
        }
    }
    return pivotRow;
}

// Функція для оновлення таблиці симплекс-методу
void updateTableau(vector<vector<double>>& tableau, int pivotRow, int pivotColumn) {
    int rowCount = tableau.size();
    int columnCount = tableau[0].size();

    double pivotElement = tableau[pivotRow][pivotColumn];

    // Ділення ведучого рядка на ведучий елемент
    for (int i = 0; i < columnCount; i++) {
        tableau[pivotRow][i] /= pivotElement;
    }

    // Оновлення інших рядків таблиці
    for (int i = 0; i < rowCount; i++) {
        if (i != pivotRow) {
            double multiplier = tableau[i][pivotColumn];
            for (int j = 0; j < columnCount; j++) {
                tableau[i][j] -= multiplier * tableau[pivotRow][j];
            }
        }
    }
}

// Функція для перевірки оптимальності розв'язку
bool isOptimal(const vector<double>& coefficients) {
    for (double coefficient : coefficients) {
        if (coefficient < 0) {
            return false;
        }
    }
    return true;
}

// Головна функція для симплекс-методу
void simplexMethod(vector<vector<double>>& tableau) {
    int rowCount = tableau.size();
    int columnCount = tableau[0].size();

    while (true) {
        // Знаходження ведучого стовпця
        int pivotColumn = findPivotColumn(tableau[0]);
        if (pivotColumn == 0) {
            break;  // Розв'язок досягнуто
        }

        // Знаходження ведучого рядка
        int pivotRow = findPivotRow(tableau, pivotColumn);
        if (pivotRow == 0) {
            break;  // Задача необмежена
        }

        // Оновлення таблиці
        updateTableau(tableau, pivotRow, pivotColumn);
    }
}

int main() {
    // Початкова симплекс-таблиця
    vector<vector<double>> tableau = {
        {-3, 2, 0, 0, 0},
        {-1, 4, 1, 0, 8},
        {2, -1, 0, -1, -7},
        {-4, 3, 0, 0, 0}
    };

    // Запуск симплекс-методу
    simplexMethod(tableau);

    // Виведення розв'язку
    cout << "Optimal solution:" << endl;
    cout << "x1 = " << tableau[1][0] << endl;
    cout << "x2 = " << tableau[2][0] << endl;

    return 0;
}