import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

VOLCANO_API_URL = "https://api.volcanoapi.com/v1/translate"
VOLCANO_API_KEY = "YOUR_VOLCANO_API_KEY"  # Replace with actual API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    target_language = request.form.get('target_language')

    if not text:
        return jsonify({"error": "Please enter text to translate"}), 400

    try:
        response = requests.post(
            VOLCANO_API_URL,
            headers={
                "Authorization": f"Bearer {VOLCANO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "target_language": target_language
            }
        )
        response.raise_for_status()
        translation = response.json()["translation"]
        return jsonify({"translation": translation})
    except requests.RequestException as e:
        return jsonify({"error": f"Translation API error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
