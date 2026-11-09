---
name: github-actions
description: Create .github/workflows/ci.yml with one job and a matrix of ubuntu/windows/macos that only calls ci.sh / ci.bat and uploads the executable and test results as artifacts. Use when /create-actions is invoked.
---

# Skill: github-actions

## Коли застосовувати

- немає `.github/workflows/ci.yml`, а `ci.sh` і `ci.bat` вже існують;
- викликано `/create-actions` або крок 4 `/init`.

## Вхідні дані

| Параметр | За замовчуванням |
|---|---|
| `branches` | `develop`, `master`, `main`, `feature/**` (push); `develop`, `master`, `main` (pull_request) |
| `ci_os` | `ubuntu-latest`, `windows-latest`, `macos-latest` |

## Результат

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [develop, master, main, "feature/**"]
  pull_request:
    branches: [develop, master, main]

jobs:
  build-and-test:
    name: build-and-test (${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build and test (Linux/macOS)
        if: runner.os != 'Windows'
        shell: bash
        run: ./ci.sh

      - name: Build and test (Windows)
        if: runner.os == 'Windows'
        shell: cmd
        run: ci.bat

      - name: Upload executable
        uses: actions/upload-artifact@v4
        with:
          name: hello-${{ matrix.os }}
          path: build/bin/
          if-no-files-found: error

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.os }}
          path: build/test-results/
          if-no-files-found: error
```

## Правила

- уся логіка складання — у `ci.sh` / `ci.bat`; workflow містить лише checkout, виклик скрипта і завантаження артефактів;
- CMake та компілятори вже встановлені на hosted-runner'ах, окремий крок налаштування не потрібен;
- без секретів, без `continue-on-error`, без `|| true`;
- `if: always()` лише для завантаження результатів тестів (щоб бачити їх навіть при падінні), помилка job при цьому не приховується;
- артефакт `build/bin/` обов'язковий (`if-no-files-found: error`).

## Порядок дій

1. Перевір, що `ci.sh` і `ci.bat` існують.
2. Створи `ci.yml` (CREATE / SKIP / diff + запит).
3. Перевір YAML: `python .claude/scripts/check.py --only workflow`.

## Перевірки

- файл парситься як YAML;
- є тригери `push` і `pull_request`;
- матриця містить три ОС;
- є виклик `ci.sh` і `ci.bat`, немає `cmake`/`g++` у `run:` безпосередньо;
- немає `continue-on-error` та `secrets.`.

## Приклад

Вхід: стандартні параметри. Очікувано: 3 job (`ubuntu-latest`, `windows-latest`, `macos-latest`), по 2 артефакти на кожну.

## Типовий сценарій помилки

| Симптом | Причина | Дія |
|---|---|---|
| `./ci.sh: Permission denied` | у git не виставлено біт виконання | `git update-index --chmod=+x ci.sh`, оновити команду `/create-build` |
| Windows-job не бачить `ci.bat` | використано `bash` замість `cmd` | `shell: cmd` для Windows-кроку |
| `Unexpected value 'branches'` | помилка відступів у YAML | виправити шаблон у цьому skill, перевірити `check.py` |
| артефакт `build/bin/` порожній | скрипт збірки не створив `hello` | виправити `ci.*`, не вимикати `if-no-files-found` |
