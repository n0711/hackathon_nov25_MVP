📘 Pipes & Persistence – Backend API
🔧 Overview

This backend service provides the data pipeline for the Learntwin project.
It collects student learning metrics (in JSON), stores them in SQLite, and exposes analytics and recommendations via a REST API built with FastAPI.

🚀 Features
| Function | Endpoint | Description |
| --------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Ingest Data (JSON)** | `POST /ingest/json` | Uploads JSON learning metrics for one or more students. Each record gets timestamped automatically. |
| **Class Mastery Analytics** | `GET /mastery/{class_id}` | Returns average learning indicators for a given class (e.g., stuck, got_it, confidence). Supports optional date filters. |
| **Recommendations** | `GET /recommend/{class_id}` | Generates class-level learning recommendations based on mastery data (simple heuristic engine). |
| **Export Data (CSV)** | `GET /export/{class_id}` | Streams all class data as a downloadable CSV file (also supports date filters). |

🧱 Data Model

Each ingested record follows this structure:

{
"class_id": "c1",
"student_id": "42",
"stuck": 0,
"got_it": 1,
"pause": 0,
"example": 1,
"confidence": 8
}

Automatically, the backend adds:

"timestamp": "2025-11-12T10:30:00Z"

Stored in SQLite as:
Field Type Description
id INTEGER Auto ID
class_id TEXT Class identifier
student_id TEXT Student identifier
stuck, got_it, pause, example INTEGER (0/1) Learning interaction flags
confidence FLOAT 1–10 scale
ts TEXT UTC timestamp

⚙️ How to Run Locally

# 1️⃣ Create virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

# 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

# 3️⃣ Set API key (optional)
```
export API_KEY=devkey
```
# 4️⃣ Start the server
```
uvicorn app:app --reload
```
Server will be available at:

http://localhost:8000

🧪 Example Usage
Ingest data

```
curl -X POST http://localhost:8000/ingest/json

  -H "X-API-Key: devkey" \
  -H "Content-Type: application/json" \
  -d @test.json
```

Get mastery for a class

```
curl -H "X-API-Key: devkey" http://localhost:8000/mastery/c1
```

Get recommendations

```
curl -H "X-API-Key: devkey" http://localhost:8000/recommend/c1
```

Export data as CSV

```
curl -H "X-API-Key: devkey" -L http://localhost:8000/export/c1 -o c1_metrics.csv
```

🧠 How Recommendations Work

    A lightweight rules-based engine evaluates class mastery:

    High “stuck” or low “confidence” → recap session

    Low “examples” → add more guided examples

    High “pause” → add micro-breaks

    High “got_it” + high “confidence” → offer enrichment tasks

    Returns structured teaching recommendations with rationale and priority.

📂 Key Files
File Purpose
 app.py FastAPI routes and startup logic
 storage.py SQLite schema and database helpers
 schemas.py Pydantic models for validation & serialization
 recommendations.py Rule-based recommendation generator
 requirements.txt Python dependencies
🧩 Integration Notes

The /recommend/{class_id} endpoint is modular — it can later be replaced with an AI or ML-based recommendation module.

Data and logic are class-centric, not student-centric, to support aggregated insights.

Every upload updates class statistics and recommendations dynamically.

## Team & Roles

LearnTwin was created by:

- **Charalampos Nadiotis** – Project manager and team leader; integration & orchestration (connecting backend and frontend, deployment, documentation) and **design/implementation of the initial AI and learning-analytics algorithms** (rules, logic, and experiments behind the insights).
- **Andreas Lazarou** – Frontend developer (UI implementation, user flows, components, and integration with backend APIs).
- **Christos Paparistodimou** – Backend developer (API design, business logic, data handling, and integration points for analytics and future extensions).

Contributions from other developers and educators are welcome via pull requests.

## Attribution

LearnTwin is free and open-source software licensed under the [MIT License](./LICENSE).

LearnTwin was initiated by **Charalampos Nadiotis + colleagues**  
(**frontend:** Andreas Lazarou, **backend:** Christos Paparistodimou, **AI/analytics logic & integration:** Charalampos Nadiotis).

If you use LearnTwin in a product, research project, or deployment that is visible to end users,
we kindly ask (but do not legally require) that you include a small note such as:

> Powered by LearnTwin – https://github.com/n0711/hackathon_nov25_MVP

This helps the project grow, demonstrate its impact in education, and attract more contributors.

