import requests
import os
from dotenv import load_dotenv
import json

# Load Broker API credentials from .env file
load_dotenv()

BROKER_AUTH = os.getenv("alpaca_broker_auth")

# Base URL for Broker API
BASE_URL = "https://broker-api.sandbox.alpaca.markets/v1/accounts"

# Headers for authentication
headers = {
    "accept": "application/json",
    "authorization": BROKER_AUTH
}

# Path to the account_raw_ids.json file in the JSON subdirectory
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "JSON", "account_raw_ids.json")

# Ensure the JSON file exists
if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
    exit(1)

# Load account IDs from the raw_account_ids.json file
with open(input_file, "r") as file:
    account_ids = json.load(file)

# Function to fetch account details
def get_account_details(account_id):
    url = f"{BASE_URL}/{account_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        account_details = response.json()
        return account_details
    else:
        print(f"Failed to fetch details for account {account_id}: {response.status_code} - {response.text}")
        return None

# Create a dictionary to store the final result
account_data = {}

# Process each account ID and store account ID and email (without the domain part)
for account_id in account_ids:
    account_details = get_account_details(account_id)
    
    if account_details:
        email = account_details.get("contact", {}).get("email_address")  # Extract email from contact
        if email:
            # Extract the part before the '@' symbol
            email_prefix = email.split('@')[0]
            account_data[email_prefix] = {
                "account_id": account_id,
                "email": email_prefix  # Use the email prefix without domain
            }
            print(f"Details for {email_prefix} saved")
        else:
            print(f"Email not found for account {account_id}")

# Path to save the output JSON file in the "JSON" subdirectory
output_file = os.path.join(script_dir, "JSON", "account_email.json")

# Ensure the "JSON" subdirectory exists
os.makedirs(os.path.join(script_dir, "JSON"), exist_ok=True)

# Save the account data to a single JSON file
with open(output_file, "w") as file:
    json.dump(account_data, file, indent=4)

print(f"All account details saved to {output_file}")
