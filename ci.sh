#!/usr/bin/env bash
# Build & test pipeline for Linux/macOS: configure -> build -> ctest -> smoke test.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> [1/4] CMake version"
cmake --version

echo "==> [2/4] Configuring and building (Release)"
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --parallel

echo "==> [3/4] Running unit tests (ctest)"
mkdir -p build/test-results
ctest --test-dir build -C Release --output-on-failure --output-junit test-results/junit.xml

echo "==> [4/4] Smoke test of build/bin/hello"
test -x build/bin/hello
OUTPUT="$(build/bin/hello)"
echo "$OUTPUT"
if [ "$OUTPUT" != "Hello, World!" ]; then
    echo "ERROR: unexpected output from build/bin/hello" >&2
    exit 1
fi
echo "CI: SUCCESS"
