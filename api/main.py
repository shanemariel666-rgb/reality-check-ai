from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests

# Set correct paths for Flask to find assets
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../static')
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    hf_token = os.getenv("HF_API_TOKEN")

    if not hf_token:
        return jsonify({"error": "Missing HF_API_TOKEN"}), 500

    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": f"Analyze this text for realism: {text}"}

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-small",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": "HuggingFace API failed", "details": response.text}), 500

    result = response.json()
    output = result[0]["generated_text"] if isinstance(result, list) else str(result)
    return jsonify({"analysis": output})

# Serve static files (important for Vercel)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../static'), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))