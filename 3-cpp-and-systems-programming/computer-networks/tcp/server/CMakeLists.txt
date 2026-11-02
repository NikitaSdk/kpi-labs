cmake_minimum_required(VERSION 3.25)
project(LAB1_TCP_SERV)

set(CMAKE_CXX_STANDARD 17)

add_executable(LAB1_TCP_SERV main.cpp)

target_link_libraries(LAB1_TCP_SERV ws2_32)