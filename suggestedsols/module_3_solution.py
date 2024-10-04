import unittest

# Section 1
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
            if not transaction['action']:
                continue
            if transaction['action'].upper() == "SELL":
                transaction_pnl[transaction_ticker] = transaction_quantity * (transaction_price - current_price)
            elif transaction['action'].upper() == "BUY":
                transaction_pnl[transaction_ticker] = transaction_quantity * (current_price - transaction_price)
    return transaction_pnl

# Section 2
class TestModule3(unittest.TestCase):

  """
  Unit Test 1 - Test Transactions PNL with a SELL action
  """
  def test_calculate_transaction_pnl_with_sell_action(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': 'SELL'} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    expected_pnl = { 'BOP': 5 * (2750.0 - 2800.0) # -250.0
    }
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl

  """
  Unit Test 2 - Test Transactions PNL - handle input case sensitivity
  """
  def test_calculate_transaction_pnl_handle_case_sensitivity(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': 'sell'} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    expected_pnl = { 'BOP': 5 * (2750.0 - 2800.0) # -250.0
    }
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl

  """
  Unit Test 3 - Test Transactions PNL - handle empty string input
  """
  def test_calculate_transaction_pnl_handle_empty_string(self):
    # given
    current_transactions = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2750.0, 'action': ""} }
    previous_portfolio = { 'Imaginary Company': {'ticker': 'BOP', 'quantity': 5, 'price': 2800.0} }
    expected_pnl = {}
    # when
    pnl = calculate_transaction_pnl(current_transactions, previous_portfolio)
    # then
    assert pnl == expected_pnl


if __name__ == '__main__':
  unittest.main()
