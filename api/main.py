from flask import Flask, render_template, request, jsonify
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")
STATIC_DIR = os.path.join(BASE_DIR, "../static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Environment variables
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    temp_path = os.path.join(BASE_DIR, "temp_upload")
    file.save(temp_path)

    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
        files = {"file": open(temp_path, "rb")}
        response = requests.post(
            "https://api-inference.huggingface.co/models/roberta-base-openai-detector",
            headers=headers,
            files=files,
        )

        if response.status_code == 200:
            hf_data = response.json()
            return jsonify({"source": "huggingface", "result": hf_data})

        return jsonify({"error": "AI analysis failed", "status": response.status_code}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(debug=True)