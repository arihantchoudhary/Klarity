"""
Starter code for the Ask-AI application's main service.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to Ask-AI!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
