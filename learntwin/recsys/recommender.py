from __future__ import annotations
from typing import List, Dict, Tuple, Optional, Iterable
from dataclasses import dataclass
import random
from learntwin.models.models_bkt import BKTModel

@dataclass(frozen=True)
class Item:
    item_id: str
    skill_id: str
    difficulty: float = 0.5

class Recommender:
    def __init__(self, bkt: BKTModel, catalog: Optional[Dict[str, Item]] = None, seed: Optional[int] = None):
        self.bkt = bkt
        self.catalog: Dict[str, Item] = catalog or {}
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def _candidate_pool(self, allow_items: Optional[Iterable[str]]) -> List[str]:
        if allow_items is None:
            return list(self.catalog.keys())
        # filter to existing items; drop Nones/empties/unknowns; unique while preserving order
        seen = set()
        pool: List[str] = []
        for x in allow_items:
            if not x or x not in self.catalog:
                continue
            if x not in seen:
                seen.add(x)
                pool.append(x)
        return pool

    def mastery_score(self, user_id: str, item: Item) -> float:
        # lower mastery = higher priority; return mastery for sorting ascending
        return self.bkt.get_mastery(user_id, item.skill_id)

    def next_items(self, user_id: str, k: int = 5, allow_items: Optional[List[str]] = None) -> List[str]:
        pool = self._candidate_pool(allow_items)
        if not pool or k <= 0:
            return []
        scored: List[Tuple[float, str]] = [
            (self.mastery_score(user_id, self.catalog[i]), i) for i in pool
        ]
        # deterministic order: sort by mastery asc, then by item_id asc as tiebreaker
        scored.sort(key=lambda t: (t[0], t[1]))
        return [i for _, i in scored[:k]]

# helper for convenience import path
def next_items(user_id: str, k: int, bkt: BKTModel, catalog: Dict[str, Item], seed: Optional[int] = None) -> List[str]:
    return Recommender(bkt, catalog, seed=seed).next_items(user_id, k)
