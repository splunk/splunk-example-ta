import random

from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "super-secret-api-token"

# Mock data for demonstration replace it with actual data retrieval logic
all_events = [{"id": i, "event": f"Event {i}"} for i in range(1, 101)]


def _should_fail_with_server_error() -> bool:
    if random.random() < 0.1:
        return True
    return False


@app.route("/events")
def events():
    # API key validation
    api_key = request.headers.get("API-Key")

    if api_key != API_KEY:
        return "Unauthorized", 401

    if _should_fail_with_server_error():
        return "Internal Server Error", 500

    # Get pagination parameters from the query string
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Calculate start and end indices for the items on the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_events = all_events[start:end]

    total_events = len(all_events)
    total_pages = (total_events + per_page - 1) // per_page

    return (
        jsonify(
            {
                "events": paginated_events,
                "page": page,
                "per_page": per_page,
                "total_events": total_events,
                "total_pages": total_pages,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
