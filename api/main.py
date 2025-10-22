from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        text_input = request.form.get('text', '')
        image_file = request.files.get('image')

        if image_file:
            # Read image in memory (no saving to disk)
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes))

            # Convert image to base64 for preview or analysis
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            result = f"✅ Image '{image_file.filename}' processed successfully (in-memory)."
        elif text_input:
            result = f"🧠 Text analyzed: \"{text_input[:80]}...\""
        else:
            result = "⚠️ Please upload an image or enter text."

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)