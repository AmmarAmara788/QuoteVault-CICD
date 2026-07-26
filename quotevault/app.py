# Quotes API (Flask). Stores quotes IN MEMORY so the image runs standalone —
# no database needed. Data resets when the process restarts (fine for a demo).
import random
from flask import Flask, jsonify, request
from .validation import validate_quote


def create_app():
    app = Flask(__name__)
    quotes = []            # in-memory store
    state = {"next_id": 1}

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/quotes")
    def list_quotes():
        return jsonify(quotes=quotes)

    @app.post("/api/quotes")
    def add_quote():
        ok, errors, value = validate_quote(request.get_json(silent=True) or {})
        if not ok:
            return jsonify(errors=errors), 400
        quote = {"id": state["next_id"], **value}
        state["next_id"] += 1
        quotes.append(quote)
        return jsonify(quote=quote), 201

    @app.get("/api/quotes/random")
    def random_quote():
        if not quotes:
            return jsonify(error="no quotes yet"), 404
        return jsonify(quote=random.choice(quotes))

    return app
