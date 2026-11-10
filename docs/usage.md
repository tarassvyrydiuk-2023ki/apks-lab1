# Інструкція запуску

## Вимоги

- Git, Python ≥ 3.8 (для `check.py`);
- CMake ≥ 3.20 і C++17-компілятор (Windows — Visual Studio 2022 / Build Tools, Linux — g++/clang, macOS — Apple clang);
- доступ до мережі (GoogleTest завантажується через `FetchContent` з `codeload.github.com`);
- Claude Code (CLI) для запуску агента.

## Запуск агента

1. Склонуйте репозиторій і перейдіть на гілку `develop` (там лише агент) — створіть нову гілку `feature/...`:

   ```
   git checkout develop
   git checkout -b feature/lab1-cpp-hello
   ```

2. Запустіть Claude Code у корені репозиторію (`claude`) і виконайте:

   ```
   /init
   ```

   Оркестратор виконає `/git-init → /create-project → /create-build → /create-actions`, створить документацію і запустить `/check`. Успіх: `INIT OK: ... (RESULT: PASS)`.

3. Окремі команди: `/git-init`, `/create-project`, `/create-build`, `/create-actions`, `/check`.

4. Лише перевірка (без Claude Code): 

   ```
   python .claude/scripts/check.py            # усі 5 груп
   python .claude/scripts/check.py --only workflow
   python .claude/scripts/check.py --no-build
   ```

## Локальна збірка і тести

| ОС | Команда |
|---|---|
| Windows | `ci.bat` |
| Linux / macOS | `./ci.sh` |

Скрипт: налаштовує CMake → збирає (Release) → запускає `ctest` (звіт `build/test-results/junit.xml`) → перевіряє, що `build/bin/hello[.exe]` друкує `Hello, World!`. Успіх: `CI: SUCCESS`, помилка: `CI: FAILED` і код виходу 1.

Лише тести: `ctest --test-dir build -C Release --output-on-failure`.
Один тест: `ctest --test-dir build -C Release -R BasicAddition -V`.

## Запуск зібраного застосунку

| ОС | Команда |
|---|---|
| Windows | `run.bat` або `build\bin\hello.exe` |
| Linux / macOS | `./run.sh` або `build/bin/hello` |

Очікуваний вивід: `Hello, World!`.

## GitHub Actions

Workflow `.github/workflows/ci.yml` запускається на `push` (`develop`, `master`, `main`, `feature/**`) і `pull_request` до `develop` / `master` / `main`. Одна job із матрицею `ubuntu-latest`, `windows-latest`, `macos-latest` викликає `ci.sh` / `ci.bat` та завантажує артефакти `hello-<os>` і `test-results-<os>`.

## Типові проблеми

| Проблема | Рішення |
|---|---|
| `cmake` не знайдено | встановіть CMake або запустіть з «Developer Command Prompt» / додайте CMake з Visual Studio до `PATH` |
| конфігурація зависає на завантаженні GoogleTest | перевірте мережу до `codeload.github.com` |
| `./ci.sh: Permission denied` | `chmod +x ci.sh run.sh` |
| `build/` у `git status` | перевірте `.gitignore` (`/git-init` додає `build/`) |
