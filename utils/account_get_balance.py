import requests
import os
import json
from dotenv import load_dotenv

# Load Broker Auth credentials from .env file
load_dotenv()
BROKER_AUTH = os.getenv("alpaca_broker_auth")

# Base URL for Alpaca API
base_url = "https://broker-api.sandbox.alpaca.markets/v1/trading/accounts"

# Headers with proper authorization
headers = {
    "accept": "application/json",
    "authorization": BROKER_AUTH
}

# Path to the account_email_updated.json file in the JSON subdirectory
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, "JSON", "account_email_updated.json")

# Path to the account_transfer_request.json file in the JSON subdirectory
transfer_request_file = os.path.join(script_dir, "JSON", "account_transfer_request.json")

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: {json_file_path} not found!")
    exit(1)

# Function to request transfer for accounts below $50,000
def request_transfer(account_id, amount_needed, account_email, ach_id):
    """
    Create a transfer request record.

    Args:
        account_id (str): The ID of the account.
        amount_needed (float): The amount needed to reach $50,000.
        account_email (str): The email associated with the account.
    
    Returns:
        dict: The transfer request data.
    """
    transfer_request = {
        f"{account_email}": {
            "account_id": account_id,
            "email": account_email,
            "ach_id": ach_id,
            "amount": f"{amount_needed:.2f}"
        }
    }
    return transfer_request

# Function to process accounts and request transfers if necessary
def process_accounts(file_path):
    """
    Reads the JSON file, checks account balances, and requests transfers for accounts below $50,000.

    Args:
        file_path (str): Path to the JSON file containing account details.
    """
    try:
        # Load the JSON data
        with open(file_path, "r") as file:
            accounts_data = json.load(file)

        # Dictionary to store all transfer requests
        all_transfer_requests = {}

        for email, account_info in accounts_data.items():
            account_id = account_info.get("account_id")
            account_name = account_info.get("email", "Unknown Account")
            ach_id = account_info.get("ach_id")
            
            # Fetch account details from the API
            url = f"{base_url}/{account_id}/account"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                account_details = response.json()
                balance = float(account_details.get("balance", 0))
                if balance < 45000:
                    amount_needed = 45000 - balance
                    print(f"Account '{account_name}' ({account_id}) has ${balance:.2f}. Requesting ${amount_needed:.2f}.")
                    transfer_request = request_transfer(account_id, amount_needed, email, ach_id)
                    all_transfer_requests.update(transfer_request)
                else:
                    print(f"Account '{account_name}' ({account_id}) has sufficient funds: ${balance:.2f}.")
            else:
                print(f"Failed to fetch details for account {account_id}: {response.status_code}")
                print(response.text)

        # Write the transfer requests to a JSON file
        with open(transfer_request_file, "w") as file:
            json.dump(all_transfer_requests, file, indent=4)

        print(f"All transfer requests saved to {transfer_request_file}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    process_accounts(json_file_path)
