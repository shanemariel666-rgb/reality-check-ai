from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Use your Hugging Face token here
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "YOUR_TOKEN_HERE")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.mimetype)}

    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    url = "https://api-inference.huggingface.co/models/umm-maybe/AI-image-detector"  # Reliable model

    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': f'Hugging Face error {response.status_code}', 'details': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
