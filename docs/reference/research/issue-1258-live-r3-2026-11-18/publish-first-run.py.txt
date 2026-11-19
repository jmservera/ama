import sys
sys.path[:0] = ["tests", "src"]
from test_ranking_publication import snap
from zava_forward.core import ranking_publication as rp
from pathlib import Path

base = Path(sys.argv[1])
res = rp.publish(snap(), base / "a" / "b" / "archive", "2026-11-18")
print("RESULT", sorted(res))
