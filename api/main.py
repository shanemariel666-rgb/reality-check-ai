from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Load API keys from environment
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']
        image_bytes = image.read()

        # Send image to Hugging Face model
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/resnet-50",
            headers=headers,
            data=image_bytes
        )

        if response.status_code != 200:
            return jsonify({'error': f'Hugging Face error: {response.text}'}), 500

        result = response.json()
        label = result[0]['label']
        score = result[0]['score']

        return jsonify({
            'label': label,
            'confidence': round(score * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
