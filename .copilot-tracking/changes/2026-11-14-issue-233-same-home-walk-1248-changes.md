# Changes: #233 same-home walk hardening

* `src/api/src/zava_forward/api/web/role-screens.js`: same-home badge; mismatched record guard.
* `src/api/tests/test_role_screens_same_home_identity.py`: new (3 tests).

Validation (from `src/api`, bare commands): `mypy` rc=0; `ruff check .` rc=0; `ruff format --check .` rc=0; unittest same-home identity, connected journey, tensions, stage-map focus, role screens, conformance, accessibility baseline, role matrix: 67 OK. Heading hierarchy browser test: 35 failures identical on the base commit (pre-existing). Not run: AT, user validation, full gate.
