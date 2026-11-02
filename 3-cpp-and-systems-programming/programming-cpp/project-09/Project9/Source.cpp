#include <iostream>
#include <string>
#include <unordered_map>
#include <cmath>
#include <fstream>
#include <algorithm>
#include <vector>


using namespace std;

// Структура для представления символа и его вероятности
struct SymbolProbability {
    char symbol;
    double probability;
};

// Структура для представления символа и его битового кода
struct SymbolCode {
    char symbol;
    string code;
};

// Функция для ввода текста из файла или с клавиатуры
string getInputText(int choice, const string& filename) {

    string text;

    if (choice == 2) {
        ifstream input(filename, ios::binary);
        if (!input.is_open()) {
            cout << "Cannot open the file." << endl;
            exit(1);
        }
        while (!input.eof()) {
            char c;
            input.get(c);
            text += c;
        }
        text.erase(text.size() - 1);
        cout << text << endl;
    }
    else if (choice == 1) {
        cout << "Type text: ";
        getline(cin, text);
    }

    return text;
}

// Функция для подсчета частот символов в тексте
unordered_map<char, int> countFrequencies(const string& text) {
    unordered_map<char, int> frequencies;
    for (char c : text) {
        frequencies[c]++;
    }
    return frequencies;
}

// Функция для вывода информации о частотах символов
void printSymbolFrequencies(const unordered_map<char, int>& frequencies) {
    for (auto pair : frequencies) {
        cout << pair.first << "-    Repeats: " << pair.second << endl;
    }
}

// Функция для подсчета энтропии и вывода информации о символах
double calculateEntropy(const string& text, int& alphabetSize) {
    unordered_map<char, int> frequencies = countFrequencies(text);
    double entropy = 0.0;
    alphabetSize = 0;

    for (auto pair : frequencies) {
        if (pair.second != 0) {
            double probability = pair.second / static_cast<double>(text.size());
            double symbentropy = probability * log2(probability);
            entropy -= symbentropy;
            alphabetSize++;
            cout << pair.first << "-    Repeats: " << pair.second
                << "  Probability: " << probability
                << "    Symbol Entropy: " << symbentropy << endl;
        }
    }

    return entropy;
}

// Функция для сортировки символов по вероятностям
vector<SymbolProbability> sortSymbolsByProbability(const unordered_map<char, int>& frequencies, int size) {
    vector<SymbolProbability> symbols;

    for (auto pair : frequencies) {
        if (pair.second != 0) {
            double probability = pair.second;// static_cast<double>(size);
            symbols.push_back({ pair.first, probability });
        }
    }

    sort(symbols.begin(), symbols.end(),
        [](const auto& a, const auto& b) {
            return a.probability > b.probability;
        });

    return symbols;
}

// Функция для выполнения алгоритма Шенона-Фано
void shannonFano
(vector<SymbolProbability>& symbols, int start, int end, vector<SymbolCode>& codeTable, string currentCode) {
    if (start < end) {
        double sum = 0.0;
        int splitIndex = start;
        double leftSum = abs(symbols[start].probability - sum);
        double rightSum = abs(symbols[start + 1].probability - sum);

        while (splitIndex < end - 1) {
            if (leftSum < rightSum) {
                ++splitIndex;
                sum += symbols[splitIndex].probability;
                leftSum = abs(symbols[start].probability - sum);
                rightSum = abs(symbols[splitIndex + 1].probability - sum);
            }
            else {
                break;
            }
        }

        shannonFano(symbols, start, splitIndex, codeTable, currentCode + '0');
        shannonFano(symbols, splitIndex + 1, end, codeTable, currentCode + '1');
    }
    else if (start == end) {
        // Один символ, добавляем его в таблицу кодов
        codeTable.push_back({ symbols[start].symbol, currentCode });
    }
}

// Функция для вывода таблицы кодов символов
void printCodeTable(const vector<SymbolCode>& codeTable) {
    cout << "Symbol Codes:" << endl;
    for (auto symbolCode : codeTable) {
        cout << symbolCode.symbol << ": " << symbolCode.code << endl;
    }
}

int main() {

 

    int choice = 0;
    string filename = "C:\\Users\\user\\source\\repos\\Project9\\Project9\\Word.txt";

    cout << "Choose input type (1-keyboard 2-file): ";
    cin >> choice;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    string text = getInputText(choice, filename);
    unordered_map<char, int> frequencies = countFrequencies(text);

    cout << "Text size: " << text.size() << endl << endl;

    int alphabetSize;
    double entropy = calculateEntropy(text, alphabetSize);

    double maxentropy = log2(text.size());
    cout << "Alphabet: " << alphabetSize << endl;
    cout << endl << "Entropy: " << entropy << endl;
    cout << "Amount of data: " << text.size() * entropy << endl;
    cout << "Max Entropy: " << maxentropy << endl;
    cout << "Absolute surplus: " << maxentropy - entropy << endl;
    cout << "Relative surplus: " << (maxentropy - entropy) / entropy << endl;

    cout << endl << "Sorted by probabilities:" << endl;
    vector<SymbolProbability> symbols = sortSymbolsByProbability(frequencies, text.size());

    for (auto symbol : symbols) {
        cout << symbol.symbol << "-    Repeats: " << frequencies[symbol.symbol]
            << "  Probability: " << symbol.probability << endl;
    }

    vector<SymbolCode> codeTable;
    shannonFano(symbols, 0, symbols.size() - 1, codeTable, "");


    printCodeTable(codeTable);

    return 0;
}