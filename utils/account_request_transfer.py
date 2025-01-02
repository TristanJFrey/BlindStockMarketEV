import requests
import json
import os
from dotenv import load_dotenv

# Load Broker Auth credentials from .env file
load_dotenv()
BROKER_AUTH = os.getenv("alpaca_broker_auth")


# Load transfer request data from the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
transfer_request_file = os.path.join(script_dir, "JSON", "account_transfer_request.json")

# Ensure the JSON file exists
if not os.path.exists(transfer_request_file):
    print(f"Error: {transfer_request_file} not found!")
    exit(1)

# API endpoint
url = "https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}/transfers"

# Headers with proper authorization
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": BROKER_AUTH
}

# Function to initiate a transfer request
def initiate_transfer(account_id, amount, ach_id, account_email):
    payload = {
        "transfer_type": "ach",
        "direction": "INCOMING",
        "timing": "immediate",
        "amount": amount,
        "relationship_id": ach_id
    }
    
    # Construct the URL with the account_id
    transfer_url = url.format(account_id=account_id)

    # Send the POST request
    response = requests.post(transfer_url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Transfer successful for account {account_email}: ${amount}")
    else:
        print(f"Failed to initiate transfer for account {account_email}: {response.status_code}")
        print(response.text)
        print("----------------------")

# Load transfer requests from the JSON file
with open(transfer_request_file, "r") as file:
    transfer_requests = json.load(file)

# Iterate through the transfer requests and initiate the transfer for each
for email, transfer_details in transfer_requests.items():
    account_id = transfer_details.get("account_id")
    amount = transfer_details.get("amount")
    ach_id = transfer_details.get("ach_id")
    
    if account_id and amount and ach_id:
        initiate_transfer(account_id, amount, ach_id, email)
    else:
        print(f"Missing data for {email}. Skipping transfer.")
