# Changes, issue 220 r12 (2026-11-23)

* src/core/src/zava_forward/core/challenges.py: adverse-key guard compares normalised keys (case, spaces, hyphens).
* src/core/tests/test_challenge_no_retaliation_220.py: regression test for key variants.
* docs/reference/research/issue-220-live-r12-key-normalisation-2026-11-23.md: note; docs/reference/log.md entry.

Validation: 220 core tests pass (10); ruff check/format and mypy clean for changed files; the 8 challenge-related core modules pass (575 tests, 162 skipped for missing SQL prerequisites); full discover run output was truncated and is not claimed. Tier: FULL not run (no rpi-checks --all, by brief); source change is small, hosted CI and coordinator gate apply.

| Criterion | Status |
| --- | --- |
| Digital and staff-recorded routes work | Proven (live r11, tests) |
| Explanations, owner, next update, resolution visible | Proven (live r11, tests) |
| Only dependent proposals and reviews stale | Proven offline |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven (live r11) |
| No retaliation, inferred refusal or delayed hazard response | Proven for constructed case; hardened offline; not deployed; long-run behaviour unproven in demo |
