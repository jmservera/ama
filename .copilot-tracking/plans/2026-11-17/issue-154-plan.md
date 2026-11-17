# Issue 154 plan (2026-11-17)

* [x] Phase 1: record measured criteria evidence (research file).
* [ ] Phase 2: add one regression test: a representative grant's expiry and revocation take effect on the next request over HTTP, with no case data in the denial (src/api/tests/test_resident_preview_api.py).
* [ ] Phase 3: run targeted tests, ruff format check, mypy for src/api; record in changes and review.

Critique (single pass, self): compatible; no source change needed because the boundary already denies (to be measured by the test). Refs #154; C2 and C5 stay unmet.
