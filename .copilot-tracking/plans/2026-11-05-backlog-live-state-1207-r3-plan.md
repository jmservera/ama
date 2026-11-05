# Plan r3: update the reviewed src-ci.yml fingerprint (Refs #1207)

* Replace only the `src-ci.yml` value in `WORKFLOW_HASHES` with the digest computed from the reviewed file. Keep every hash check, drift detection, receipt verification, job and check name and permission unchanged. Add no ignored or broad coverage entries.
* Classification: no change; the per-job classification already covers the unchanged step count.
* Correct the validation gap honestly: run `test_rpi_checks`, `test_ci_affected` and `test_backlog_sync` together, plus the existing ruff check, ruff format, both mypy invocations and actionlint on the five gate workflows. External caches under `/tmp`, `PYTHONDONTWRITEBYTECODE=1`, final `git status --short --ignored` empty.
* No heavy gate, browser, SQL or build; #1208 owns the shared native-check slot. No push, PR change or merge.
* Critique: not repeated for the task (one-pass rule); the correction is compatible with the confirmed scope.
