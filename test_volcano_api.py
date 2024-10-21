import os
import requests

VOLCANO_API_URL = "https://api.volcanoapi.com/v1/translate"
VOLCANO_API_KEY = os.environ.get("VOLCANO_API_KEY")

def test_volcano_api():
    if not VOLCANO_API_KEY:
        print("Error: VOLCANO_API_KEY is not set in the environment variables")
        return

    try:
        response = requests.post(
            VOLCANO_API_URL,
            headers={
                "Authorization": f"Bearer {VOLCANO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "text": "Hello, world!",
                "source_language": "en",
                "target_language": "zh"
            },
            timeout=10
        )
        response.raise_for_status()
        translation = response.json()["translation"]
        print(f"Successfully connected to Volcano API. Translation: {translation}")
    except requests.RequestException as e:
        print(f"Error connecting to Volcano API: {str(e)}")

if __name__ == "__main__":
    test_volcano_api()
