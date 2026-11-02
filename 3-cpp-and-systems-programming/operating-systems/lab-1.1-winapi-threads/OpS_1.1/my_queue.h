#pragma once
#include <iostream>
using namespace std;

class Queue
{
	struct Node;

private:
	int size;
	Node* head; 
	Node* tail; 

public:
	Queue(); 
	~Queue();

	void push(int a);
	int pop();
	int get(int a);
	int get_size();
	void print_queue();
};