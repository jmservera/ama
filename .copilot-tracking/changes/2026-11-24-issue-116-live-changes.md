# Issue 116 live changes (2026-11-24)

Files: src/core/src/zava_forward/core/ai.py (MAX_PARTS=8, `input-too-many-parts`), src/core/tests/test_ai_input_bounds.py (one test), docs/reference/research/issue-116-live-r13-evidence-2026-11-24.md, docs/reference/README.md, docs/reference/log.md.
Witness note: implement-start recorded a qualification that source was dirty (the edit ran in parallel with the witness call).
Tier: FULL (src change); `rpi-checks.py --all` not run, left to the coordinator.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Every role tested against every endpoint | Proven (already ticked) | Prior rounds r1-r12 |
| Contractor view has no vulnerability reason anywhere | Proven (already ticked) | Prior rounds |
| Free-text redaction approach decided | Proven (already ticked) | ADR/OD record |
| Roles allowed to see vulnerability reason confirmed | Proven (already ticked) | OD-14, OD-19 |
| RAI: allowlists at every provider boundary (unticked) | Unproven | Code-level allowlist and inventory tests pass, a further gap fixed here; live payload contents are not observable from deployed apps; independent review and hosted CI outstanding |
| Six other RAI boxes | Proven (already ticked) | Prior rounds |
