#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>

using namespace std;


std::vector<double> Spam_Percentage_Calculate(std::vector<std::string>& new_messages, std::unordered_map<std::string, double>& norm_spam_percentage)
{
    std::vector<double> spam_percentages;
    for (const auto& message : new_messages)
    {
        double percent = 1.0;
        std::istringstream iss(message);
        std::string word;
        while (iss >> word)
        {
            auto it = norm_spam_percentage.find(word);
            if (it != norm_spam_percentage.end())
            {
                percent *= it->second;
            }
            else
            {
                percent *= 0.5; // новое слово
            }
        }
        spam_percentages.push_back(percent);
    }
    return spam_percentages;
}
int main()
{
    unordered_map<string, double> norm_spam_percentage = {
        {"Hello", 0.5},
        {"shoes", 0.83},
        {"snikers", 0.25},
        {"special", 0.5},
        {"for", 0.25},
        {"on", 0.58},
        {"discout", 0.5},
        {"sales", 0.5},
        {"Hi", 0.83},
        {"boots", 0.5},
        {"Hey", 0.17},
        {"rebate", 0.5},
        {"some", 0.25},
        {"you", 0.25},
    };
    vector<string> new_messages = { "Hello rebate shoes", "Hello blabla"};
    vector<double> percentages = Spam_Percentage_Calculate(new_messages, norm_spam_percentage);
    // ¬ыводим значени€ вектора на консоль
    for (double p : percentages) {
        cout << "Spam percentage: " << 0.5 * p << endl;
    }

    return 0;
}