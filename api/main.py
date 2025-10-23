from flask import Flask, render_template, request, jsonify
import os
import requests
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure logging for debugging on Vercel
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Load environment tokens
        hf_token = os.getenv("HF_API_TOKEN")
        replicate_token = os.getenv("REPLICATE_API_TOKEN")

        if not hf_token:
            return jsonify({"error": "Missing HF_API_TOKEN in environment"}), 500

        # Query Hugging Face model
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {"inputs": f"Determine if this text seems AI-generated or human-written:\n\n{text}"}

        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-small",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            app.logger.error(f"Hugging Face API error: {response.text}")
            return jsonify({
                "error": "Hugging Face API call failed",
                "status_code": response.status_code,
                "details": response.text
            }), 500

        # Parse Hugging Face response safely
        try:
            result = response.json()
            output = (
                result[0]["generated_text"]
                if isinstance(result, list) and "generated_text" in result[0]
                else str(result)
            )
        except Exception as e:
            app.logger.error(f"Error parsing response: {e}")
            return jsonify({"error": "Invalid response from Hugging Face"}), 500

        return jsonify({"analysis": output})

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)