from collections import defaultdict
import time

request_counts = defaultdict(list)
request_404_counts = defaultdict(list)
login_fail_counts = defaultdict(list)

def too_many_requests(ip, threshold=100, window=10):
    now = time.time()
    request_counts[ip] = [t for t in request_counts[ip] if now - t < window]
    request_counts[ip].append(now)
    return len(request_counts[ip]) > threshold

def record_404(ip):
    now = time.time()
    request_404_counts[ip] = [t for t in request_404_counts[ip] if now - t < 10]
    request_404_counts[ip].append(now)

def too_many_404s(ip, threshold=10, window=10):
    now = time.time()
    request_404_counts[ip] = [t for t in request_404_counts[ip] if now - t < window]
    return len(request_404_counts[ip]) > threshold

def record_login_failure(ip):
    now = time.time()
    login_fail_counts[ip] = [t for t in login_fail_counts[ip] if now - t < 60]
    login_fail_counts[ip].append(now)

def too_many_login_fails(ip, threshold=20, window=60):
    now = time.time()
    login_fail_counts[ip] = [t for t in login_fail_counts[ip] if now - t < window]
    return len(login_fail_counts[ip]) > threshold

def is_suspicious(ip):
    return (
            too_many_requests(ip)
            or too_many_404s(ip)
            or too_many_login_fails(ip)
    )