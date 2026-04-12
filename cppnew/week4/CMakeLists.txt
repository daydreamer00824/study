cmake_minimum_required(VERSION 3.28)

project(opencv_c++)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

add_executable(main src/main.cpp src/image.cpp)

target_include_directories(main PRIVATE include)
target_link_libraries(main PRIVATE ${OpenCV_LIBS})
