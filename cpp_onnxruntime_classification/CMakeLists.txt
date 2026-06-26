cmake_minimum_required(VERSION 3.28)

project(test)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)


set(ORT_DIR /home/daydreamer/third_party/onnxruntime)
set(ORT_INCLUDE_DIR ${ORT_DIR}/include)
set(ORT_LIB_DIR ${ORT_DIR}/lib)
set(ORT_LIB ${ORT_LIB_DIR}/libonnxruntime.so)

add_executable(cpp_ort_infer
	src/main.cpp
	src/timer.cpp
	src/image_process.cpp
	src/postprocess.cpp
	src/label_map.cpp
	src/ort_runner.cpp
	src/batch_infer.cpp
)

add_executable(cpp_ort_benchmark
        src/benchmark_main.cpp
        src/benchmark.cpp
        src/timer.cpp
        src/image_process.cpp
        src/postprocess.cpp
        src/label_map.cpp
        src/ort_runner.cpp
        src/batch_infer.cpp
)

foreach(target cpp_ort_infer cpp_ort_benchmark)
    target_include_directories(${target} PRIVATE
            ${CMAKE_SOURCE_DIR}/include
            ${ORT_INCLUDE_DIR}
            ${OpenCV_INCLUDE_DIRS}
    )

    target_link_libraries(${target} PRIVATE
            ${OpenCV_LIBS}
            ${ORT_LIB}
    )

    set_target_properties(${target} PROPERTIES
            BUILD_RPATH ${ORT_LIB_DIR}
    )
endforeach()

