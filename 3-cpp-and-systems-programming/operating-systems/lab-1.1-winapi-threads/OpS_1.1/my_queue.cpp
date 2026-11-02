#include "my_queue.h"


struct Queue::Node
{
	int data;
	Node* next;
	Node(int data, Node* next)
	{
		this->data = data;
		this->next = next;
	}
};


Queue::Queue() 
{
	head = nullptr;
	tail = nullptr;
	size = 0;
}

Queue:: ~Queue()
{
	if (head == nullptr)
	{
		return;
	}
	Node* next = head->next;
	while (next != nullptr)
	{
		delete head;
		head = next;
		next = head->next;
	}
	delete head;
}

void Queue::push (int data)
{
	if (tail == nullptr)
	{
		tail = new Node(data, nullptr);
		head = tail;
	}
	else
	{
		tail->next = new Node(data, nullptr);
		tail = tail->next;
	}
	size++;
}

void Queue :: print_queue()
{
	if (head == nullptr)
	{
		cout << "Queue is empty.";
		return;
	}
	cout << "Queue: ";

	Node* temp = head;

	for (int i = 0; i < size; i++)
	{
		cout << temp->data << " ";
		temp = temp->next;
	}

}

int Queue::pop()
{
	if (head == nullptr)
	{
		cout << "Queue is empty." << endl;
		return -1;
	}

	int ret_data = head->data;
	Node* new_head = head->next;
	delete head;
	head = new_head;
	if (head == nullptr)
	{
		tail = head;
	}
	size--;
	return ret_data;
}

int Queue::get(int n)
{
	if (n < 0 || n > size)
	{
		cout << "Cannot find element under this index." << endl;
	}
	if (head == nullptr)
	{
		cout << "Queue is empty." << endl;
	}

	Node* temp = head;
	for (int i = 0; i < n; i++)
	{
		temp = temp->next;
	}
	return temp->data;
}

int Queue::get_size()
{
	return size;
}
