from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)

# Simple homepage with image
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reality Check AI</title>
  <link rel="icon" type="image/png" href="{{ url_for('static', filename='logo.png') }}">
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f4f4f9;
      text-align: center;
      margin-top: 80px;
    }
    .card {
      background: white;
      max-width: 420px;
      margin: auto;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    img {
      width: 100px;
      margin-bottom: 20px;
    }
    input, textarea {
      width: 90%;
      padding: 10px;
      margin: 8px 0;
      border-radius: 8px;
      border: 1px solid #ccc;
    }
    button {
      background: #007bff;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
    }
    button:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <div class="card">
    <img src="{{ url_for('static', filename='logo.png') }}" alt="Reality Check AI Logo">
    <h1>Reality Check AI</h1>
    <p>Upload an image or enter text to verify authenticity.</p>

    <form id="uploadForm" enctype="multipart/form-data">
      <input type="file" name="file"><br>
      <textarea name="text" placeholder="Paste text or claim here..."></textarea><br>
      <button type="submit">Analyze</button>
    </form>

    <div id="result"></div>
  </div>

  <script>
    const form = document.getElementById('uploadForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const res = await fetch('/analyze', { method: 'POST', body: data });
      const json = await res.json();
      document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(json, null, 2) + '</pre>';
    });
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    text = request.form.get('text')
    result = {"status": "success"}

    if file:
        result["file"] = file.filename
    if text:
        result["text_length"] = len(text)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
