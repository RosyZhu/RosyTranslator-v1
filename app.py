import os
import logging
from flask import Flask, render_template, request, jsonify
from volcengine.maas import MaasService, MaasException

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

# Initialize MaasService
maas_service = MaasService('maas-api.ml-platform-cn-beijing.volces.com', VOLCANO_API_KEY, VOLCANO_API_SECRET)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')

    if not text:
        return jsonify({"error": "Please enter text to translate"}), 400

    if not VOLCANO_API_KEY or not VOLCANO_API_SECRET:
        logging.error("VOLCANO_API_KEY or VOLCANO_API_SECRET is not set in the environment variables")
        return jsonify({"error": "Translation service is not configured properly"}), 500

    try:
        response = maas_service.create_translation(
            model='translation',
            input_data={
                "text": text,
                "source_language": "en",
                "target_language": "zh"
            }
        )
        translation = response['result']['translation']
        logging.info(f"Successfully translated text: '{text}' to '{translation}'")
        return jsonify({"translation": translation})
    except MaasException as e:
        logging.error(f"Translation API error: {str(e)}")
        return jsonify({"error": "An error occurred during translation. Please try again later."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
