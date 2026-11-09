#!/usr/bin/env python3
"""Deterministic checker behind the /check command (lab 1, variant 1: C++/CMake/GoogleTest).

Groups: agent, structure, build, workflow, git.
Usage: python .claude/scripts/check.py [--only GROUP] [--no-build]
Prints "[FAIL] <group>: <check>" lines and a final "RESULT: PASS|FAIL".
It never modifies tracked files (the build step only recreates the ignored build/ dir).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IS_WIN = os.name == "nt"
GROUPS = ["agent", "structure", "build", "workflow", "git"]

total = 0
failed = 0


def check(group: str, name: str, ok: bool, details: str = "") -> bool:
    global total, failed
    total += 1
    if ok:
        print(f"[ OK ] {group}: {name}")
    else:
        failed += 1
        print(f"[FAIL] {group}: {name}" + (f" — {details}" if details else ""))
    return ok


def read(rel: str) -> str:
    p = ROOT / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def run(cmd: list[str], env: dict | None = None, timeout: int = 900) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=timeout)


# --------------------------------------------------------------------------- agent
def check_agent() -> None:
    g = "agent"
    manifest = read(".claude/agents/build-engineer.md")
    check(g, "manifest exists", bool(manifest))
    for section in ["Роль", "Область відповідальності", "Правила роботи з файлами",
                    "Заборонені дії", "Критерії успішного завершення"]:
        check(g, f"manifest has section '{section}'", f"## {section}" in manifest)
    check(g, "manifest forbids force-push / reset --hard", "git push --force" in manifest and "git reset --hard" in manifest)

    skills = ["project-scaffold", "build-and-test", "github-actions"]
    for s in skills:
        text = read(f".claude/skills/{s}/SKILL.md")
        check(g, f"skill {s} exists", bool(text))
        for sec in ["Коли застосовувати", "Вхідні дані", "Порядок дій", "Перевірки", "Приклад",
                    "Типовий сценарій помилки"]:
            check(g, f"skill {s} has '{sec}'", f"## {sec}" in text)

    commands = ["git-init", "create-project", "create-build", "create-actions", "check", "init"]
    for c in commands:
        text = read(f".claude/commands/{c}.md")
        check(g, f"command /{c} exists", bool(text))
        for sec in ["Передумови" if c != "init" else "Передумови", "Дії" if c != "init" else "Кроки",
                    "Очікувані файли", "Перевірка", "Повідомлення про помилку"]:
            if c == "init" and sec == "Дії":
                continue
            check(g, f"command /{c} has '{sec}'", f"## {sec}" in text or f"## {sec} " in text
                  or re.search(rf"^## {re.escape(sec)}", text, re.M) is not None)

    init = read(".claude/commands/init.md")
    order = [init.find(f"/{c}`") for c in ["git-init", "create-project", "create-build", "create-actions", "check"]]
    check(g, "init calls commands in the right order", all(o >= 0 for o in order) and order == sorted(order))
    check(g, "init stops on first error (INIT FAILED)", "INIT FAILED at step" in init)
    check(g, "init has step 4a (docs before /check)", "Крок 4a" in init)


# --------------------------------------------------------------------------- structure
def check_structure() -> None:
    g = "structure"
    required = [
        "CMakeLists.txt", "src/main.cpp", "src/hello.cpp", "include/hello/hello.hpp",
        "tests/test_hello.cpp", "ci.sh", "ci.bat", "run.sh", "run.bat",
        ".github/workflows/ci.yml", ".gitignore", ".gitattributes", "README.md", "CLAUDE.md",
        "docs/usage.md", "docs/architecture.md", "docs/ai-log.md",
    ]
    missing = [f for f in required if not (ROOT / f).is_file()]
    check(g, "required project files", not missing, f"missing {missing}")
    check(g, "tests contain BasicAddition", "BasicAddition" in read("tests/test_hello.cpp"))
    check(g, "main.cpp has main()", "int main" in read("src/main.cpp"))
    check(g, "CMake uses GoogleTest + enable_testing",
          "GTest::gtest_main" in read("CMakeLists.txt") and "enable_testing()" in read("CMakeLists.txt"))
    check(g, "CMake defines target 'hello'", "add_executable(hello" in read("CMakeLists.txt"))
    check(g, "ci.sh uses set -euo pipefail", "set -euo pipefail" in read("ci.sh"))
    check(g, "ci.bat uses goto :fail", "goto :fail" in read("ci.bat"))
    for f in ["ci.sh", "ci.bat", ".github/workflows/ci.yml"]:
        check(g, f"{f} has no error hiding", "|| true" not in read(f) and "continue-on-error" not in read(f))
    ci_sh = (ROOT / "ci.sh").read_bytes() if (ROOT / "ci.sh").is_file() else b""
    ci_bat = (ROOT / "ci.bat").read_bytes() if (ROOT / "ci.bat").is_file() else b""
    check(g, "ci.sh uses LF", bool(ci_sh) and b"\r\n" not in ci_sh)
    check(g, "ci.bat uses CRLF", bool(ci_bat) and b"\r\n" in ci_bat and b"\n" not in ci_bat.replace(b"\r\n", b""))


# --------------------------------------------------------------------------- build
def find_cmake_dir() -> str | None:
    if shutil.which("cmake"):
        return None
    candidates = []
    for pf in [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")]:
        if not pf:
            continue
        for edition in ["Community", "Professional", "Enterprise", "BuildTools"]:
            for year in ["2022", "2019"]:
                candidates.append(Path(pf) / "Microsoft Visual Studio" / year / edition /
                                  "Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin")
    for c in candidates:
        if (c / "cmake.exe").is_file():
            return str(c)
    return None


def check_build() -> None:
    g = "build"
    env = os.environ.copy()
    extra = find_cmake_dir()
    if extra:
        env["PATH"] = extra + os.pathsep + env["PATH"]
    check(g, "cmake available", shutil.which("cmake", path=env["PATH"]) is not None, "cmake not found in PATH")
    # Explicit relative path: cmd may not search the current directory (NoDefaultCurrentDirectoryInExePath).
    script = ["cmd", "/c", ".\\ci.bat"] if IS_WIN else ["bash", "./ci.sh"]
    if not (ROOT / script[-1].lstrip(".\\/")).is_file():
        check(g, "ci script exists", False, f"{script[-1]} missing")
        return
    r = run(script, env=env)
    tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-8:])
    check(g, "ci script succeeded", r.returncode == 0, f"exit code {r.returncode}\n{tail}")
    exe = ROOT / "build" / "bin" / ("hello.exe" if IS_WIN else "hello")
    check(g, "executable build/bin/hello exists", exe.is_file())
    if exe.is_file():
        out = run([str(exe)]).stdout.strip()
        check(g, "hello prints 'Hello, World!'", out == "Hello, World!", repr(out))
    check(g, "junit.xml produced", (ROOT / "build" / "test-results" / "junit.xml").is_file())
    junit = read("build/test-results/junit.xml")
    check(g, "BasicAddition passed", "BasicAddition" in junit and "<failure" not in junit)


# --------------------------------------------------------------------------- workflow
def check_workflow() -> None:
    g = "workflow"
    text = read(".github/workflows/ci.yml")
    check(g, "ci.yml exists", bool(text))
    data = None
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        check(g, "ci.yml is valid YAML", isinstance(data, dict))
    except ImportError:
        check(g, "ci.yml is valid YAML (pyyaml absent, structural check only)",
              "\njobs:" in text and "\non:" in text)
    check(g, "triggers push", re.search(r"^\s{2}push:", text, re.M) is not None)
    check(g, "triggers pull_request", re.search(r"^\s{2}pull_request:", text, re.M) is not None)
    check(g, "single job with matrix of 3 OS",
          all(os_ in text for os_ in ["ubuntu-latest", "windows-latest", "macos-latest"]) and "matrix:" in text
          and len(re.findall(r"^  [\w-]+:\s*$", text.split("jobs:", 1)[-1], re.M)) == 1)
    check(g, "calls ci.sh and ci.bat", "./ci.sh" in text and "ci.bat" in text)
    check(g, "no direct cmake/compiler calls in run:", not re.search(r"run:.*\b(cmake|g\+\+|clang|cl\.exe)\b", text))
    check(g, "no secrets / continue-on-error", "secrets." not in text and "continue-on-error" not in text)
    check(g, "uploads artifacts", text.count("actions/upload-artifact") >= 2)


# --------------------------------------------------------------------------- git
def check_git() -> None:
    g = "git"
    gi = [l.strip() for l in read(".gitignore").splitlines() if l.strip() and not l.startswith("#")]
    check(g, ".gitignore has build/", "build/" in gi)
    check(g, ".gitignore has no duplicate lines", len(gi) == len(set(gi)))
    check(g, ".gitattributes has eol rules", "*.sh text eol=lf" in read(".gitattributes")
          and "*.bat text eol=crlf" in read(".gitattributes"))
    if shutil.which("git") and (ROOT / ".git").exists():
        tracked = run(["git", "ls-files"]).stdout.splitlines()
        bad = [f for f in tracked if re.match(r"^(build|out|_deps|CMakeFiles|Testing)/", f) or f.endswith("CMakeCache.txt")]
        check(g, "no build artifacts tracked by git", not bad, str(bad[:5]))
        secret_re = re.compile(r"(ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
                               r"-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16})")
        leaks = [f for f in tracked if (ROOT / f).is_file() and f != ".claude/scripts/check.py"
                 and secret_re.search((ROOT / f).read_text(encoding="utf-8", errors="ignore"))]
        check(g, "no secrets in tracked files", not leaks, str(leaks))
    else:
        check(g, "git repository present", False, "no .git or git missing")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=GROUPS)
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args()
    funcs = {"agent": check_agent, "structure": check_structure, "build": check_build,
             "workflow": check_workflow, "git": check_git}
    for grp in GROUPS:
        if args.only and grp != args.only:
            continue
        if grp == "build" and args.no_build and not args.only:
            continue
        funcs[grp]()
    if failed:
        print(f"RESULT: FAIL ({failed} of {total} checks failed)")
        return 1
    print(f"RESULT: PASS ({total} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
