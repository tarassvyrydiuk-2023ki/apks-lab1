cmake_minimum_required(VERSION 3.20)
project(hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Executables always go to build/bin (also for multi-config generators).
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
foreach(cfg IN ITEMS DEBUG RELEASE RELWITHDEBINFO MINSIZEREL)
    set("CMAKE_RUNTIME_OUTPUT_DIRECTORY_${cfg}" "${CMAKE_BINARY_DIR}/bin")
endforeach()

add_library(hello_core src/hello.cpp)
target_include_directories(hello_core PUBLIC include)

add_executable(hello src/main.cpp)
target_link_libraries(hello PRIVATE hello_core)

enable_testing()

include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://codeload.github.com/google/googletest/zip/refs/tags/v1.14.0
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(hello_tests tests/test_hello.cpp)
target_link_libraries(hello_tests PRIVATE hello_core GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(hello_tests)
