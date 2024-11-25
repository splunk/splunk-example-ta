#!/bin/bash
set -e
# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_DIR="$SCRIPT_DIR/../ui"

cd "$SCRIPT_DIR"/..
echo "🛑 Stopping any running Docker containers"
docker compose down
echo "🐍 Setting up a Python environment and deps"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

echo "🏗 Building the project with ucc-gen"
ucc-gen build

echo "📦 Installing npm dependencies"
npm --prefix "$UI_DIR" install
echo "🔧 Building UI assets"
npm --prefix "$UI_DIR" run build

# running on ARM macOS
export DOCKER_DEFAULT_PLATFORM=linux/amd64
echo "🐳 Starting Docker containers"
docker compose up -d --build --wait

echo "🚀 Done! It is now running at http://localhost:8000"