from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        files = {"file": (file.filename, file.read())}

        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        model_url = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

        response = requests.post(model_url, headers=headers, files=files)
        if response.status_code != 200:
            return jsonify({
                "error": f"Hugging Face API error {response.status_code}",
                "details": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
