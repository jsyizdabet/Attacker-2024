import pandas as pd
import numpy as np
import vnstock as vn

def calculate_portfolio_return(data):
    # Filter rows with signals to buy
    buy_signals = data[data['signal'] == 'Buy']

    # Initialize a dictionary to store purchase prices
    purchase_prices = {}

    # Calculate purchase prices for each stock
    for _, row in buy_signals.iterrows():
        ticker = row['ticker']
        price = row['price']
        if ticker not in purchase_prices:
            purchase_prices[ticker] = price

    # Filter rows with signals to sell
    sell_signals = data[data['signal'] == 'Sell']

    # Calculate selling prices and returns for each stock
    total_return = 0
    for _, row in sell_signals.iterrows():
        ticker = row['ticker']
        if ticker in purchase_prices:
            purchase_price = purchase_prices[ticker]
            selling_price = row['price']
            stock_return = (selling_price - purchase_price) / purchase_price
            total_return += stock_return

    return total_return

# Example usage:
# Assume 'data' is your DataFrame containing ticker, date, price, and signal columns
# Call the function to calculate the portfolio return
