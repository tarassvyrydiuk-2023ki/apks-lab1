@echo off
rem Runs the built executable (build it first with ci.bat).
setlocal
cd /d "%~dp0"
if not exist "build\bin\hello.exe" (
    echo build\bin\hello.exe not found. Run ci.bat first. 1>&2
    exit /b 1
)
"build\bin\hello.exe" %*
exit /b %ERRORLEVEL%
