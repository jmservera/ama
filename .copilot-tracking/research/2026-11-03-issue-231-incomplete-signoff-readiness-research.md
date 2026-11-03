# Research: issue #231 slice 4, incomplete sign-off records

Disposition: executed (reused slices 1-3 evidence). Planning Readiness: Ready.

* Merged work already delivered for #231: #656 (technical and quality queue screens), #769 (browser keyboard and axe evidence), #807 (unresolved source conflicts block readiness). Nothing is redone.
* Reading `signoffState` in `src/api/src/zava_forward/api/web/role-screens.js`: any record with `status` "Signed off" counted as valid, even with no named person or no design version. `src/core/src/zava_forward/core/signoffs.py` always records `by` and `version`, so a record without them is incomplete evidence and must not show readiness.
* Older design versions on unaffected sign-offs are deliberate (scoped invalidation); the existing test `test_unaffected_older_signoffs_and_no_conflicts_stay_ready` keeps that. No age-based staleness threshold exists and none is invented.
* Remaining unmet criteria after this slice: 4 (WCAG conformance needs AT and human acceptance, #151, #155) and 5 (Fluent component adoption, #150).
* Slice choice: smallest change that closes a missing-evidence hole in criterion 1.
