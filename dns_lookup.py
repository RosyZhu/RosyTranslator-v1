import socket
import requests

def dns_lookup(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"The IP address of {domain} is: {ip_address}")
        return ip_address
    except socket.gaierror:
        print(f"Unable to resolve the domain: {domain}")
        return None

def check_api_connection(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"Connection to {url} successful. Status code: {response.status_code}")
        return True
    except requests.RequestException as e:
        print(f"Error connecting to {url}: {str(e)}")
        return False

if __name__ == "__main__":
    domain = "api.volcanoapi.com"
    ip_address = dns_lookup(domain)
    
    if ip_address:
        print("Attempting to connect to the API using the resolved IP...")
        check_api_connection(f"https://{ip_address}")
    else:
        print("Attempting to connect to the API using the domain name...")
        check_api_connection(f"https://{domain}")
    
    print("\nTrying alternative DNS servers...")
    alt_dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    for dns_server in alt_dns_servers:
        try:
            resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver.settimeout(5)
            resolver.connect((dns_server, 53))
            resolver.send(b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03api\x0avolcanoapi\x03com\x00\x00\x01\x00\x01')
            data = resolver.recv(1024)
            if data:
                print(f"Successfully resolved using DNS server {dns_server}")
                check_api_connection(f"https://{domain}")
                break
        except Exception as e:
            print(f"Failed to resolve using DNS server {dns_server}: {str(e)}")
        finally:
            resolver.close()
