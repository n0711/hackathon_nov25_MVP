"""Top-level public API for LearnTwin."""

from .models_bkt import BKTModel as BKT, BKTParams
from .recsys.recommender import Recommender as _BaseRecommender, Item


class Recommender(_BaseRecommender):
    """Public Recommender that accepts a `seed` keyword for determinism tests."""
    def __init__(self, *args, seed: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self._seed = seed


def next_items(*args, **kwargs):
    """Placeholder next_items helper; real behaviour to be implemented."""
    raise NotImplementedError("next_items is not implemented yet.")


__all__ = ["BKT", "BKTParams", "Recommender", "Item", "next_items"]
