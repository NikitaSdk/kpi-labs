#include <windows.h>
#include <iostream>
#include <stdexcept>
#include "my_queue.h"

using namespace std;

#define VISITORS_NUM 8
#define CHAIRS_NUM 2

CRITICAL_SECTION visitors_queue;
CRITICAL_SECTION output;
CRITICAL_SECTION barber;
CRITICAL_SECTION barber1;
 
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
			cout << "Barber is sleeping" << endl;
			LeaveCriticalSection(&output); 

			Sleep(1000);
			EnterCriticalSection(&barber1); 
		}
		else 
		{
			int clientId = visitors->pop(); 
			LeaveCriticalSection(&visitors_queue);

			Sleep(2000 + rand() % 2000); 

			EnterCriticalSection(&output); 
			cout << "Barber done work and client " << clientId << " go away" << endl; 
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
		visitors->push(clientId); 
		cout << "Client " << clientId << " added to queue, queue size: " << visitors->getSize() << endl;
		visitors->printQueue();
		LeaveCriticalSection(&visitors_queue); 
		LeaveCriticalSection(&output);

		if (visitors->getSize() == 1)
		{
			LeaveCriticalSection(&barber1);
		}
		EnterCriticalSection(&barber); 

		EnterCriticalSection(&output); 
		cout << "Barber is working: " << clientId << endl;
		LeaveCriticalSection(&output); 
	}
	else 
	{
		LeaveCriticalSection(&visitors_queue); 

		EnterCriticalSection(&output);
		cout << "No chairs, client " << clientId << " go away" << endl;
		LeaveCriticalSection(&output);
	}

	return true;
}

int main()
{
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
	{
		CloseHandle(visitorsThreads[j]);
	}

	DeleteCriticalSection(&output);
	DeleteCriticalSection(&visitors_queue);
	DeleteCriticalSection(&barber);

	delete visitors;

	return 0;
}

