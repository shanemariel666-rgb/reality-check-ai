# api/main.py
import os
import time
import base64
import json
import traceback
import requests
from flask import Flask, request, jsonify, render_template

# App: static/templates are at project root; Vercel runs api/main.py
app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Environment variables
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
REPLICATE_IMAGE_MODEL = os.environ.get("REPLICATE_IMAGE_MODEL")  # e.g. model version id (sha)
REPLICATE_VIDEO_MODEL = os.environ.get("REPLICATE_VIDEO_MODEL")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
HF_TEXT_MODEL = os.environ.get("HF_TEXT_MODEL", "openai-community/roberta-base-openai-detector")

# Helpers: polling replicate prediction until done
def poll_replicate_prediction(prediction_id, token, timeout=90):
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
    headers = {"Authorization": f"Token {token}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(url, headers=headers, timeout=20)
        try:
            j = r.json()
        except Exception:
            return {"error": "invalid_json_from_replicate", "status_code": r.status_code, "text": r.text}
        status = j.get("status")
        if status == "succeeded":
            return {"ok": True, "result": j}
        if status == "failed":
            return {"error": "prediction_failed", "details": j}
        time.sleep(1.0)
    return {"error": "prediction_timeout"}

# Normalize HF text response into friendly verdict when possible
def normalize_hf_text(resp_json):
    # Many HF detectors return list of dicts with label/score
    if isinstance(resp_json, list) and resp_json:
        first = resp_json[0]
        return {"verdict": first.get("label"), "confidence": first.get("score"), "raw": resp_json}
    if isinstance(resp_json, dict):
        # some models return { "label": "...", "score": ... }
        if "label" in resp_json:
            return {"verdict": resp_json.get("label"), "confidence": resp_json.get("score"), "raw": resp_json}
    return {"verdict": None, "confidence": None, "raw": resp_json}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({"ok": True, "service": "Reality Check AI"})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts multipart form-data:
      - file: image or short video (optional)
      - text: string (optional)
    Returns JSON with verdicts and the raw API outputs.
    """
    try:
        # basic input check
        text = request.form.get("text", "").strip()
        file = request.files.get("file")

        if not text and not file:
            return jsonify({"error": "No input provided. Send 'text' or upload a 'file'."}), 400

        # ---- TEXT path (Hugging Face) ----
        if text:
            if not HUGGINGFACE_API_KEY:
                return jsonify({"error": "Hugging Face key not configured (HUGGINGFACE_API_KEY)."}), 500

            hf_model = HF_TEXT_MODEL
            hf_url = f"https://api-inference.huggingface.co/models/{hf_model}"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            payload = {"inputs": text}

            resp = requests.post(hf_url, headers=headers, json=payload, timeout=30)
            try:
                j = resp.json()
            except Exception:
                return jsonify({"error": "Hugging Face returned invalid JSON", "status": resp.status_code, "text": resp.text}), 502

            normalized = normalize_hf_text(j)
            return jsonify({"type": "text", "verdict": normalized["verdict"], "confidence": normalized["confidence"], "raw": normalized["raw"]})

        # ---- FILE path (image/video) using Replicate ----
        if file:
            if not REPLICATE_API_TOKEN:
                return jsonify({"error": "Replicate API token not configured (REPLICATE_API_TOKEN)."}), 500

            # Read file bytes and upload to Replicate's uploads endpoint
            uploaded = None
            headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}

            # Use streaming upload (files parameter)
            files = {"file": (file.filename, file.stream, file.mimetype)}
            upload_resp = requests.post("https://api.replicate.com/v1/upload", headers=headers, files=files, timeout=60)

            if upload_resp.status_code not in (200, 201):
                # return upload failure details
                try:
                    detail = upload_resp.json()
                except Exception:
                    detail = upload_resp.text
                return jsonify({"error": "replicate_upload_failed", "status": upload_resp.status_code, "details": detail}), 502

            upload_json = upload_resp.json()
            image_url = upload_json.get("urls", {}).get("get")
            if not image_url:
                return jsonify({"error": "no_upload_url_returned", "details": upload_json}), 502

            # Choose model based on mimetype: image -> image model; video -> video model
            mimetype = file.mimetype or ""
            if mimetype.startswith("video/"):
                model_version = os.environ.get("REPLICATE_VIDEO_MODEL") or REPLICATE_VIDEO_MODEL
            else:
                model_version = os.environ.get("REPLICATE_IMAGE_MODEL") or REPLICATE_IMAGE_MODEL

            if not model_version:
                return jsonify({"error": "No model configured. Set REPLICATE_IMAGE_MODEL or REPLICATE_VIDEO_MODEL env var."}), 500

            # Create prediction
            prediction_payload = {"version": model_version, "input": {"image": image_url}}
            pred_resp = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=prediction_payload,
