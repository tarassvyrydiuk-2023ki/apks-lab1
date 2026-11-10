---
name: project-scaffold
description: Create the minimal C++ Hello World project layout (src/, include/, tests/, docs/), the README "Запуск проєкту" section and the initial .gitignore / .gitattributes. Use when the project has no source tree yet or when /create-project is invoked.
---

# Skill: project-scaffold

## Коли застосовувати

- у репозиторії немає `src/main.cpp`;
- викликано `/create-project` або крок 2 оркестратора `/init`.

## Вхідні дані

| Параметр | За замовчуванням | Примітка |
|---|---|---|
| `language` | `cpp` | лише C++17 (варіант 1) |
| `project_name` | `hello` | ім'я виконуваного файлу і CMake-проєкту |

## Результат (файли)

| Файл | Призначення |
|---|---|
| `include/hello/hello.hpp` | оголошення `hello::greeting()` і `hello::add(a, b)` |
| `src/hello.cpp` | реалізація бібліотеки `hello_core` |
| `src/main.cpp` | `int main()` → друкує `Hello, World!` |
| `.gitignore` | `build/`, `out/`, `_deps/`, `CMakeFiles/`, `CMakeCache.txt`, `Testing/`, `.vs/`, `.idea/` |
| `.gitattributes` | `*.sh text eol=lf`, `*.bat text eol=crlf`, `.claude/** linguist-vendored` (скрипти агента не враховуються в статистиці мов GitHub) |
| `README.md` (розділ «Запуск проєкту») | ПІБ, група, варіант, опис, спосіб запуску агента |

### Шаблон `include/hello/hello.hpp`

```cpp
#pragma once

#include <string>

namespace hello {

// Returns the greeting printed by the executable.
std::string greeting();

// Adds two numbers (used to demonstrate unit testing).
double add(double a, double b);

}  // namespace hello
```

### Шаблон `src/hello.cpp`

```cpp
#include "hello/hello.hpp"

namespace hello {

std::string greeting() { return "Hello, World!"; }

double add(double a, double b) { return a + b; }

}  // namespace hello
```

### Шаблон `src/main.cpp`

```cpp
#include <iostream>

#include "hello/hello.hpp"

int main() {
    std::cout << hello::greeting() << std::endl;
    return 0;
}
```

## Порядок дій

1. Перевір передумови: корінь репозиторію, `git` доступний.
2. Для кожного файлу: не існує → створи; існує й збігається → `SKIP <file>`; існує й відрізняється → покажи diff і запитай користувача.
3. Рядки `.gitignore` додавай лише якщо їх ще немає (без дублікатів).
4. Не створюй `CMakeLists.txt` — це робить skill `build-and-test`.

## Перевірки

- `src/main.cpp`, `src/hello.cpp`, `include/hello/hello.hpp` існують;
- у `src/main.cpp` є `int main`; у `hello.cpp` — `Hello, World!`;
- у `.gitignore` є `build/` і немає повторів;
- у `.gitattributes` є правила для `*.sh`, `*.bat` і `.claude/** linguist-vendored`;
- автоматично: `python .claude/scripts/check.py --only scaffold` → `RESULT: PASS`.

## Приклад

Вхід: `language=cpp project_name=hello`.
Очікувано: створено 3 файли коду, `.gitignore`, `.gitattributes`, у `README.md` — розділ «Запуск проєкту».

## Типовий сценарій помилки

| Симптом | Причина | Дія |
|---|---|---|
| `.gitignore` містить `build/` двічі | команду запустили повторно без перевірки | перед додаванням перевіряти наявність рядка |
| `src/main.cpp` вже існує з іншим вмістом | користувач змінив файл | не перезаписувати, показати diff, запитати |
| `include/hello/hello.hpp` не знайдено при збірці | помилка в `target_include_directories` | виправити skill `build-and-test`, а не копіювати файл вручну |
| `check.py --only structure` після кроку 2 → `FAIL` (бракує `CMakeLists.txt`, `ci.*`, `docs/*`) | група `structure` перевіряє весь проєкт, а не лише цей крок | для кроку 2 використовувати `check.py --only scaffold` |
