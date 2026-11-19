"""Read-only ledger probe for issue 114 (rerun r2, 2026-11-18), run as a throwaway job on the demo database.

Opens the live store, never writes. Prints counts, booleans, error class names and hashes only.
Tamper checks run on in-memory copies of the live audit entries.
"""

import copy
import json

from zava_forward.core import ledger
from zava_forward.core.factory import open_store


def out(step, **kw):
    print(json.dumps({"step": step, **kw}, default=str))


def prob(r):
    p = r["problem"] or {}
    return dict(intact=r["intact"], at_entry=p.get("entry"), reason=p.get("reason"))


s = open_store()
out("store", cls=type(s).__name__, has_reliance=hasattr(s, "verify_ledger_before_reliance"))
entries = list(s.audit_entries())
out("entries", count=len(entries), keys=sorted(entries[0]), head=entries[-1]["hash"])

rep = s.verify_ledger()
out("verify_ledger", intact=rep["intact"], entries=rep["entries"], digests=rep["digests_checked"])
yrep = s.verify_ledger_by_year()
out("verify_by_year", intact=yrep["intact"], years={y: v["entries"] for y, v in yrep["years"].items()})

if hasattr(s, "verify_ledger_before_reliance"):
    r = s.verify_ledger_before_reliance(current_year=2026, seal_past_years=False)
    out(
        "reliance",
        allowed=r.get("reliance_allowed"),
        years=sorted(r.get("years", {})),
        problems=sorted({p["code"] for p in r.get("problems", [])}),
    )

mid = len(entries) // 2
t = copy.deepcopy(entries)
t[mid]["detail"] = "tampered"
out("tamper-edit-detail", expected=mid + 1, **prob(ledger.verify_entries(t)))

t = copy.deepcopy(entries)
del t[mid]
out("tamper-delete-entry", expected=mid + 1, **prob(ledger.verify_entries(t)))

t = copy.deepcopy(entries)
t[mid], t[mid + 1] = t[mid + 1], t[mid]
out("tamper-reorder", **prob(ledger.verify_entries(t)))

# Tail truncation and a re-hashed tail rewrite pass the chain alone; only an external digest shows them.
dg = ledger.make_digest(len(entries), entries[-1]["hash"])
r = ledger.verify_entries(entries[:-5], [dg])
out("tamper-truncate-vs-digest", intact=r["intact"], mismatches=[m["reason"] for m in r["digest_mismatches"]])
t = copy.deepcopy(entries)
t[-1]["detail"] = "rewritten"
t[-1]["hash"] = ledger.entry_hash(t[-1])
r = ledger.verify_entries(t, [dg])
out(
    "tamper-rewrite-tail-vs-digest",
    chain_intact_alone=ledger.verify_entries(t)["intact"],
    intact_with_digest=r["intact"],
    mismatches=[m["reason"] for m in r["digest_mismatches"]],
)

# Per-year sealing on an in-memory two-year chain rebuilt from live entry shapes.
yr, prev = [], ledger.GENESIS
for i, e in enumerate(entries[:200]):
    at = "2025-06-01T00:00:00" if i < 100 else "2026-06-01T00:00:00"
    n = ledger.make_entry(e["who"], e["action"], e["case"], e["detail"], prev, at=at)
    yr.append(n)
    prev = n["hash"]
digs = ledger.year_digests(yr, before="2026")
r = ledger.verify_years(yr, digs)
out("two-year-seal-intact", intact=r["intact"], sealed=r.get("sealed_years", sorted(y for y, v in r["years"].items() if v.get("sealed"))), years={y: v["entries"] for y, v in r["years"].items()})
bad = copy.deepcopy(yr)
bad[10]["detail"] = "tampered"
r = ledger.verify_years(bad, digs)
out("two-year-tamper-2025", intact=r["intact"], problems={y: v["problems"] for y, v in r["years"].items() if v["problems"]})

for name, sql in (
    ("native-sp_verify_database_ledger", "EXEC sys.sp_verify_database_ledger N'[]'"),
    ("ledger-blocks", "SELECT COUNT(*), MAX(block_id) FROM sys.database_ledger_blocks"),
    ("ledger-tables", "SELECT COUNT(*) FROM sys.tables WHERE ledger_type <> 0"),
):
    try:
        row = s.db.execute(sql).fetchall()
        out(name, ok=True, rows=[list(x) for x in row][:3] if "native" not in name else "returned")
    except Exception as error:
        out(name, ok=False, error=type(error).__name__, text=str(error)[:200])
