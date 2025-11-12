from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple 
@dataclass
class BKTParams:
    p_init: float = 0.2
    p_learn: float = 0.15
    p_guess: float = 0.2
    p_slip: float = 0.1

class BKTModel:
def __init__(self, params: BKTParams | None = None):
        self.params = params or BKTParams()
        self._state: Dict[Tuple[str, str], float] = {} 

    def _init_state(self, user_id: str, skill_id: str) -> float:
        key = (user_id, skill_id)
        if key not in self._state:
            self._state[key] = self.params.p_init
        return self._state[key]

    def update(self, user_id: str, skill_id: str, correct: int) -> float:
        pL = self._init_state(user_id, skill_id)
        g, s, t = self.params.p_guess, self.params.p_slip, self.params.p_learn
        if correct not in (0, 1):
            raise ValueError("correct must be 0 or 1")
        if correct == 1:
            num = pL * (1 - s); den = num + (1 - pL) * g
        else:
            num = pL * s;       den = num + (1 - pL) * (1 - g)
        p_post  = 0.0 if den == 0 else num / den
        p_after = p_post + (1 - p_post) * t
        self._state[(user_id, skill_id)] = p_after
        return p_after

    def get_mastery(self, user_id: str, skill_id: str) -> float:
        return self._state.get((user_id, skill_id), self.params.p_init)

def get_mastery(user_id: str, skill_id: str, model: "BKTModel | None" = None) -> float: 
    m = model or BKTModel()
    return m.get_mastery(user_id, skill_id)
