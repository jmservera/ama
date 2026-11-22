# Changes: issue 462 live recheck (2026-11-22)

Evidence only; no `src/` change, so the focused tier applies and no test or gate suite was needed. Tier basis: documentation and evidence files only.

## Files

* `docs/reference/research/resident-showcase-live-r5-2026-11-22.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-22-resident-showcase-live/` (script, JSON, five screenshots)
* RPI artifacts under `.copilot-tracking/`

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven (demo) | This run's dated artifacts; existing threat model; October independent review not re-derived |
| 2. #444/#455 and failed rubric resolved | Unproven | Needs hosted rubric run and thread state; not possible without a push |
| 6. Pre-spend record | Proven (demo) | r3 record; no fresh cost figure; USD 700 owner decision |
| 7. Deployed showcase, real HTTPS login, negative paths in a browser | Proven (demo, desktop) | 36 passing live checks in `live-checks.json`; screenshots |
| 3, 4, 5, 8 (ticked) | Not reopened | 3 and 4 re-observed live; 5 not re-run; 8 digest changed, source commit unconfirmed |

Observations for the owner: `minReplicas` is now 1 (standing cost), image digest differs from r4, `aoai-resident-469` no longer found, no HSTS header.
