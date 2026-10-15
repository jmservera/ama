# Changes: retire prototype/ (#202 step 1)

* Deleted 10 tracked `prototype/` files and `.github/workflows/prototype-validation.yml`.
* `.github/rubric/artifacts.json`: removed `prototype/deploy/**/*.bicep`.
* `.github/rubric/scripts/test_prepare.py`: removed stale prototype fixtures; generated-file cases use `src/` paths.
* Docs updated: rubric README (removed prototype sections), capstone README, ADR 0006, parity matrix, coordinator agent, reference index; log appended.

## Validation

* mvp: `PYTHONPATH=. python3 -m unittest discover -s tests -q` 719 tests OK (skipped=92), run before the change (mvp/ untouched).
* `tools/rename-zava-tests.py`: same 7 pre-existing errors as baseline.
* rubric scripts: 19 failed before, 11 failed after; the 8 removed were stale prototype cases; the remaining 11 are pre-existing.
* grep for `prototype/`: remaining hits are dated history, ADR/matrix records or explanatory notes.
