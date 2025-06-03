from flask import Flask, request, render_template, send_file, redirect, url_for
from collections import defaultdict
import os

app = Flask(__name__)
trap_hits = defaultdict(int)
LOG_FILE = "trap_log.txt"

@app.route('/trap', methods=['GET', 'POST'])
def trap():
    ip = request.remote_addr
    trap_hits[ip] += 1
    with open(LOG_FILE, "a") as log:
        log.write(f"{ip} hit the trap with {request.method} {request.path}\n")
    return {"status": "fake", "data": "Here is some fake data. 😈"}

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", hits=dict(trap_hits))

@app.route('/reset', methods=['POST'])
def reset():
    trap_hits.clear()
    open(LOG_FILE, 'w').close()  # clear log file
    return redirect(url_for('dashboard'))

@app.route('/export')
def export():
    return send_file(LOG_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5001)
