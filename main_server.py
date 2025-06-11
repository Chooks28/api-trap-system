from flask import Flask, request, redirect, jsonify
from ip_detector import is_suspicious,record_404,record_login_failure

app = Flask(__name__)
flagged_ips = set()
LOG_FILE = "trap_log.txt"

USER_DB = {
    "alice": "password123",
    "bob": "secure456"
}


@app.before_request
def check_ip():
    ip = request.remote_addr
    if is_suspicious(ip):
        flagged_ips.add(ip)
    if ip in flagged_ips:
        with open(LOG_FILE, "a") as log:
            log.write(f"{ip} was redirected from main_server.py at endpoint {request.path}\n")
        return redirect("http://127.0.0.1:5001/trap", code=307)

@app.after_request
def track_404(response):
    if response.status_code == 404:
        ip = request.remote_addr
        record_404(ip)
    return response

@app.route('/api/data')
def real_data():
    return {"status": "success", "data": "This is real API data"}

@app.route('/api/login', methods=['POST'])
def login():
    ip = request.remote_addr
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in USER_DB and USER_DB[username] == password:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        record_login_failure(ip)
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(port=5000)

