from flask import Flask, request

app = Flask(__name__)

API_KEY = "super-secret-api-token"


@app.route("/auth")
def auth():
    return API_KEY


@app.route("/events")
def users():
    api_key = request.headers.get("API-Key")
    if api_key != API_KEY:
        return "Unauthorized", 401
    return {"event": "hello world"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
