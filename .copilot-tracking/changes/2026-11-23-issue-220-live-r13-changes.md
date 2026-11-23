# Changes, issue 220 r13 (2026-11-23)

* src/core/src/zava_forward/core/challenges.py: `_normalise_key` applies NFKC, drops format characters, splits camelCase and collapses non-alphanumeric runs.
* src/core/tests/test_challenge_no_retaliation_220.py: regression test (10 sub-tests fail without the change).
* docs/reference/research/issue-220-live-r13-key-variants-2026-11-23.md, README index and log entry.

Validation: 33 tests in the four 220 challenge core modules pass; ruff check and format clean; mypy no error in changed files. Tier: FULL applies (src change) but rpi-checks --all is not run by brief; hosted CI and coordinator gate apply.

| Criterion | Status |
| --- | --- |
| Digital and staff-recorded routes work | Proven (live r11, tests) |
| Explanations, owner, next update, resolution visible | Proven (live r11, tests) |
| Only dependent proposals and reviews stale | Proven offline |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven (live r11) |
| No retaliation, inferred refusal or delayed hazard response | Proven for constructed case; hardened offline; not deployed; long-run behaviour unproven in demo (needs production history) |
