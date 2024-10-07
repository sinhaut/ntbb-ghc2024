import unittest

"""
Purpose:
Identify bugs and fix the corresponding unit tests in this file for the function provided.

Section 1 contains the function to calculate the transactions PNL
Section 2 contains some unit tests to verify its functionality
"""

# Section 1
#######################################################################
# TODO: Find the bugs in the following code.                          #
# Look at transactions_module3.csv to see if we can process it.       #
#######################################################################

def calculate_transaction_pnl(all_transactions, current_holdings_portfolio):
    # transaction_pnl is a dictionary map from security to trasaction_pnl
    transaction_pnl = {}
    for security, transaction in all_transactions.items():
        transaction_quantity = transaction['quantity']
        transaction_price = transaction['price']
        transaction_ticker = transaction['ticker']
        if security in current_holdings_portfolio:
            current_position = current_holdings_portfolio[security]
            current_price = current_position['price']
            if transaction['action'] == "SELL":
                transaction_pnl[transaction_ticker] = transaction_quantity * (transaction_price - current_price)
            else:
                transaction_pnl[transaction_ticker] = transaction_quantity * (current_price - transaction_price)
    return transaction_pnl

# Section 2
"""
The following test class contains 3 unit tests.
Test 1 - Provided as an example to test the "SELL" action
Test 2 - This test will fail. Fix the code in calculate_transaction_pnl to make it pass.
Test 3 - This test will fail. Fix the code in calculate_transaction_pnl to make it pass.
"""
class TestModule3(unittest.TestCase):
  """
  Unit Test 1 - Test Transactions PNL with a SELL action
  Example Unit Test - Do not change this
  """
  def test_calculate_transaction_pnl_with_sell_action(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': 'SELL'} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    sell_action_calc = 5 * (2750.0 - 2800.0)
    expected_pnl = { 'BOP': -250.0} # answer from sell_action_calc
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl
    print("Passed Unit Test 1")

  """
  Unit Test 2 - Test Transactions PNL - handle input case sensitivity
  Update current_transactions to test the lower cased format input for action column
  If test fails, update calculate_transaction_pnl function to fix the test
  """
  def test_calculate_transaction_pnl_handle_case_sensitivity(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': 'sell'} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    sell_action_calc = 5 * (2750.0 - 2800.0)
    expected_pnl = { 'BOP': -250.0} # answer from sell_action_calc
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl
    print("Passed Unit Test 2")
    

  """
  Unit Test 3 - Test Transactions PNL - handle empty string input
  Update current_transactions and expected_pnl to test the empty input for action column
  If test fails, update calculate_transaction_pnl function to fix the test
  """
  def test_calculate_transaction_pnl_handle_empty_string(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': ''} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    sell_action_calc = 5 * (2750.0 - 2800.0)
    expected_pnl = {} # answer from sell_action_calc
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl
    print("Passed Unit Test 3")


if __name__ == '__main__':
  unittest.main()
