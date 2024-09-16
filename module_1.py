CURR_FILENAME = 'data_folder/portfolio_currdate'
PREV_FILENAME = 'data_folder/portfolio_prevdate'

"""
Parameters: 
  as_of_date - The current date used in a PNL calculation
  prev_date - The previous date used in a PNL calculation
"""
def run_report(as_of_date, prev_date):
  p1, p2 = {}, {}
  with open(CURR_FILENAME, 'r') as currPortfolioFile:
    reader = csv.DictReader(currPortfoliFile)
    for row in reader:
      s = row['SecurityName']
      t = row['Ticker']
      p1[s] = {'ticker':t}
  
