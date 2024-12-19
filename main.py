import sys
from utils import order, close_orders, close_positions

def main():
    """
    Main function to execute specific modules based on command-line arguments.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <mode>")
        print("Modes:")
        print("  0 - Run orders.py for trading.")
        print("  1 - Run close_orders.py to cancel all orders.")
        print("  2 - Run close_positions.py to close all positions.")
        return

    try:
        mode = int(sys.argv[1])
        if mode == 0:
            print("Running orders.py for trading...")
            order.run_trading()
        elif mode == 1:
            print("Running close_orders.py to cancel all orders...")
            close_orders.delete_orders()
        elif mode == 2:
            print("Running close_positions.py to close all positions...")
            close_positions.delete_positions()
        else:
            print("Invalid mode. Please choose 0, 1, or 2.")
    except ValueError:
        print("Invalid input. Please provide a numerical argument (0, 1, or 2).")

if __name__ == "__main__":
    main()
