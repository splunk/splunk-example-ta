cd ../
docker compose down
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ucc-gen build
# running on ARM macOS
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose up -d
