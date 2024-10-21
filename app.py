import os
import logging
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Set up logging
logging.basicConfig(level=logging.INFO)

VOLCANO_API_URL = "https://api.volcanoapi.com/v1/translate"
VOLCANO_API_KEY = os.environ.get("VOLCANO_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')

    if not text:
        return jsonify({"error": "Please enter text to translate"}), 400

    if not VOLCANO_API_KEY:
        logging.error("VOLCANO_API_KEY is not set in the environment variables")
        return jsonify({"error": "Translation service is not configured properly"}), 500

    try:
        response = requests.post(
            VOLCANO_API_URL,
            headers={
                "Authorization": f"Bearer {VOLCANO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "source_language": "en",
                "target_language": "zh"
            }
        )
        response.raise_for_status()
        translation = response.json()["translation"]
        logging.info(f"Successfully translated text: '{text}' to '{translation}'")
        return jsonify({"translation": translation})
    except requests.RequestException as e:
        logging.error(f"Translation API error: {str(e)}")
        return jsonify({"error": "An error occurred during translation. Please try again later."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
