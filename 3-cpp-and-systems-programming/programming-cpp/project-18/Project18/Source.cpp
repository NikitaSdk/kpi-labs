#include <iostream> // Бібліотека вводу/виводу
#include <string> // Бібліотека для роботи зі стрічками
#include <vector> // Бібліотека для роботи з векторами
#include <thread> // Бібліотека для роботи з потоками
#include <chrono> // Бібліотека для роботи з часом
#include <mutex> // Бібліотека для синхронізації потоків
#include <winsock2.h> // Бібліотека Windows Sockets API для роботи з мережами
#include <ws2tcpip.h> // Бібліотека для роботи з IP-адресами

#pragma comment(lib, "ws2_32.lib") // Лінковка з бібліотекою Winsock

const int PORT = 8080; // Визначення порту, на якому буде здійснюватись з'єднання
const std::string SERVER_IP = "127.0.0.1"; // IP-адреса сервера (локальний адрес)

void initializeWinsock() {
    WSADATA wsaData; // Структура для інформації про Winsock
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData); // Ініціалізація Winsock
    if (result != 0) {
        std::cerr << "WSAStartup failed: " << result << std::endl;
        exit(1);
    }
}

SOCKET createSocket() {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0); // Створення TCP сокету
    if (sock == INVALID_SOCKET) {
        std::cerr << "Error at socket(): " << WSAGetLastError() << std::endl;
        WSACleanup();
        exit(1);
    }

    sockaddr_in serverAddr; // Структура адреси сервера
    serverAddr.sin_family = AF_INET; // Тип адреси (IPv4)
    serverAddr.sin_port = htons(PORT); // Порт
    inet_pton(AF_INET, SERVER_IP.c_str(), &serverAddr.sin_addr); // Конвертація IP-адреси з стрічки в бінарний вигляд

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        exit(1);
    }

    return sock;
}

void sendRequest(SOCKET sock, const std::string& path) {
    std::string request = "GET " + path + " HTTP/1.1\r\nHost: " + SERVER_IP + "\r\nConnection: close\r\n\r\n"; // Формування HTTP-запиту
    send(sock, request.c_str(), request.length(), 0); // Відправлення запиту

    char buffer[4096];
    int received = recv(sock, buffer, sizeof(buffer), 0); // Отримання відповіді від сервера
    if (received > 0) {
        std::cout << "Received response for " << path << ": " << std::string(buffer, received) << std::endl; // Вивід відповіді
    }

    closesocket(sock); // Закриття сокета
}

int main() {
    initializeWinsock(); // Ініціалізація Winsock

    int numClients;
    std::cout << "Enter the number of clients: "; // Запит на кількість клієнтів
    std::cin >> numClients;

    std::vector<std::thread> clients; // Вектор потоків для клієнтів
    for (int i = 0; i < numClients; ++i) {
        clients.push_back(std::thread([] {
            SOCKET sock = createSocket(); // Створення сокету
            sendRequest(sock, "/index.html"); // Відправлення запиту на першу сторінку
            SOCKET sock2 = createSocket(); // Створення другого сокету
            sendRequest(sock2, "/page2.html"); // Відправлення запиту на другу сторінку
            }));
    }
    for (auto& client : clients) {
        client.join(); // Завершення потоків
    }
    WSACleanup(); // Очищення ресурсів Winsock
    return 0;
}