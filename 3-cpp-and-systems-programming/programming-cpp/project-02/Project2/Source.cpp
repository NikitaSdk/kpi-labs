#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>

using namespace std;

struct Type_of_message
{
	string message;
	bool isSpam = 0;
};

void Spam_Percentage_Calculate()
{


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

	for (int i = 0; i < first_six_messages.size(); i++)
	{
		if (first_six_messages[i].isSpam)
		{
			cout << first_six_messages[i].message<<" "<< " (SPAM) " << endl;
		}
		else
		{
			cout << first_six_messages[i].message << " " << " (NOT SPAM) " << endl;
		}
	}

	unordered_map <string, int> words;
	unordered_map <string, int> spam_counter;
	
	int iterator = 0;
	for (auto& i : first_six_messages)
	{
		istringstream iss(first_six_messages[iterator].message);
		string word;
		while (iss >> word) 
		{
			 words[word]++;
			 
			 if (first_six_messages[iterator].isSpam == true)
			 {
				 spam_counter[word]++;
			 }
			 if (first_six_messages[iterator].isSpam == false)
			 {
				 spam_counter[word] + 0;
			 } 
		}
		iterator++;
	}
	

	vector <int> all_amount;
	vector <int> spam_amount;
	vector <double> spam_percent;
	vector <double> not_spam_percent;
	vector <double> normal_spam_percent;
	vector <double> normal_not_spam_percent;
	vector <string> all_words;


	cout << endl;
	for (auto& pair : words) 
	{
		all_amount.push_back(pair.second);
		cout <<"Word: " << pair.first <<"\t " << "Amount: " << pair.second << endl;
	}
	cout << endl;
	for (auto& pair : spam_counter)
	{
		spam_amount.push_back(pair.second);
		cout <<"Word: "<< pair.first << "\t " << "Spam amount: " << pair.second << endl;
	}
	cout << endl;

	int itr = 0;
	for (auto& pair : words)
	{
		double a = double(spam_amount[itr]) / double(all_amount[itr]);
		spam_percent.push_back(a);
		double b = 1 - a;
		not_spam_percent.push_back(b);
		cout << "Word: "<< pair.first << "\t % Spam: " << spam_percent[itr] << " \t " << "% Not spam: " << not_spam_percent[itr] << endl;
		itr++;
	}
	cout << endl;
	int itr1 = 0;
	for (auto& pair : words)
	{
		double p_norm_spam = (double(pair.second) * double(spam_percent[itr1]) + 0.5)/ (double(pair.second) + 1);
		double p_norm_not_spam = 1 - p_norm_spam;
		p_norm_spam = round(p_norm_spam * 100) / 100;
		p_norm_not_spam = round(p_norm_not_spam * 100) / 100;
		cout<<"Word: "<<pair.first << "\tNormal prob SPAM: " << p_norm_spam << " \t Normal prob Not_SPAM: " << p_norm_not_spam << endl;
		itr1++;
	}

	return 0;
}