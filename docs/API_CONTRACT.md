# Learntwin — API & CLI Contract — 2025-11-12T08:48:42+02:00

## REST (offline-ready)
- **Endpoint**: POST /analyze
- **URL**: http://localhost:5057/analyze (offline stub)
- **Headers**: Content-Type: application/json
- **Body**:
  {
    "csv_path": "string (optional when offline)",
    "offline": true
  }

### Request examples
1) Offline demo (preferred for Phase A):
   { "offline": true }

2) Online shape (reserved for Phase B+):
   { "csv_path": "relative/or/absolute/path/to/sample.csv", "offline": false }

### Response (200 OK, application/json)
{
  "summary": { "n_students": int, "n_events": int, "mean_score": float },
  "insights": [
    {"title": "string", "metric": "string", "change_pct|delta": number, "confidence": number (0..1)}
  ],
  "actions": [
    {"title": "string", "description": "string"}
  ],
  "meta": { "run_id": "string", "created_at": "ISO-8601", "version": "semver" }
}

### Error (4xx/5xx)
{ "error": "human-readable message", "meta": { "run_id": "string", "created_at": "ISO-8601" } }

## CLI
- **Command**: .\\scripts\\analyze.ps1 -CsvPath .\\fixtures\\sample.csv -Offline
- **Params**:
  -CsvPath  : path to CSV (optional in offline mode)
  -Offline  : switch; when present, returns fixture JSON directly
- **Output**: JSON to stdout (same schema as REST)

## Schema (frozen for Phase A)
- CSV columns: student_id, activity, timestamp (ISO-8601), score (0..100 int)
- JSON schema: see Response above; do not change field names.

## Non-goals in Phase A
- No authentication, streaming, pagination, or cloud storage.
- No schema auto-detection; only the single CSV shape above.
