from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional, Tuple

# Public item type (internal annotations use ItemT to avoid shadowing the factory)
ItemT = Dict[str, Any]
Catalog = Dict[str, ItemT]

def Item(item_id: str, skill_id: str, p: float = 0.5) -> ItemT:
    """Factory used by tests/teammates: build a canonical item dict."""
    return {"item_id": str(item_id), "skill_id": str(skill_id), "p": float(p)}

class Recommender:
    """
    Mastery-first recommender:
      1) lower mastery first (asc)
      2) tie-break by item_id (asc)
    Candidates accepted as:
      - None           -> whole catalog
      - Iterable[str]  -> ids
      - Iterable[dict] -> rows with BOTH "item_id" and "skill_id"
    If any dict row is malformed, the batch is treated as malformed and returns [].
    """
    def __init__(self,
                 bkt: Optional[Any] = None,
                 catalog: Optional[Catalog] = None,
                 seed: Optional[int] = None) -> None:
        self.bkt: Optional[Any] = bkt
        self.catalog: Catalog = {}
        if catalog:
            for k, v in catalog.items():
                iid = str(k)
                obj: ItemT = dict(v) if isinstance(v, dict) else {"item_id": iid}
                obj.setdefault("item_id", iid)
                self.catalog[iid] = obj
        self._seed = seed  # API parity

    def _candidate_pool(self, candidates: Optional[Iterable[Any]]
                        ) -> Tuple[List[str], Dict[str, ItemT]]:
        objects: Catalog = dict(self.catalog)

        if candidates is None:
            return (sorted(objects.keys()), objects)

        # STRICT: any dict row missing required keys invalidates the batch
        for x in candidates:
            if isinstance(x, dict) and not ("item_id" in x and "skill_id" in x):
                return ([], objects)

        seen = set()
        pool: List[str] = []

        for x in candidates:
            if not x:
                continue
            if isinstance(x, str):
                iid = x
                objects.setdefault(iid, {"item_id": iid})
            elif isinstance(x, dict):  # guaranteed to have both keys
                iid = str(x["item_id"])
                if iid not in objects:
                    objects[iid] = dict(x)
                else:
                    merged = dict(objects[iid])
                    merged.update(x)
                    objects[iid] = merged
            else:
                continue

            if iid not in seen:
                seen.add(iid)
                pool.append(iid)

        pool.sort()
        return (pool, objects)

    def mastery_score(self, user_id: str, item_id: str) -> float:
        if self.bkt is not None and hasattr(self.bkt, "mastery_score"):
            try:
                return float(self.bkt.mastery_score(user_id, self.catalog.get(item_id, {"item_id": item_id})))
            except Exception:
                return 0.5
        return 0.5

    def next_items(self, user_id: str, candidates: Optional[Iterable[Any]] = None, k: int = 5
                   ) -> List[ItemT]:
        pool_ids, objects = self._candidate_pool(candidates)
        if not pool_ids or k <= 0:
            return []
        scored: List[tuple[float, str]] = [(self.mastery_score(user_id, iid), iid) for iid in pool_ids]
        scored.sort(key=lambda t: (t[0], t[1]))  # mastery asc, then id asc
        top_ids = [iid for _, iid in scored[:k]]
        return [dict(objects[iid]) for iid in top_ids]

# Convenience helper (public): return ids only
def next_items(user_id: str, k: int, bkt: Optional[Any] = None,
               catalog: Optional[Catalog] = None, seed: Optional[int] = None) -> List[str]:
    rec = Recommender(bkt=bkt, catalog=catalog, seed=seed)
    return [x["item_id"] for x in rec.next_items(user_id=user_id, k=k)]
