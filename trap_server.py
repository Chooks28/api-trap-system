from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os

app = Flask(__name__)
LOG_FILE = "trap_log.txt"

USER_DB = {
    "alice": "password123",
    "bob": "secure456"
}

@app.route('/trap', methods=['GET', 'POST'])
def trap():
    ip = request.remote_addr
    with open(LOG_FILE, "a") as log:
        log.write(f"{ip} hit the trap with {request.method} {request.path}\n")
    return {"status": "fake", "data": "Here is some fake data. 😈"}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in USER_DB and USER_DB[username] == password:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/dashboard')
def dashboard():
    redirects = {}
    trap_hits = {}

    try:
        with open(LOG_FILE, "r") as log:
            for line in log:
                parts = line.split()
                if len(parts) >= 1:
                    ip = parts[0]
                    if "redirected" in line:
                        redirects[ip] = redirects.get(ip, 0) + 1
                    elif "hit the trap" in line:
                        trap_hits[ip] = trap_hits.get(ip, 0) + 1
    except FileNotFoundError:
        pass

    all_ips = set(redirects.keys()) | set(trap_hits.keys())
    combined_stats = {
        ip: {
            "redirects": redirects.get(ip, 0),
            "trap_hits": trap_hits.get(ip, 0)
        }
        for ip in all_ips
    }

    return render_template("dashboard.html", hits=combined_stats)

@app.route('/reset', methods=['POST'])
def reset():
    open(LOG_FILE, 'w').close()
    return redirect(url_for('dashboard'))

@app.route('/export')
def export():
    return send_file(LOG_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5001)

