---
description: Лише перевірити агента, структуру, складання, тести, YAML workflow і Git (нічого не змінює у відстежуваних файлах)
---

# /check

Виконує детермінований скрипт `.claude/scripts/check.py`.

## Передумови

- Python >= 3.8 у PATH (лише стандартна бібліотека; `pyyaml` — за наявності).

## Дії

1. Виконай `python .claude/scripts/check.py` (опції: `--only agent|structure|build|workflow|git|scaffold`, `--no-build`). Група `scaffold` — лише для перевірки кроку `/create-project`, у повний запуск не входить. Скрипт сам перемикає вивід на UTF-8, тому додаткові змінні середовища (`PYTHONIOENCODING`) не потрібні.
2. Скрипт перевіряє 5 груп:
   - **agent** — manifest, 3 skills, 6 commands, порядок викликів у `init.md`, розділи у skills;
   - **structure** — файли проєкту, `docs/usage.md`, `docs/architecture.md`, `docs/ai-log.md`, `BasicAddition` у тестах;
   - **build** — запускає `ci.bat`/`ci.sh`, перевіряє `build/bin/hello[.exe]` і його вивід;
   - **workflow** — YAML, `push`/`pull_request`, матриця з трьома ОС, лише виклики `ci.*`;
   - **git** — `build/` не відстежується, немає секретів, немає дублікатів у `.gitignore`.
3. Виведи `RESULT: PASS (<N> checks)` або `RESULT: FAIL` зі списком `[FAIL] <група>: <перевірка>`.

## Очікувані файли

Нічого не створює у відстежуваних файлах (лише `build/`, що ігнорується Git).

## Перевірка

Після запуску `git status --short` не повинен показувати нових змін, зроблених `/check`.

## Повідомлення про помилку

```
[FAIL] <group>: <check> — <details>
RESULT: FAIL (<failed> of <total>)
```

## Ідемпотентність

Команда лише читає; може перестворювати каталог `build/`.
