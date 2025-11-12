from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional, Tuple

Item = Dict[str, Any]
__all__ = ["Recommender", "Item", "next_items"]

# Import BKT model from this package (with safe fallbacks)
try:
    from ..models_bkt import BKTModel  # preferred (package-relative)
except Exception:  # pragma: no cover
    try:
        from learntwin.models_bkt import BKTModel  # absolute fallback
    except Exception:  # pragma: no cover
        BKTModel = object  # type: ignore

ItemObj = Dict[str, Any]
Catalog = Dict[str, ItemObj]

class Recommender:
    """Rank by lowest mastery first, tie-break by item_id (deterministic)."""

    def __init__(
        self,
        bkt: Optional[BKTModel] = None,
        catalog: Optional[Catalog] = None,
        seed: Optional[int] = None,  # accepted for determinism parity
    ) -> None:
        self.bkt: Optional[BKTModel] = bkt
        self.catalog: Catalog = {}
        if catalog:
            for k, v in catalog.items():
                if isinstance(v, dict):
                    obj = dict(v)
                    obj["item_id"] = obj.get("item_id", k)
                else:
                    obj = {"item_id": k}
                self.catalog[obj["item_id"]] = obj
        self._seed = seed

    def _candidate_pool(
        self, candidates: Optional[Iterable[Any]]
    ) -> Tuple[List[str], Dict[str, ItemObj]]:
        """Return (list_of_ids, id->object). Accepts str or dict candidates; skips malformed."""
        id_to_obj: Dict[str, ItemObj] = {}
        pool: List[str] = []
        seen = set()

        if candidates is None:
            for iid, obj in self.catalog.items():
                if iid in seen:
                    continue
                seen.add(iid)
                pool.append(iid)
                id_to_obj[iid] = obj if isinstance(obj, dict) else {"item_id": iid}
            return pool, id_to_obj

        for x in candidates:
            if isinstance(x, str):
                iid = x
                if not iid or iid in seen:
                    continue
                seen.add(iid)
                pool.append(iid)
                base = self.catalog.get(iid, {})
                obj: ItemObj = base if isinstance(base, dict) else {}
                if "item_id" not in obj:
                    obj = {"item_id": iid, **obj}
                id_to_obj[iid] = obj
                continue

            if isinstance(x, dict):
                iid = x.get("item_id")
                if not isinstance(iid, str) or not iid or iid in seen:
                    continue
                seen.add(iid)
                pool.append(iid)
                base = self.catalog.get(iid, {})
                base_obj: ItemObj = base if isinstance(base, dict) else {}
                obj = {**base_obj, **x, "item_id": iid}
                id_to_obj[iid] = obj
                continue
            # else skip malformed

        return pool, id_to_obj

    def mastery_score(self, user_id: str, skill_or_item: str) -> float:
        """Return mastery in [0,1]; use BKT if available, else 0.5."""
        skill = skill_or_item
        obj = self.catalog.get(skill_or_item)
        if isinstance(obj, dict) and isinstance(obj.get("skill_id"), str):
            skill = obj["skill_id"]

        if self.bkt is None:
            return 0.5

        try:
            if hasattr(self.bkt, "get_mastery"):
                return float(self.bkt.get_mastery(user_id, skill))  # type: ignore
            if hasattr(self.bkt, "mastery"):
                return float(self.bkt.mastery(user_id, skill))  # type: ignore
            if hasattr(self.bkt, "estimate"):
                return float(self.bkt.estimate(user_id, skill))  # type: ignore
        except Exception:
            return 0.5
        return 0.5

    def next_items(
        self,
        user_id: str,
        candidates: Optional[Iterable[Any]] = None,
        k: int = 5,
    ) -> List[ItemObj]:
        """Return top-k as list[dict] with at least {"item_id": ...}."""
        pool, id_to_obj = self._candidate_pool(candidates)

        def score(iid: str) -> float:
            try:
                return self.mastery_score(user_id, iid)
            except Exception:
                return 0.5

        scored = sorted(((score(i), i) for i in pool), key=lambda t: (t[0], t[1]))
        top_ids = [i for _, i in scored[:k]]

        out: List[ItemObj] = []
        for iid in top_ids:
            obj = id_to_obj.get(iid)
            if not isinstance(obj, dict):
                obj = {"item_id": iid}
            out.append(obj)
        return out

def next_items(
    user_id: str,
    k: int,
    bkt: Optional[BKTModel] = None,
    catalog: Optional[Catalog] = None,
    candidates: Optional[Iterable[Any]] = None,
    seed: Optional[int] = None,
) -> List[ItemObj]:
    return Recommender(bkt=bkt, catalog=catalog, seed=seed).next_items(
        user_id=user_id, candidates=candidates, k=k
    )
