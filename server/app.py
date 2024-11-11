import random

from flask import Flask, request

app = Flask(__name__)

API_KEY = "super-secret-api-token"


def _should_fail_with_server_error() -> bool:
    if random.random() < 0.1:
        return True
    return False


@app.route("/events")
def events():
    api_key = request.headers.get("API-Key")
    if api_key != API_KEY:
        return "Unauthorized", 401
    if _should_fail_with_server_error():
        return "Internal Server Error", 500
    return {"event": "hello world"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
