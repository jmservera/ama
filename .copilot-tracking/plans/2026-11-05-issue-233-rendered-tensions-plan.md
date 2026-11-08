# Plan: issue 233 rendered tension sequence

Research: ../research/2026-11-05-issue-233-rendered-tensions-research.md. Details: ../details/2026-11-05-issue-233-rendered-tensions-details.md. Tier: FOCUSED (test and documentation only; no production, security, SQL, finance, infrastructure or deployment change). Refs #233, Refs #149; no closing keyword.

* [x] Phase 1: add `src/api/checks/atlas_tensions_browser_check.py` using the shared harness and fixture
* [x] Phase 2: mutation control proving the package-order assertion can fail
* [x] Phase 3: update `atlas-screen-trace.md`, `src/api/README.md`, `log.md`, and the one pinned phrase in `test_role_screens_conformance.py`
* [x] Phase 4: focused validation (ruff, mypy, atlas checker, unit tests, real Chromium run under the shared lock)
* [ ] Phase 5: commit, then focused gate `tools/rpi-checks.py --changed` on the frozen head with an external receipt (non-blocking lock admission; pending handoff if busy)

Critique (single pass, self-applied): compatible. No new application behaviour, CSS or API semantics; the only response change is test-side ordering of the real `/api/packages` payload. Scope expansion into full-tier categories is not planned. A product defect would stop work for coordinator scoping; none was reproduced.
