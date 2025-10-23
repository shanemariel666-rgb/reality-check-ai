from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/umm-maybe/AI-image-detector"
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
REPLICATE_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_bytes = file.read()

    try:
        # Try Hugging Face API
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=headers,
            data=file_bytes,
        )

        if response.status_code == 401:
            return jsonify({"error": "Unauthorized – check your Hugging Face token"}), 401
        elif response.status_code != 200:
            return jsonify({"error": f"Hugging Face API error {response.status_code}"}), 500

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            label = result[0].get("label", "Unknown")
            score = result[0].get("score", 0)
            return jsonify({"label": label, "score": round(score * 100, 2)})

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))