from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Learntwin backend")

class Payload(BaseModel):
    data: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(payload: Payload):
    """
    Minimal placeholder recommender.
    Replace the body of this function with your real logic later.
    For now it just echoes which keys it received.
    """
    return {
        "received_keys": list(payload.data.keys()),
        "message": "Learntwin backend is running (placeholder logic)."
    }
