# Plan: #175 source provenance close-out

* Scope: acceptance criterion 2 only; no new package code.
* Phases:
  * [x] Replace provisional licence and attribution wording for the three ONS/MHCLG sources in `provenance-register.json`, with verification notes; keep `retrieval_date` null.
  * [x] Update `test_synthetic_provenance.py` so the strict audit expects only `missing_or_invalid_retrieval_date`.
  * [x] Update the data dictionary audit table and append a log entry.
  * [x] Run core provenance tests, ruff check, ruff format --check, mypy.
  * [x] Commit, push, open PR with `Refs #175`.
* Critique (single pass, direct): inventing retrieval dates or weakening the audit would be fabricated evidence; rejected. Verdict: proceed.
