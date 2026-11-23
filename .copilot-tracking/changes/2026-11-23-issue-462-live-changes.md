# Changes: issue 462 close-out (2026-11-23)

Evidence only; no `src/` change, so the focused tier applies (no full gate, no rpi-checks). Tier basis: documentation and evidence files only.

## Files

* `docs/reference/research/resident-showcase-live-r6-2026-11-23.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-23-resident-showcase-live/` (script, JSON, five screenshots, az state, headers)

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven (demo) | This run's dated artifacts; threat model `docs/reference/research/resident-demo-threat-model-2026-11-16.md`; October independent review not re-derived |
| 2. #444/#455 and failed rubric resolved | Partly proven: #444 CLOSED, #455 MERGED 2026-10-25; rubric rerun and no-manual-edit unproven | Needs hosted rubric history; not available without a push |
| 3, 4, 5, 8 (ticked) | 3 and 4 re-observed live; 5 not re-run; 8 digests recorded, source commit unconfirmed | `live-checks.json`, `az-state.txt` |
| 6. Pre-spend record | Proven (demo) | r3 record; no fresh cost figure; USD 700 owner decision supersedes the October cap |
| 7. Deployed showcase, HTTPS login, negative paths in a browser | Proven (demo, desktop) | 36 passing live checks on revision 0000026 |
