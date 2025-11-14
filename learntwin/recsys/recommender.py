from __future__ import annotations
from typing import List, Dict, Tuple
from dataclasses import dataclass
from learntwin.models.models_bkt import BKTModel
@dataclass
class Item:
    item_id: str
    skill_id: str
    difficulty: float = 0.5

class Recommender:
    def __init__(self, bkt: BKTModel, catalog: Dict[str, Item]):
        self.bkt = bkt
        self.catalog = catalog
    def score(self, user_id: str, item: Item) -> float:
        p = self.bkt.get_mastery(user_id, item.skill_id)
        return 1.0 - abs(p - 0.5)
    def next_items(self, user_id: str, k: int = 5, allow_items: List[str] | None = None) -> List[str]:
        pool = allow_items or list(self.catalog.keys())
        scored: List[Tuple[float, str]] = [(self.score(user_id, self.catalog[i]), i) for i in pool if i in self.catalog]
        scored.sort(reverse=True)
        return [i for _, i in scored[:k]] 

