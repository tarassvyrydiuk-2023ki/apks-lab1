@echo off
rem Build & test pipeline for Windows: configure -> build -> ctest -> smoke test.
setlocal EnableExtensions
cd /d "%~dp0"

echo ==^> [1/4] CMake version
cmake --version || goto :fail

echo ==^> [2/4] Configuring and building (Release)
cmake -S . -B build || goto :fail
cmake --build build --config Release --parallel || goto :fail

echo ==^> [3/4] Running unit tests (ctest)
if not exist "build\test-results" mkdir "build\test-results"
ctest --test-dir build -C Release --output-on-failure --output-junit test-results\junit.xml || goto :fail

echo ==^> [4/4] Smoke test of build\bin\hello.exe
if not exist "build\bin\hello.exe" goto :fail
set "OUTPUT="
for /f "delims=" %%L in ('"build\bin\hello.exe"') do set "OUTPUT=%%L"
echo %OUTPUT%
if not "%OUTPUT%"=="Hello, World!" (
    echo ERROR: unexpected output from build\bin\hello.exe 1>&2
    goto :fail
)
echo CI: SUCCESS
exit /b 0

:fail
echo CI: FAILED 1>&2
exit /b 1
