#include <iostream>
#include <winsock2.h>
#include <vector>
#include <thread>
#include <chrono>
#include <mutex>

#pragma comment(lib, "ws2_32.lib")

const int NUM_THREADS = 8;

std::mutex cout_mutex;

void Compute(std::vector<std::vector<int>>& matrix, int start, int end) {
    for (int i = start; i < end; ++i) {
        for (int j = 0; j < matrix.size(); ++j) {
            std::swap(matrix[i][j], matrix[matrix.size() - 1 - i][j]);
        }
    }
}

void handle_client(SOCKET clientSocket, int clientNumber) {
    int size;
    recv(clientSocket, (char*)&size, sizeof(size), 0);

    std::vector<std::vector<int>> matrix (size,std::vector<int>(size));
    for (auto& row : matrix) {
        recv(clientSocket, (char*)row.data(), sizeof(int) * row.size(), 0);
    }
    // 8
    auto start_time = std::chrono::high_resolution_clock::now();
    std::vector<std::thread> threads;
    int segment = size / NUM_THREADS;
    for (int i = 0; i < NUM_THREADS; ++i) {
        int start = i * segment;
        int end = (i + 1) * segment;
        if (i == NUM_THREADS - 1) end = size;
        threads.emplace_back(Compute, std::ref(matrix), start, end);
    }
    for (auto& thread : threads)
    {
        thread.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    for (const auto& row : matrix) {
        send(clientSocket, (char*)row.data(), sizeof(int) * row.size(), 0);
    }

    std::lock_guard<std::mutex> lock(cout_mutex);
    std::cout << "Client " << clientNumber << " (Socket: " << clientSocket << "): Matrix processed and sent back. Processing time: " << elapsed.count() << " seconds." << std::endl;

    closesocket(clientSocket);
}

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in service;
    service.sin_family = AF_INET;
    service.sin_addr.s_addr = INADDR_ANY;
    service.sin_port = htons(27015);
    bind(ListenSocket, (SOCKADDR *)&service, sizeof(service));
    listen(ListenSocket, SOMAXCONN);
    std::cout << "Server is waiting for clients..." << std::endl;
    int clientNumber = 0;

    while (true) {
        SOCKET ClientSocket = accept(ListenSocket, NULL, NULL);
        if (ClientSocket == INVALID_SOCKET){
            continue;
        }
        std::thread clientThread(handle_client, ClientSocket, ++clientNumber);
        clientThread.detach();
    }
    closesocket(ListenSocket);
    WSACleanup();
    return 0;
}
