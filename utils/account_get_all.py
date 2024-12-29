import requests
import os
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

accounts = get_all_accounts(page=1, per_page=50)
print(f"Total accounts retrieved: {len(accounts)}")
for account in accounts:
    print(account)
