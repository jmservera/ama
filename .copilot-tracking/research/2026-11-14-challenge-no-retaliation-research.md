# Issue #220 research: no retaliation, inferred refusal or delayed hazard response

* Task: challenge-no-retaliation (Research disposition: executed; Planning Readiness: Ready)
* Existing: `core/challenges.py` already had PROTECTED_CASE_KEYS, GUARANTEES, `assert_no_retaliation`; `resident_decisions.py` guards challenge open, resolve and nomination correction; `store.detail` exposes `challenge_guarantees`; `panels.js` renders them.
* Gap: no explicit machine-readable `no_retaliation: True`, `inferred_refusal: False`, `hazard_response_delayed: False` on the records or detail payload, and no plain-language assurance line in the workbench.
