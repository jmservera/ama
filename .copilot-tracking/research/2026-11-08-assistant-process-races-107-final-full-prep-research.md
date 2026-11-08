# Research: issue 107 final FULL preparation (light, no execution)

Date: 2026-11-08. Task slug: `assistant-process-races-107-final-full-prep`.
Session: 29d9e541-c760-43f7-805e-f6ccfbb6f37e. Mode: LIGHT preparation. No SQL, Docker, browser, scanner or FULL run; 1258 owns the shared gate.
Research disposition: executed (trusted source and Git metadata only). Planning Readiness: Ready.

## Verified start state

| Item | Evidence |
| --- | --- |
| Worktree and branch | `/home/azureuser/source/ama-wt/issue-107-process-races`, `test/assistant-process-races-107` |
| HEAD and tree | `b34a8563a84b8bd4a885c35de4f01c266e78e46b`, `7ebea12f53d935f26c7d8f889cdd5ae2113cbf6f` |
| Cleanliness | `git status --short --ignored` empty before writes |
| Main | `origin/main` fetched once, `f548b65f4aa31eb92a2cc9cb801130e422daed7f`, unchanged and an ancestor of HEAD, so no new merge |
| Output path | `/home/azureuser/.local/share/ama/gates/g107-final-full-r1` does not exist (metadata check); 57 bytes |
| Free space (metadata) | root 39,151,984,640 bytes, /mnt 4,501,475,328 bytes (informational only; the runner admits resources itself) |

## Source identity versus b34 and main (Git blob ids)

| Path | HEAD = b34 blob | origin/main blob |
| --- | --- | --- |
| `src/api/tests/test_assistant_release.py` | `b8aa64e887e1...` | differs (this branch's test delta) |
| `src/api/tests/assistant_process_worker.py` | `99896e373682...` | absent on main (new, test-only) |
| `tools/rpi-checks.py` | `4ead23d7543f...` | same |
| `src/core/src/zava_forward/core/mssqlstore.py` | `842d790484ea...` | same |
| `src/core/src/zava_forward/core/store.py` | `a99948569d64...` | same |
| `.github/rubric/rubric.json` | `059efb2efa0a...` | same |

`git diff --stat origin/main HEAD` outside `.copilot-tracking` lists only the two test files (289 insertions, 2 deletions).

## The two new real process methods

Both live in the `ProcessRaces` mixin of `src/api/tests/test_assistant_release.py` and neither has a docstring, so verbose unittest prints one line per test:

* `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance`
* `test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment`

`class MssqlUnleasedRevocation(MssqlFixture, ProcessRaces, Base)` is guarded by `skipUnless(ZF_TEST_MSSQL == "1")`, so it inherits both. `SqliteUnleasedRevocation(ProcessRaces, Base)` runs them against the SQLite proxy and is not SQL acceptance.

## Trusted discovery and environment contract (`tools/rpi-checks.py`)

* `SQL_SELECTORS` (line 39) includes `test_assistant_release.MssqlUnleasedRevocation`; class selection therefore discovers both inherited methods. No runner change and no `--extra-test` is needed.
* `Runner.sql()` (line 2285) installs hashed `src/api/requirements.txt`, probes the driver, starts one owned disposable `mcr.microsoft.com/mssql/server:2022-latest` container bound to 127.0.0.1, waits for readiness, creates `rpi_disposable`, then runs `python -m unittest -v *SQL_SELECTORS` in `src/api` with `ZF_TEST_MSSQL=1` and `ZF_SQL_*` pointing at that container (`integration=True`).
* The worker child process inherits only forwarded keys plus `ZF_SQL_*` from the fixture's `sql_env` and forces `ZF_TEST_MSSQL=1`, so each OS process reopens the same disposable database. `ZF_DATA` is a per-test temp file.
* `--extra-test` runs outside this environment and would skip; it is not used.
* Skip rules (lines 1462-1486): with `integration=True` any skip not in `SQL_NOT_APPLICABLE` raises GateError. The only listed pair is a JSON-only hazard test, so a skipped `MssqlUnleasedRevocation` would fail the SQL group. The gate fails closed, but a passing group alone is not proof of these two methods; the log must be checked for the `ok` lines.
* `--out` limit: with `browser` selected the Chromium socket bound is 58 bytes for `--out`; the planned path is 57 bytes and fits.

Conclusion: no gap. The trusted SQL command executes both methods in the actual disposable SQL environment. This is a source-reading result only; nothing was executed.

## Exact post-run success evidence required (future FULL)

In the raw SQL group log:

* `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance (test_assistant_release.MssqlUnleasedRevocation.test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance) ... ok`
* `test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment (test_assistant_release.MssqlUnleasedRevocation.test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment) ... ok`
* Neither line carries `skipped`; the same method names under `SqliteUnleasedRevocation` do not count.
* Group exit 0, a `Ran N tests` line with N>0, a final `OK` or `OK (skipped=1)` (the one allowed JSON-only hazard skip, `SQL_NOT_APPLICABLE`, is the only skip tolerated; amended after critique), container id and published port recorded in the receipt, `images.mssql` present.

## Prior results and limits

The 194 tests / 61 skips run (2026-11-08, SQLite proxy, see the currency changes record) stays attributed to that date and source. It is not MSSQL evidence. Actual MSSQL execution, the FULL receipt, independent exact-head review, hosted checks and named human approvals remain open. This preparation is not delivery, and it neither accepts whole #107 or #104 nor establishes real-model, attestation or Azure evidence.
