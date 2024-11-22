#!/bin/bash
set -e

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_DIR="$SCRIPT_DIR/../ui"

cd "$SCRIPT_DIR"/..
docker compose down
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ucc-gen build
# running on ARM macOS
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose up -d --build --wait


npm --prefix "$UI_DIR" install
npm --prefix "$UI_DIR" run dev