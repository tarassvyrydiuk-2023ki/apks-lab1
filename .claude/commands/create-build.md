---
description: Створити CMake-складання, GoogleTest-тести та скрипти ci.*/run.* за skill build-and-test
---

# /create-build

Застосовує skill `build-and-test`.

## Передумови

- існують `src/main.cpp`, `src/hello.cpp`, `include/hello/hello.hpp` (результат `/create-project`);
- встановлено `cmake >= 3.20` і C++17-компілятор (на Windows — Visual Studio Build Tools); мережа для завантаження GoogleTest.

## Дії

1. Прочитай `.claude/skills/build-and-test/SKILL.md`.
2. Створи `CMakeLists.txt`, `tests/test_hello.cpp`, `ci.sh`, `ci.bat`, `run.sh`, `run.bat` (CREATE / SKIP / diff + запит).
3. Переконайся, що `*.sh` мають LF, `*.bat` — CRLF; для `ci.sh`/`run.sh` встанови біт виконання в git (`git update-index --chmod=+x`).
4. Запусти `ci.sh` (Linux/macOS) або `ci.bat` (Windows).

## Очікувані файли

`CMakeLists.txt`, `tests/test_hello.cpp`, `ci.sh`, `ci.bat`, `run.sh`, `run.bat`; після запуску — `build/bin/hello[.exe]`, `build/test-results/junit.xml`.

## Перевірка

- `ci.*` завершується `CI: SUCCESS`;
- `ctest` містить `HelloTest.BasicAddition` — Passed;
- `build/bin/hello[.exe]` друкує `Hello, World!`.

## Повідомлення про помилку

```
CREATE-BUILD FAILED: <етап ci.*> — <повідомлення>. Fix: skill build-and-test
```

## Ідемпотентність

Існуючі файли пропускаються; `build/` перестворюється скриптом без шкоди для відстежуваних файлів.
