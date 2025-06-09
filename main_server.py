from flask import Flask, request, redirect
from ip_detector import is_suspicious

app = Flask(__name__)
flagged_ips = set()
LOG_FILE = "trap_log.txt"  # Shared log file

@app.before_request
def check_ip():
    ip = request.remote_addr
    if is_suspicious(ip):
        flagged_ips.add(ip)
    if ip in flagged_ips:
        with open(LOG_FILE, "a") as log:
            log.write(f"{ip} was redirected from main_server.py at endpoint {request.path}\n")
        return redirect("http://localhost:5001/trap", code=307)

@app.route('/api/data')
def real_data():
    return {"status": "success", "data": "This is real API data"}

if __name__ == "__main__":
    app.run(port=5000)

