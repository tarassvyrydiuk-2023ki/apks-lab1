---
description: Оркестратор — git-init → create-project → create-build → create-actions → check
---

# /init (orchestrator)

Послідовно виконує commands, передаючи результат кожного кроку наступному. Зупиняється на першій помилці.

## Передумови (перевіряються до кроку 1)

- `git` доступний, каталог — репозиторій;
- Python >= 3.8, `cmake >= 3.20`, C++17-компілятор;
- поточна гілка — `feature/...` (не `master`/`main`/`develop`); інакше зупинись і запитай користувача;
- рекомендовано чисте робоче дерево (окрім `.claude/`).

## Кроки

| № | Command | Використовує | Очікуваний результат |
|---|---|---|---|
| 1 | `/git-init` | skill `project-scaffold` | `.gitignore`, `.gitattributes`, `git status` |
| 2 | `/create-project` | skill `project-scaffold` | `src/`, `include/`; `Hello, World!` |
| 3 | `/create-build` | skill `build-and-test` | `CMakeLists.txt`, тести, `ci.*`, `run.*`, `build/bin/hello` |
| 4 | `/create-actions` | skill `github-actions` | `.github/workflows/ci.yml` |
| 5 | `/check` | усе вище | `RESULT: PASS` / `FAIL` |

Крок 4a (виконується **до** `/check`, бо `/check` вимагає `docs/usage.md`):

- створи `docs/usage.md`, якщо його немає: точні команди запуску агента (`/init`, `/check`, окремі commands), локальної збірки (`ci.sh`/`ci.bat`), запуску застосунку (`run.*`, `build/bin/hello`);
- допиши `docs/ai-log.md`: запуск оркестратора, результат кожного кроку, помилки та рішення.

Після кроків 2–4a (якщо команда створила або змінила файли) запропонуй окремий змістовний коміт:

- крок 1+2: `feat: scaffold C++ Hello World project`
- крок 3: `build: add CMake build, GoogleTest tests and ci scripts`
- крок 4: `ci: add GitHub Actions matrix for Windows, Linux and macOS`
- крок 4a: `docs: add usage guide and AI interaction log`

Коміти виконуй лише локально; `git push` і створення PR — тільки на прохання користувача. Наприкінці виведи підсумковий звіт і допиши в `docs/ai-log.md` результат `/check`.

## Обробка помилок

- Якщо крок завершився помилкою — **зупинись**. Не виконуй наступні кроки, не позначай роботу успішною.
- Виведи: номер і назву кроку, повідомлення про помилку команди, останні рядки логу, яку command/skill треба виправити.
- Не приховуй помилку (`|| true`, пропуск тестів, ручна правка згенерованого результату).
- Після виправлення інструкцій можна перезапустити `/init`: усі кроки ідемпотентні й пропускають вже готові файли.

## Очікувані файли

Усі файли з команд 1–4, а також `docs/usage.md` і `docs/ai-log.md`.

## Перевірка

Крок 5 (`/check`) повертає `RESULT: PASS`. Без цього `/init` вважається невдалим.

## Повідомлення про помилку

```
INIT FAILED at step <N>/5 (<command>): <message>
Fix: <skill/command to update>, then re-run /init
```

Успіх:

```
INIT OK: git-init ✓ create-project ✓ create-build ✓ create-actions ✓ check ✓ (RESULT: PASS)
```
