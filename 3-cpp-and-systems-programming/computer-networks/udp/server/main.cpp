#include <iostream>
#include <winsock2.h>


#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsData;
    int iResult = WSAStartup(MAKEWORD(2, 2), &wsData);
    if (iResult != 0) {
        std::cerr << "WSAStartup failed: " << iResult << std::endl;
        return 1;
    }

    SOCKET udpservsocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udpservsocket == INVALID_SOCKET) {
        std::cerr << "Error at socket(): " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(223);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    iResult = bind(udpservsocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    if (iResult == SOCKET_ERROR) {
        std::cerr << "Bind failed with error: " << WSAGetLastError() << std::endl;
        closesocket(udpservsocket);
        WSACleanup();
        return 1;
    }
    sockaddr_in client;
    int clientSize = sizeof(client);
    int numbers[15];
    iResult = recvfrom(udpservsocket, (char*)numbers, sizeof(numbers), 0, (sockaddr*)&client, &clientSize);
    if (iResult == SOCKET_ERROR) {
        std::cerr << "recvfrom failed with error: " << WSAGetLastError() << std::endl;
        closesocket(udpservsocket);
        WSACleanup();
        return 1;
    }
    std::cout << "Received numbers:" << std::endl;
    for (int i = 0; i < 15; ++i) {
        std::cout << "Number " << i + 1 << ": " << numbers[i] << std::endl;
    }
    closesocket(udpservsocket);
    WSACleanup();
    return 0;
}
