# Issue 108 details (2026-11-04, r2)

* src/agents/src/zava_forward/agents/candidate_comparison.py: add freeze parameter, held_out report block, baseline-versus-frozen check, held_out_basis per candidate.
* src/agents/tests/test_candidate_comparison.py: five tests (no freeze, frozen, cheaper-but-worse failure on frozen cases, outside the freeze, insufficient freeze).
* src/agents/README.md and docs/reference/log.md updated.
