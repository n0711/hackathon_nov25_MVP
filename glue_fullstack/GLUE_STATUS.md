# Glue Full-Stack Status (Learntwin)

## What Works
- Node.js backend (Express) running at: http://localhost:3000
- Static UI served from: glue_fullstack/backend/public/index.html
- One API endpoint: POST /api/mock
- End-to-end flow: UI or any client -> POST http://localhost:3000/api/mock -> JSON response.

## Sample Request (JSON)
{
  "learnerId": "demo-learner-2",
  "goal": "End-to-end sanity check",
  "notes": "Port 3000 fixed, server restarted"
}

## Sample Response Shape (JSON)
{
  "status": "ok",
  "source": "glue-backend-mock",
  "receivedInput": { "...": "echo of request" },
  "recommendation": "This is a MOCK response. Later this will call IBM / AI.",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}

## How to Run (for teammates)
1. Install Node.js (LTS).
2. From repo root: .\start_glue_fullstack.ps1
3. Browser opens at: http://localhost:3000
4. Frontend calls: POST http://localhost:3000/api/mock with JSON body.
