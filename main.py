from flask import Flask, render_template, request, jsonify
import os, requests

app = Flask(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("user_input", "")
    if not text:
        return jsonify({"error": "No input provided"}), 400

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}

    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
            headers=headers,
            json=payload,
            timeout=30
        )
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
