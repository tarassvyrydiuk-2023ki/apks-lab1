---
description: Перевірити Git-репозиторій, створити/доповнити .gitignore і .gitattributes, показати git status
---

# /git-init

Використовує skill `project-scaffold` (розділ про `.gitignore` та `.gitattributes`).

## Передумови

- `git` встановлений (`git --version`);
- поточний каталог — корінь репозиторію (`git rev-parse --show-toplevel`);
- поточна гілка не `master`/`main` (робота ведеться у `feature/...`); якщо це `master`/`main` — зупинись і запитай користувача.

## Дії

1. Виведи `git branch --show-current`, `git remote -v`.
2. Створи або доповни `.gitignore` рядками зі skill (`build/`, `out/`, `_deps/`, `CMakeFiles/`, `CMakeCache.txt`, `Testing/`, `.vs/`, `.idea/`). Додавай лише ті рядки, яких ще немає.
3. Створи `.gitattributes` (`*.sh text eol=lf`, `*.bat text eol=crlf`, `.claude/** linguist-vendored`), якщо його немає; якщо є — додай лише відсутні рядки.
4. Виведи `git status --short`.

## Очікувані файли

`.gitignore`, `.gitattributes`.

## Перевірка

`python .claude/scripts/check.py --only git` → `RESULT: PASS` (немає дублікатів у `.gitignore`, `build/` ігнорується).

## Повідомлення про помилку

```
GIT-INIT FAILED: <причина>. Fix: <що зробити>
```

## Ідемпотентність

Повторний запуск не додає рядків, що вже є, і не змінює `.gitattributes`, якщо він відповідає вимогам (`SKIP`).
