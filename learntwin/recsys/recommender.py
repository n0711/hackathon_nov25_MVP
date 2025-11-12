from __future__ import annotations
from typing import List, Dict, Tuple, Optional, Iterable, Union
from dataclasses import dataclass
import random
from learntwin.models.models_bkt import BKTModel, BKTParams

@dataclass(frozen=True)
class Item:
    item_id: str
    skill_id: str
    difficulty: float = 0.5

Candidate = Union[str, Dict[str, str]]

class Recommender:
    def __init__(
        self,
        bkt: Optional[BKTModel] = None,
        catalog: Optional[Dict[str, Item]] = None,
        seed: Optional[int] = None,
    ):
        self.bkt = bkt or BKTModel(BKTParams())
        self.catalog: Dict[str, Item] = catalog or {}
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def _parse_candidates(self, candidates: Optional[Iterable[Candidate]]) -> Tuple[List[str], Dict[str, Item]]:
        """
        Returns (pool_ids, extra_items) where:
          - pool_ids: validated item_ids to consider
          - extra_items: ephemeral Items built from dict candidates not in self.catalog
        Malformed rows (missing item_id/skill_id) are dropped.
        """
        if candidates is None:
            return list(self.catalog.keys()), {}

        seen: set[str] = set()
        pool: List[str] = []
        extra: Dict[str, Item] = {}

        for x in candidates:
            item_id: Optional[str] = None
            skill_id: Optional[str] = None

            if isinstance(x, str):
                item_id = x
                # if item_id is unknown AND no skill supplied, we just skip it below
            elif isinstance(x, dict):
                item_id = x.get("item_id")
                skill_id = x.get("skill_id")
            else:
                continue  # unsupported type

            if not item_id:
                continue

            # If not in base catalog and we have a skill_id, create ephemeral Item
            if item_id not in self.catalog and skill_id:
                extra[item_id] = Item(item_id=item_id, skill_id=skill_id, difficulty=0.5)

            # accept only once
            if item_id not in seen and (item_id in self.catalog or item_id in extra):
                seen.add(item_id)
                pool.append(item_id)

        return pool, extra

    def mastery_score(self, user_id: str, item: Item) -> float:
        # lower mastery ? recommend earlier
        return self.bkt.get_mastery(user_id, item.skill_id)

    def next_items(
        self,
        user_id: str,
        candidates: Optional[List[Candidate]] = None,
        k: int = 5,
        **kwargs,
    ) -> List[str]:
        # allow alias allow_items=
        if candidates is None and "allow_items" in kwargs and kwargs["allow_items"] is not None:
            candidates = kwargs["allow_items"]

        pool, extra = self._parse_candidates(candidates)
        if not pool or k <= 0:
            return []

        # build a local view of the catalog (do not mutate self.catalog)
        local_catalog: Dict[str, Item] = dict(self.catalog)
        if extra:
            local_catalog.update(extra)

        scored: List[Tuple[float, str]] = [
            (self.mastery_score(user_id, local_catalog[i]), i) for i in pool
        ]
        # deterministic: sort by mastery asc, then item_id asc
        scored.sort(key=lambda t: (t[0], t[1]))
        return [i for _, i in scored[:k]]

def next_items(user_id: str, k: int, bkt: Optional[BKTModel] = None, catalog: Optional[Dict[str, Item]] = None, seed: Optional[int] = None) -> List[str]:
    return Recommender(bkt=bkt, catalog=catalog, seed=seed).next_items(user_id, k=k)
