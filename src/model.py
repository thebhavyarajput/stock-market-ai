import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from pathlib import Path

MODEL_DIR = Path('model')
MODEL_DIR.mkdir(exist_ok=True)

def create_lstm_model(input_shape):
    model = Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(50, return_sequences=True),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
    return model

def train_model(ticker, epochs=50, batch_size=32):
    X = np.load(f'data/processed/{ticker}_X.npy')
    y = np.load(f'data/processed/{ticker}_y.npy')
    
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    
    model_path = MODEL_DIR / f'stock_lstm_{ticker}.h5'
    model.save(model_path)
    print(f'Model saved to {model_path}')
    return model

if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    train_model(ticker)
