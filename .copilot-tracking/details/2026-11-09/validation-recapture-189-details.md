<!-- markdownlint-disable-file -->
# Issue 189 validation recapture phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/validation-recapture-189-plan.md).

## P2 Preconditions

`git status --short` empty; `git rev-parse HEAD^` is `d985f149590f83a50a6d9db08312f21ecf7bc01b`; `git diff --name-only d985f1495 HEAD` only under `.copilot-tracking/`; `git fetch origin` then `git diff --stat 8d6f029ca origin/main -- src infra tools` empty; `env | grep -c '^ZF_'` is 0 and `unset ZF_RESIDENT_AZURE_TEST ZF_RESIDENT_MSSQL ZF_SQL_SERVER ZF_SQL_TASK_MANIFEST` before every producer; `sha256sum` of the axe asset equals the pin.

## P3 Capture layout

Owned directory outside the repository: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/capture-189-validation-recapture/` (created fresh with plain `mkdir`, which fails if it exists; never reused, never deleted). Per producer `<name>.stdout`, `<name>.stderr`, `<name>.exit`, `<name>.cmd`. Wrapper (saved as `run.sh` in the directory): `"$@" >"$n.stdout" 2>"$n.stderr"; rc=$?; printf '%s\n' "$rc" >"$n.exit"` with no `errexit`, no pipe, no `tee`; a missing or empty exit file means not run. Plus `env.txt` (versions, resolved module paths of `zava_forward.api`, `zava_forward.core`, `zava_forward.agents` and each test module, `ZF_` variable count only), `identity.txt` (HEAD, tree, `src`/`infra`/`tools`/`.github` trees, origin/main, `git status --short --ignored` excluding caches, a content hash of tracked `src` taken before and after the capture), `hashes.sha256` (sha256 of every raw file, written last, then `sha256sum -c` run) and `hashes.sha256.sha256`.

Commands from `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest <module> -v` for the eight modules. From `src/core`: `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_priority_order -v` and `test_resident_decisions -v`. Browser from `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js`. Syntax: `node --check src/api/src/zava_forward/api/web/app.js` and `.../web/simulator-control.js` (paths confirmed before use). Each producer must report a nonzero test count reconciled with the verbose ok and skipped lines; the browser must print every expected state and finish with exit 0. Producers run sequentially; nothing queued; only the run's Chromium and an ephemeral loopback port; no process is killed by name.

## P4 Records

Skips (decorator reason strings, grouped with counts) and observed guard refusals are recorded separately; if no actual refusal occurs the record says so. The manifest sha256 and its retained location are written into the changes record. Raw logs are not committed.

## P5 Equivalence proof

`git diff --name-only d985f1495 HEAD`; `git rev-parse d985f1495:src HEAD:src` (and `infra`, `tools`, `.github`) equal; recorded in the changes record and handoff.

The proof is run again after the evidence commit exists, against the committed HEAD, and a final `git status --short` must be empty.
