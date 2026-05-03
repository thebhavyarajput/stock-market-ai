import numpy as np
from tensorflow.keras.models import load_model
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

MODEL_DIR = Path('model')
DATA_DIR = Path('data/processed')

def predict_future(ticker, num_days=30):
    model = load_model(MODEL_DIR / f'stock_lstm_{ticker}.h5')
    scaler = np.load(DATA_DIR / f'{ticker}_scaler.npy', allow_pickle=True).item()
    
    # Load last 60 days
    X = np.load(DATA_DIR / f'{ticker}_X.npy')[-1].reshape(1, -1, 1)
    
    predictions = []
    current_X = X.copy()
    for _ in range(num_days):
        pred = model.predict(current_X, verbose=0)[0,0]
        predictions.append(pred)
        new_X = np.roll(current_X, -1, axis=1)
        new_X[0, -1, 0] = pred
        current_X = new_X
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1,1)).flatten().tolist()
    return predictions

if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    preds = predict_future(ticker)
    print(f'Next 30 days predictions for {ticker}: {preds[:5]}...')
