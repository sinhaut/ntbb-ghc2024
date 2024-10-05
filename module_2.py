import csv
import sys


"""
Purpose:
The `run_report` function below calculates the holding pnl for a portfolio.

Goal 1:
This function does a number of tasks.
Break down this function into multiple functions that each have 1 purpose.
Think about naming - what do you want to call these new functions?

Goal 2:
Note that the run_report(client_name) function is the only one that is called but client_name is unused.
How can you handle various clients to get the correct report?

Goal 3:
Add a calculation for transaction_pnl and total_pnl using the function below:
 transaction_pnl = transaction_quantity * (eod_price - transaction_price) if action == BUY
 transaction_pnl = transaction_quantity * (transaction_price - eod_price) if action == SELL
 total_pnl = holdings_pnl + transaction_pnl
You can find the transactions files in the data folder to extract transaction_price and transaction
"""

CURRENT_HOLDINGS_FILENAME = '/content/ntbb-ghc2024/data_files/holdings_current_eod_positions.csv'
PREVIOUS_HOLDINGS_FILENAME = '/content/ntbb-ghc2024/data_files/holdings_previous_eod_positions.csv'
TRANSACTIONS_FILENAME = '/content/ntbb-ghc2024/data_files/transactions.csv'

ROUNDING_DECIMAL = 2 # keep any reusable constants at the top

def run_report(client_name):
    # Read position data from current and previous holdings files in corresponding dictionaries
    # Example entry current_holdings_portfolio = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 2, 'price': 100}}
    current_holdings_portfolio, previous_holdings_portfolio = {}, {}

    # Read from current holdings file
    with open(CURRENT_HOLDINGS_FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            security = row['SecurityName']
            ticker = row['Ticker']
            quantity = int(row['Quantity'])
            price = float(row['Price'])
            current_holdings_portfolio[security] = {'ticker': ticker, 'quantity': quantity, 'price': price}

    # Read from previous holdings file
    with open(PREVIOUS_HOLDINGS_FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # For each security, read the position and price
            security = row['SecurityName']
            ticker = row['Ticker']
            quantity = int(row['Quantity'])
            price = float(row['Price'])
            previous_holdings_portfolio[security] = {'ticker': ticker, 'quantity': quantity, 'price': price}

    # Calculate the holding PNL using the information from the holdings files
    # Example entry holdings_pnl = {'Imaginary Company':-10}
    holdings_pnl = {}
    for security, current_position in current_holdings_portfolio.items():
        if security in previous_holdings_portfolio:
            # assume holdings are not changed, calculate the gain or loss based on market price difference
            previous_position = previous_holdings_portfolio[security]
            quantity = previous_position['quantity']
            current_price = current_position['price']
            previous_price = previous_position['price']
            holdings_pnl[security] = quantity * (current_price - previous_price)

    # Print out the Profit and Loss Report to the console
    print('Holdings Profit and Loss Report:')
    str_fmt = "{:<30} {:<35}"
    print(str_fmt.format('Security','PNL'))
    for security, gain_loss in holdings_pnl.items():
        print(str_fmt.format(security, round(gain_loss, ROUNDING_DECIMAL)))

    # Hint: Add code to handle various clients. Pseudocode provided below: 
    # if client_name == 'Client_A': print holdings_pnl
    # if client_name == 'Client_B': print transactions_pnl
    # if client_name == 'Client_C': print total_pnl

# DO NOT EDIT THE MAIN FUNCTION BELOW
if __name__ == "__main__":
    all_clients = ['Client_A', 'Client_B', 'Client_C']
    for client_name in all_clients:
        print('=====================================================')
        print(f'Generating PNL Report for {client_name}')
        print('=====================================================\n')
        run_report(client_name)
        print(f'\nFinished generating PNL Report for {client_name}\n')
