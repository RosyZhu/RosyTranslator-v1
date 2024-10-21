import requests

def check_volcano_api_status():
    urls_to_check = [
        "https://volcanoapi.com",
        "https://docs.volcanoapi.com",
        "https://status.volcanoapi.com"
    ]
    
    for url in urls_to_check:
        try:
            response = requests.get(url, timeout=10)
            print(f"Status for {url}: {response.status_code}")
            if response.status_code == 200:
                print(f"Successfully connected to {url}")
                return True
        except requests.RequestException as e:
            print(f"Error connecting to {url}: {str(e)}")
    
    return False

if __name__ == "__main__":
    if check_volcano_api_status():
        print("Volcano API or related pages are accessible.")
    else:
        print("Unable to connect to any Volcano API related pages. The service might be down or inaccessible from this environment.")
