#include "my_queue.h"

using namespace std;


struct Queue::Node
{
	int key;
	Node* next;
	Node(int key, Node* next)
	{
		this->key = key;
		this->next = next;
	}
};

Queue::Queue()
{
	head = nullptr;
	tail = nullptr;
}

Queue :: ~Queue()
{
	Node* current = head;
	while (current)
	{
		Node* next = current->next;
		delete current;
		current = next;
	}
}


void Queue::push(int key)
{
	Node* newNode = new Node(key, nullptr);

	if (tail == nullptr)
	{
		head = newNode;
		tail = newNode;
	}
	else
	{
		tail->next = newNode;
		tail = newNode;
	}
}

int Queue::pop()
{
	if (head == nullptr)
	{
		throw length_error("Queue is empty.");
	}

	Node* temp = head;
	int val = temp->key;

	head = head->next;
	if (head == nullptr)
	{
		tail = nullptr;
	}

	delete temp;
	return val;
}

int Queue:: getSize()
{
	int size = 0;
	Node* current = head;
	while (current)
	{
		size++;
		current = current->next;
	}
	return size;

}

void Queue::printQueue()
{
	cout << "Queue: ";
	Node* current = head;
	while (current)
	{
		cout << current->key << " ";
		current = current->next;
	}
	cout << endl;
}