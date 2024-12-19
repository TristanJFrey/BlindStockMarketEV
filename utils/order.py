import requests
import threading
import random
import os
from dotenv import load_dotenv
from utils.generate_ratios import generate_profit_ratios

load_dotenv()

# Constants for API credentials
API_KEY = os.getenv("alpaca_key")
SECRET_KEY = os.getenv("alpaca_secret")

# Alpaca API Endpoints
BASE_TRADE_URL = "https://data.alpaca.markets/v2/stocks"
BASE_ORDER_URL = "https://paper-api.alpaca.markets/v2/orders"

# Headers for Alpaca API
HEADERS = {
    "accept": "application/json",
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
}

def trade_thread(symbol, side, profit_ratios, qty=1):
    """
    Thread function to handle buy or sell trades.
    
    Args:
        symbol (str): Stock symbol.
        side (str): Trade side, either 'buy' or 'sell'.
        profit_ratios (list): List containing [buy_ratio, sell_ratio].
        qty (int): Quantity of stocks to trade. Defaults to 1.
    """
    try:
        # Get the latest trade price
        latest_trade_url = f"{BASE_TRADE_URL}/{symbol}/trades/latest"
        response = requests.get(latest_trade_url, headers=HEADERS)
        response.raise_for_status()
        latest_trade_data = response.json()
        entry_price = float(latest_trade_data['trade']['p'])

        # Calculate stop-loss and take-profit prices
        take_profit_distance = entry_price * profit_ratios[0]
        stop_loss_distance = entry_price * profit_ratios[1]

        if side == "buy":
            take_profit_price = round(entry_price + take_profit_distance, 2)
            stop_loss_price = round(entry_price - stop_loss_distance, 2)
        else:  # == "sell"
            take_profit_price = round(entry_price - take_profit_distance, 2)
            stop_loss_price = round(entry_price + stop_loss_distance, 2)

        # Check if stop loss or take profit are zero
        if stop_loss_price == 0.0 or take_profit_price == 0.0:
            raise ValueError(f"Stop loss or take profit cannot be zero for {symbol} ({side}).")

        print(f"Symbol: {symbol}, Side: {side}, Entry Price: {entry_price}")
        print(f"Stop Loss: {stop_loss_price}, Take Profit: {take_profit_price}")

        # Prepare the order payload with OCO parameters
        payload = {
            "side": side,
            "type": "market",  # Market order to execute immediately
            "time_in_force": "day",
            "symbol": symbol,
            "qty": str(qty),
            "stop_loss": {
                "stop_price": str(stop_loss_price),
                "limit_price": str(stop_loss_price),  # Optional, but recommended for stop-limit orders
            },
            "take_profit": {
                "limit_price": str(take_profit_price),
            }
        }

        # Submit the order
        response = requests.post(BASE_ORDER_URL, json=payload, headers=HEADERS)
        
        
        # print(f"\n -----------------------------------------------------------\n"
        #        f"Order Response for {symbol} ({side}): {response.text}")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error in {side} thread for {symbol}: {e}")

def create_threads(symbol, ratios, side):
    """
    Create and return threads for multiple profit ratios.
    
    Args:
        symbol (str): Stock symbol.
        ratios (list): List of profit ratios to use for trades.
        side (str): Trade side, either 'buy' or 'sell'.
        
    Returns:
        list: List of threading.Thread objects.
    """
    return [threading.Thread(target=trade_thread, args=(symbol, side, ratio)) for ratio in ratios]

def run_trading(symbol="NDAQ", profit_ratios_count=20):
    """
    Run the trading process by creating threads for buy or sell actions with random profit ratios.

    Args:
        symbol (str): The stock symbol to trade.
        profit_ratios_count (int): The number of profit ratios to generate for trading.
    """
    # Generate random profit ratios
    profit_ratios = generate_profit_ratios(profit_ratios_count)

    # Randomly decide trade direction (buy or sell)
    is_buy = random.choice([True, False])

    # Create threads based on the trade direction
    side = "buy" if is_buy else "sell"
    action = "Buy" if is_buy else "Sell"
    print(f"-------------------------\nExecuting {action} Threads...\n-------------------------")
    threads = create_threads(symbol, profit_ratios, side)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("-------------------------\nTrading completed.")

if __name__ == "__main__":
    run_trading()
