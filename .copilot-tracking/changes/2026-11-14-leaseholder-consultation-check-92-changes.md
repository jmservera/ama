# Changes: leaseholder consultation check (#92)

* `src/core/src/zava_forward/core/procurement.py`: new field, helpers, gate and list output.
* `src/api/src/zava_forward/api/web/role-screens.js`: checklist row shows status and blocked reason.
* `src/core/tests/test_consultation_controls.py`: `test_leaseholder_status_defaults_unknown_and_blocks_each_status`.
* Validation: `PYTHONPATH=tests:src TMPDIR=/dev/shm/zf-tmp python3 -m unittest test_consultation_controls` (48 run, 17 SQL skips, OK); ruff and mypy clean; `node --check` on the JS. No `unittest discover`; browser harness not run.
