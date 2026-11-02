#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <vector>
#include <cstdlib>
#include <thread>
#include <mutex>

#pragma comment(lib, "ws2_32.lib")

std::mutex cout_mutex;

std::vector<std::vector<int>> generate_matrix(int size) {
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            matrix[i][j] = rand() % 10;
        }
    }
    return matrix;
}

void send_matrix(const SOCKET& socket, const std::vector<std::vector<int>>& matrix) {
    int size = matrix.size();
    send(socket, (char*)&size, sizeof(size), 0);
    for (const auto& row : matrix) {
        send(socket, (char*)row.data(), sizeof(int) * row.size(), 0);
    }
}

std::vector<std::vector<int>> receive_matrix(const SOCKET& socket, int size) {
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size));
    for (auto& row : matrix) {
        recv(socket, (char*)row.data(), sizeof(int) * row.size(), 0);
    }
    return matrix;
}

void client_process(int client_id) {
    int size = 1000 + client_id * 1000;
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET ConnectSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(27015);
    inet_pton(AF_INET, "192.168.0.106", &addr.sin_addr);
    if (connect(ConnectSocket, (sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::lock_guard<std::mutex> lock(cout_mutex);
        std::cerr << "Client " << client_id << ": Server connection error." << std::endl;
        closesocket(ConnectSocket);
        WSACleanup();
        return;
    }
    auto matrix = generate_matrix(size);
    {
        std::lock_guard<std::mutex> lock(cout_mutex);
        std::cout << "Client " << client_id << ": Matrix generated and sent. Size: " << size <<" x "<< size << std::endl;
    }
    send_matrix(ConnectSocket, matrix);
    auto received_matrix = receive_matrix(ConnectSocket, size);
    {
        std::lock_guard<std::mutex> lock(cout_mutex);
        std::cout << "Client " << client_id << ": Processed matrix received." << std::endl;
    }
    closesocket(ConnectSocket);
    WSACleanup();
}

int main() {
    int client_count;
    std::cout << "Enter number of clients: ";
    std::cin >> client_count;
    std::vector<std::thread> clients;
    for (int i = 0; i < client_count; i++) {
        clients.emplace_back(client_process, i + 1);
    }
    for (auto& client : clients) {
        client.join();
    }
    return 0;
}
