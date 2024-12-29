import os
from dotenv import load_dotenv
import requests
import account_get_all

# Load Broker API credentials from .env file
load_dotenv()

BROKER_AUTH = os.getenv("alpaca_broker_auth")

# Base URL for ACH relationships
BASE_URL = "https://broker-api.sandbox.alpaca.markets/v1/accounts"

# List of account IDs to process
account_ids = account_get_all.account_ids

# ACH relationship payload
payload = {
    "bank_account_type": "CHECKING",
    "account_owner_name": "Kind Archimedes",
    "bank_account_number": "32131231abc",
    "bank_routing_number": "123103716",
    "nickname": "Bank of America Checking"
}

# Headers for the request
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": BROKER_AUTH
}

def create_ach_relationship(account_id):
    """
    Creates an ACH relationship for a given account ID.

    Args:
        account_id (str): The account ID.

    Returns:
        str: Response text from the API.
    """
    url = f"{BASE_URL}/{account_id}/ach_relationships"
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error creating ACH relationship for account {account_id}: {e}"

# Process each account ID
for account_id in account_ids:
    print(f"Processing account ID: {account_id}")
    result = create_ach_relationship(account_id)
    print(result)
