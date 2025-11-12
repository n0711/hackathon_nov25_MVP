from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List


app = FastAPI(title="Learntwin backend")

# Allow local dev frontends to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # for hackathon demo we allow everything
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Payload(BaseModel):
    data: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok"}


def _extract_mastery(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Try to find a mastery dict inside the incoming JSON.
    We look for a key called 'mastery' or any numeric-only dict.
    """
    if isinstance(data.get("mastery"), dict):
        return {
            k: float(v)
            for k, v in data["mastery"].items()
            if isinstance(v, (int, float))
        }

    for _, v in data.items():
        if isinstance(v, dict) and all(isinstance(val, (int, float)) for val in v.values()):
            return {kk: float(vv) for kk, vv in v.items()}

    return {}


@app.post("/recommend")
def recommend(payload: Payload):
    """
    Rule-based recommender for demo:
    - Find mastery dict
    - Sort ascending by mastery
    - Return up to 3 weakest topics as 'reinforce' recommendations
    """
    mastery = _extract_mastery(payload.data)

    if not mastery:
        return {
            "received_keys": list(payload.data.keys()),
            "recommendations": [],
            "message": "No mastery structure found in JSON; nothing to recommend.",
        }

    sorted_topics: List[tuple[str, float]] = sorted(mastery.items(), key=lambda kv: kv[1])
    weakest = sorted_topics[:3]

    recommendations = [
        {"topic": name, "mastery": score, "action": "reinforce"}
        for name, score in weakest
    ]

    return {
        "received_keys": list(payload.data.keys()),
        "mastery_topics": list(mastery.keys()),
        "recommendations": recommendations,
        "message": "Learntwin backend produced rule-based recommendations.",
    }
