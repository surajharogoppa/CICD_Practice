from flask import Flask, jsonify, request, render_template_string
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

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask CI/CD API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            padding: 30px;
            text-align: center;
            border-bottom: 2px solid #00d4ff33;
        }

        header h1 { font-size: 2rem; color: #00d4ff; }
        header p { color: #888; margin-top: 8px; }

        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 20px;
            background: #1a1a2e;
            border-bottom: 1px solid #ffffff11;
        }

        .stat { text-align: center; }
        .stat-number { font-size: 1.8rem; font-weight: bold; color: #00d4ff; }
        .stat-label { font-size: 0.75rem; color: #888; text-transform: uppercase; }

        .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 24px;
        }

        .card {
            background: #1a1a2e;
            border: 1px solid #ffffff11;
            border-radius: 12px;
            padding: 24px;
            transition: border-color 0.3s;
        }

        .card:hover { border-color: #00d4ff55; }

        .card h2 {
            font-size: 1rem;
            color: #00d4ff;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card p { color: #aaa; font-size: 0.9rem; line-height: 1.6; }

        button {
            background: #00d4ff22;
            color: #00d4ff;
            border: 1px solid #00d4ff55;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            margin-top: 14px;
            transition: all 0.2s;
        }

        button:hover { background: #00d4ff44; }

        input {
            width: 100%;
            padding: 8px 12px;
            background: #0f0f1a;
            border: 1px solid #ffffff22;
            border-radius: 8px;
            color: #e0e0e0;
            font-size: 0.85rem;
            margin-top: 8px;
        }

        input:focus { outline: none; border-color: #00d4ff55; }

        .result {
            margin-top: 14px;
            padding: 12px;
            background: #0f0f1a;
            border-radius: 8px;
            border-left: 3px solid #00d4ff;
            font-size: 0.85rem;
            color: #ccc;
            min-height: 44px;
            display: none;
            word-break: break-all;   /* ← add this */
            overflow-wrap: break-word; /* ← and this as backup */
        }
        }

        .result.show { display: block; }

        .joke-setup { color: #ccc; font-style: italic; }
        .joke-punchline { color: #00d4ff; margin-top: 8px; font-weight: bold; }

        .message-list { max-height: 180px; overflow-y: auto; margin-top: 12px; }
        .message-item {
            padding: 8px;
            border-bottom: 1px solid #ffffff11;
            font-size: 0.82rem;
        }
        .message-item span { color: #00d4ff; font-weight: bold; }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 8px;
        }
        .get { background: #00d4ff22; color: #00d4ff; }
        .post { background: #00ff8822; color: #00ff88; }
        .patch { background: #ff880022; color: #ff8800; }

        footer {
            text-align: center;
            padding: 30px;
            color: #444;
            font-size: 0.8rem;
            margin-top: 60px;
            border-top: 1px solid #ffffff11;
        }

        #server-time { color: #00d4ff; }
    </style>
</head>
<body>

<header>
    <h1>🚀 Flask CI/CD API</h1>
    <p>Live on Docker · Deployed via GitHub Actions · Hosted on Render</p>
</header>

<div class="stats-bar">
    <div class="stat">
        <div class="stat-number" id="visit-count">-</div>
        <div class="stat-label">Total Visits</div>
    </div>
    <div class="stat">
        <div class="stat-number" id="user-count">-</div>
        <div class="stat-label">Users</div>
    </div>
    <div class="stat">
        <div class="stat-number" id="message-count">-</div>
        <div class="stat-label">Messages</div>
    </div>
    <div class="stat">
        <div class="stat-number" id="server-time">-</div>
        <div class="stat-label">Server Time</div>
    </div>
</div>

<div class="container">
    <div class="grid">

        <!-- Joke Card -->
        <div class="card">
            <h2>😂 Random Joke <span class="badge get">GET</span></h2>
            <p>Click to get a random developer joke.</p>
            <button onclick="getJoke()">Get Joke</button>
            <div class="result" id="joke-result"></div>
        </div>

        <!-- Quote Card -->
        <div class="card">
            <h2>💬 Random Quote <span class="badge get">GET</span></h2>
            <p>Get an inspiring programming quote.</p>
            <button onclick="getQuote()">Get Quote</button>
            <div class="result" id="quote-result"></div>
        </div>

        <!-- Coin Flip -->
        <div class="card">
            <h2>🪙 Coin Flip <span class="badge get">GET</span></h2>
            <p>Flip a coin and test your luck.</p>
            <button onclick="coinFlip()">Flip Coin</button>
            <div class="result" id="coin-result"></div>
        </div>

        <!-- Dice Roller -->
        <div class="card">
            <h2>🎲 Dice Roller <span class="badge get">GET</span></h2>
            <p>Roll dice with custom sides and count.</p>
            <input type="number" id="dice-sides" placeholder="Sides (default 6)" min="2" max="100"/>
            <input type="number" id="dice-count" placeholder="Count (default 1)" min="1" max="10"/>
            <button onclick="rollDice()">Roll Dice</button>
            <div class="result" id="dice-result"></div>
        </div>

        <!-- Register -->
        <div class="card">
            <h2>👤 Register User <span class="badge post">POST</span></h2>
            <p>Create a new user account.</p>
            <input type="text" id="reg-username" placeholder="Username"/>
            <input type="password" id="reg-password" placeholder="Password"/>
            <button onclick="registerUser()">Register</button>
            <div class="result" id="reg-result"></div>
        </div>

        <!-- Login -->
        <div class="card">
            <h2>🔐 Login <span class="badge post">POST</span></h2>
            <p>Login with your credentials.</p>
            <input type="text" id="login-username" placeholder="Username"/>
            <input type="password" id="login-password" placeholder="Password"/>
            <button onclick="loginUser()">Login</button>
            <div class="result" id="login-result"></div>
        </div>

        <!-- Post Message -->
        <div class="card">
            <h2>📝 Post Message <span class="badge post">POST</span></h2>
            <p>Post a public message (must be registered).</p>
            <input type="text" id="msg-username" placeholder="Your username"/>
            <input type="text" id="msg-text" placeholder="Your message (max 200 chars)"/>
            <button onclick="postMessage()">Post Message</button>
            <div class="result" id="msg-result"></div>
        </div>

        <!-- Message Board -->
        <div class="card">
            <h2>📋 Message Board <span class="badge get">GET</span></h2>
            <p>See the latest public messages.</p>
            <button onclick="getMessages()">Load Messages</button>
            <div class="message-list" id="messages-list"></div>
        </div>

        <!-- Word Count -->
        <div class="card">
            <h2>🔤 Word Counter <span class="badge post">POST</span></h2>
            <p>Count words and characters in your text.</p>
            <input type="text" id="wc-text" placeholder="Type something..."/>
            <button onclick="wordCount()">Count</button>
            <div class="result" id="wc-result"></div>
        </div>

        <!-- Reverse String -->
        <div class="card">
            <h2>🔁 Reverse Text <span class="badge post">POST</span></h2>
            <p>Reverse any string instantly.</p>
            <input type="text" id="rev-text" placeholder="Type something..."/>
            <button onclick="reverseText()">Reverse</button>
            <div class="result" id="rev-result"></div>
        </div>

    </div>
</div>

<footer>
    Built with Flask · Dockerized · CI/CD via GitHub Actions · Hosted on Render
</footer>

<script>
    // ── Helpers ──────────────────────────────────────────
    function show(id, html) {
        const el = document.getElementById(id);
        el.innerHTML = html;
        el.classList.add("show");
    }

    async function get(url) {
        const res = await fetch(url);
        return res.json();
    }

    async function post(url, body) {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        return res.json();
    }

    // ── Load Stats ───────────────────────────────────────
    async function loadStats() {
        const info = await get("/info");
        const users = await get("/users");
        const msgs = await get("/messages");

        document.getElementById("visit-count").textContent = info.total_visits;
        document.getElementById("user-count").textContent = users.total;
        document.getElementById("message-count").textContent = msgs.total;
        document.getElementById("server-time").textContent = info.time.split(" ")[1];
    }

    // ── Joke ─────────────────────────────────────────────
    async function getJoke() {
        const d = await get("/joke");
        show("joke-result", `
            <div class="joke-setup">"${d.setup}"</div>
            <div class="joke-punchline">→ ${d.punchline}</div>
        `);
    }

    // ── Quote ────────────────────────────────────────────
    async function getQuote() {
        const d = await get("/quote");
        show("quote-result", `"${d.quote}" <br><br>— <b>${d.author}</b>`);
    }

    // ── Coin Flip ────────────────────────────────────────
    async function coinFlip() {
        const d = await get("/coinflip");
        const emoji = d.result === "Heads" ? "🌝" : "🌚";
        show("coin-result", `${emoji} <b>${d.result}</b>`);
    }

    // ── Dice ─────────────────────────────────────────────
    async function rollDice() {
        const sides = document.getElementById("dice-sides").value || 6;
        const count = document.getElementById("dice-count").value || 1;
        const d = await get(`/dice?sides=${sides}&count=${count}`);
        if (d.error) return show("dice-result", `❌ ${d.error}`);
        show("dice-result", `🎲 Rolls: <b>${d.rolls.join(", ")}</b> | Total: <b>${d.total}</b>`);
    }

    // ── Register ─────────────────────────────────────────
    async function registerUser() {
        const username = document.getElementById("reg-username").value;
        const password = document.getElementById("reg-password").value;
        const d = await post("/users/register", { username, password });
        if (d.error) return show("reg-result", `❌ ${d.error}`);
        show("reg-result", `✅ ${d.message} — welcome <b>${d.username}</b>!`);
        loadStats();
    }

    // ── Login ────────────────────────────────────────────
    async function loginUser() {
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;
        const d = await post("/users/login", { username, password });
        if (d.error) return show("login-result", `❌ ${d.error}`);
        show("login-result", `✅ ${d.message} | Messages posted: <b>${d.total_messages}</b>`);
    }

    // ── Post Message ─────────────────────────────────────
    async function postMessage() {
        const username = document.getElementById("msg-username").value;
        const text = document.getElementById("msg-text").value;
        const d = await post("/messages", { username, text });
        if (d.error) return show("msg-result", `❌ ${d.error}`);
        show("msg-result", `✅ ${d.message}`);
        loadStats();
    }

    // ── Get Messages ─────────────────────────────────────
    async function getMessages() {
        const d = await get("/messages");
        const list = document.getElementById("messages-list");
        if (d.messages.length === 0) {
            list.innerHTML = "<div class='message-item'>No messages yet.</div>";
            return;
        }
        list.innerHTML = d.messages.reverse().map(m => `
            <div class="message-item">
                <span>${m.username}</span>: ${m.text}
                <div style="color:#555; font-size:0.75rem">${m.posted_at}</div>
            </div>
        `).join("");
    }

    // ── Word Count ───────────────────────────────────────
    async function wordCount() {
        const text = document.getElementById("wc-text").value;
        const d = await post("/utils/wordcount", { text });
        if (d.error) return show("wc-result", `❌ ${d.error}`);
        show("wc-result", `Words: <b>${d.word_count}</b> | Chars: <b>${d.char_count}</b> | No spaces: <b>${d.char_count_no_spaces}</b>`);
    }

    // ── Reverse ──────────────────────────────────────────
    async function reverseText() {
        const text = document.getElementById("rev-text").value;
        const d = await post("/utils/reverse", { text });
        if (d.error) return show("rev-result", `❌ ${d.error}`);
        show("rev-result", `🔁 <b>${d.reversed}</b>`);
    }

    // ── Init ─────────────────────────────────────────────
    loadStats();
    setInterval(loadStats, 10000); // refresh stats every 10 seconds
</script>

</body>
</html>
"""

# ─── Routes ───────────────────────────────────────────────

@app.route("/")
def home():
    visit_counter["count"] += 1
    return render_template_string(HTML)

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