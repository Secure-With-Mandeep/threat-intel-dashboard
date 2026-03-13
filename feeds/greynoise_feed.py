import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GREYNOISE_API_KEY")
BASE_URL = "https://api.greynoise.io/v3"

HEADERS = {
    "key": API_KEY,
    "Accept": "application/json"
}

def quick_check(ip_address):
    """Quick check - is this IP noise or not?"""
    response = requests.get(
        f"{BASE_URL}/community/{ip_address}",
        headers=HEADERS
    )

    if response.status_code == 200:
        data = response.json()
        return {
            "ip": ip_address,
            "noise": data.get("noise", False),
            "riot": data.get("riot", False),
            "classification": data.get("classification", "unknown"),
            "message": data.get("message", ""),
            "source": "GreyNoise"
        }
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


if __name__ == "__main__":
    print("Testing GreyNoise connection...\n")

    result = quick_check("8.8.8.8")
    if result:
        print(f"IP: {result['ip']}")
        print(f"Noise: {result['noise']}")
        print(f"RIOT (known good): {result['riot']}")
        print(f"Classification: {result['classification']}")
        print(f"Message: {result['message']}")
        print("\n✅ GreyNoise connection successful!")
