from __future__ import annotations
from dataclasses import dataclass
import time
from learntwin import BKT, Recommender

def main():
    bkt = BKT(seed=0)
    rec = Recommender(seed=0)

    t0 = time.perf_counter()
    _ = bkt.get_mastery("u1","add")
    t1 = time.perf_counter()
    _ = bkt.update("u1","add", True)
    t2 = time.perf_counter()
    _ = rec.next_items("u1", [{"item_id":"i1","skill_id":"add"}]*10, k=5)
    t3 = time.perf_counter()

    print(f"get_mastery: {(t1-t0)*1000:.3f} ms")
    print(f"update: {(t2-t1)*1000:.3f} ms")
    print(f"next_items: {(t3-t2)*1000:.3f} ms")

if __name__ == "__main__":
    main()
