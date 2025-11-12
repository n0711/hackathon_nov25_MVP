# Learntwin — Demo Flow (Frozen)  — 2025-11-12T08:47:19+02:00

## One-line value prop
Upload a small, anonymized learning-activity CSV → get 3 concise insights + 2 suggested actions, offline-capable.

## Happy path (strict)
1) User opens the UI landing page (offline mode ON by default).
2) User selects a provided sample CSV from /fixtures (we ship 1 tiny file).
3) UI calls local gateway in offline mode → gateway serves precomputed JSON fixture.
4) UI renders: (a) summary KPIs, (b) “top 3 insights”, (c) “2 recommended actions”.
5) User clicks “Reset Demo” → state cleared, same flow repeatable.

## Non-goals (today)
- No auth, no multi-user, no live DB, no uploads to cloud.
- No file formats beyond the single CSV schema below.
- No advanced visualization beyond simple cards and one bar chart.

## Minimal input schema (CSV)
Columns (exact, case-sensitive):
student_id, activity, timestamp, score
- timestamp: ISO-8601
- score: 0..100 integer
We ship one tiny sample: 40–80 rows.

## Minimal output schema (JSON)
{
  "summary": { "n_students": int, "n_events": int, "mean_score": float },
  "insights": [
    {"title": "Engagement uptick on Wednesdays", "metric": "events_per_day", "change_pct": 12.5, "confidence": 0.82},
    {"title": "Low-score cluster in Module 3", "metric": "avg_score_m3", "delta": -8.1, "confidence": 0.77},
    {"title": "Late-night activity correlates with lower scores", "metric": "night_vs_day_delta", "delta": -5.4, "confidence": 0.71}
  ],
  "actions": [
    {"title": "Micro-recap for Module 3", "description": "Auto-push a 3-item recap before the next session."},
    {"title": "Nudge to night-owl cohort", "description": "Suggest daytime study blocks to affected students."}
  ],
  "meta": { "run_id": "offline-demo-001", "created_at": "ISO-8601", "version": "0.1.0" }
}

## Offline demo path (authoritative)
- Gateway returns fixture: /fixtures/offline_demo.json (exactly matching output schema).
- UI has a visible “Offline mode” badge; no network calls are made.
- A reset button/script clears state and reloads fixtures.

## Interfaces to lock next
- REST: POST /analyze (offline mode bypasses compute, returns fixture)
- CLI: .\scripts\analyze.ps1 -CsvPath .\fixtures\sample.csv -Offline
(REST or CLI is sufficient for the demo; we will keep both signatures consistent.)

## Risks we explicitly avoid today
- Live model training/inference online.
- Variable schemas from arbitrary datasets.
- Any feature that changes this flow.

-- End of frozen flow --
