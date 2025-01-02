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

def get_ach_relationships(account_id):
    """
    Fetches ACH relationships for a given account ID.
    
    Args:
        account_id (str): The account ID.
    
    Returns:
        list: List of ACH relationship IDs.
    """
    try:
        # Endpoint for ACH relationships
        url = f"{BASE_URL}/{account_id}/ach_relationships"
        
        # API request
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        # Parse JSON response and extract ACH IDs
        relationships = response.json()
        return [relationship["id"] for relationship in relationships]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ACH relationships for account {account_id}: {e}")
        return []

# Load the existing account_email.json file
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "JSON", "account_email.json")

try:
    with open(input_file, "r") as file:
        account_email_data = json.load(file)
except FileNotFoundError:
    print(f"{input_file} not found. Please ensure the file exists.")
    exit()

# Loop through the entries in the account_email.json file
for email, account_data in account_email_data.items():
    account_id = account_data['account_id']
    
    # Fetch ACH relationships for the account
    ach_ids = get_ach_relationships(account_id)
    
    # Update the account data with the first ACH ID (if exists)
    account_data['ach_id'] = ach_ids[0] if ach_ids else None

# Save the updated account_email.json file with ACH IDs
output_file = os.path.join(script_dir, "JSON", "account_email_updated.json")
with open(output_file, "w") as file:
    json.dump(account_email_data, file, indent=4)

print(f"Updated account_email.json with ACH IDs. Saved to {output_file}")
