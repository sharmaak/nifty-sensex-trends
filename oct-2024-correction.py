"""
Goal: Analyse stocks which were corrected least during October 2024 fall of
      Indian stock market. The Nifty fell about 8% without any bad economic
      news. Also, the global stocks markets did not show any correction during
      this period.

Outcome: Identify stocks which were least impacted during this phase. This
      would be an indicator of quality stocks.

Scope: We shall consider stocks which are part of the following indices:
         1. Nifty 100
         2. Nifty Midcap 100
         3. Nifty Smallcap 100

Author: Amit Kumar Sharma (https://x.com handle: @dadhee_wale_baba)
"""
import csv
import os
import time
from pprint import pprint

import requests
import yfinance as yf
from pandas import DataFrame


def percent(v1: float, v2: float) -> float:
    return round(float(100*(v2-v1)/v1), 2)


def process_stock(symbol, from_date, to_date) -> float:
        print(f"Processing {symbol} ...")
        # 1. Fetch candles
        df = yf.download(f'{symbol}.NS', interval='1d', period='3mo', progress=False)
        l = len(df)-1

        # 2. Calculate gain % between the two dates
        return percent(df['Close'].loc[from_date], df['Close'].loc[to_date]) if l >= 1 else -1



def download_nse_index_files(output_dir='downloads', failed_file='failed.txt'):
    """
    Downloads Nifty index constituents files from Nifty website and saves them.
    """
    urls = []
    names = [ '100', 'midcap100', 'smallcap100' ]

    for n in names:
        urls.append(f"https://nsearchives.nseindia.com/content/indices/ind_nifty{n}list.csv")

    # Send this header to ensure Nifty allows the request. It blocks if
    # User-Agent is not from a standard browser.
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1"
    }
    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the failed file in write mode
    with open(failed_file, 'w') as failed:
        for url in urls:
            try:
                print('Processing: ' + url)
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()  # Raise an HTTPError for bad responses

                # Extract the filename from the URL
                filename = os.path.join(output_dir, url.split('/')[-1])

                # Save the content to a file
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {url} to {filename}")

            except requests.RequestException as e:
                # Write the failed URL to the failed file
                failed.write(url + '\n')
                print(f"Failed to download {url}: {e}")

def get_index_name(clue: str):
    if clue == '100':
        result = 'Nifty 100'
    elif clue == 'midcap100':
        result = 'Nifty Midcap 100'
    elif clue == 'smallcap100':
        result = 'Nifty Smallcap 100'
    else:
        result = clue
    return result

def create_index_stocks_dict(folder='downloads'):
    index_stocks = {}

    # Iterate over all CSV files in the specified folder
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            filepath = os.path.join(folder, filename)

            # Read the CSV file
            with open(filepath, 'r') as file:
                reader = csv.DictReader(file)

                # Process each row in the file
                for row in reader:
                    symbol = row['Symbol']

                    # Append the filename to the list for the given symbol
                    index_name = get_index_name(filename.replace('ind_nifty', '').replace('list.csv', ''))
                    index_stocks.update({symbol: index_name})
    return index_stocks



if __name__=='__main__':
    # --- BEGIN: Date range to evaluate ---
    from_date = '2024-09-27 00:00:00'
    to_date = '2024-10-31 00:00:00'
    output_file = 'oct-2024-correction.xlsx'
    # --- END: Date range to evaluate ---

    download_nse_index_files()
    index_stocks = create_index_stocks_dict()
    print(f"Total {len(index_stocks)} stocks found")
    pprint(index_stocks)

    results = []
    start_time = time.time()
    for stock in index_stocks.keys():
        index_name = index_stocks[stock]
        gain_pct = process_stock(stock, from_date, to_date)
        results.append([index_name, stock, gain_pct])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time {elapsed_time/60: .2f} minutes.")

    # Create a dataframe
    df = DataFrame(data=results, columns=['Index', 'Symbol', 'Change %'])
    df.to_excel(output_file, index=False, engine='openpyxl')



