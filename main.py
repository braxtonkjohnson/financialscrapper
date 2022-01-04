import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
import lxml
from lxml import html
import requests

import tickers
from tickers import *

for stocks in tickers.tl:
    url = 'https://finance.yahoo.com/quote/' + stocks + '/cash-flow?p=' + stocks
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1',  # Do Not Track Request Header
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)
    (tree.xpath("//h1/text()"))
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.

    try:
        assert len(table_rows) > 0

        parsed_rows = []

        for table_row in table_rows:
            parsed_row = []
            el = table_row.xpath("./div")

            none_count = 0

            for rs in el:
                try:
                    (text,) = rs.xpath('.//span/text()[1]')
                    parsed_row.append(text)
                except ValueError:
                    parsed_row.append(np.NaN)
                    none_count += 1

            if (none_count < 4):
                parsed_rows.append(parsed_row)

        df = pd.DataFrame(parsed_rows)
        df = df.set_index(0)  # Set the index to the first column: 'Period Ending'.
        df = df.transpose()  # Transpose the DataFrame, so that our header contains the account names

        # Rename the "Breakdown" column to "Date"
        cols = list(df.columns)
        cols[0] = 'Date'
        df = df.set_axis(cols, axis='columns', inplace=False)
        numeric_columns = list(df.columns)[1::]  # Take all columns, except the first (which is the 'Date' column)

        for column_name in numeric_columns:
            df[column_name] = df[column_name].str.replace(',', '')  # Remove the thousands separator
            df[column_name] = df[column_name].astype(np.float64)  # Convert the column to float64

        try:
            ocf_column = df['Operating Cash Flow']
            ocf_row = ocf_column.iloc[0]
            cap_column = df['Capital Expenditure']
            cap_row = cap_column.iloc[0]
            owners_earnings = (ocf_row + cap_row)
            gr = df['Free Cash Flow']
            growth_sum = []
            for x in range (1,5):
                gr_row = gr.iloc[x]
                growth_sum.append(gr_row)
            growth_rate = sum(growth_sum)
            print(growth_sum)
            print(growth_rate)
            print(df)
            print(f"{stocks} - {owners_earnings}")
        except:
            print(f"NO DATA FOUND FOR {stocks}")

    except:
        continue







