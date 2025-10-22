from flask import Flask, render_template, request, jsonify, send_from_directory
import requests, os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    image = request.files.get('image')
    if not image:
        return jsonify({'error': 'No image uploaded'}), 400

    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    if not HUGGINGFACE_TOKEN:
        return jsonify({'error': 'Missing Hugging Face token'}), 500

    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    api_url = "https://api-inference.huggingface.co/models/orion-ai/AI-image-detector"
    response = requests.post(api_url, headers=headers, files={"file": image})

    if response.status_code != 200:
        return jsonify({'error': 'Failed to analyze image', 'details': response.text}), 500

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
