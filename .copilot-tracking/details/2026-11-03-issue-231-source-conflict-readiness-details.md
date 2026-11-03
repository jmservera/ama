# Details: issue #231 slice 3

* `src/api/src/zava_forward/api/web/role-screens.js`: in `technical-queue`, each source query whose `assetStatus` is "Unresolved" adds "Source conflict {id} ({field}) is unresolved. Owner: {name}." to the readiness reasons.
* `src/api/tests/test_technical_quality_screens.py`: `tech_case` records a resolution event for SQ-1; new `test_unresolved_source_conflict_blocks_readiness`.
* `src/api/checks/role_screens_browser_check.py`: story `231` asserts "is unresolved. Owner:"; stories `231`, `231q` and `226` read each panel after scrolling it into view.
* `src/api/README.md`: story description mentions unresolved source conflicts.
