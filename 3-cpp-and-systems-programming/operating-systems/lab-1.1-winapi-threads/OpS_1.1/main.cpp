#include <iostream>
#include <windows.h>
#include <vector>
#include "my_queue.h"

using namespace std;

HANDLE producer;           
HANDLE consumer;
HANDLE empty_queue;
HANDLE full_queue;
HANDLE block_queue;

DWORD WINAPI ThreadProdProc(LPVOID param)
{
	Queue* queue = static_cast<Queue*>(param);

	int item = 0;
	int i = 0;
	srand(GetCurrentThreadId()); 

	while (++i < 3)
	{
		WaitForSingleObject(producer, INFINITE); 
		WaitForSingleObject(empty_queue, INFINITE); 
		WaitForSingleObject(block_queue, INFINITE); 
		item = rand(); 
		queue->print_queue(); 
		cout << "\nQueue size = " << queue->get_size() << "\nProducer " << GetCurrentThreadId() << " is pushing " << item << endl << endl;

		if (queue->get_size() == 1)
		{
			queue->push(item); 
			ReleaseSemaphore(block_queue, 1, NULL); 
		}
		else 
		{
			ReleaseSemaphore(block_queue, 1, NULL); 
			queue->push(item);
		}

		Sleep(500);
		
		ReleaseSemaphore(full_queue, 1, NULL);
		ReleaseSemaphore(producer, 1, NULL);
	}
	return true;
}


DWORD WINAPI ThreadConsProc(LPVOID param)
{
	Queue* queue = static_cast<Queue*>(param);
	int item = 0;
	int i = 0;
	srand(GetCurrentThreadId()); 

	while (++i < 3)
	{
		WaitForSingleObject(consumer, INFINITE); 
		WaitForSingleObject(full_queue, INFINITE); 
		WaitForSingleObject(block_queue, INFINITE); 
		item = queue->get(0);
		queue->print_queue(); 
		cout << "\nQueue size = " << queue->get_size() << "\nConsumer " << GetCurrentThreadId() << " is popping " << item << endl << endl;

		if (queue->get_size() == 1)
		{
			queue->pop(); 
			ReleaseSemaphore(block_queue, 1, NULL); 
		}
		else 
		{
			ReleaseSemaphore(block_queue, 1, NULL); 
			queue->pop(); 
		}
		Sleep(1000); 
		ReleaseSemaphore(empty_queue, 1, NULL); 
		ReleaseSemaphore(consumer, 1, NULL); 
	}
	return true;
}

int main()
{
	int queue_size, producer_num, consumer_num;
	Queue queue;
	cout << "Enter max size of queue: ";
	cin >> queue_size;
	cout << "Enter the number of producers: ";
	cin >> producer_num;
	cout << "Enter the number of consumers: ";
	cin >> consumer_num;
	cout << endl;

	vector<HANDLE> producer_threads(producer_num);
	vector<HANDLE> consumer_threads(consumer_num);

	producer = CreateSemaphore(NULL, 1, 1, NULL);
	consumer = CreateSemaphore(NULL, 1, 1, NULL);
	empty_queue = CreateSemaphore(NULL, queue_size, queue_size, NULL);
	full_queue = CreateSemaphore(NULL, 0, queue_size, NULL);
	block_queue = CreateSemaphore(NULL, 1, 1, NULL);

	for (int i = 0; i < producer_num; i++)
	{
		if ( (producer_threads[i] = CreateThread(NULL, 0, ThreadProdProc, &queue, 0, NULL)) == NULL )
		{
			cout << "CreateThread error." << endl;
		}
	}

	for (int i = 0; i < consumer_num; i++)
	{
		if ((consumer_threads[i] = CreateThread(NULL, 0, ThreadConsProc, &queue, 0, NULL)) == NULL)
		{
			cout << "CreateThread error." << endl;
		}
	}

	for (int i = 0; i < producer_num; i++)
	{
		WaitForSingleObject(producer_threads[i], INFINITE);
	}
	for (int i = 0; i < consumer_num; i++)
	{
		WaitForSingleObject(consumer_threads[i], INFINITE);
	}

	CloseHandle(producer);
	CloseHandle(consumer); 
	CloseHandle(empty_queue);
	CloseHandle(full_queue);
	CloseHandle(block_queue);

	return 0;
}
