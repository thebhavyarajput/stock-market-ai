# Fix Backend Down - Complete Local Setup

## Current Status
✅ Project files correct, Neon DB ready
🔄 Setup virtualenv, deps, servers

## Step-by-Step Fix (Execute in order):

### 1. Verify .env [Pending]
Read .env - must contain:
```
DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```
**If missing/incomplete:** Replace `your_neon_db_url` below:
```bash
echo 'DATABASE_URL=your_neon_db_url_here' > .env
```

### 2. Backend Setup [Pending]
```bash
# Create/activate virtualenv (Mac/Linux)
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt
```

### 3. Start Backend Server [Pending]
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
✅ Success: See \"Uvicorn running on http://0.0.0.0:8000\"

### 4. Frontend Setup [Pending]
New terminal:
```bash
cd frontend
npm install
npm start
```
✅ Success: \"Local: http://localhost:3000\"

### 5. Test [Pending]
- Visit http://localhost:3000
- Enter AAPL → See chart + predictions
- No more \"backend down\"

## Troubleshooting
- DB error? Check .env DATABASE_URL format
- Port busy? Kill processes: `lsof -ti:8000 | xargs kill -9`
- Deps fail? `pip install --upgrade pip`

**Mark [✅] each step as completed!**
