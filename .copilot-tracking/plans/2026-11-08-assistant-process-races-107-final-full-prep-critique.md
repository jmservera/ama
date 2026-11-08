# Critique: issue 107 final FULL preparation plan

Date: 2026-11-08. One execution, one reviewer (rubber-duck, independent of the author), run before any change record. Verdict: Revise. Not repeated.

| Finding | Severity | Disposition |
| --- | --- | --- |
| Success criterion said a final `OK`; the SQL group tolerates one JSON-only hazard skip so the summary can be `OK (skipped=1)` (verified: `src/core/tests/test_hazard_referral.py:312`, `SQL_NOT_APPLICABLE`) | Blocking | Accepted. Research amended to allow only that skip and still require both MSSQL method `ok` lines. |
| Console output inside `--out` would pre-create the directory or disturb receipt hashing | Blocking | Accepted. Separate external file; nothing written in `--out`. |
| `rc=$?` after a `tee` pipeline records tee's status | Blocking | Accepted. Plan requires redirection with `$?` or `${PIPESTATUS[0]}`. |
| A lock-timeout refusal leaves a directory but no receipt, so `--resume` does not apply | Non-blocking | Accepted. Plan says preserve it and use a new path. |

The reviewer confirmed that `SQL_SELECTORS` discovers both inherited methods and that `Runner.sql()` supplies the disposable MSSQL environment, while noting that execution is not yet demonstrated. This matches the research conclusion, which stays "source-read, not executed".
