#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib") // Зв'язок з бібліотекою Winsock для роботи з мережевими функціями

// Визначення порту, на якому буде працювати сервер
const int PORT = 8080;
// Шлях до директорії з файлами, які сервер буде віддавати
const std::string DIRECTORY_PATH = "C:/Users/user/CLionProjects/Paralel_5_Server1/cmake-build-debug/";

// Функція для читання файлів з диску
std::string Read_file(const std::string& filePath) {
    std::ifstream file(DIRECTORY_PATH + filePath); // Відкриття файлу
    if (!file.is_open()) { // Перевірка чи файл відкритий
        return ""; // Повернення порожньої стрічки, якщо файл не відкрито
    }
    std::stringstream buff; // Створення стріму для зчитування даних
    buff << file.rdbuf(); // Зчитування даних з файлу
    return buff.str(); // Повернення зчитаних даних у вигляді стрічки
}

// Клас для управління пулом потоків
class ThreadPool {
private:
    std::vector<std::thread> workers; // Вектор робочих потоків
    std::queue<std::function<void()>> tasks; // Черга завдань
    std::mutex queue_mutex; // М'ютекс для синхронізації доступу до черги
    std::condition_variable con_var; // Умовна змінна для організації роботи потоків
    bool stop; // Змінна для зупинки пулу потоків

// Конструктор ThreadPool, що ініціалізує пул потоків.
public:
    ThreadPool(size_t threads) : stop(false) {
        for (size_t i = 0; i < threads; ++i) {
            // Створення і додавання нових робочих потоків до вектора workers.
            workers.emplace_back([this] {
                // Безкінечний цикл, у якому поток виконує завдання з черги.
                while (true) {
                    std::function<void()> task;
                    {
                        // Захист доступу до черги завдань через м'ютекс.
                        std::unique_lock<std::mutex> lock(this->queue_mutex);
                        // Очікування на умовній змінній доки не з'являться завдання або не буде встановлено stop.
                        this->con_var.wait(lock, [this] { return this->stop || !this->tasks.empty(); });
                        // Вихід з циклу, якщо пул зупинено і завдань немає.
                        if (this->stop && this->tasks.empty())
                            return;
                        // Вилучення завдання з черги.
                        task = std::move(this->tasks.front());
                        this->tasks.pop();
                    }
                    // Виконання завдання.
                    task();
                }
                });
        }
    }

    // Метод для додавання нового завдання у чергу.
    void enqueue(std::function<void()> task) {
        {
            // Захист черги завдань через м'ютекс.
            std::unique_lock<std::mutex> lock(queue_mutex);
            // Перевірка, чи пул не зупинено.
            if (stop) {
                std::cout << "stop queue." << std::endl;
                return;
            }
            // Додавання завдання до черги.
            tasks.emplace(task);
        }
        // Повідомлення одного з очікуючих потоків, що завдання доступне.
        con_var.notify_one();
    }

    // Деструктор ThreadPool, який зупиняє всі потоки та очікує їх завершення.
    ~ThreadPool() {
        {
            // Захист спільного ресурсу через м'ютекс та встановлення stop у true.
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        // Пробудження всіх потоків.
        con_var.notify_all();
        // Очікування завершення всіх потоків.
        for (std::thread& worker : workers) {
            worker.join();
        }
    }
};

// Функція для обробки запитів від клієнтів
void handleRequest(SOCKET clientSocket) {
    char buffer[1024]; // Буфер для зберігання даних від клієнта
    int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0); // Отримання даних від клієнта
    if (bytesReceived > 0) { // Перевірка, чи були отримані дані
        buffer[bytesReceived] = '\0'; // Закінчення стрічки нульовим символом
        std::string request(buffer); // Створення стрічки з буфера
        std::size_t pos = request.find("GET "); // Пошук початку запиту GET
        if (pos != std::string::npos) { // Якщо запит знайдено
            std::size_t endPos = request.find(" HTTP/1.1", pos + 4); // Пошук кінця запиту
            if (endPos != std::string::npos) { // Якщо кінець запиту знайдено
                std::string path = request.substr(pos + 4, endPos - (pos + 4)); // Визначення шляху запиту
                std::string filename;
                if (path == "/page2.html") {
                    filename = "page2.html"; // Вибір файлу для відповіді
                }
                else {
                    filename = "index.html"; // Вибір файлу для відповіді
                }

                std::string content = Read_file(filename); // Читання файлу
                std::string response;
                if (content.empty()) { // Якщо файл не знайдено
                    std::string notFoundMessage = "<html><body><h1>404 Not Found</h1></body></html>";
                    response = "HTTP/1.1 404 Not Found\r\nContent-Length: " + std::to_string(notFoundMessage.length()) + "\r\nContent-Type: text/html\r\n\r\n" + notFoundMessage;
                }
                else { // Якщо файл знайдено
                    response = "HTTP/1.1 200 OK\r\nContent-Length: " + std::to_string(content.length()) + "\r\nContent-Type: text/html\r\n\r\n" + content;
                }
                send(clientSocket, response.c_str(), response.length(), 0); // Відправлення відповіді клієнту
            }
        }
    }
    closesocket(clientSocket); // Закриття сокета
}

// Функція для запуску сервера
void startServer() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) { // Ініціалізація Winsock
        std::cerr << "WSAStartup failed.\n";
        exit(1);
    }

    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); // Створення сокета
    if (serverSocket == INVALID_SOCKET) { // Перевірка на успішність створення сокета
        std::cerr << "Socket creation failed: " << WSAGetLastError() << '\n';
        WSACleanup();
        exit(1);
    }

    sockaddr_in serverAddr; // Структура для адреси сервера
    memset(&serverAddr, 0, sizeof(serverAddr)); // Ініціалізація структури нулями
    serverAddr.sin_family = AF_INET; // Тип адреси
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY); // Адреса сервера (дозволяє приймати будь-яке з'єднання)
    serverAddr.sin_port = htons(PORT); // Порт сервера

    if (bind(serverSocket, (SOCKADDR*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) { // Прив'язка адреси до сокета
        std::cerr << "Bind failed: " << WSAGetLastError() << '\n';
        closesocket(serverSocket);
        WSACleanup();
        exit(1);
    }

    if (listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) { // Початок прослуховування порту
        std::cerr << "Listen failed: " << WSAGetLastError() << '\n';
        closesocket(serverSocket);
        WSACleanup();
        exit(1);
    }

    std::cout << "Server is listening on port " << PORT << "...\n"; // Повідомлення про успішний запуск сервера
    ThreadPool pool(4); // Створення пулу потоків

    while (true) { // Безкінечний цикл для приймання з'єднань
        sockaddr_in clientAddr; // Структура для адреси клієнта
        int clientAddrSize = sizeof(clientAddr); // Розмір адреси клієнта
        SOCKET clientSocket = accept(serverSocket, (SOCKADDR*)&clientAddr, &clientAddrSize); // Приймання з'єднання
        if (clientSocket != INVALID_SOCKET) { // Якщо з'єднання успішне
            pool.enqueue([clientSocket]() { handleRequest(clientSocket); }); // Додавання завдання у пул потоків
        }
    }
    closesocket(serverSocket); // Закриття сокета сервера
    WSACleanup(); // Очищення ресурсів Winsock
}

int main() {
    startServer(); // Запуск сервера
    return 0; // Завершення програми
}
