# Issue 462 integration and local final gate: prospective plan and capacity admission (2026-10-25T22:33Z)

Written and committed BEFORE the gate runs. Gate execution only; not whole-PR review, not product
acceptance. No source edits, push, PR or Azure write. Coordinator source assessment precedes publication.

## Integration

* `git fetch origin main` at 22:30Z: `origin/main` is `c8d16059c0c0a22c4ffba88c6b65ac068f64accc`.
  `git merge-base --is-ancestor origin/main HEAD` returned true. No merge is needed and none is made.

## Capacity admission (observed 2026-10-25T22:31Z)

* Memory 15 GiB total, 11 GiB available; disk 21 GB free on `/` (92 percent).
* `/tmp/ama-rpi-heavy.lock` has no holder (`fuser` empty); no `rpi-checks.py`, build or test process.
  Only unrelated processes: Playwright MCP helpers and this Copilot session.
* Containers: `ama-350-feedback-sql` (793cb3650397) is up and untouched. Container 00d297e974c0 is not
  present in `docker ps -a`; stated here as observed, not changed or recreated. Previews: none touched.
* Output directory `/tmp/ama-462-local-final-gate1` is absent, as required.
* Admission: proceed with `--lock-timeout 0`. If the lock is busy or capacity fails, stop without
  queueing, killing or deleting. All venvs, browser paths, logs and receipts are retained until
  coordinator approval.

## Command (attached, no sleep loops)

`python3 tools/rpi-checks.py --all --base c8d16059c0c0a22c4ffba88c6b65ac068f64accc --lock-timeout 0
--out /tmp/ama-462-local-final-gate1`, from the clean committed worktree. Then
`--verify-receipt <receipt.json> --base <fresh origin/main>`. No commit after the gate.

## Runner coverage (read of `tools/rpi-checks.py`, before the run)

* Covered by existing discovery: `unittest discover` per project, so the new core, api tests (resident
  showcase, verifier subprocess test, resident demo API) run, plus `infra/tests`.
* Suspected gaps, reported not fixed: `checks.resident_demo_browser_check`, `Dockerfile.resident-demo`
  build (runner builds `<project>/Dockerfile` only) and the local SQL view test (needs
  `ZF_TEST_MSSQL`) are not named in the runner. Not claimed as covered; the earlier local-slice
  browser, Docker and SQL results remain the only evidence for them.

## Blocked and unchanged

G1 budget, G2 synthetic provenance, G3 SQL view and principal, G4 private write path. Cost totals
25.4677 and MTD 303.711 were recomputed; projections are not verified headroom. No real password or
verifier accessed.

## Outcome (appended 2026-10-25T23:02Z; the gate failed)

* First attempt (`GATEPID` 1377628) was BLOCKED immediately: "Candidate has ignored inputs". This
  checkout holds ignored caches and editable-install egg-info used by `/home/azureuser/.venvs/ama462`;
  nothing was deleted. The gate was rerun from a clean detached worktree
  `/tmp/ama-462-candidate-581ebda0` at the same commit.
* Second attempt: actual gate PID 1377819, head `581ebda0142551706cfe359581d427f961228460`, base
  `c8d16059c0c0a22c4ffba88c6b65ac068f64accc`, output `/tmp/ama-462-local-final-gate1`, log
  `/tmp/ama-462-gate1b.log`. It ended `BLOCKED: project-core failed (1)` at 23:00Z; failed receipt
  `receipt.json` retained, status `failed`, owner `d7f386da5fb974b32e0be065`. The API Docker controls step
  passed before the failure was reported; no other step is claimed.
* Cause (`0012-project-core.log`): 1341 tests, 1 error, 167 skipped.
  `src/core/tests/test_resident_showcase_sql.py:18` imports `mssql_python` at module level without a skip,
  and the runner's core venv does not install it. The core suite therefore fails at import. This is a
  defect in the committed test from the local slice (b7bcf019), missed because the earlier
  development venv had the package. It is not fixed here: no source edit is authorised mid-gate or in
  this turn, and a fix needs a new commit and a full gate rerun.
* Not verified: `--verify-receipt` was not run (failed receipt). No pass is claimed.
* Retained, not deleted: the output directory, venvs, logs and the clean candidate worktree.
