# Issue 116 live r14 changes (2026-11-24)

Files: src/agents/src/zava_forward/agents/heldout_aoai.py (shared `approved_payload` before any request), src/agents/tests/test_heldout_aoai.py (one test, fails without the fix), docs/reference/research/issue-116-live-r14-evidence-2026-11-24.md, docs/reference/README.md, docs/reference/log.md.
Validation: heldout tests 84 OK; test_dispatch and test_chat_heldout 33 OK; ruff and mypy clean. Full agents suite output was truncated, so it is not claimed.
Tier: FULL (src change); rpi-checks.py --all not run, left to the coordinator.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Every role tested against every endpoint | Proven (ticked) | Rounds r1-r13 |
| Contractor view has no vulnerability reason anywhere | Proven (ticked) | Prior rounds |
| Free-text redaction approach decided | Proven (ticked) | ADR/OD record |
| Roles allowed to see vulnerability reason confirmed | Proven (ticked) | OD-14, OD-19 |
| RAI: allowlists at every provider boundary | Unproven | Held-out gap fixed here and all four call sites inventoried; live payloads not observable from deployed apps; independent review and hosted CI outstanding |
| Six other RAI boxes | Proven (ticked) | Prior rounds |
