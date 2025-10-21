from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Simple test page
@app.route('/')
def home():
    return render_template_string("""
        <html>
        <head>
            <title>Reality Check AI</title>
            <style>
                body {
                    background-color: #0f172a;
                    color: white;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                }
                input, button {
                    padding: 10px;
                    margin: 10px;
                    border-radius: 8px;
                    border: none;
                }
                button {
                    background: #2563eb;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background: #1e40af;
                }
            </style>
        </head>
        <body>
            <h1>Reality Check AI 🔍</h1>
            <p>Upload an image, video, or text to verify authenticity.</p>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <button type="submit">Analyze</button>
            </form>
        </body>
        </html>
    """)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    # Simulate AI analysis
    return jsonify({
        "file": filename,
        "result": "This content appears authentic.",
        "confidence": "98%"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
