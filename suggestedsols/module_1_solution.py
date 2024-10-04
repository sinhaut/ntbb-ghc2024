import csv
import sys

"""
Suggested solutions for module_1.py
"""
CURRENT_HOLDINGS_FILENAME = 'bloomberg/pnl_calc/data/holdings_current_eod_positions.csv'
PREVIOUS_HOLDINGS_FILENAME = 'bloomberg/pnl_calc/data/holdings_previous_eod_positions.csv'
ROUNDING_DECIMAL = 2 # keep any reusable constants at the top

def run_report():
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


# DO NOT EDIT THE MAIN FUNCTION BELOW
if __name__ == "__main__":
    print('Generating PNL Report...\n')
    run_report()
    print('\nFinished generating PNL Report for module_1.py')
