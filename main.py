from flask import Flask, request, jsonify, render_template_string
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home page UI
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reality Check AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f7f7f7;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 450px;
                width: 100%;
            }
            h1 {
                color: #111;
            }
            input, textarea, button {
                margin-top: 1rem;
                width: 100%;
                padding: 0.8rem;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            button {
                background: #0056ff;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                background: #0041cc;
            }
            pre {
                text-align: left;
                background: #f0f0f0;
                padding: 1rem;
                border-radius: 10px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Reality Check AI</h1>
            <p>Upload an image or enter text to verify authenticity.</p>
            <form id="analyzeForm">
                <input type="file" id="image" name="image">
                <textarea id="text" name="text" placeholder="Paste text or claim here..."></textarea>
                <button type="submit">Analyze</button>
            </form>
            <pre id="result"></pre>
        </div>

        <script>
            document.getElementById("analyzeForm").ons