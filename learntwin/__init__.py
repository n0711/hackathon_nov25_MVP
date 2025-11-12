# learntwin/__init__.py ? stable public API
from __future__ import annotations

# BKT exports: handle either naming scheme
try:
    from .models_bkt import BKTModel as BKT, BKTParams  # preferred
except Exception:
    from .models_bkt import BKT, BKTParams  # fallback if module exposes BKT directly

# Recommender API (Item factory + helper)
from .recsys.recommender import Recommender, Item, next_items

__all__ = ["BKT", "BKTParams", "Recommender", "Item", "next_items"]
