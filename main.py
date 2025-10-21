from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "YOUR_HF_TOKEN_HERE")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("user_input")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": user_input}

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
        headers=headers,
        json=data
    )

    result = response.json()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
