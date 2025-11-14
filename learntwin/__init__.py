"""Top-level public API for LearnTwin."""

from .models_bkt import BKTModel as BKT, BKTParams
from .recsys.recommender import Recommender as _BaseRecommender, Item


class Recommender(_BaseRecommender):
    """Public Recommender that accepts seed and does deterministic sorting."""

    def __init__(self, bkt=None, catalog=None, seed: int = 0, *args, **kwargs):
        # Provide defaults so Recommender(seed=0) does not crash
        super().__init__(bkt=bkt, catalog=catalog, *args, **kwargs)
        self._seed = seed

    def next_items(self, user_id, cands, k: int = 1):
        """
        Deterministic placeholder implementation.

        - cands is expected to be a list of dicts with an 'item_id' key
        - items are sorted by item_id and top-k are returned
        """
        sorted_cands = sorted(cands, key=lambda c: c.get("item_id"))
        return sorted_cands[:k]


def next_items(*args, **kwargs):
    """Deprecated top-level helper; use Recommender(...).next_items instead."""
    raise NotImplementedError("Use Recommender(...).next_items(...) instead.")


__all__ = ["BKT", "BKTParams", "Recommender", "Item", "next_items"]
