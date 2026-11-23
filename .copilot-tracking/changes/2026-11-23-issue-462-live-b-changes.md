# Changes: issue 462 second pass (2026-11-23)

Documentation only; no `src/` change, focused tier (no full gate, no rpi-checks). Files: `docs/reference/research/resident-showcase-live-r7-2026-11-23.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), this pass's dated artifacts.

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven (demo) | Dated artifacts; threat model 2026-11-16; October independent review not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven for hosted-history clauses; local-preview clause not re-tested | `gh` run history: one failure, bot-authored score commits, later runs on changed SHAs, success at merge |
| 3, 4 (ticked) | Re-observed live in r6 | 36 Playwright checks |
| 5 (ticked) | Not re-run | No source change |
| 6. Pre-spend record | Proven (demo) | r3; USD 700 decision; no fresh cost figure |
| 7. Browser proof | Proven (demo, desktop) | r6 |
| 8 (ticked) | Unchanged | Source commit behind digests unconfirmed |

Remaining owner-gated or optional: ticking criteria, HSTS header follow-up (needs full tier).
