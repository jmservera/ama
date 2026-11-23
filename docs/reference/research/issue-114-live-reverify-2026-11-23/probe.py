"""Read-only ledger and capacity probe for issue 114 (re-verification, 2026-11-23), run as a throwaway job.

Opens the live store and never writes. Prints counts, booleans, class names and hashes only.
"""

import json

from zava_forward.core import ledger
from zava_forward.core.factory import open_store


def out(step, **kw):
    print(json.dumps({"step": step, **kw}, default=str))


s = open_store()
out(
    "store",
    cls=type(s).__name__,
    has_reliance=hasattr(s, "verify_ledger_before_reliance"),
    has_require=hasattr(s, "require_verified_ledger_for_reliance"),
)
entries = list(s.audit_entries())
out("entries", count=len(entries), head=entries[-1]["hash"] if entries else None)
rep = s.verify_ledger()
out("verify_ledger", intact=rep["intact"], entries=rep["entries"], digests=rep["digests_checked"])
yrep = ledger.verify_years(entries)
out(
    "verify_years",
    intact=yrep["intact"],
    years={y: dict(entries=v["entries"], intact=v["intact"]) for y, v in yrep["years"].items()},
)
if hasattr(s, "verify_ledger_before_reliance"):
    r = s.verify_ledger_before_reliance(seal_past_years=False, require_sealed_past_years=False)
    out(
        "reliance_gate_no_seal",
        reliance_allowed=r["reliance_allowed"],
        intact=r["intact"],
        entries=r["entries"],
        audit_head_matches=r["audit_head_matches"],
        problem_codes=sorted({p["code"] for p in r["problems"]}),
    )
    r2 = s.verify_ledger_before_reliance(seal_past_years=False, current_year=2027)
    out(
        "reliance_gate_year_2027_unsealed_past_year",
        reliance_allowed=r2["reliance_allowed"],
        problem_codes=sorted({p["code"] for p in r2["problems"]}),
    )
