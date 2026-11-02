#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsData;
    int iResult = WSAStartup(MAKEWORD(2, 2), &wsData);
    if (iResult != 0) {
        std::cerr << "WSAStartup failed: " << iResult << std::endl;
        return 1;
    }

    SOCKET udpclsocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udpclsocket == INVALID_SOCKET) {
        std::cerr << "Error at socket(): " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }

    sockaddr_in linkto;
    linkto.sin_family = AF_INET;
    linkto.sin_port = htons(223);
    inet_pton(AF_INET, "192.168.0.106", &linkto.sin_addr);

    int numbers[15] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    std::cout << "Sending data to the server: Starting" << std::endl;
    sendto(udpclsocket, (char*)numbers, sizeof(numbers), 0, (sockaddr*)&linkto, sizeof(linkto));
    std::cout << "Sending data to the server: Completed" << std::endl;

    closesocket(udpclsocket);
    WSACleanup();
    return 0;
}

