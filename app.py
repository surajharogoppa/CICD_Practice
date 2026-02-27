from flask import Flask, jsonify, request,render_template
import datetime
import random
import hashlib
import os

app = Flask(__name__)

# ─── In-Memory Storage ────────────────────────────────────

users = {}
messages = []
visit_counter = {"count": 0}

jokes = [
    {"setup": "Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs!"},
    {"setup": "Why did the developer go broke?", "punchline": "Because he used up all his cache!"},
    {"setup": "What is a computer's favorite snack?", "punchline": "Microchips!"},
    {"setup": "Why do Java developers wear glasses?", "punchline": "Because they don't C#!"},
    {"setup": "How many programmers does it take to change a lightbulb?", "punchline": "None, that's a hardware problem!"},
]

quotes = [
    {"text": "Code is like humor. When you have to explain it, it is bad.", "author": "Cory House"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"text": "Java is to JavaScript what car is to carpet.", "author": "Chris Heilmann"},
    {"text": "Sometimes it pays to stay in bed on Monday rather than spending the rest of the week debugging.", "author": "Dan Salomon"},
]

# ─── HTML Dashboard ───────────────────────────────────────



# ─── Routes ───────────────────────────────────────────────

@app.route("/")
def home():
    visit_counter["count"] += 1
    return render_template("index.html")

@app.route("/info")
def info():
    return jsonify({
        "total_visits": visit_counter["count"],
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "users": len(users),
        "messages": len(messages)
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/joke")
def random_joke():
    joke = random.choice(jokes)
    return jsonify({"setup": joke["setup"], "punchline": joke["punchline"], "total_jokes": len(jokes)})

@app.route("/quote")
def random_quote():
    quote = random.choice(quotes)
    return jsonify({"quote": quote["text"], "author": quote["author"]})

@app.route("/coinflip")
def coinflip():
    result = random.choice(["Heads", "Tails"])
    return jsonify({"result": result})

@app.route("/dice")
def roll_dice():
    sides = request.args.get("sides", 6, type=int)
    count = request.args.get("count", 1, type=int)
    if sides < 2 or sides > 100:
        return jsonify({"error": "Sides must be between 2 and 100"}), 400
    if count < 1 or count > 10:
        return jsonify({"error": "Count must be between 1 and 10"}), 400
    rolls = [random.randint(1, sides) for _ in range(count)]
    return jsonify({"rolls": rolls, "total": sum(rolls), "sides": sides, "count": count})

@app.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password are required"}), 400
    username = data["username"].strip().lower()
    if username in users:
        return jsonify({"error": "Username already exists"}), 409
    hashed = hashlib.sha256(data["password"].encode()).hexdigest()
    users[username] = {
        "username": username,
        "password": hashed,
        "joined_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message_count": 0
    }
    return jsonify({"message": "User registered successfully", "username": username, "joined_at": users[username]["joined_at"]}), 201

@app.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password are required"}), 400
    username = data["username"].strip().lower()
    hashed = hashlib.sha256(data["password"].encode()).hexdigest()
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if users[username]["password"] != hashed:
        return jsonify({"error": "Wrong password"}), 401
    return jsonify({"message": f"Welcome back {username}!", "joined_at": users[username]["joined_at"], "total_messages": users[username]["message_count"]})

@app.route("/users", methods=["GET"])
def get_users():
    public = [{"username": u["username"], "joined_at": u["joined_at"], "message_count": u["message_count"]} for u in users.values()]
    return jsonify({"users": public, "total": len(public)})

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": messages[-20:], "total": len(messages)})

@app.route("/messages", methods=["POST"])
def post_message():
    data = request.get_json()
    if not data or "username" not in data or "text" not in data:
        return jsonify({"error": "username and text are required"}), 400
    username = data["username"].strip().lower()
    if username not in users:
        return jsonify({"error": "Register first before posting"}), 403
    if len(data["text"]) > 200:
        return jsonify({"error": "Message too long, max 200 characters"}), 400
    message = {"id": len(messages) + 1, "username": username, "text": data["text"], "posted_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    messages.append(message)
    users[username]["message_count"] += 1
    return jsonify({"message": "Posted successfully", "post": message}), 201

@app.route("/utils/reverse", methods=["POST"])
def reverse_string():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Provide a text field"}), 400
    return jsonify({"original": data["text"], "reversed": data["text"][::-1]})

@app.route("/utils/wordcount", methods=["POST"])
def word_count():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Provide a text field"}), 400
    text = data["text"]
    return jsonify({"text": text, "word_count": len(text.split()), "char_count": len(text), "char_count_no_spaces": len(text.replace(" ", ""))})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)