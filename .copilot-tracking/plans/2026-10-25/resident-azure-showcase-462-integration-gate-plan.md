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
