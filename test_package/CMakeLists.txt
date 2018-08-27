project(date-example CXX C)
cmake_minimum_required(VERSION 2.8.11)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

find_package(date REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(ZLIB REQUIRED)

file(GLOB SOURCE_FILES *.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME}
    ${DATE_LIBRARIES}
    ${OpenSSL_LIBRARIES}
    ${ZLIB_LIBRARIES}
    )
