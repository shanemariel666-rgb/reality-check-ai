from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os
import base64
import traceback

app = Flask(__name__)
CORS(app)

# Load API keys
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Reality Check AI</title>
    <style>
        body { font-family: Arial; background: #f4f4f9; text-align: center; padding: 40px; }
        .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 400px; margin: auto; }
        input, textarea { width: 90%; padding: 10px; margin: 8px; border-radius: 8px; border: 1px solid #ccc; }
        button { background-color: #007BFF; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        pre { text-align: left; background: #f0f0f0; padding: 15px; border-radius: 8px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Reality Check AI</h2>
        <p>Upload an image or enter text to verify authenticity.</p>
        <form id="upload-form" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <textarea name="text" rows="3" placeholder="Paste text or claim here..."></textarea><br>
            <button type="submit">Analyze</button>
        </form>
        <pre id="result"></pre>
    </div>
    <script>
        const form = document.getElementById("upload-form");
        form.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const res = await fetch("/analyze", { method: "POST", body: formData });
            const data = await res.json();
            document.getElementById("result").innerText = JSON.stringify(data, null, 2);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        text_input = request.form.get('text', '').strip()
        file = request.files.get('file')

        # 1️⃣ If no input
        if not text_input and not file:
            return jsonify({"error": "Please provide text or image input"}), 400

        # 2️⃣ If text input → analyze via Hugging Face
        if text_input:
            if not HUGGINGFACE_TOKEN:
                return jsonify({"error": "Missing HUGGINGFACE_TOKEN"}), 500

            api_url = "https://api-inference.huggingface.co/models/microsoft/deberta-v3-small"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
            response = requests.post(api_url, headers=headers, json={"inputs": text_input})
            result = response.json()
            return jsonify({"type": "text", "input": text_input, "result": result})

        # 3️⃣ If image input → analyze via Replicate
        if file:
            if not REPLICATE_API_TOKEN:
                return jsonify({"error": "Missing REPLICATE_API_TOKEN"}), 500

            image_bytes = file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            image_data_uri = f"data:image/png;base64,{image_base64}"

            headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
            payload = {
                "version": "a16f1e64b6b9284a3e98b8b1b1a90b83b2e8e741b8adf417e4bced3e2a69b3a3",
                "input": {"image": image_data_uri}
            }

            response = requests.post("https://api.replicate.com/v1/predictions",
                                     headers=headers, json=payload)
            result = response.json()
            return jsonify({"type": "image", "result": result})

    except Exception as e:
        error_message = traceback.format_exc()
        return jsonify({"error": "Server error", "details": error_message}), 500


if __name__ == '__main__':
    app.run(debug=True)