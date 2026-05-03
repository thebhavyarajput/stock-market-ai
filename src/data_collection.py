import pandas as pd
import requests
import os
from pathlib import Path

DATA_DIR = Path('src/data/raw')
DATA_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = "3ab56217f71cc47203ea11d79000430f"

def fetch_stock_data(ticker, start="2014-01-01", end="2026-12-31"):
    url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={ticker}&limit=10000"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from MarketStack: {response.text}")
    
    data = response.json()
    if 'data' not in data:
        raise Exception(f"Marketstack API error: {data}")
    
    records = []
    for row in data['data']:
        records.append({
            'Date': row['date'][:10],
            'Open': row['open'],
            'High': row['high'],
            'Low': row['low'],
            'Close': row['close'],
            'Volume': row['volume']
        })
    df = pd.DataFrame(records)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        # Marketstack returns descending date default. Sort to ascending.
        df.sort_values('Date', inplace=True)
        df.set_index('Date', inplace=True)
        # Replicate yfinance multi-index column format to maintain pipeline compatibility
        df.columns = pd.MultiIndex.from_product([df.columns, [ticker]])
    
    filepath = DATA_DIR / f'{ticker}.csv'
    df.to_csv(filepath)
    print(f'Data saved to {filepath} ({len(df)} rows)')
    return df

if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    fetch_stock_data(ticker)
