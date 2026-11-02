#include <iostream>
#include <fstream>
#include <map>
#include "Windows.h"


int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    std::map<char, int> charCount; // Використовуємо для зберігання унікальних символів
    char character;
    int all_char = 0;
    float PiSUM = 0;
    float LogSUM = 0;
    float EntrSUM = 0;

    std::ifstream inputFile("Words.txt", std::ios::binary); // Відкриття файлу в бінарному режимі

    if (!inputFile.is_open()) // Перевірка на відкриття файлу
    {
        std::cerr << "Unable to open file." << std::endl;
        return 1;
    }


    while (inputFile.get(character)) // Зчитування символів з файлу і повернення його коду в однобайтовій кодовій таблиці
    {
        charCount[character]++; // зчитування унікальних символів
        all_char++; // збільшення загальної кількості символів
    }

    inputFile.close();

    std::cout << "Symbols " << "\tP[i] " << "\t\t Log(P[i]) " << "\tEntropy" << std::endl;
    for (const auto& pair : charCount)  // обрахунки значень
    {
        PiSUM = PiSUM + float(pair.second) / all_char;
        LogSUM = LogSUM + log2(float(pair.second) / all_char);
        EntrSUM = EntrSUM + float(pair.second) / all_char * log2(float(pair.second) / all_char);

        if (pair.first == ' ') {
            std::cout << "Space" << "=" << pair.second << "\t\t" << float(pair.second) / all_char << "\t " << log2(float(pair.second) / all_char) << "\t" << -1 * float(pair.second) / all_char * log2(float(pair.second) / all_char) << std::endl;
        }
        else {
            std::cout << pair.first << "=" << pair.second << "\t\t" << float(pair.second) / all_char << "\t " << log2(float(pair.second) / all_char) << "\t" << -1 * float(pair.second) / all_char * log2(float(pair.second) / all_char) << std::endl;
        }
    }

    EntrSUM = EntrSUM * (-1);
    std::cout << std::endl;
    std::cout << "Symbol count: " << all_char << std::endl;
    std::cout << "Sum P[i]: " << PiSUM << std::endl;
    std::cout << "Sum Log(P[i]): " << LogSUM << std::endl;
    std::cout << "Н: " << EntrSUM << std::endl;
    std::cout << std::endl;

    std::cout << "Amount of info: " << all_char * EntrSUM << std::endl;
    std::cout << "Max entropy: " << log2(charCount.size()) << std::endl;
    std::cout << "Absolute excess: " << log2(charCount.size()) - EntrSUM << std::endl;
    std::cout << "Relative excess: " << (log2(charCount.size()) - EntrSUM) / EntrSUM << std::endl;

    return 0;
}
