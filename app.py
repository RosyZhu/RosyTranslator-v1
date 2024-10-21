import os
import logging
import json
from flask import Flask, render_template, request, jsonify
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Set up logging
logging.basicConfig(level=logging.INFO)

VOLCANO_API_KEY = os.environ.get("VOLCANO_API_KEY")
VOLCANO_API_SECRET = os.environ.get("VOLCANO_API_SECRET")

# Check if VOLCANO_API_KEY and VOLCANO_API_SECRET are set
if not VOLCANO_API_KEY or not VOLCANO_API_SECRET:
    logging.error("VOLCANO_API_KEY or VOLCANO_API_SECRET is not set in the environment variables")
else:
    logging.info("VOLCANO_API_KEY and VOLCANO_API_SECRET are properly set")

# Set up the service info and API info
k_service_info = ServiceInfo('translate.volcengineapi.com', {'Content-Type': 'application/json'}, Credentials(VOLCANO_API_KEY, VOLCANO_API_SECRET, 'translate', 'cn-north-1'), 5, 5)
k_query = {'Action': 'TranslateText', 'Version': '2020-06-01'}
k_api_info = {'translate': ApiInfo('POST', '/', k_query, {}, {})}
service = Service(k_service_info, k_api_info)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    if not text or not source_language or not target_language:
        return jsonify({"error": "Please provide text, source language, and target language"}), 400

    if not VOLCANO_API_KEY or not VOLCANO_API_SECRET:
        logging.error("VOLCANO_API_KEY or VOLCANO_API_SECRET is not set in the environment variables")
        return jsonify({"error": "Translation service is not configured properly"}), 500

    try:
        body = {
            'SourceLanguage': source_language,
            'TargetLanguage': target_language,
            'TextList': [text]
        }
        res = service.json('translate', {}, json.dumps(body))
        translation = json.loads(res)['TranslationList'][0]['Translation']
        logging.info(f"Successfully translated text from {source_language} to {target_language}: '{text}' to '{translation}'")
        return jsonify({"translation": translation})
    except Exception as e:
        logging.error(f"Translation API error: {str(e)}")
        return jsonify({"error": "An error occurred during translation. Please try again later."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
