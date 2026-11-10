---
description: Створити початковий C++ Hello World проєкт за skill project-scaffold
---

# /create-project

Застосовує skill `project-scaffold`. Параметри: `language=cpp`, `project_name=hello`.

## Передумови

- виконано `/git-init` (існує `.gitignore`);
- репозиторій чистий або зміни стосуються лише файлів агента.

## Дії

1. Прочитай `.claude/skills/project-scaffold/SKILL.md`.
2. Створи `include/hello/hello.hpp`, `src/hello.cpp`, `src/main.cpp` за шаблонами (CREATE / SKIP / diff + запит).
3. Створи або онови розділ «Запуск проєкту» в `README.md` (ПІБ, група, варіант, опис, запуск агента).

## Очікувані файли

`include/hello/hello.hpp`, `src/hello.cpp`, `src/main.cpp`, `README.md`.

## Перевірка

Окремої збірки ще немає, тому перевіряються лише файли цього кроку: `python .claude/scripts/check.py --only scaffold` → `RESULT: PASS`.
Не використовуй тут `--only structure`: ця група перевіряє весь проєкт (`CMakeLists.txt`, `ci.*`, `ci.yml`, `docs/*`) і на кроці 2 закономірно дає `FAIL`.
Повна перевірка виконується в `/check` (крок 5).

## Повідомлення про помилку

```
CREATE-PROJECT FAILED: <файл> — <причина>. Fix: <skill/command>
```

## Ідемпотентність

Існуючі файли з правильним вмістом пропускаються (`SKIP <file>`); відмінні — не перезаписуються.
