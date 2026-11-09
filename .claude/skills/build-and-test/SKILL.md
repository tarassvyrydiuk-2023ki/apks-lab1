---
name: build-and-test
description: Create the CMake build system, the testable add() function, the GoogleTest unit test BasicAddition and the cross-platform scripts ci.sh/ci.bat/run.sh/run.bat that build build/bin/hello[.exe]. Use when /create-build is invoked.
---

# Skill: build-and-test

## Коли застосовувати

- є вихідний код (`src/`, `include/`), але немає `CMakeLists.txt` чи тестів;
- викликано `/create-build` або крок 3 `/init`.

## Вхідні дані

| Параметр | За замовчуванням |
|---|---|
| `project_name` | `hello` |
| `cmake_min` | `3.20` |
| `gtest_version` | `v1.14.0` (`FetchContent`, фіксований тег) |

## Результат (файли)

| Файл | Призначення |
|---|---|
| `CMakeLists.txt` | бібліотека `hello_core`, виконуваний файл `hello`, `enable_testing()`, GoogleTest |
| `tests/test_hello.cpp` | тести GoogleTest, зокрема `BasicAddition` |
| `ci.sh` | збірка + тести + smoke test (Linux/macOS), LF |
| `ci.bat` | збірка + тести + smoke test (Windows), CRLF |
| `run.sh` / `run.bat` | запуск `build/bin/hello[.exe]` |

### Шаблон `CMakeLists.txt`

```cmake
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
```

### Шаблон `tests/test_hello.cpp`

```cpp
#include <gtest/gtest.h>

#include <string>

#include "hello/hello.hpp"

TEST(HelloTest, BasicAddition) {
    EXPECT_DOUBLE_EQ(hello::add(2, 3), 5);
}

TEST(HelloTest, AdditionWithNegativesAndZero) {
    EXPECT_DOUBLE_EQ(hello::add(0, 0), 0);
    EXPECT_DOUBLE_EQ(hello::add(-1, 1), 0);
    EXPECT_DOUBLE_EQ(hello::add(2.5, 0.5), 3.0);
}

TEST(HelloTest, Greeting) {
    EXPECT_EQ(hello::greeting(), std::string("Hello, World!"));
}
```

### Шаблон `ci.sh` (LF)

```sh
#!/usr/bin/env bash
# Build & test pipeline for Linux/macOS: configure -> build -> ctest -> smoke test.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> [1/4] CMake version"
cmake --version

echo "==> [2/4] Configuring and building (Release)"
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --parallel

echo "==> [3/4] Running unit tests (ctest)"
mkdir -p build/test-results
ctest --test-dir build -C Release --output-on-failure --output-junit test-results/junit.xml

echo "==> [4/4] Smoke test of build/bin/hello"
test -x build/bin/hello
OUTPUT="$(build/bin/hello)"
echo "$OUTPUT"
if [ "$OUTPUT" != "Hello, World!" ]; then
    echo "ERROR: unexpected output from build/bin/hello" >&2
    exit 1
fi
echo "CI: SUCCESS"
```

### Шаблон `ci.bat` (CRLF)

```bat
@echo off
rem Build & test pipeline for Windows: configure -> build -> ctest -> smoke test.
setlocal EnableExtensions
cd /d "%~dp0"

echo ==^> [1/4] CMake version
cmake --version || goto :fail

echo ==^> [2/4] Configuring and building (Release)
cmake -S . -B build || goto :fail
cmake --build build --config Release --parallel || goto :fail

echo ==^> [3/4] Running unit tests (ctest)
if not exist "build\test-results" mkdir "build\test-results"
ctest --test-dir build -C Release --output-on-failure --output-junit test-results\junit.xml || goto :fail

echo ==^> [4/4] Smoke test of build\bin\hello.exe
if not exist "build\bin\hello.exe" goto :fail
set "OUTPUT="
for /f "delims=" %%L in ('"build\bin\hello.exe"') do set "OUTPUT=%%L"
echo %OUTPUT%
if not "%OUTPUT%"=="Hello, World!" (
    echo ERROR: unexpected output from build\bin\hello.exe 1>&2
    goto :fail
)
echo CI: SUCCESS
exit /b 0

:fail
echo CI: FAILED 1>&2
exit /b 1
```

`run.sh` → `exec build/bin/hello "$@"` (з перевіркою, що файл існує). `run.bat` → `build\bin\hello.exe %*`.

## Порядок дій

1. Створи файли за шаблонами (правила CREATE / SKIP / diff + запит).
2. Переконайся, що `ci.sh` має LF, `ci.bat` — CRLF.
3. Запусти `ci.sh` (або `ci.bat` на Windows) і дочекайся `CI: SUCCESS`.
4. Переконайся, що `build/bin/hello[.exe]` існує і `build/` не відстежується Git.

## Перевірки

- `cmake -S . -B build` без помилок; ключі в `CMakeLists.txt` не дублюються;
- `ctest` показує тест `HelloTest.BasicAddition` як `Passed`;
- `build/bin/hello[.exe]` друкує `Hello, World!`;
- у скриптах немає `|| true`.

## Приклад

Вхід: `project_name=hello`. Очікувано: `ci.bat` → `100% tests passed, 0 tests failed out of 3`, `CI: SUCCESS`.

## Типовий сценарій помилки

| Симптом | Причина | Дія |
|---|---|---|
| `hello.exe` лежить у `build/bin/Release/` | не задано `CMAKE_RUNTIME_OUTPUT_DIRECTORY_<CONFIG>` для multi-config генератора | виправити шаблон CMake у цьому skill |
| `ctest: No tests were found` | відсутній `enable_testing()` перед `gtest_discover_tests` | виправити шаблон |
| `LNK2038: mismatch detected for 'RuntimeLibrary'` (MSVC) | не задано `gtest_force_shared_crt` | додати `set(gtest_force_shared_crt ON ...)` |
| `ci.bat` нестабільно виконує `goto :fail` | файл збережено з LF | конвертувати у CRLF, покластися на `.gitattributes` |
| `cmake: command not found` | CMake не встановлено / не в PATH | зупинитись і повідомити, чого бракує |
| конфігурація «зависає» на `FetchContent` | `github.com/.../archive/...` недоступний у мережі, редірект на `codeload` не відбувається | у шаблоні використовувати пряме посилання `https://codeload.github.com/google/googletest/zip/refs/tags/<tag>` |
| `CMake Warning (dev) ... CMP0135` | не задано `DOWNLOAD_EXTRACT_TIMESTAMP` | додати `DOWNLOAD_EXTRACT_TIMESTAMP TRUE` у `FetchContent_Declare` |
