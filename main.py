from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# === API KEYS FROM ENVIRONMENT ===
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")

# === HOME PAGE ===
@app.route("/", methods=["GET"])
def home():
    # Render your web interface from /templates/index.html
    return render_template("index.html")

# === ANALYZE ENDPOINT ===
@app.route("/analyze", methods=["POST"])
def analyze():
    """Handles both text and image analysis."""
    file = request.files.get("file")
    text = request.form.get("text")

    # ---- TEXT CHECK: Hugging Face ----
    if text:
        try:
            headers =
