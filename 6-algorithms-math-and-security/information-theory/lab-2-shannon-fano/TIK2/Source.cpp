#include <iostream>
#include <fstream>
#include <map>
#include <cmath>
#include <vector>
#include <algorithm>
#include <string>
#include "Windows.h"
#include <bitset>
#include <sstream>


void setConsoleEncoding() {

    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

}

struct Symbol {
    char symbol;
    int frequency;
    std::string code;
};

std::map<char, int> readCharacterCounts(const std::string& filename, int& totalCharacters) {

    std::map<char, int> charCount;

    uint8_t character;

    std::ifstream inputFile(filename, std::ios::binary);

    if (!inputFile.is_open()) {
        std::cerr << "Unable to open file." << std::endl;
        exit(1);
    }

    while (true) {
        character = inputFile.get();
        if (inputFile.eof())
        {
            break;
        }
        charCount[character]++;
        totalCharacters++;
    }

    inputFile.close();

    return charCount;
}

bool compareProbability(const Symbol& a, const Symbol& b) {
    return a.frequency > b.frequency;
}

void sortTable(const std::map<char, int>& charCount, std::vector<Symbol>& probabilityVector, int totalCharacters) {
    for (const auto& pair : charCount) {
        float probability = static_cast<float>(pair.second) / totalCharacters;
        probabilityVector.push_back({ pair.first, pair.second, "" });
    }

    std::sort(probabilityVector.begin(), probabilityVector.end(), compareProbability);
}

void printTable(const std::vector<Symbol>& probabilityVector, const std::map<char, int>& charCount) {
    std::cout << "Відсортована таблиця:" << std::endl;
    std::cout << "Символ\tЧастота\tКод" << std::endl;

    for (const auto& symbol : probabilityVector) {
        if (symbol.symbol == ' ') {
            std::cout << "Space\t";
        }
        else {
            std::cout << symbol.symbol << "\t";
        }
        std::cout << symbol.frequency << "\t" << symbol.code << std::endl;
    }
}

void calculateValues(const std::map<char, int>& charCount, int totalCharacters) {
    float PiSUM = 0;
    float LogSUM = 0;
    float EntrSUM = 0;

    std::cout << "Таблиця:" << std::endl;
    std::cout << "Символ\tЧастота\tP[i]\t\tLog(P[i])\tEntropy" << std::endl;

    for (auto& pair : charCount) {
        PiSUM += static_cast<float>(pair.second) / totalCharacters;
        LogSUM += log2(static_cast<float>(pair.second) / totalCharacters);
        EntrSUM += static_cast<float>(pair.second) / totalCharacters * log2(static_cast<float>(pair.second) / totalCharacters);

        if (pair.first == ' ') {
            std::cout << "Space\t";
        }
        else {
            std::cout << pair.first << "\t";
        }

        std::cout << pair.second << "\t" << static_cast<float>(pair.second) / totalCharacters
            << "\t\t" << log2(static_cast<float>(pair.second) / totalCharacters)
            << "\t" << -1 * static_cast<float>(pair.second) / totalCharacters * log2(static_cast<float>(pair.second) / totalCharacters)
            << std::endl;
    }

    EntrSUM *= -1;

    std::cout << std::endl;
    std::cout << "Symbol count: " << totalCharacters << std::endl;
    std::cout << "Sum P[i]: " << PiSUM << std::endl;
    std::cout << "Sum Log(P[i]): " << LogSUM << std::endl;
    std::cout << "H: " << EntrSUM << std::endl;
    std::cout << std::endl;

    std::cout << "Amount of info: " << totalCharacters * EntrSUM << std::endl;
    std::cout << "Max entropy: " << log2(charCount.size()) << std::endl;
    std::cout << "Absolute excess: " << log2(charCount.size()) - EntrSUM << std::endl;
    std::cout << "Relative excess: " << (log2(charCount.size()) - EntrSUM) / EntrSUM << std::endl;
    std::cout << std::endl;
}

struct Node {

    Symbol symbol;
    Node* left;
    Node* right;
};

void traverseAndPrintTree(Node* root, std::string currentCode) {
    if (root != nullptr) {
        if (root->left != nullptr) {
            traverseAndPrintTree(root->left, currentCode + "0");
        }

        if (root->right != nullptr) {
            if (root->left == nullptr) {
                std::cout << root->symbol.symbol << "\t" << currentCode << std::endl;
            }
            traverseAndPrintTree(root->right, currentCode + "1");
        }

        // Добавлен блок обработки листового узла
        if (root->left == nullptr && root->right == nullptr) {
            std::cout << root->symbol.symbol << "\t" << currentCode << std::endl;
        }
    }
}

void buildShannonFanoTree(std::vector<Symbol>& probabilityVector, Node*& root, int start, int end, std::string currentCode) {

   // std::cout << "1" << std::endl;

    if (start > end) {
        return;
    }

    if (start == end) {
        root = new Node;
        root->symbol = probabilityVector[start];
        root->left = nullptr;
        root->right = nullptr;
        probabilityVector[start].code += currentCode;
        return;
    }

    int sum = 0;
    for (int i = start; i <= end; ++i) {
        sum += probabilityVector[i].frequency;
    }

    int currentSum = 0;
    int index = start;
    while (currentSum < sum / 2)
    {
        currentSum += probabilityVector[index].frequency;
        index++;
    }

    /*
    while ( currentSum + probabilityVector[index].frequency * 2 <= sum) {
        currentSum += probabilityVector[index].frequency;

        // Проверка, ближе ли текущий индекс к середине
        int midpointDifference = std::abs(2 * currentSum - sum);
        if (midpointDifference < closestMidpoint) {
            closestMidpoint = midpointDifference;
            index++;
        }
        else {
            break;
        }
    }
    */
    root = new Node;
    root->left = nullptr;
    root->right = nullptr;

    buildShannonFanoTree (probabilityVector, root->left, start, index - 1, currentCode + "0");
    buildShannonFanoTree (probabilityVector, root->right, index, end, currentCode + "1");
}

std::string readSentenceFromFile(const std::string& filename) {

    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Unable to open file: " << filename << std::endl;
        exit(1);
    }

    std::string sentence;
    std::getline(file, sentence);

    file.close();

    return sentence;
}

std::string encodeSentence(const std::string& sentence, const std::map<char, std::string>& encodingMap) {
    std::string encodedString;

    for (char character : sentence) {
        auto it = encodingMap.find(character);
        if (it != encodingMap.end()) {
            encodedString += it->second;
        }
        else {
            std::cerr << "Symbol not found: " << character << std::endl;
        }
    }
    return encodedString;
}

void writeBinaryFile(const std::string& filename, const std::string& data) {
    std::ofstream file(filename, std::ios::binary);
    if (file.is_open()) {
        for (std::size_t i = 0; i < data.length(); i += 8) {
            std::bitset<8> byte;
            for (std::size_t j = 0; j < 8; ++j) {
                if (i + j < data.length()) {
                    byte[7 - j] = (data[i + j] == '1');
                }
            }
            char byteChar = static_cast<char>(byte.to_ulong());
            file.write(&byteChar, 1);
        }
        file.close();
    }
    else {
        std::cerr << "Unable to open file: " << filename << std::endl;
    }
}

std::string reverseString(const std::string& input) {
    std::string reversed;
    for (auto it = input.rbegin(); it != input.rend(); ++it) {
        reversed += *it;
    }
    return reversed;
}

std::string readBinaryFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (file.is_open()) {
        std::ostringstream oss;
        char byte;

        while (file.read(&byte, 1)) {
            std::bitset<8> bits(byte);
            oss << bits;
        }

        file.close();
        return oss.str();
    }
    else {
        std::cerr << "Unable to open file: " << filename << std::endl;
        return "";
    }
}

void decodeBinaryFile(const std::string& filename, const std::map<std::string, char>& decodingMap) {

    std::string encodedBits = readBinaryFile(filename);
    std::string currentCode = "";
    std::string decodedSentence = "";
    for (char bit : encodedBits) {
        std::cout << bit;
        //std::cout << currentCode << std::endl;
        currentCode += bit;
        auto it = decodingMap.find(currentCode);
        if (it != decodingMap.end()) {

            decodedSentence += it->second;
            currentCode.clear();
        }
    }
    std::cout << std::endl;
    std::cout << "Decoded Sentence: " << decodedSentence << std::endl;
}

int main() {

    setConsoleEncoding();

    int totalCharacters = 0;
    std::map<char, int> charCount = readCharacterCounts("Words.txt", totalCharacters);

    std::vector<Symbol> probabilityVector;

    calculateValues(charCount, totalCharacters);
    sortTable(charCount, probabilityVector, totalCharacters);
    printTable(probabilityVector, charCount);

    Node* root = nullptr;
    buildShannonFanoTree(probabilityVector, root, 0, probabilityVector.size() - 1, "");

    std::cout << "\nШеннон-Фано дерево:" << std::endl;
    std::cout << "Символ\tКод" << std::endl;

    traverseAndPrintTree(root, "");

    std::map<char, std::string> encodingMap;
    std::map<std::string, char> decodingMap;

    for (const Symbol& element : probabilityVector) {
        encodingMap[element.symbol] = element.code;
    }

    for (const Symbol& element : probabilityVector) {
        decodingMap[element.code] = element.symbol;
    }

    std::string sentence = readSentenceFromFile("Words.txt");
    std::string encodedString = encodeSentence(sentence, encodingMap);
    writeBinaryFile("test.bin", encodedString);

    decodeBinaryFile("test.bin", decodingMap);

    delete root;

    return 0;
}