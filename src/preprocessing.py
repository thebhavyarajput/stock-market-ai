import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
from pathlib import Path

DATA_DIR = Path('data')
PROCESSED_DIR = DATA_DIR / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Sequence params
LOOK_BACK = 60

def preprocess_stock_data(ticker):
    raw_df = pd.read_csv(DATA_DIR / 'raw' / f'{ticker}.csv', index_col=0, parse_dates=True)
    data = raw_df['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(LOOK_BACK, len(scaled_data)):
        X.append(scaled_data[i-LOOK_BACK:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    np.save(PROCESSED_DIR / f'{ticker}_X.npy', X)
    np.save(PROCESSED_DIR / f'{ticker}_y.npy', y)
    np.save(PROCESSED_DIR / f'{ticker}_scaler.npy', scaler)
    print(f'Preprocessed data saved for {ticker}')

if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    preprocess_stock_data(ticker)
