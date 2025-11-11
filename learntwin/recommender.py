from __future__ import annotations
from typing import List, Dict, Any, Iterable, Tuple
from .models_bkt import BKT

def _key_det(item: Dict[str, Any]) -> Tuple[str, str]:
    # Deterministic tiebreak by (skill_id, item_id)
    return (str(item.get("skill_id", "")), str(item.get("item_id", "")))

class Recommender:
    """
    Rank candidates by 1 - mastery(skill_id) (lower mastery first),
    then deterministic tie-break on (skill_id, item_id).
    """
    def __init__(self, bkt: BKT | None = None, seed: int = 0):
        self.seed = seed
        self.bkt = bkt or BKT()

    def next_items(
        self,
        user_id: str,
        candidates: Iterable[Dict[str, Any]],
        k: int = 5
    ) -> List[Dict[str, Any]]:
        mastery_cache: Dict[str, float] = {}
        scored: List[Tuple[float, Tuple[str, str], Dict[str, Any]]] = []

        for c in candidates:
            skill = str(c.get("skill_id", ""))
            if not skill or "item_id" not in c:
                continue
            if skill not in mastery_cache:
                mastery_cache[skill] = self.bkt.get_mastery(user_id, skill)
            mastery = mastery_cache[skill]
            score = 1.0 - mastery
            scored.append((score, _key_det(c), c))

        # Sort by score desc, then deterministic tie-break asc
        scored.sort(key=lambda t: (-t[0], t[1]))
        return [c for _, __, c in scored[:max(0, int(k))]]
