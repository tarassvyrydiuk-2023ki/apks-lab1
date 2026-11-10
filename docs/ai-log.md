# Журнал взаємодії з AI (Claude Code)

Студент: Свиридюк Тарас Русланович, КІ-408, варіант 1 (C++, CMake, GoogleTest / CTest).
Інструмент: Claude Code (CLI). Усі файли агента та проєкту створені AI-інструментом за запитом студента; результат переглянуто й перевірено командою `/check` та ручними запусками.

## Хронологія

| № | Запит | Результат |
|---|---|---|
| 1 | Прочитати методичку (`task1.pdf`) і приклад звіту; виконати лабораторну для варіанта 1 | визначено: C++, CMake, GoogleTest/CTest; формат агента Claude Code (`.claude/`) |
| 2 | Створити агента (гілка `develop`) | 3 коміти: manifest + CLAUDE.md + architecture, 3 skills, 6 commands + `check.py`; `check.py --only agent` → `RESULT: PASS (67)` |
| 3 | `/init` → `/git-init`, `/create-project` | `.gitignore`, `.gitattributes`, `include/hello/hello.hpp`, `src/hello.cpp`, `src/main.cpp` |
| 4 | `/init` → `/create-build` | `CMakeLists.txt`, `tests/test_hello.cpp`, `ci.sh`, `ci.bat`, `run.sh`, `run.bat`; перший запуск `ci.bat` завис на конфігурації (помилка 1) |
| 5 | виправлення skill `build-and-test` (URL GoogleTest, `BUILD_GMOCK`) і повторний `ci.bat` | `100% tests passed, 0 tests failed out of 3`, `CI: SUCCESS` |
| 6 | `/init` → `/create-actions`, крок 4a, `/check` | див. розділ «Результат /check» нижче |

## Помилки та рішення

### Помилка 1 — зависання `FetchContent` при завантаженні GoogleTest

- **Симптом:** `ci.bat` зупинився після попередження `CMP0135` на конфігурації; `build/_deps/googletest-src` порожній. `curl https://github.com/...` — `Connection timed out`, тоді як `api.github.com` і `codeload.github.com` відповідають.
- **Причина:** шаблон у skill `build-and-test` використовував `https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip`, а `github.com` у цій мережі недоступний.
- **Рішення (через інструкції, а не ручну правку результату):** у skill `build-and-test` URL замінено на `https://codeload.github.com/google/googletest/zip/refs/tags/v1.14.0`, додано `DOWNLOAD_EXTRACT_TIMESTAMP TRUE` (прибирає попередження CMP0135) і рядки в таблицю типових помилок; `CMakeLists.txt` оновлено за виправленим шаблоном. Виправлення skill перенесено в `develop`.

### Рішення — вимкнено збірку GoogleMock

`BUILD_GMOCK OFF` у шаблоні skill і в `CMakeLists.txt`: GoogleMock не використовується, збірка швидша.

### Помилка 2 — запуск `.bat` з поточного каталогу

- **Симптом:** `cmd /c ci.bat` → `'ci.bat' is not recognized as an internal or external command`.
- **Причина:** у середовищі вимкнено пошук виконуваних файлів у поточному каталозі.
- **Рішення:** `check.py` (скрипт агента) тепер запускає `cmd /c .\ci.bat` з явним відносним шляхом; для ручного запуску з PowerShell — `.\ci.bat`. Виправлення перенесено в `develop`.

## Результат /check

Локально (Windows 11, Visual Studio 2022, CMake 3.31, MSVC 19.44): `python .claude/scripts/check.py` → `RESULT: PASS (99 checks)`; перевірка не змінює відстежувані файли.

Навмисно зламана функція (`return a + b + 1`): `ctest` → `HelloTest.BasicAddition ***Failed` (`Which is: 6`), `ci.bat` → `CI: FAILED`, код виходу 1, `/check` → `[FAIL] build: ci script succeeded`, `RESULT: FAIL (2 of 99 checks failed)`. Після відновлення функції — знову `RESULT: PASS`.

Запуск у GitHub Actions виконується лише після `git push` на прохання користувача; результати Actions додаються до звіту окремо.

## 2026-11-10 — відтворення результату запуском `/init` з гілки `develop`

Щоб підтвердити, що агент із `develop` відтворює результат, у Claude Code на новій гілці `feature/video-demo` (створена з `develop`) виконано `/init`. Оркестратор пройшов усі кроки й завершився `INIT OK: git-init ✓ create-project ✓ create-build ✓ create-actions ✓ check ✓ (RESULT: PASS)`. Під час прогону знайдено ще дві помилки в інструкціях агента; їх виправлено в `develop` (коміт `db736fb`):

### Помилка 3 — `/create-project` перевіряв увесь проєкт

- **Симптом:** після кроку 2 `check.py --only structure` → `FAIL` (бракує `CMakeLists.txt`, `ci.*`, `docs/*`), хоча крок виконано правильно.
- **Причина:** група `structure` перевіряє файли всього проєкту, які створюються лише на кроках 3–4a.
- **Рішення:** у `check.py` додано окрему групу `scaffold` (лише файли кроків 1–2, у повний `/check` не входить); `create-project.md` і skill `project-scaffold` використовують `--only scaffold`.

### Помилка 4 — `UnicodeEncodeError` у `check.py`

- **Симптом:** при перенаправленні виводу у файл на Windows `check.py` падав з `UnicodeEncodeError` (кодування `cp1252` не підтримує кирилицю).
- **Рішення:** `check.py` на старті перемикає `stdout`/`stderr` на UTF-8; `PYTHONIOENCODING` більше не потрібен (`check.md` оновлено).

Повторний `/init` після виправлень: кроки 1–4 — `SKIP` (файли відповідають шаблонам, ідемпотентність), `/check` → `RESULT: PASS (99 checks)`.

Перевірка гілки `feature/lab1-cpp-hello` після злиття `develop`: чиста збірка `ci.bat` → 3/3 тести, `CI: SUCCESS`; `check.py` → `RESULT: PASS (99 checks)`; `check.py --only scaffold` → `RESULT: PASS (7 checks)`.

### GitHub Actions — черга macOS-раннерів

Для `pull_request`-запусків PR #1 job `macos-latest` кілька разів скасовувався з анотацією `The job was not acquired by Runner of type hosted even after multiple attempts` (брак вільних macOS-раннерів GitHub); один запуск завершився `Internal server error` без старту job. Це проблеми інфраструктури GitHub, а не коду: на тому ж коміті push-запуск пройшов на всіх трьох ОС. Рішення — перезапуск job без змін у workflow.

## 2026-11-10 — перестворення репозиторію з чистою історією

Після серії злиттів `develop` → `feature` і примусових оновлень гілок (через що на GitHub залишались застарілі кешовані дані) репозиторій перестворено з тим самим вмістом і лінійною історією: `develop` — коміти агента (створення + виправлення 1–4 + правило `linguist-vendored` для `.claude/`), `feature/lab1-cpp-hello` — `develop` + 4 коміти кроків `/init` (scaffold, build, ci, docs). Вміст файлів не змінювався (порівняння дерев — 0 відмінностей); локально `ci.bat` → `CI: SUCCESS`, `check.py` → `RESULT: PASS (99 checks)`. Pull request `lab1/finish` і запуски GitHub Actions створено заново.
