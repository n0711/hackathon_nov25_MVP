"""
Compatibility wrapper for BKT model.

Tests and __init__.py expect BKTModel and BKTParams to live in
`learntwin.models_bkt`, but the actual implementation is in
`learntwin.models.models_bkt`.

This module simply re-exports those symbols.
"""

from .models.models_bkt import BKTModel, BKTParams

__all__ = ["BKTModel", "BKTParams"]
