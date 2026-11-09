---
description: Створити GitHub Actions workflow з матрицею Windows/Linux/macOS за skill github-actions
---

# /create-actions

Застосовує skill `github-actions`.

## Передумови

- існують `ci.sh` і `ci.bat` (результат `/create-build`).

## Дії

1. Прочитай `.claude/skills/github-actions/SKILL.md`.
2. Створи `.github/workflows/ci.yml` за шаблоном (CREATE / SKIP / diff + запит).
3. Не додавай секретів, `continue-on-error`, прямих викликів `cmake`/компілятора у `run:`.

## Очікувані файли

`.github/workflows/ci.yml`.

## Перевірка

`python .claude/scripts/check.py --only workflow` → `RESULT: PASS` (валідний YAML, `push` + `pull_request`, три ОС, виклики `ci.sh`/`ci.bat`).
Фактичний запуск у GitHub Actions — лише після `git push`, який виконує користувач.

## Повідомлення про помилку

```
CREATE-ACTIONS FAILED: <причина>. Fix: skill github-actions
```

## Ідемпотентність

Якщо `ci.yml` вже відповідає вимогам — `SKIP`; якщо відрізняється — diff і запит.
