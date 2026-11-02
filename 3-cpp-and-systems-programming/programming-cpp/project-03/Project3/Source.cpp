#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>

using namespace std;

// тип даних, який буде використовуватися для позначення назви листа + спам/не спам 
struct Type_of_message
{
	string message;
	bool isSpam = 0; // true - spam, false - not spam 
};

// функція для підрахунку слів
void WordCounter(vector <Type_of_message> &messages , unordered_map <string, int>&words, unordered_map <string, int>&spam_counter)
{
	int iterator = 0;
	for (auto& i : messages)
	{
		istringstream iss(messages[iterator].message);
		string word;
		while (iss >> word)
		{
			words[word]++;

			if (messages[iterator].isSpam == true)
			{
				spam_counter[word]++;
			}
			if (messages[iterator].isSpam == false)
			{
				spam_counter[word] + 0;
			}
		}
		iterator++;
	}
}
//функція для показу словника у консолі 
void ShowWords( unordered_map <string, int> &unorder_map )
{
	cout << endl;
	for (auto& pair : unorder_map)
	{
		cout << "Word: " << pair.first << "\t " << "Amount: " << pair.second << endl;
	}
}
// функція для підрахунку % спаму 
void SpamProbability(unordered_map <string, int>& words, unordered_map <string, int>& spam_counter, unordered_map <string, double>& unorder_map)
{
	for (auto& pair : words)
	{
		double spam = double(spam_counter[pair.first] / double(words[pair.first]));
		unorder_map.emplace(pair.first, spam);
	}

}
// функція для підрахунку нормованого % спаму 
void NormSpamProbability(unordered_map <string, int> &words, unordered_map <string, double> &spam_percentage, unordered_map <string, double> &norm_spam_percentage)
{
	for (auto& pair : words)
	{
		double p_norm_spam = (double(pair.second) * double(spam_percentage[pair.first]) + 0.5) / (double(pair.second) + 1);
		p_norm_spam = round(p_norm_spam * 100) / 100;
		norm_spam_percentage.emplace(pair.first, p_norm_spam);
	}
}
//функція для показу словника у консолі 
void ShowPersentage(unordered_map <string, double>& unorder_map)
{
	cout << endl;
	for (auto& pair : unorder_map)
	{
		cout << "Word: " << pair.first << "\t " << "Spam : " << pair.second << "\t Not spam : "<< 1 - pair.second << endl;
	}
}
// функція, що підраховує % належності листа до спаму
vector<double> Spam_Percentage_Calculate(vector<Type_of_message>& new_messages, unordered_map<string, double>& norm_spam_percentage)
{
	std::vector<double> spam_percentages;
	int iterator = 0;
	for (auto& message : new_messages)
	{
		double percent = 1.0;
		istringstream iss(new_messages[iterator].message); // розділення i-го елемента масиву повідомлень на слова 
		string word;
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
		iterator++;
	}
	for (int i = 0; i < spam_percentages.size(); i++)
	{
		spam_percentages[i] *= 0.5;
	}
	return spam_percentages;
}
// функція, що підраховує % належності листа до не спаму
vector<double> Not_spam_Percentage_Calculate( vector<Type_of_message>& new_messages, unordered_map<string, double>& norm_spam_percentage)
{
	std::vector<double> not_spam_percentages;
	int iterator = 0;
	for (auto& message : new_messages)
	{
		double percent = 1.0;
		std::istringstream iss(new_messages[iterator].message); // розділення i-го елемента масиву повідомлень на слова 
		std::string word;
		while (iss >> word)
		{
			auto it = norm_spam_percentage.find(word);
			if (it != norm_spam_percentage.end())
			{
				percent *= 1-(it->second);
			}
			else
			{
				percent *= 0.5; // якщо нове слово
			}
		}
		not_spam_percentages.push_back(percent);
		iterator++;
	}
	for (int i = 0; i < not_spam_percentages.size(); i++)
	{
		not_spam_percentages[i] *= 0.5;
	}
	return not_spam_percentages;
}

int main()
{
	vector <Type_of_message> first_six_messages;
	Type_of_message A, B, C, D, E, F;
	A.isSpam = true;
	A.message = "Hello special sales on boots";
	B.isSpam = true;
	B.message = "Hi discout on shoes";
	C.isSpam = false;
	C.message = "Hey rebate on snikers";
	D.isSpam = false;
	D.message = "Hello special discout on boots";
	E.isSpam = true;
	E.message = "Hi rebate on shoes";
	F.isSpam = false;
	F.message = "Hey some sales for you";

	first_six_messages.push_back(A);
	first_six_messages.push_back(B);
	first_six_messages.push_back(C);
	first_six_messages.push_back(D);
	first_six_messages.push_back(E);
	first_six_messages.push_back(F);

	for (int i = 0; i < first_six_messages.size(); i++) // вивід у консоль початкових даних 
	{
		if (first_six_messages[i].isSpam)
		{
			cout << first_six_messages[i].message << " " << " (SPAM) " << endl;
		}
		else
		{
			cout << first_six_messages[i].message << " " << " (NOT SPAM) " << endl;
		}
	}

	unordered_map <string, int> words; // зберігання всіх слів, і їх кількості
	unordered_map <string, int> spam_counter; // зберігання кількості СПАМ слів 
	unordered_map <string, double> spam_percentage; // зберігання слово - відсоток спаму
	unordered_map <string, double> norm_spam_percentage; // зберігання слово - нормований відсоток спаму

	WordCounter(first_six_messages, words, spam_counter);
	ShowWords(words);
	ShowWords(spam_counter);

	SpamProbability(words, spam_counter, spam_percentage);
	ShowPersentage(spam_percentage);

	NormSpamProbability(words, spam_percentage, norm_spam_percentage);
	ShowPersentage(norm_spam_percentage);

	cout << endl;
	vector <Type_of_message> new_messages;
	Type_of_message message1, message2, message3, message4;
	message1.isSpam = true;
	message1.message = "Hello rebate shoes";
	message2.isSpam = false;
	message2.message = "Hi sales on shoes";
	message3.isSpam = false;
	message3.message = "Hey discount on snikers";
	message4.isSpam = true;
	message4.message = "Only today special sales on boots";

	new_messages.push_back(message1);
	new_messages.push_back(message2);
	new_messages.push_back(message3);
	new_messages.push_back(message4);

	vector<double> spam_percentages = Spam_Percentage_Calculate(new_messages, norm_spam_percentage);
	vector<double> not_spam_percentages = Not_spam_Percentage_Calculate(new_messages, norm_spam_percentage);
	vector<string>meaning;
	for (int i = 0; i < spam_percentages.size(); i++)
	{
		if (0.5 * spam_percentages[i] > 0.5 * not_spam_percentages[i])
		{
			meaning.push_back(" SPAM");
			cout << "Message: " << new_messages[i].message <<" [isSpam: "<<new_messages[i].isSpam <<"]" << "\t Spam " << spam_percentages[i] << "\t" << " Not spam " << not_spam_percentages[i] << meaning[i] << endl;
		}
		if (0.5 * spam_percentages[i] < 0.5 * not_spam_percentages[i])
		{
			meaning.push_back(" NOT SPAM");
			cout << "Message: " << new_messages[i].message <<" [isSpam: " << new_messages[i].isSpam << "]" <<  "\t  Spam " << spam_percentages[i] << "\t" << " Not spam " << not_spam_percentages[i] << meaning[i] << endl;
		}
		cout << endl;
	}

	double correctness_of_work = 0;
	double a = 0;
	double b = 0;
	for (int i = 0; i < meaning.size(); i++) // підрахунок % правильності роботи коду
	{
		if (new_messages[i].isSpam == true && meaning[i] == " SPAM")
		{	
			a++;
			b++;
		}
		if (new_messages[i].isSpam == false && meaning[i] == " NOT SPAM")
		{
			a++;
			b++;
		}
		if (new_messages[i].isSpam == true && meaning[i] != " SPAM")
		{
			b++;
		}
		if (new_messages[i].isSpam == false && meaning[i] != " NOT SPAM")
		{
			b++;
		}

	}
	correctness_of_work = a / b;//) * 100;
	cout <<"Correctness of work : "<< correctness_of_work <<" % " << endl;
	
	return 0;
}