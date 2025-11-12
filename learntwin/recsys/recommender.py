from __future__ import annotations
from typing import List, Dict, Tuple, Optional, Iterable
from dataclasses import dataclass
import random
from learntwin.models.models_bkt import BKTModel, BKTParams

@dataclass(frozen=True)
class Item:
    item_id: str
    skill_id: str
    difficulty: float = 0.5

class Recommender:
    def __init__(
        self,
        bkt: Optional[BKTModel] = None,
        catalog: Optional[Dict[str, Item]] = None,
        seed: Optional[int] = None,
    ):
        # allow tests to instantiate without passing BKT explicitly
        self.bkt = bkt or BKTModel(BKTParams())
        self.catalog: Dict[str, Item] = catalog or {}
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def _candidate_pool(self, candidates: Optional[Iterable[str]]) -> List[str]:
        if candidates is None:
            return list(self.catalog.keys())
        seen = set()
        pool: List[str] = []
        for x in candidates:
            if not x or x not in self.catalog:
                continue
            if x not in seen:
                seen.add(x)
                pool.append(x)
        return pool

    def mastery_score(self, user_id: str, item: Item) -> float:
        # lower mastery ? recommend earlier
        return self.bkt.get_mastery(user_id, item.skill_id)

    # NOTE: signature ordered to avoid "multiple values for argument 'k'"
    def next_items(
        self,
        user_id: str,
        candidates: Optional[List[str]] = None,
        k: int = 5,
        **kwargs,
    ) -> List[str]:
        # accept alias allow_items= for back-compat
        if candidates is None and "allow_items" in kwargs and kwargs["allow_items"] is not None:
            candidates = kwargs["allow_items"]

        pool = self._candidate_pool(candidates)
        if not pool or k <= 0:
            return []

        scored: List[Tuple[float, str]] = [
            (self.mastery_score(user_id, self.catalog[i]), i) for i in pool
        ]
        # deterministic: sort by mastery asc, then item_id asc
        scored.sort(key=lambda t: (t[0], t[1]))
        return [i for _, i in scored[:k]]

# helper for convenience import path
def next_items(user_id: str, k: int, bkt: Optional[BKTModel] = None, catalog: Optional[Dict[str, Item]] = None, seed: Optional[int] = None) -> List[str]:
    return Recommender(bkt=bkt, catalog=catalog, seed=seed).next_items(user_id, k=k)
