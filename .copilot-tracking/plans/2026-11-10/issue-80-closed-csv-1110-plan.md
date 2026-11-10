<!-- markdownlint-disable-file -->
# Plan: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

Research: [research](../../research/2026-11-10/issue-80-closed-csv-1110-research.md). Details: [details](../../details/2026-11-10/issue-80-closed-csv-1110-details.md). Critique: [critique](./issue-80-closed-csv-1110-critique.md).

Branch feat/demo-closed-page-csv-80-1110, base fe59ef56, target main, Refs #80 only. Owner DEMO FOCUSED tier.

## Phases

* [ ] P1 progress.py: `CLOSED_EXPORT_FIELDS` and `closed_csv(result)`: fixed columns, header always, `safe_cell`, primitives only.
* [ ] P2 server.py: `get_kind` maps `/api/closed-cases.csv` to `cases`; the existing progress/closed dispatch also serves the CSV path with identical read and error mapping, attachment only on success.
* [ ] P3 progress.js `closed()`: native link and copy after a successful load, normalized page and limit.
* [ ] P4 tests: `test_progress_dashboard.py` (JSON-versus-CSV parity, filters, pages, limit, empty headers, history cases, escaping, no mutation/audit, HTTP roles and rejection parity) and `test_role_endpoint_inventory.py` route entry. Failing-first.
* [ ] P5 `checks/progress_browser_check.py`: keyboard Enter download, real downloaded bytes against filtered page IDs, reset, page 2, empty, read error, nonmanager.
* [ ] P6 README note in the existing progress section and the test docs of the endpoint.
* [ ] P7 validation: targeted tests, default configured `mypy` from src/api with no file selectors, configured ruff check and format check, browser check under a non-queued lock, #96 merge-tree check.

## Boundaries

No Store/SqlStore/importer/exception/core lifecycle/schema/persistence/model/infra edits; no shared exporter change; `/api/cases.csv` unchanged; no writes, audit or events; no push/PR/merge.

## Validation commands

From src/api with the owned venv: `python -m unittest discover -s tests -p "<module>.py"` with `PYTHONPATH=../core/tests:../agents/tests`; `mypy`; `ruff check`; `ruff format --check`; `flock -n /tmp/ama-rpi-heavy.lock python -m checks.progress_browser_check --axe <pinned asset> --out <scratch>`.
