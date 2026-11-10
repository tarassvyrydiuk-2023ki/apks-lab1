#!/usr/bin/env bash
# Runs the built executable (build it first with ./ci.sh).
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x build/bin/hello ]; then
    echo "build/bin/hello not found. Run ./ci.sh first." >&2
    exit 1
fi
exec build/bin/hello "$@"
