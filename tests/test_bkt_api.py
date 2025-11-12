from learntwin import BKT

def test_bkt_api_shape():
    bkt = BKT()
    m0 = bkt.get_mastery("u1", "add")
    assert 0.0 <= m0 <= 1.0
    m1 = bkt.update("u1", "add", True)
    assert 0.0 <= m1 <= 1.0
