# Changes r3 (Refs #1207, PR #1209)

* `tools/rpi-checks.py`: `WORKFLOW_HASHES["src-ci.yml"]` changed from `99a20cf0...2055c` to `197606992ba38bc5f705770a30d2ed0a5d7be5ded2166e441abb110ffd744476`, computed with `sha256sum` from the reviewed file. One line; nothing else.
* Reproduced failure before the edit: `test_rpi_checks` 82 tests, 2 failures (the two hosted-failing tests).
* Validation after the edit, `PYTHONDONTWRITEBYTECODE=1`, `RUFF_CACHE_DIR` and `MYPY_CACHE_DIR` under `/tmp/c1207`:
  * `python3 -m unittest discover -s tools -p test_rpi_checks.py`: 82 tests OK.
  * `-p test_ci_affected.py`: 19 tests OK.
  * `-p test_backlog_sync.py`: 11 tests OK.
  * `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on the five tool files: passed; `ruff format --isolated --line-length 100 --check`: 5 files formatted.
  * `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` and `mypy --ignore-missing-imports tools/test_backlog_sync.py tools/backlog-sync.py`: no issues.
  * `actionlint -config-file infra/tests/actionlint.yaml` on the five gate workflows: exit 0. Running it over all workflows also reports an unrelated pre-existing `rubric-score.lock.yml` permission-scope message; not in the gate set and not changed.
* Not run: complete gate, browser, SQL, build (out of scope; #1208 owns the shared slot). Hosted CI must re-run after the coordinator's batched push.
* Earlier static Pass (r2 review) and the hosted failure remain recorded unchanged as separate evidence.
