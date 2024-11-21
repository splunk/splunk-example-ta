import random

from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "super-secret-api-token"

# Mock data for demonstration replace it with actual data retrieval logic
all_events = [{"id": i, "event": f"Event {i}"} for i in range(1, 101)]


# Mock data for demonstration replace it with actual data retrieval logic
def get_mocked_events(page_num: int, per_page: int):
    return [
        {"id": i, "event": f"Event {i}"}
        for i in range(page_num * per_page, (page_num + 1) * per_page)
    ]


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
    page = request.args.get("page", 0, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Calculate start and end indices for the items on the current page
    paginated_events = get_mocked_events(page, per_page)

    total_events = len(paginated_events)
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
