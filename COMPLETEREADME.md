# LearnTwin - Complete Setup Guide

Real-time, privacy-first micro-feedback for any classroom. This guide will help you set up and run both the frontend and backend.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Verifying It Works](#verifying-it-works)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js)

To verify your installations:
```bash
python3 --version
node --version
npm --version
```

---

## Project Structure

```
hackathon_nov25_MVP/
├── backend/              # FastAPI backend
│   ├── app.py           # Main API application
│   ├── schemas.py       # Data validation schemas
│   ├── storage.py       # SQLite database operations
│   ├── models_bkt.py    # BKT models
│   ├── recommender.py   # Recommendation engine
│   ├── app.db           # SQLite database (created on first run)
│   └── check_db.py      # Database inspection tool
│
└── frontend/            # React + Vite frontend
    ├── src/
    │   ├── App.jsx      # Main app component
    │   ├── StudentView.jsx  # Student interface
    │   ├── DashboardView.jsx # Teacher dashboard
    │   └── api.js       # Backend API integration
    ├── package.json     # Node dependencies
    └── .env             # Environment configuration
```

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Python Dependencies
```bash
python3 -m pip install fastapi uvicorn pydantic
```

### 3. Verify Backend Configuration
The backend uses these default settings (can be customized via environment variables):
- **Port**: `8000`
- **API Key**: `devkey`
- **Database**: `app.db` (SQLite, created automatically)

---

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
The `.env` file should already be configured with:
```
VITE_API_URL=http://localhost:8000
VITE_API_KEY=devkey
```

If the file doesn't exist, create `frontend/.env` with the above content.

---

## Running the Application

### Step 1: Start the Backend Server

Open a terminal and run:
```bash
cd backend
python3 -m uvicorn app:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**Keep this terminal open** - the backend is now running.

### Step 2: Start the Frontend Server

Open a **new terminal** and run:
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v7.2.2  ready in XXX ms

➜  Local:   http://localhost:5174/
```

**Keep this terminal open** - the frontend is now running.

### Step 3: Open in Browser

Navigate to: **http://localhost:5174**

You should see the LearnTwin homepage with options for students and teachers.

---

## Verifying It Works

### Test 1: Check Backend is Running

In a new terminal:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok"}
```

### Test 2: Test Data Submission (Live Mode)

1. Open browser to: **http://localhost:5174**
2. Click **"Student Demo"**
3. Click **"Switch to Live Mode"**
4. Set confidence slider to any value (e.g., 4)
5. Click any signal button (e.g., "Got it ✅")
6. You should see a green confirmation message: "✅ Got it sent!"

### Test 3: Check Backend Received the Data

In the backend terminal, you should see:
```
INFO:     127.0.0.1:XXXXX - "POST /ingest/json HTTP/1.1" 200 OK
```

### Test 4: Verify Database Storage

```bash
cd backend
python3 check_db.py
```

Expected output:
```
Total records in database: X
============================================================

Recent records (most recent first):
------------------------------------------------------------

ID: X
  Class ID: 1234
  Student ID: XXXXXX
  Signals: Stuck=0, GotIt=1, Pause=0, Example=0
  Confidence: 8/10
  Time: 2025-11-12T16:00:15.046Z
```

### Test 5: Check Analytics API

```bash
curl -H "X-API-Key: devkey" http://localhost:8000/mastery/1234
```

Expected response:
```json
{
  "class_id": "1234",
  "population": 5,
  "rate_stuck": 0.2,
  "rate_got_it": 0.6,
  "rate_pause": 0.0,
  "rate_example": 0.2,
  "avg_confidence": 7.4,
  "last_timestamp": "2025-11-12T16:00:31.989Z"
}
```

### Test 6: Test Reflection Mode

1. In browser, switch to **"Reflection Mode"**
2. Enter a name: "Test Student"
3. Click signals multiple times:
   - Stuck: 2x
   - Got it: 3x
   - Pause: 1x
4. Set confidence: 4
5. Click **"Submit Reflection"**
6. You should see: "✅ Thank you! Your reflection has been submitted."

Check the database again:
```bash
cd backend
python3 check_db.py
```

You should see 6 new records (2 stuck + 3 got_it + 1 pause).

---

## API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

#### 1. Health Check
```bash
GET /health
```
Returns API status (no authentication required).

#### 2. Ingest Metrics
```bash
POST /ingest/json
Headers: X-API-Key: devkey
Content-Type: application/json

Body: [
  {
    "class_id": "c1",
    "student_id": 123,
    "stuck": 0,
    "got_it": 1,
    "pause": 0,
    "example": 0,
    "confidence": 7,
    "timestamp": "2025-11-12T15:00:00Z"
  }
]
```

Response:
```json
{
  "rows_ok": 1,
  "rows_skipped": 0,
  "errors": []
}
```

#### 3. Get Class Mastery
```bash
GET /mastery/{class_id}
Headers: X-API-Key: devkey
```

Response:
```json
{
  "class_id": "c1",
  "population": 100,
  "rate_stuck": 0.15,
  "rate_got_it": 0.65,
  "rate_pause": 0.10,
  "rate_example": 0.10,
  "avg_confidence": 7.8,
  "last_timestamp": "2025-11-12T16:00:00Z"
}
```

#### 4. Get Recommendations
```bash
GET /recommend/{class_id}
Headers: X-API-Key: devkey
```

Response:
```json
{
  "class_id": "c1",
  "focus": [],
  "note": "Recommender not yet implemented."
}
```

---

## Data Format

### Signal Types (Binary Flags)
Each metric record contains 4 binary flags (0 or 1):
- **stuck**: Student is stuck and needs help
- **got_it**: Student understands the concept
- **pause**: Student needs a break/slower pace
- **example**: Student wants an example

### Confidence Scale
- Frontend: 1-5 slider
- Backend: 1-10 scale (automatically converted: frontend × 2)

### Example JSON
```json
{
  "class_id": "c2",
  "student_id": 1,
  "stuck": 0,
  "got_it": 1,
  "pause": 0,
  "example": 0,
  "confidence": 8,
  "timestamp": "2025-11-12T14:55:30Z"
}
```

---

## Troubleshooting

### Backend won't start

**Problem**: Port 8000 already in use
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

**Problem**: ModuleNotFoundError
```bash
# Reinstall dependencies
cd backend
python3 -m pip install --upgrade fastapi uvicorn pydantic
```

### Frontend won't start

**Problem**: Port 5173/5174 already in use
- The frontend will automatically try the next available port
- Check the terminal output for the actual URL

**Problem**: Dependencies not installed
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors in Browser Console

If you see CORS errors:
1. Make sure backend is running with CORS middleware (already configured in `app.py`)
2. Check that `.env` file has correct `VITE_API_URL`
3. Restart both frontend and backend

### Data Not Appearing in Database

1. Check backend logs for errors
2. Verify API key matches:
   - Frontend `.env`: `VITE_API_KEY=devkey`
   - Backend `app.py`: `API_KEY = "devkey"`
3. Look for 401 Unauthorized errors in browser console

### Browser Shows "Failed to send signal"

1. Check backend is running: `curl http://localhost:8000/health`
2. Check frontend .env file exists with correct values
3. Check browser console for detailed error messages
4. Verify no firewall blocking localhost connections

---

## Stopping the Servers

To stop the servers, press **Ctrl+C** in each terminal window.

To stop them from running in the background:
```bash
# Find processes
# Windows:
tasklist | findstr "python\|node"

# Mac/Linux:
ps aux | grep "python\|node"

# Kill specific process
# Windows:
taskkill /PID <PID> /F

# Mac/Linux:
kill <PID>
```

---

## Database Management

### View All Data
```bash
cd backend
python3 check_db.py
```

### Query Database Directly
```bash
cd backend
sqlite3 app.db "SELECT * FROM metrics LIMIT 10;"
```

### Reset Database
```bash
cd backend
rm app.db
# Database will be recreated on next backend startup
```

### Export Data
```bash
cd backend
sqlite3 app.db ".mode csv" ".output metrics.csv" "SELECT * FROM metrics;"
```

---

## Next Steps

- **Customize session codes**: Modify frontend to use meaningful class IDs
- **Add authentication**: Implement proper user authentication
- **Deploy**: Host on cloud platform (Heroku, Railway, Vercel)
- **Analytics dashboard**: Build teacher dashboard with real-time charts
- **Recommendations**: Implement the recommendation engine in `recommender.py`

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs for error messages
3. Check browser console for frontend errors
4. Verify both servers are running on correct ports

---

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- SQLite (Database)
- Pydantic (Data validation)

**Frontend:**
- React 19
- Vite (Build tool)
- Vanilla CSS

---

**Last Updated**: November 2025
