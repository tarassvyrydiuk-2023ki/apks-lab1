# Лабораторна робота №1 — Проєктування AI-агента для автоматизації розробки та CI/CD

| | |
|---|---|
| Студент | Свиридюк Тарас Русланович |
| Група | КІ-408 |
| Варіант | 1 — C++, CMake, GoogleTest / CTest |
| AI-інструмент | Claude Code (CLI) |

## Опис

Репозиторій містить AI-агента `build-engineer` (manifest, 3 skills, 5 commands, оркестратор `/init`, скрипт перевірки `check.py`), який створює, збирає та тестує мінімальний кросплатформний C++ проєкт **Hello World** і підключає GitHub Actions для Windows, Linux та macOS.

- Гілка `develop` — агент з інструкціями (`.claude/`, `CLAUDE.md`, `docs/architecture.md`).
- Гілка `feature/lab1-cpp-hello` — проєкт, згенерований агентом (код, тести, CMake, CI, документація).

Архітектура: [docs/architecture.md](docs/architecture.md). Інструкція запуску: [docs/usage.md](docs/usage.md). Журнал AI: [docs/ai-log.md](docs/ai-log.md).

## Запуск проєкту

Запуск агента (Claude Code у корені репозиторію, гілка `feature/...`):

```
/init      # git-init → create-project → create-build → create-actions → check
/check     # лише перевірка
```

Локальна збірка і тести (потрібні CMake ≥ 3.20 та C++17-компілятор):

```
ci.bat     # Windows
./ci.sh    # Linux / macOS
```

Запуск застосунку: `run.bat` / `./run.sh` (або `build/bin/hello[.exe]`) → `Hello, World!`.
