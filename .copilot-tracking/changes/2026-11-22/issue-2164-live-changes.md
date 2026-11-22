# Changes: #2164 (2026-11-22)

Tier: FULL candidate (src change to an authorisation control). The coordinator runs the gates; `rpi-checks.py --all` was not run. Hosted CI, independent exact-head review and human approval remain outstanding.

## Source changes

* src/core/src/zava_forward/core/assistants.py `Assistants.authorize`: a roster-bound Entra principal (`bound` set by `identity.bind`) is re-read from its roster row by bound email; the row must carry the same oid and a matching or empty tid, and the common check then enforces role, `disabled`, `active` and the row `case_ids`/`areas`. view_only Entra principals are refused. Unbound Entra principals keep the earlier unscoped behaviour (decision recorded in the research note).
* src/api/tests/test_assistants.py (`ReviewTests`): `test_bound_entra_staff_inherit_roster_scope_and_revocation` and `test_unbound_and_view_only_entra_principals`.

## Validation

* `python3 -m unittest test_assistants -q` in src/api (PYTHONPATH as in the instructions): 146 tests OK, 63 skipped.
* The two new tests fail on HEAD source and pass with the change (checked by temporarily restoring the old file).
* `ruff check` clean on both files; `mypy` in src/api clean; `mypy` in src/core reports 3 errors in telemetry.py and synthetic/device_provision.py (missing opentelemetry stubs, unused ignore), files this change does not touch.
* Not run: full src/core suite, hosted CI, live Azure (see table).

## Per-criterion table

| Criterion (issue body) | Status | Evidence |
| --- | --- | --- |
| Decide whether roster-bound Entra staff inherit the scope of their bound row | Proven (decision implemented) | Research note; authorize change; scope test |
| Test: scope bypass for Entra staff | Proven | `test_bound_entra_staff_inherit_roster_scope_and_revocation` covers case_ids, areas, revoked/disabled/inactive/role/oid change, deleted row, invoke and listing |
| Test: view_only with an eligible role | Proven | `test_unbound_and_view_only_entra_principals` |
| Live Azure proof of the deployed behaviour | Unproven | Not required by the issue; the deployed apps run the earlier image and no image was rebuilt or deployed, no Azure resource was created |
