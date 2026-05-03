import sys
import yfinance as yf
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
# Inline imports - run from project root
import sys
sys.path.insert(0, '.')
from data_collection import fetch_stock_data
from preprocessing import preprocess_stock_data

DATA_DIR = Path('data/processed')
MODEL_DIR = Path('model')
DATA_DIR.mkdir(exist_ok=True, parents=True)
MODEL_DIR.mkdir(exist_ok=True, parents=True)

def create_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=True),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def data_pipeline(ticker):
    print(f"Starting pipeline for {ticker}...")
    
    # 1. Fetch data
    df = fetch_stock_data(ticker, start="2014-01-01", end="2024-10-01")
    df = df['Close'].dropna()  # Simplify to Close price
    
    # 2. Preprocess
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df.values.reshape(-1,1))
    
    # Create sequences (60 days lookback)
    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Save processed
    np.save(DATA_DIR / f'{ticker}_X.npy', X)
    np.save(DATA_DIR / f'{ticker}_y.npy', y)
    np.save(DATA_DIR / f'{ticker}_scaler.npy', scaler)
    
    # 3. Train model
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.1, verbose=1)
    
    # Save model
    model.save(MODEL_DIR / f'stock_lstm_{ticker}.h5')
    
    print(f"Pipeline complete for {ticker}! Files saved.")
    return model, scaler

if __name__ == '__main__':
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    data_pipeline(ticker)

