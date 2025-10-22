from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' in request.files:
            image = request.files['image']
            image_path = os.path.join(app.static_folder, 'uploaded_image.png')
            image.save(image_path)
            return jsonify({
                "status": "success",
                "message": "Image uploaded successfully.",
                "path": image_path
            })
        elif 'text' in request.form:
            text = request.form['text']
            if not text.strip():
                return jsonify({"error": "No text provided"}), 400
            return jsonify({
                "status": "success",
                "analysis": f"AI Verification complete for: '{text}'"
            })
        else:
            return jsonify({"error": "No input provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
