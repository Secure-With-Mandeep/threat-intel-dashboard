import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
BASE_URL = "https://api.abuseipdb.com/api/v2"

def check_ip(ip_address):
    """Check a single IP against AbuseIPDB"""
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90,
        "verbose": True
    }

    response = requests.get(
        f"{BASE_URL}/check",
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error: {response.status_code}")
        return None

def get_blacklist(limit=100):
    """Pull top blacklisted IPs"""
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "confidenceMinimum": 90,
        "limit": limit
    }

    response = requests.get(
        f"{BASE_URL}/blacklist",
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    # Quick test
    print("Testing AbuseIPDB connection...\n")

    result = check_ip("8.8.8.8")
    if result:
        print(f"IP: {result['ipAddress']}")
        print(f"Abuse Score: {result['abuseConfidenceScore']}")
        print(f"Country: {result['countryCode']}")
        print(f"Total Reports: {result['totalReports']}")
        print("\n✅ AbuseIPDB connection successful!")
       
