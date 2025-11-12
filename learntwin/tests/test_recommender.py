from __future__ import annotations
from dataclasses import dataclass
from learntwin.models.models_bkt import BKTModel, BKTParams
from learntwin.recsys.recommender import Recommender, Item
def test_next_items_deterministic_catalog_order_independent():
    bkt = BKTModel(BKTParams(p_init=0.2))
    catalog = {"i1":Item("i1","s1",0.4),"i2":Item("i2","s2",0.6),"i3":Item("i3","s1",0.7)}
    r = Recommender(bkt, catalog)
    a = r.next_items("u1",k=2); b = r.next_items("u1",k=2)
    assert a==b and len(a)==2
