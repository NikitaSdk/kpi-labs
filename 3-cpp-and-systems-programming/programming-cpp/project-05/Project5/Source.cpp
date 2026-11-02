#include <windows.h>
#include <iostream>
#include <stdexcept>

#define VISITORS_NUM 8
#define CHAIRS_NUM 2

CRITICAL_SECTION visitors_queue;
CRITICAL_SECTION output;
CRITICAL_SECTION barber;
CRITICAL_SECTION barber1;

using namespace std;

class Queue
{
private:
	struct Node
	{
		int key;
		Node* next;
		Node(int key, Node* next) : key(key), next(next) {}
	};

	Node* front;
	Node* rear;

public:
	Queue() : front(nullptr), rear(nullptr) {}

	~Queue()
	{
		Node* current = front;
		while (current)
		{
			Node* next = current->next;
			delete current;
			current = next;
		}
	}

	void enqueue(int key)
	{
		Node* newNode = new Node(key, nullptr);

		if (rear == nullptr)
		{
			front = newNode;
			rear = newNode;
		}
		else
		{
			rear->next = newNode;
			rear = newNode;
		}
	}

	int dequeue()
	{
		if (front == nullptr)
			throw length_error("Queue is empty.");

		Node* temp = front;
		int val = temp->key;

		front = front->next;
		if (front == nullptr)
			rear = nullptr;

		delete temp;
		return val;
	}

	int getSize() const
	{
		int size = 0;
		Node* current = front;
		while (current)
		{
			size++;
			current = current->next;
		}
		return size;
	}

	void printQueue() const
	{
		cout << "Очередь: ";
		Node* current = front;
		while (current)
		{
			cout << current->key << " ";
			current = current->next;
		}
		cout << endl;
	}
};

Queue* visitors;

DWORD WINAPI functionBarber(LPVOID arg)
{
	while (true)
	{
		EnterCriticalSection(&visitors_queue);

		if (visitors->getSize() == 0)
		{
			LeaveCriticalSection(&visitors_queue);
			EnterCriticalSection(&output);
			cout << "Барбер спит" << endl;
			LeaveCriticalSection(&output);

			Sleep(1000);
			EnterCriticalSection(&barber1);
		}
		else
		{
			int clientId = visitors->dequeue();
			LeaveCriticalSection(&visitors_queue);

			Sleep(2000 + rand() % 2000);

			EnterCriticalSection(&output);
			cout << "-----------------Барбер закончил, клиент " << clientId << " уходит" << endl;
			LeaveCriticalSection(&output);

			LeaveCriticalSection(&barber);
		}
	}
	return true;
}

DWORD WINAPI functionVisit(LPVOID arg)
{
	int clientId = *static_cast<int*>(arg) + 1;

	EnterCriticalSection(&visitors_queue);
	if ((CHAIRS_NUM - visitors->getSize()) > 0)
	{
		EnterCriticalSection(&output);
		visitors->enqueue(clientId);
		cout << "Клиент " << clientId << " добавлен в очередь, длина очереди: " << visitors->getSize() << endl;
		visitors->printQueue();
		LeaveCriticalSection(&visitors_queue);
		LeaveCriticalSection(&output);

		if (visitors->getSize() == 1)
		{
			LeaveCriticalSection(&barber1);
		}
		EnterCriticalSection(&barber);

		EnterCriticalSection(&output);
		cout << "+++++++++++++++++Барбер приступил к работе " << clientId << endl;
		LeaveCriticalSection(&output);
	}
	else
	{
		LeaveCriticalSection(&visitors_queue);

		EnterCriticalSection(&output);
		cout << "!!!Нет свободных мест, клиент " << clientId << " уходит" << endl;
		LeaveCriticalSection(&output);
	}

	return true;
}

int main()
{
	setlocale(LC_ALL, "ru");

	DWORD threadId;

	HANDLE barberThread;
	HANDLE visitorsThreads[VISITORS_NUM];

	int visitorsIds[VISITORS_NUM];
	visitors = new Queue();

	InitializeCriticalSection(&output);
	InitializeCriticalSection(&visitors_queue);
	InitializeCriticalSection(&barber);
	InitializeCriticalSection(&barber1);
	EnterCriticalSection(&barber1);

	barberThread = CreateThread(NULL, 0, &functionBarber, NULL, 0, &threadId);
	for (int i = 0; i < VISITORS_NUM; ++i)
	{
		visitorsIds[i] = i;
		Sleep(1000 + rand() % 500);
		visitorsThreads[i] = CreateThread(NULL, 0, &functionVisit, &visitorsIds[i], 0, &threadId);
	}
	WaitForSingleObject(barberThread, INFINITE);
	WaitForMultipleObjects(VISITORS_NUM, visitorsThreads, true, INFINITE);

	CloseHandle(barberThread);
	for (int j = 0; j < VISITORS_NUM; ++j)
		CloseHandle(visitorsThreads[j]);

	DeleteCriticalSection(&output);
	DeleteCriticalSection(&visitors_queue);
	DeleteCriticalSection(&barber);

	delete visitors;

	return 0;
}