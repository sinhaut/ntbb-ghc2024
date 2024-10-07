import csv
import sys

## Important filenames and constants
CURRENT_HOLDINGS_FILENAME = '/content/ntbb-ghc2024/data_files/holdings_current_eod_positions.csv'
PREVIOUS_HOLDINGS_FILENAME = '/content/ntbb-ghc2024/data_files/holdings_previous_eod_positions.csv'
TRANSACTIONS_FILENAME = '/content/ntbb-ghc2024/data_files/transactions.csv'
ROUNDING_DECIMAL = 2

"""
Name: load_holdings_portfolio
Returns: all_holdings (dict) - A map of security name to a map of its metadata (ticker, quantity, and price)
    Ex. all_holdings = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 2, 'price': 100}}
Parameters:
 'filename' (string) - the filename being processed

Note - this can load both the current and previous holdings portfolios into the same dictionary data structure
"""
def load_holdings_portfolio(filename):
    all_holdings = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # For each security, read the position and price
            security = row['SecurityName']
            ticker = row['Ticker']
            quantity = int(row['Quantity'])
            price = float(row['Price'])
            all_holdings[security] = {'ticker': ticker, 'quantity': quantity, 'price': price}
    return all_holdings

"""
Name: load_transactions_portfolio
Returns: all_transactions (dict) - A map of security name to a map of its metadata (ticker, quantity, price, action)
    Ex. all_transactions = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 2, 'price': 100, 'action': 'SELL'}}
Parameters:
 'filename' - a string, for the filename being processed

Note - the only difference between this and holdings portfolio is adding 'action'
"""
def load_transactions_portfolio(filename):
    all_transactions = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # For each security, read the position, price and transaction type
            security = row['SecurityName']
            ticker = row['Ticker']
            quantity = int(row['Quantity'])
            transaction_price = float(row['TransactionPrice'])
            transaction_type = row['Action']
            all_transactions[security] = {'ticker': ticker, 'quantity': quantity, 'price': transaction_price, 'action': transaction_type}
    return all_transactions

"""
Name: calculate_holdings_pnl
This function calculates the holdings_pnl for each security given a current and previous holdings portfolio.
Holdings PNL is only calculated for securities that exist in the previous portfolio.
This reperesents the market price difference between current eod and previous eod price.

Returns: holdings_pnl (dict) - A map of security name to its holding pnl value (int)
    Ex. holdings_pnl = {'Imaginary Company': -10}
Parameters:
 'current_holdings_portfolio' (dict) - a map of holdings data from the current date
 'previous_holdings_portfolio' (dict) - a map of holdings data from the previous date
"""
def calculate_holdings_pnl(current_holdings_portfolio, previous_holdings_portfolio):
    holdings_pnl = {}
    for security, current_position in current_holdings_portfolio.items():
        if security in previous_holdings_portfolio:
            previous_position = previous_holdings_portfolio[security]
            quantity = previous_position['quantity']
            current_price = current_position['price']
            previous_price = previous_position['price']
            holdings_pnl[security] = quantity * (current_price - previous_price)
    return holdings_pnl

"""
Name: calculate_transactions_pnl
This function calculates the transactions_pnl for each security given a transactions and current holdings portfolio.
Transactions PNL is only calculated for securities that exist in the current portfolio.
This reperesents the market price difference between the transaction price and the current eod price.

Returns: transactions_pnl (dict) - A map of security name to its transaction pnl value (int)
    Ex. transactions_pnl = {'Imaginary Company': -10}
Parameters:
 'all_transactions' (dict) - a map of transactions data for all securities
    Ex. all_transactions = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 2, 'price': 100, 'action': 'SELL'}}
 'current_holdings_portfolio' (dict) - a map of holdings data for all securities from the current date
    Ex. current_holdings_portfolio = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 1, 'price': 200}}
"""
def calculate_transactions_pnl(all_transactions, current_holdings_portfolio):
    transactions_pnl = {}
    for security, transaction in all_transactions.items():
        transaction_quantity = transaction['quantity']
        transaction_price = transaction['price']
        if security in current_holdings_portfolio:
            current_eod_price = current_holdings_portfolio[security]['price']
            if transaction['action'] == "SELL":
                transactions_pnl[security] = transaction_quantity * (transaction_price - current_eod_price)
            elif transaction['action'] == "BUY":
                transactions_pnl[security] = transaction_quantity * (current_eod_price - transaction_price)
            else:
                print(f"Transaction type: {transaction['action']} is not valid, it MUST be either SELL or BUY")
    return transactions_pnl

"""
Name: calculate_total_pnl
This function adds the holding and transaction pnl of each security if it exists.
If the security does not exist in either, the value used for that security is 0

Returns: total_pnl (dict) - A map of security name to its total pnl value (int)
Parameters:
 holdings_pnl (dict) - A map of security name to its holding pnl value (int)
 transactions_pnl (dict) - A map of security name to its transaction pnl value (int)
"""
def calculate_total_pnl(holdings_pnl, transactions_pnl):
    total_pnl = {}
    # Get the set of keys in both holdings and transactions
    all_securities = holdings_pnl.keys() | transactions_pnl.keys()
    for security in all_securities:
        total_pnl[security] = holdings_pnl.get(security, 0) + transactions_pnl.get(security, 0)
    return total_pnl

"""
Name: generate_report
This function prints the formatted PNL report to the console

Returns: nothing
Parameters:
 pnl (dict) - A map of security name to its pnl value (int)

Note - This can be used to print any PNL report (holdings/transactions/total)
"""
def generate_report(pnl):
    print('------------------------------------------------')
    str_fmt = "{:<30} {:<35}"
    print(str_fmt.format('Security','PNL'))
    print('------------------------------------------------')
    for security, gain_loss in pnl.items():
        print(str_fmt.format(security, round(gain_loss, ROUNDING_DECIMAL)))
    print('------------------------------------------------')

"""
Name: run_report
This function takes in a client_name and runs the necessary calculations and prints the output

Returns: nothing
Parameters:
 client_name (string) - Name of the client for which we want to create the report

Note
"""
def run_report(client_name):
    if client_name == 'Client_A':
        # Client A only wants the Holdings PNL Report
        print("Generating Holdings Profit & Loss Report for Client A\n") # debug string - can be removed
        current_holdings_portfolio = load_holdings_portfolio(CURRENT_HOLDINGS_FILENAME)
        previous_holdings_portfolio = load_holdings_portfolio(PREVIOUS_HOLDINGS_FILENAME)

        holdings_pnl = calculate_holdings_pnl(current_holdings_portfolio, previous_holdings_portfolio)
        generate_report(holdings_pnl)

    elif client_name == 'Client_B':
        # Client B only wants the Transactions PNL Report
        print("Generating Transactions Profit & Loss Report for Client B\n")
        current_holdings_portfolio = load_holdings_portfolio(CURRENT_HOLDINGS_FILENAME)
        all_transactions = load_transactions_portfolio(TRANSACTIONS_FILENAME)

        transactions_pnl = calculate_transactions_pnl(all_transactions, current_holdings_portfolio)
        generate_report(transactions_pnl)

    elif client_name == "Client_C":
        # Client C only wants the Total PNL Report
        print("Generating Total Profit & Loss Report for Client C\n")
        current_holdings_portfolio = load_holdings_portfolio(CURRENT_HOLDINGS_FILENAME)
        previous_holdings_portfolio = load_holdings_portfolio(PREVIOUS_HOLDINGS_FILENAME)
        all_transactions = load_transactions_portfolio(TRANSACTIONS_FILENAME)

        holdings_pnl = calculate_holdings_pnl(current_holdings_portfolio, previous_holdings_portfolio)
        transactions_pnl = calculate_transactions_pnl(all_transactions, current_holdings_portfolio)
        total_pnl = calculate_total_pnl(holdings_pnl, transactions_pnl)
        generate_report(total_pnl)

    else:
        # We should not reach this case in the provided code
        print("Invalid client provided! Exiting Program.")
        exit(1)

# DO NOT EDIT THE MAIN FUNCTION BELOW
if __name__ == "__main__":
    all_clients = ['Client_A', 'Client_B', 'Client_C']
    for client_name in all_clients:
        print('===========================================================')
        print(f'{client_name} PNL Report')
        run_report(client_name)
        print(f'\nFinished generating PNL Report for {client_name}\n')
