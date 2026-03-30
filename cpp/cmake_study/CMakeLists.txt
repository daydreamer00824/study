cmake_minimum_required(VERSION 3.28)

project(timer)

set(CMAKE_CXX_STANDARD 17)

add_executable(timercout
	src/timer.cpp
       	src/timermain.cpp)

target_include_directories(timercout PRIVATE include)
