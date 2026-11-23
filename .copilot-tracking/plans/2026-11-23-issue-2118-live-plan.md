# Plan: issue 2118 live walkthrough (2026-11-23)

Tier: focused (documentation and evidence only, no src change).

1. Write the dated research note, index entry and log entry.
2. Run `test_map_sensors.py` as the main comparison.
3. Record the per-criterion table in the changes record; do not tick the box.

## Critique (executed once)

* Verdict: proceed. Risk: calling the SQL hop proven without a trace. Disposition: applied; the table says "inferred" and leaves ticking to the owner.
* Risk: the screenshot shows a loading state. Disposition: applied; the note says the verdict rests on API responses.
* No code gap, so no src edit, no FULL tier.
