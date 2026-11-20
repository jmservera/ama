# Plan: issue 73 requirement trace matrix and offline test (2026-11-20)

Refs #73. Research: ../../research/2026-11-20/issue-73-requirement-trace-research.md

* Phase 1: add `docs/reference/research/issue-73-requirement-trace-2026-11-20.md` with one row per requirement (BG-011, FR-001 to FR-007, FR-032, FR-034, NFR-003) naming a cited `path::test` check or a recorded deferral.
* Phase 2: add `tools/test_epic_73_requirement_trace.py`, offline: every requirement has one row; each cited check file exists and defines the named test; deferrals carry a reason; the note never records the epic accepted.
* Phase 3: run the cited tests and the new test; record results in the matrix note and changes record; update index and log.
* Validation tier: FOCUSED (tools and docs only, no src change, no SQL/security/infra).
