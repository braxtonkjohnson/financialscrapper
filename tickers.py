import pandas as pd


# reads the CSV file with pandas
nyse_tickers = pd.read_csv("nasdaq_screener_1638812010252.csv")
# Isolates the ticker symbol in the Data Set
all_tickers = nyse_tickers["Symbol"]
# Adds all ticker symbols into a list in alphabetical order
pre_ticker_list = all_tickers.to_list()
tl = [ticker_list for ticker_list in pre_ticker_list if not '^' in ticker_list]