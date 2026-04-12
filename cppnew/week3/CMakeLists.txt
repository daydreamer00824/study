cmake_minimum_required(VERSION 3.28)

project(scan)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


add_executable(main
	src/main.cpp
	src/timer.cpp
	src/path.cpp
	src/readpath.cpp)

target_include_directories(main PRIVATE include)
