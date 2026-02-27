from flask import Flask, jsonify
import os
import datetime
import platform

app = Flask(__name__)

visit_counter = {"count": 0}

# ─── Home ─────────────────────────────────────────────────

@app.route("/")
def home():
    visit_counter["count"] += 1
    return jsonify({
        "message": "Welcome to Flask API!",
        "status" : "success",
        "total_visits": visit_counter["count"],
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/info")
def info():
    return jsonify({
        "python_version": platform.python_version(),
        "os": platform.system(),
        "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.getenv("FLASK_ENV", "development")
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)