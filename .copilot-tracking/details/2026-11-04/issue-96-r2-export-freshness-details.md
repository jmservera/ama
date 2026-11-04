<!-- markdownlint-disable-file -->
# Details: issue-96-r2-export-freshness

* Phase 1: `BODY_KEYS` names the hashed export body. `export_freshness` rebuilds the body from the saved copy, checks the hash (else Invalid), re-runs `draft_export`, and compares per field (value, state, source ID, version, hash, locator) plus the current stale fields. Reasons: schema digest changed, input version changed, or source/state changed.
* Phase 2: tests cover a source version bump (only `epc` stale, `area` unaffected), an input correction (only `area`), a newer schema (all fields), edited or incomplete copies (Invalid), on JSON and SQL stores.
* Phase 3: `src/core/README.md` and `docs/reference/log.md`.
* Phase 4: `unittest test_form_export test_form_review test_form_staging`, ruff, mypy `--cache-dir=/tmp/mypy-96`.
