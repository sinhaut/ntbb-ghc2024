import csv
import sys

"""
Purpose:
The 'run_report' function below calculates the holding pnl for a portfolio.
Review the naming of variables in the function and update them using principles learned.

DATA FILES:
CURRENT_HOLDINGS - Holdings portfolio for end of day on today's date
PREVIOUS_HOLDINGS - Holdings portfolio for end of day on yesterday's date

FORMATTING:
The format for both holdings files is as follows:
SecurityName, Ticker, Quantity, Price

# SecurityName - the common name for the stock.
# Ticker       - an identifer for the stock.
# Quantity     - the num share of the stock you have in your portfolio at the end of the day.
# Price        - how much the stock is traded at at the end of the day.

IMPORTANT CALCULATIONS:
holdings_pnl = holding_quantity * (current_eod_price - previous_eod_price)
"""
##########################################################################################################
# TO DO: Please review the function below and replace all the improper variable names with better names. #
##########################################################################################################

CURRENT_HOLDINGS_FILENAME = 'data/holdings_current_eod_positions.csv'
PREVIOUS_HOLDINGS_FILENAME = 'data/holdings_previous_eod_positions.csv'

def run_report():
    # Read position data from current and previous holdings files in corresponding dictionaries
    # Example entry p1 = {'Imaginary Company': {'ticker': 'BOP', 'quantity': 2, 'price': 100}}
    p1, p2 = {}, {}

    # Read from current holdings file
    with open(CURRENT_HOLDINGS_FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = row['SecurityName']
            t = row['Ticker']
            q = int(row['Quantity'])
            price = float(row['Price'])
            p1[s] = {'ticker': t, 'quantity': q, 'price': price}

    # Read from previous holdings file
    with open(PREVIOUS_HOLDINGS_FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # For each security, read the quantity and price
            sec = row['SecurityName']
            ticker = row['Ticker']
            qty = int(row['Quantity'])
            price = float(row['Price'])
            p2[sec] = {'ticker': ticker, 'quantity': qty, 'price': price}

    # Calculate the holding PNL using the information from the holdings files
    # Example entry pnl = {'Imaginary Company':-10}
    pnl = {}
    for security, todayInfo in p1.items():
        if security in p2:
            # assume holdings are not changed, calculate the gain or loss based on market price difference
            yesterday_info = p2[security]
            pos = yesterday_info['quantity']
            price1 = todayInfo['price']
            price2 = yesterday_info['price']
            pnl[security] = pos * (price1- price2)

    # Print out the Profit and Loss Report to the console
    print('Holdings Profit and Loss Report:')
    str_fmt = "{:<30} {:<35}"
    print(str_fmt.format('Security','PNL'))
    for security, gain_loss in pnl.items():
        print(str_fmt.format(security, round(gain_loss, 2)))

# DO NOT EDIT THE MAIN FUNCTION BELOW
if __name__ == "__main__":
    print('Generating PNL Report...\n')
    run_report()
    print('\nFinished generating PNL Report for module_1.py')
