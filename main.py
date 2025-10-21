from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"message": "Reality Check AI API is running successfully!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
