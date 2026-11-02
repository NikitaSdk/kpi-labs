cmake_minimum_required(VERSION 3.25)
project(Paralel4_Server)

set(CMAKE_CXX_STANDARD 17)

add_executable(Paralel4_Server main.cpp)

target_link_libraries(Paralel4_Server ws2_32)

