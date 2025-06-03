from collections import defaultdict
import time

request_counts = defaultdict(list)

def is_suspicious(ip):
    now = time.time()
    request_counts[ip] = [t for t in request_counts[ip] if now - t < 10]
    request_counts[ip].append(now)
    return len(request_counts[ip]) > 5  # >5 requests in 10 seconds = suspicious
