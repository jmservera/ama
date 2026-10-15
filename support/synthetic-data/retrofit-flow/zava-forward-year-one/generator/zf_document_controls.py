"""SYNTHETIC DATA ONLY. Document-control fixtures: scan outcomes, retention triggers and legal holds.

Walks 120 homes picked from the 60,000-home synthetic stock register (the same
cluster-spread pick as zf_documents.py) and gives each three constructed
uploads with a scan class, a retention trigger and, for a fixed share, a legal
hold. No file bytes and no real personal data; the scan payloads are
descriptors that the tests turn into bytes. Same seed and register give
byte-identical output.

Usage:
    python3 zf_document_controls.py --seed 20260901 --out ../../../../src/core/evals/document_control_fixtures.json
"""
import argparse
import hashlib
import json
import os
import random
from datetime import date, timedelta

from zf_documents import REGISTER, _pick_families, load_register

VERSION = "document-control-fixtures-v1"
AS_OF = "2026-10-15"
KINDS = ("EPC", "Survey", "Design", "Consent", "Funding evidence", "Photo")
SCAN_CLASSES = ("clean", "clean", "clean", "clean", "test-marker", "type-mismatch")
LABEL = "SYNTHETIC - constructed control fixture, not a real document or a real retention decision"


def build(register, seed, count=120):
    homes = _pick_families(register, seed)[:count]
    rng = random.Random(f"{seed}:document-controls")
    as_of = date.fromisoformat(AS_OF)
    cases = []
    for i, row in enumerate(homes, 1):
        closed = rng.random() < 0.7
        trigger = (as_of - timedelta(days=rng.randint(30, 365 * 9))).isoformat() if closed else None
        cases.append({
            "case_id": f"DC-{i:03d}", "is_synthetic": True, "label": LABEL, "synthetic_home_id": row["synthetic_home_id"],
            "closed": closed, "retention_trigger": trigger, "legal_hold": rng.random() < 0.15,
            "uploads": [{"name": f"{k.lower().replace(' ', '-')}-{i:03d}.{'png' if k == 'Photo' else 'pdf'}", "kind": k,
                         "scan_class": rng.choice(SCAN_CLASSES)}
                        for k in rng.sample(KINDS, 3)]})
    out = {"is_synthetic": True, "generator_version": VERSION, "seed": seed, "as_of": AS_OF,
           "stock_register_rows": len(register), "cases": cases}
    out["content_sha256"] = hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260901)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = build(load_register(REGISTER), a.seed)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"wrote {a.out}: {len(out['cases'])} cases")


if __name__ == "__main__":
    main()
