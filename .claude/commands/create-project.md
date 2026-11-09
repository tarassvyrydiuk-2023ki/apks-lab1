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

Окремої збірки ще немає, тому перевірка структурна: `python .claude/scripts/check.py --only structure`.
Повна перевірка запуску виконується після `/create-build`.

## Повідомлення про помилку

```
CREATE-PROJECT FAILED: <файл> — <причина>. Fix: <skill/command>
```

## Ідемпотентність

Існуючі файли з правильним вмістом пропускаються (`SKIP <file>`); відмінні — не перезаписуються.
