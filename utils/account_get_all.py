import requests
import os
import json
from dotenv import load_dotenv

# Load Broker Auth credentials from .env file
load_dotenv()
BROKER_AUTH = os.getenv("alpaca_broker_auth")

# Base URL for Broker API
BASE_URL = "https://broker-api.sandbox.alpaca.markets/v1/accounts"

# Headers for authentication
HEADERS = {
    "accept": "application/json",
    "authorization": BROKER_AUTH
}

def get_all_accounts(page=1, per_page=100):
    """
    Fetches all accounts from Alpaca Broker API.
    
    Args:
        page (int): Page number for paginated results.
        per_page (int): Number of accounts per page (max 100).
    
    Returns:
        list: List of accounts.
    """
    try:
        # Endpoint with pagination
        url = f"{BASE_URL}?page={page}&per_page={per_page}"
        
        # API request
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse JSON response
        accounts = response.json()
        return accounts
    except requests.exceptions.RequestException as e:
        print(f"Error fetching accounts: {e}")
        return []

# Fetch accounts
accounts = get_all_accounts(page=1, per_page=50)

# Extract account IDs
account_ids = [account['id'] for account in accounts]

# Ensure the "JSON" subdirectory exists, relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "JSON")
os.makedirs(output_dir, exist_ok=True)

# Save account IDs to the "JSON" directory
output_file = os.path.join(output_dir, "account_raw_ids.json")
with open(output_file, "w") as file:
    json.dump(account_ids, file, indent=4)

print(f"Account IDs saved to {output_file}")
