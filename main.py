from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os
from PIL import Image

app = Flask(__name__)
CORS(app)

# ======================
# Environment Variables
# ======================
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# ======================
# Simple HTML interface
# ======================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Reality Check AI</title>
    <style>
        body { font-family: Arial; text-align: center; background: #f4f4f9; margin: 40px; }
        .card { background: #fff; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 400px; margin: auto; }
        input, textarea { width: 90%; margin: 10px; padding