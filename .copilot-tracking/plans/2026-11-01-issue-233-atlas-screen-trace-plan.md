# Plan: issue 233 atlas UX findings and role journeys to screens (2026-11-01)

1. Add `docs/reference/research/ux/atlas-screen-trace.md`: perspective-to-screen table (confirms/changes/hypothesis), theme table (screen or recorded deferral), tension resolutions, same-home walkthrough (8 stages), accessibility and design-system boundaries.
2. Add `src/core/src/zava_forward/core/atlas_screen_trace.py` (offline checker, reads PRD, atlas and the trace doc) and `src/core/tests/test_atlas_screen_trace.py`.
3. Update profile review #233 row, docs/reference/README.md index, log.md.
4. Validate: new unit tests, ruff check, ruff format --check, mypy for src/core. Commit, push, PR (Refs #233: criteria 5 and 6 unproven).

Critique (single pass, self): do not claim unmerged screens as delivered; do not tick accessibility; walkthrough must not reuse existing example ids as stages; checker must fail on missing perspective/theme or missing hypothesis label. Accepted.

* Correction cycle 2026-11-01: two PR 713 review threads accepted as valid; no research change.
