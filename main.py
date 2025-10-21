from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Render the homepage we added in templates/index.html
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # For now, we simulate analysis
        filename = file.filename
        fake_result = {
            "filename": filename,
            "analysis": "Image/video/text appears authentic with no detected tampering.",
            "confidence": "92%",
            "notes": "This is a demo result. Real AI model integration coming soon."
        }
        return jsonify(fake_result), 200

    except Exception as e:
        # If anything goes wrong, we still return valid JSON
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Flask local run for debugging
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
