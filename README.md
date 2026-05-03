# AI Stock Market Predictor 🚀

## 🚀 Quick Start
1. Backend: `uvicorn backend.main:app --reload`
2. Frontend: `cd frontend && npm start`
3. Open http://localhost:3000

**Multi-Ticker**: Enter AAPL/TSLA/etc. App auto-prepares model via `/prepare/{ticker}` if needed.

## 🛠️ Development
```
# Prepare new ticker (10+ yrs data)
python src/data_pipeline.py NVDA

# APIs
curl http://localhost:8000/data/TSLA
curl -X POST http://localhost:8000/prepare/TSLA
curl -X POST http://localhost:8000/predict/ -d '{\"ticker\":\"TSLA\",\"days\":30}'
```

## 🏗️ Architecture
```
yfinance → data_pipeline.py → LSTM model → FastAPI → React Charts
PostgreSQL (Neon) for caching
```

## 📊 Features
- Real-time stock data & AI predictions (LSTM)
- Multi-ticker support (AAPL, TSLA, NVDA...)
- BUY/SELL signals
- Historical charts + future forecasts

## ☁️ Deployment
**Backend (Railway)**:
```
railway login
railway init  
railway up
# Add DATABASE_URL to vars
```

**Frontend (Vercel)**:
```
cd frontend
npm i -g vercel
vercel --prod
```

## 🔧 Config
- `.env`: DATABASE_URL (Neon Postgres)

## Tech Stack
- ML: TensorFlow/Keras LSTM
- Backend: FastAPI + SQLAlchemy + Neon Postgres
- Frontend: React + Chart.js
- Data: yfinance

**Live Demo**: http://localhost:3000

