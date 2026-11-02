#include <iostream>
#include <windows.h>
#include <vector>

using namespace std;



using namespace std;
//клас черги на базі однозв'язного списку
class Queue
{
	struct Node
	{
		int data;
		Node* next;
		Node(int data, Node* next)
		{
			this->data = data;
			this->next = next;
		}
	};
	// приватні поля черги
private:
	int size;
	Node* head; // початок черги
	Node* tail; // кінець черги 

public:
	Queue() // конструктор черги
	{
		head = nullptr;
		tail = nullptr;
		size = 0;
	};
	~Queue() // деструктор черги
	{
		if (head == nullptr)
			return;
		Node* next = head->next;
		while (next != nullptr)
		{
			delete head;
			head = next;
			next = head->next;
		}
		delete head;
	};

	// публічні методи черги
	void push(int data)
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

	int pop()
	{
		if (head == nullptr)
			throw length_error("Queue is empty.");
		int ret_data = head->data;
		Node* new_head = head->next;
		delete head;
		head = new_head;
		if (head == nullptr)
			tail = head;
		size--;
		return ret_data;
	}

	int get(int n)
	{
		if (n < 0 || n > size)
			throw out_of_range("Cannot find element under this index.");
		if (head == nullptr)
			throw length_error("Queue is empty.");
		Node* temp = head;
		for (int i = 0; i < n; i++)
			temp = temp->next;
		return temp->data;
	}


	int get_size()
	{
		return size;
	}

	void print_queue()
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
};

DWORD WINAPI ThreadProdProc(LPVOID);
DWORD WINAPI ThreadConsProc(LPVOID);

HANDLE prod, cons, emptyQ, fullQ, blockQ;

int main()
{
	int N, prodNum, consNum;
	Queue queue;
	cout << "Enter max size of queue: ";
	cin >> N;
	cout << "Enter the number of producers: ";
	cin >> prodNum;
	cout << "Enter the number of consumers: ";
	cin >> consNum;
	cout << endl;
	// вектори потоків виробників та споживачів
	vector<HANDLE> prodThreads(prodNum);
	vector<HANDLE> consThreads(consNum);
	// ініціалізація семафорів
	prod = CreateSemaphore(NULL, 1, 1, NULL);
	cons = CreateSemaphore(NULL, 1, 1, NULL);
	emptyQ = CreateSemaphore(NULL, N, N, NULL);
	fullQ = CreateSemaphore(NULL, 0, N, NULL);
	blockQ = CreateSemaphore(NULL, 1, 1, NULL);
	// створення потоків
	for (int i = 0; i < prodNum; i++)
		if ((prodThreads[i] = CreateThread(NULL, 0, ThreadProdProc, &queue,
			0, NULL)) == NULL)
			cout << "CreateThread error." << endl;
	for (int i = 0; i < consNum; i++)
		if ((consThreads[i] = CreateThread(NULL, 0, ThreadConsProc, &queue,
			0, NULL)) == NULL)
			cout << "CreateThread error." << endl;
	// очікування на завершення кожного зі створених потоків
	for (int i = 0; i < prodNum; i++)
		WaitForSingleObject(prodThreads[i], INFINITE);
	for (int i = 0; i < consNum; i++)
		WaitForSingleObject(consThreads[i], INFINITE);
	//закриття семафорів
	CloseHandle(prod);
	CloseHandle(cons);
	CloseHandle(emptyQ);
	CloseHandle(fullQ);
	CloseHandle(blockQ);
}

DWORD WINAPI ThreadProdProc(LPVOID param)
{
	// приведення прийнятого параметру функції до типу "Queue<int>*"
	Queue* queue = static_cast<Queue*>(param);
	int item, i = 0;
	srand(GetCurrentThreadId());
	while (++i < 3)
	{
		WaitForSingleObject(prod, INFINITE); // семафор зменшує розмірічильника на 1 (допускає лише 1 виробника)
		WaitForSingleObject(emptyQ, INFINITE); // семафор зменшує розмірлічильника на 1 (допускає потік виробника поки черга не повна)
		WaitForSingleObject(blockQ, INFINITE); // семафор зменшує розмірлічильника на 1 (допускає лише 1 потік до черги)
		item = rand();
		queue->print_queue();
		cout << "\nQueue size = " << queue->get_size() << "\nProducer " <<
			GetCurrentThreadId() << " is pushing " << item << endl << endl;
		// якщо розмір черги = 1, лише один потік може її змінювати
		if (queue->get_size() == 1)
		{
			queue->push(item); // додаємо елемент
			ReleaseSemaphore(blockQ, 1, NULL); // потім відпускаємо семафор
		}
		else // у іншому випадку початок черги може змінюватися іншим потоком
		{
			ReleaseSemaphore(blockQ, 1, NULL); // одразу відпускаємо семафор
			queue->push(item); // додавання елементу паралельно з потоком	споживача
		}
		Sleep(300);
		ReleaseSemaphore(fullQ, 1, NULL); // якщо черга була порожня товідпускаємо семафор для доступу потоку споживача
			ReleaseSemaphore(prod, 1, NULL); // збільшення лічильника семафору на1 для доступу іншого потоку виробника
	}
	return true;
}

DWORD WINAPI ThreadConsProc(LPVOID param)
{
	// приведення прийнятого параметру функції до типу "Queue<int>*"
	Queue* queue = static_cast<Queue*>(param);
	int item, i = 0;
	srand(GetCurrentThreadId());
	while (++i < 3)
	{
		WaitForSingleObject(cons, INFINITE); // семафор зменшує розмілічильника на 1 (допускає лише 1 споживача)
			WaitForSingleObject(fullQ, INFINITE); // семафор зменшує розмірлічильника на 1 (допускає потік споживача поки черга не порожня)
			WaitForSingleObject(blockQ, INFINITE); // семафор зменшує розмілічильника на 1 (допускає лише 1 потік до черги)
			item = queue->get(0);
		queue->print_queue();
		cout << "\nQueue size = " << queue->get_size() << "\nConsumer " <<
			GetCurrentThreadId() << " is popping " << item << endl << endl;
		// якщо розмір черги = 1, лише один потік може її змінювати
		if (queue->get_size() == 1)
		{
			queue->pop(); // видаляємо елемент
			ReleaseSemaphore(blockQ, 1, NULL); // потім відпускаємо семафор
		}
		else // у іншому випадку кінець черги може змінюватися іншим потоком
		{
			ReleaseSemaphore(blockQ, 1, NULL); // одразу відпускаємо семафор
			queue->pop(); // видалення елементу паралельно з потокомвиробника
		}
		Sleep(700);
		ReleaseSemaphore(emptyQ, 1, NULL); // якщо черга була повна товідпускаємо семафор для доступу потоку виробника
		ReleaseSemaphore(cons, 1, NULL); // збільшення лічильника семафору на1 для доступу іншого потоку споживача
	}
	return true;
}