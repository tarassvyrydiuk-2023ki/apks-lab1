# Архітектура AI-агента build-engineer

Лабораторна робота №1, варіант 1 — **C++, CMake, GoogleTest / CTest**. AI-інструмент: Claude Code (CLI).

## Які проблеми вирішує агент

| Проблема | Як вирішує агент |
|---|---|
| Неоднозначний запит «зроби проєкт» | точні шаблони кожного файлу у skills |
| Розбіжність локальної збірки та CI | вся логіка — у `ci.sh` / `ci.bat`, `ci.yml` лише викликає їх |
| Артефакти складання / секрети в Git | `/git-init` доповнює `.gitignore`, `/check` перевіряє `git ls-files` і шукає секрети |
| Різні каталоги виводу у multi-config генераторів (MSVC) | `CMAKE_RUNTIME_OUTPUT_DIRECTORY_<CONFIG>` у шаблоні CMake: завжди `build/bin/` |
| «Успіх» без перевірки | оркестратор успішний лише після `RESULT: PASS` скрипта `check.py` |
| Повторний запуск ламає файли | кожна команда ідемпотентна: CREATE / SKIP / diff + запит, без перезапису |
| Небезпечні дії AI | заборони в manifest: видалення, force-push, push без запиту, секрети, `\|\| true` |

## Відповідність структурі з методички (Copilot → Claude Code)

| Методичка (Copilot) | Реалізація (Claude Code) |
|---|---|
| `.github/agents/build-engineer.agent.md` | `.claude/agents/build-engineer.md` (subagent) + `CLAUDE.md` |
| `.github/skills/*/SKILL.md` | `.claude/skills/{project-scaffold,build-and-test,github-actions}/SKILL.md` |
| `.github/prompts/*.prompt.md` | `.claude/commands/*.md` (slash-команди) |
| `init.prompt.md`, `check.prompt.md` | `.claude/commands/init.md`, `check.md` + `.claude/scripts/check.py` |
| `.github/workflows/ci.yml` | `.github/workflows/ci.yml` (без змін) |
| `CMakeLists.txt` | `CMakeLists.txt` + `ci.sh` / `ci.bat` (варіант 1) |

## Skills

| Skill | Вхід | Результат |
|---|---|---|
| `project-scaffold` | `language`, `project_name` | `include/`, `src/`, `.gitignore`, `.gitattributes`, README-розділ |
| `build-and-test` | `project_name`, `cmake_min`, `gtest_version` | `CMakeLists.txt`, `tests/test_hello.cpp`, `ci.*`, `run.*` |
| `github-actions` | гілки, список ОС | `.github/workflows/ci.yml` |

## Commands, доступні користувачу

`/git-init`, `/create-project`, `/create-build`, `/create-actions`, `/check`, а також оркестратор `/init`.

## Дані, що передаються між етапами

| Від | До | Що передається |
|---|---|---|
| `/git-init` | `/create-project` | гілка `feature/...`, `.gitignore`, `.gitattributes` |
| `/create-project` | `/create-build` | `include/hello/hello.hpp`, `src/*.cpp` (API `greeting()`, `add()`) |
| `/create-build` | `/create-actions` | наявність `ci.sh` / `ci.bat` і шлях артефакту `build/bin/hello[.exe]`, `build/test-results/junit.xml` |
| `/create-actions` | крок 4a | `ci.yml` |
| крок 4a | `/check` | `docs/usage.md`, `docs/ai-log.md` |
| `/check` | користувач | `RESULT: PASS` / `FAIL` з переліком `[FAIL] <group>: <check>` |

## Схема взаємодії

```
 CLAUDE.md ─────────────► manifest (build-engineer)   правила, заборони, критерії
                                   │
 user ──► /init (orchestrator) ────┤
            │ 1 /git-init ─────────┼─► skill project-scaffold ─► .gitignore, .gitattributes
            │ 2 /create-project ───┼─► skill project-scaffold ─► include/, src/
            │ 3 /create-build ─────┼─► skill build-and-test ───► CMakeLists, tests, ci.*, run.*
            │ 4 /create-actions ───┼─► skill github-actions ───► .github/workflows/ci.yml
            │ 4a docs ─────────────┘                            docs/usage.md, docs/ai-log.md
            └ 5 /check ──────────────► .claude/scripts/check.py ─► RESULT: PASS | FAIL
```

## Як оркестратор обробляє помилки

1. Перевіряє передумови (git, cmake, C++-компілятор, Python, гілка `feature/...`).
2. Виконує кроки 1–4, крок 4a (документація) і крок 5 `/check`.
3. На першій помилці зупиняється з повідомленням `INIT FAILED at step N/5 (<command>)`; наступні кроки не виконуються, нічого не видаляється.
4. Виправлення вноситься в інструкції (skill або command), а не в згенерований результат; після цього `/init` можна перезапустити — усі кроки ідемпотентні.
5. Успіхом вважається лише `RESULT: PASS` від `check.py`.

## Безпека

- Заборонено: видалення файлів (крім `build/`), `git push --force`, `git reset --hard`, `git rebase`, автоматичний `push` і створення PR, робота із секретами, приховування помилок (`|| true`, `continue-on-error`).
- `check.py` не змінює відстежувані файли та перевіряє відсутність артефактів і секретів у Git.
