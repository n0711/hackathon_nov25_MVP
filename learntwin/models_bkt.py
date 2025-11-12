from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
@dataclass
class BKTParams:
    # Prior mastery P(L0)
    p_init: float = 0.2
    # Learning probability per step P(T)
    p_learn: float = 0.15
    # Slip P(S): wrong despite mastery
    p_slip: float = 0.1
    # Guess P(G): right without mastery
    p_guess: float = 0.2

def _clip01(x: float, eps: float = 1e-12) -> float:
    if x <= eps: return eps
    if x >= 1 - eps: return 1 - eps
    return x

class BKT:
    """
    Standard BKT:
      prior p = P(L_{t-1})
      if correct:   p* = p(1-S) / [p(1-S) + (1-p)G]
      if incorrect: p* = p S     / [p S     + (1-p)(1-G)]
      transition:   p' = p* + (1 - p*) T
    """
    def __init__(self, params: BKTParams | None = None, seed: int = 0) -> None:
        self.params = params or BKTParams()
        self.seed = seed  # kept for determinism tests
        self.state: Dict[Tuple[str, str], float] = {}

    def get_mastery(self, user_id: str, skill_id: str) -> float:
        return self.state.get((user_id, skill_id), _clip01(self.params.p_init))

    def _posterior(self, prior: float, is_correct: bool) -> float:
        p = _clip01(prior)
        S = _clip01(self.params.p_slip)
        G = _clip01(self.params.p_guess)
        if is_correct:
            num = p * (1.0 - S)
            den = num + (1.0 - p) * G
        else:
            num = p * S
            den = num + (1.0 - p) * (1.0 - G)
        den = _clip01(den)
        return _clip01(num / den)

    def update(self, user_id: str, skill_id: str, is_correct: bool) -> float:
        p_prior = self.get_mastery(user_id, skill_id)
        p_star = self._posterior(p_prior, is_correct)        # after observing response
        T = _clip01(self.params.p_learn)
        p_next = _clip01(p_star + (1.0 - p_star) * T)        # learning transition
        self.state[(user_id, skill_id)] = p_next
        return p_next
