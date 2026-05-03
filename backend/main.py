from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from src.data_collection import fetch_stock_data
from src.predict import predict_future
import pandas as pd
from pathlib import Path
from .database import engine, get_db
from .models import Base, StockData, Prediction
from sqlalchemy.orm import Session
from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Stock Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Stock Prediction API"}

@app.get("/data/{ticker}")
def get_stock_data(ticker: str, db: Session = Depends(get_db)):
    try:
        # Check DB first
        stocks = db.query(StockData).filter(StockData.ticker == ticker).order_by(StockData.date.desc()).limit(30).all()
        if stocks:
            return [{"date": s.date.isoformat(), "open": float(s.open), "high": float(s.high), "low": float(s.low), "close": float(s.close), "volume": s.volume} for s in stocks]
        
        # Fallback to yfinance and save to DB
        df = fetch_stock_data(ticker, start="2019-01-01", end="2024-10-01")
        df_simple = df.droplevel(1, axis=1).tail(30).reset_index()
        
        # Save to DB
        for _, row in df_simple.iterrows():
            stock = StockData(
                ticker=ticker,
                date=row['Date'],
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=int(row['Volume'])
            )
            db.add(stock)
        db.commit()
        
        return df_simple.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PredictRequest(BaseModel):
    ticker: str
    days: int = 30

@app.post("/predict/")
def predict_stock(request: PredictRequest, db: Session = Depends(get_db)):
    try:
        preds = predict_future(request.ticker, request.days)
        
        # Save predictions to DB
        for i, pred_price in enumerate(preds):
            pred = Prediction(
                ticker=request.ticker,
                predicted_price=float(pred_price),
                predicted_date=pd.Timestamp.now() + pd.Timedelta(days=i+1)
            )
            db.add(pred)
        db.commit()
        
        return {"ticker": request.ticker, "predictions": [float(p) for p in preds]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prepare/{ticker}")
def prepare_model(ticker: str):
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "src/data_pipeline.py", ticker])
        return {"message": f"Model prepared for {ticker}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

