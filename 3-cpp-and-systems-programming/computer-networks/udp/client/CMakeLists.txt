cmake_minimum_required(VERSION 3.25)
project(LAB1_UDP_CLIENT)

set(CMAKE_CXX_STANDARD 17)

add_executable(LAB1_UDP_CLIENT main.cpp)

target_link_libraries(LAB1_UDP_CLIENT ws2_32)
