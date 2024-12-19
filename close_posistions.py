import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Constants for API credentials
API_KEY = os.getenv("alpaca_key")
SECRET_KEY = os.getenv("alpaca_secret")

# Common headers for Alpaca API
HEADERS = {
    "accept": "application/json",
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
}

def delete_positions():
    """
    Close all positions by sending a DELETE request to the positions endpoint.
    """
    positions_url = "https://paper-api.alpaca.markets/v2/positions"
    try:
        response = requests.delete(positions_url, headers=HEADERS)
        response.raise_for_status()
        print("Positions closed successfully:")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while closing positions: {e}")

if __name__ == "__main__":
    print("Closing all positions...")
    delete_positions()
