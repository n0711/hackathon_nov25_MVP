from __future__ import annotations
from learntwin import BKT, Recommender

def test_bkt_deterministic_seed():
    a = BKT(seed=42)
    b = BKT(seed=42)
    a.update("u1", "add", True)
    b.update("u1", "add", True)
    assert a.get_mastery("u1","add") == b.get_mastery("u1","add")

def test_recommender_deterministic_sort():
    rec = Recommender(seed=0)
    cands = [
        {"item_id":"i2","skill_id":"add"},
        {"item_id":"i1","skill_id":"add"},
        {"item_id":"i3","skill_id":"sub"},
    ]
    out = rec.next_items("u1", cands, k=2)
    assert [x["item_id"] for x in out] == ["i1","i2"]
