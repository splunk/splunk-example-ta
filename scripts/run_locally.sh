SCRIPT_DIR=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
REPO_ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

cd ../
docker compose down
python3 -m venv .venv
source .venv/bin/activate
cd $REPO_ROOT_DIR
pip install -r requirements-dev.txt
ucc-gen build
# running on ARM macOS
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose up -d --build
echo -n "Waiting Splunk for run"
until curl -Lsk "https://localhost:8088/services/collector/health" &>/dev/null ; do echo -n "." && sleep 5 ; done
 