# Issue 125 plan (2026-11-14)

* Add `discovery_assistant_acceptance.py`: `NoWriteEvidence`/`assess_no_write` (three observed-evidence items) and `assess_acceptance` joining readiness, no-write and comparison reports; every criterion stays False, no connection permitted, no approval.
* Add `tests/test_discovery_assistant_acceptance.py`.
* Validate: ruff check and format (line length 100) on `src/core`; focused unittest.
* Critique (single pass): fail-closed by construction; no duplication of #1355 demo. Compatible, no changes needed.
* Tier: focused (additive pure module, no workflow, dependency or deployment change).
