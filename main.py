from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# === API KEYS FROM ENVIRONMENT ===
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")

# === HOME PAGE ===
@app.route("/", methods=["GET"])
def home():
    # Render your web interface from /templates/index.html
    return render_template("index.html")

# === ANALYZE ENDPOINT ===
@app.route("/analyze", methods=["POST"])
def analyze():
    """Handles both text and image analysis."""
    file = request.files.get("file")
    text = request.form.get("text")

    # ---- TEXT CHECK: Hugging Face ----
    if text:
        try:
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            data = {"inputs": text}
            response = requests.post(
                "https://api-inference.huggingface.co/models/openai-community/roberta-base-openai-detector",
                headers=headers,
                json=data,
                timeout=30
            )
            return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": f"Hugging Face error: {str(e)}"}), 500

    # ---- IMAGE/VIDEO CHECK: Replicate ----
    elif file:
        try:
            headers = {"Authorization": f"Token {REPLICATE_API_KEY}"}

            # Step 1: upload file to Replicate's temporary storage
            upload_response = requests.post(
                "https://api.replicate.com/v1/uploads",
                headers=headers,
                files={"file": (file.filename, file.stream, file.mimetype)},
                timeout=60
            )
            upload_json = upload_response.json()
            if "urls" not in upload_json:
                return jsonify({"error": "Upload failed", "details": upload_json}), 400
            upload_url = upload_json["urls"]["get"]

            # Step 2: run a forensics/detection model on uploaded file
            # This version ID belongs to a public image forensics model
            model_version = "cffb5e5b6d31e580c2f911a65194d7a911dd7d54b7014966212fcf857f5d2f6c"
            prediction = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json={
                    "version": model_version,
                    "input": {"image": upload_url}
                },
                timeout=60
            )
            return jsonify(prediction.json())

        except Exception as e:
            return jsonify({"error": f"Replicate error: {str(e)}"}), 500

    else:
        return jsonify({"error": "No file or text provided"}), 400


# === SERVER RUN ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)