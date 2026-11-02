#pragma once
#include <stdexcept>
#include <iostream>
using namespace std;

class Queue
{
private:

	struct Node;
	Node* head;
	Node* tail;

public:
	Queue();
	~Queue();

	void push(int key);

	int pop();

	int getSize();

	void printQueue();

};