cmake_minimum_required(VERSION 3.25)
project(Paralel4_Client)

set(CMAKE_CXX_STANDARD 17)

add_executable(Paralel4_Client main.cpp)

target_link_libraries(Paralel4_Client ws2_32)

