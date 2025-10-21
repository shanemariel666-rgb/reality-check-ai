from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")

@app.route("/", methods=["GET"])
def home():
    # Render your web interface
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    text = request.form.get("text")

    if text:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        data = {"inputs": text}
        response = requests.post(
            "https://api-inference.huggingface.co/models/roberta-base-openai-detector",
            headers=headers, json=data
        )
        return jsonify(response.json())

    elif file:
        headers = {"Authorization": f"Token {REPLICATE_API_KEY}"}
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json={
                "version": "a16z-infra/clip:latest",
                "input": {"image": "data:image/jpeg;base64,"}
            }
        )
        return jsonify(response.json())

    else:
        return jsonify({"error": "No file or text provided"}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
