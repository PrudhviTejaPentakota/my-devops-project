from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUESTS = Counter('hello_requests_total', 'Total Hello requests')

@app.route("/")
def hello():
    REQUESTS.inc()
    return "Hello from DevOps Project! 🚀"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
