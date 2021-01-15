
cmake_minimum_required(VERSION 3.10.2)
project(Bookstore_2020)
set(CMAKE_CXX_STANDARD 14)
# SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
include_directories(
        ${PROJECT_SOURCE_DIR}/src/
        ${PROJECT_SOURCE_DIR}/src/include/
)
AUX_SOURCE_DIRECTORY(src DIR_SRCS)
add_executable(code src/main.cpp)
