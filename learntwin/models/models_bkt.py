from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Tuple


@dataclass
class BKTParams:
    """Minimal placeholder parameters for BKT."""
    p_init: float = 0.2
    p_learn: float = 0.15
    p_slip: float = 0.1
    p_guess: float = 0.2


class BKTModel:
    """
    Minimal placeholder BKT-style model so that imports and tests can run.

    This is not a full BKT implementation; it just stores a mastery value
    per (user, skill) and nudges it up/down based on correctness.
    """
    def __init__(self, params: Optional[BKTParams] = None, seed: int = 0) -> None:
        self.params = params or BKTParams()
        self.seed = seed
        self._state: Dict[Tuple[str, str], float] = {}

    def get_mastery(self, user_id: str, skill_id: str) -> float:
        return self._state.get((user_id, skill_id), self.params.p_init)

    def update(self, user_id: str, skill_id: str, is_correct: bool) -> float:
        m = self.get_mastery(user_id, skill_id)
        delta = self.params.p_learn * (1.0 if is_correct else -0.5)
        new_m = max(0.0, min(1.0, m + delta))
        self._state[(user_id, skill_id)] = new_m
        return new_m
