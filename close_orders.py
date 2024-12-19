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

def delete_orders():
    """
    Cancel all orders by sending a DELETE request to the orders endpoint.
    """
    orders_url = "https://paper-api.alpaca.markets/v2/orders"
    try:
        response = requests.delete(orders_url, headers=HEADERS)
        response.raise_for_status()
        print("Orders canceled successfully:")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while canceling orders: {e}")

if __name__ == "__main__":
    print("Canceling all orders...")
    delete_orders()
