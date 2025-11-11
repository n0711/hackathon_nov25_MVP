from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from learntwin import BKT, Recommender

app = FastAPI(title="Learntwin API", version="0.1.0")

# shared demo instances
bkt = BKT()
rec = Recommender(bkt=bkt)

class GetMasteryReq(BaseModel):
    user_id: str
    skill_id: str

class GetMasteryResp(BaseModel):
    user_id: str
    skill_id: str
    mastery: float

class Candidate(BaseModel):
    item_id: str
    skill_id: str

class NextItemsReq(BaseModel):
    user_id: str
    candidates: List[Candidate]
    k: int = 5

class NextItemsResp(BaseModel):
    user_id: str
    items: List[Dict[str, Any]]

@app.post("/api/get_mastery", response_model=GetMasteryResp)
def get_mastery(req: GetMasteryReq):
    m = bkt.get_mastery(req.user_id, req.skill_id)
    return {"user_id": req.user_id, "skill_id": req.skill_id, "mastery": float(m)}

@app.post("/api/update")
def update(user_id: str, skill_id: str, is_correct: bool):
    m = bkt.update(user_id, skill_id, is_correct)
    return {"user_id": user_id, "skill_id": skill_id, "mastery": float(m)}

@app.post("/api/next_items", response_model=NextItemsResp)
def next_items(req: NextItemsReq):
    items = rec.next_items(req.user_id, [c.dict() for c in req.candidates], k=req.k)
    return {"user_id": req.user_id, "items": items}