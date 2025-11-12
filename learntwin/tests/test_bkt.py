from __future__ import annotations
from learntwin.models.models_bkt import BKTModel, BKTParams
def test_bkt_update_math_correct_then_incorrect():
    m = BKTModel(BKTParams(p_init=0.2,p_learn=0.15,p_guess=0.2,p_slip=0.1))
    p1 = m.update("u1","s1",1); p2 = m.update("u1","s1",0)
    assert 0<=p1<=1 and 0<=p2<=1 and p1!=p2
def test_get_mastery_default_init():
    m = BKTModel(BKTParams(p_init=0.3))
    assert abs(m.get_mastery("uX","sY")-0.3) < 1e-9
