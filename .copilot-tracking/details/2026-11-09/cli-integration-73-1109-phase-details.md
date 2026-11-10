# Phase details: cli-integration-73-1109

Plan: `.copilot-tracking/plans/2026-11-09/cli-integration-73-1109-plan.md`. Evidence: research C1 to C8.

## P01 Pre-merge qualification

* P01-T01 Confirm cwd, branch `feat/demo-exception-workflows-73-1109`, HEAD `a4317567...`, local ref `origin/main` equals `3bc20719...` (no fetch), `user.name`/`user.email` noreply. Allowed state: no tracked modification; the only untracked paths are the named RPI artifacts (research, plan, details, critique, later changes/review/state). Assert no path collision of those artifacts in `git ls-tree -r origin/main`. Merge happens before any tracking commit; tracking is committed in P04.
* P01-T02 Create venv at `/home/azureuser/.copilot/session-state/bf04da76-898b-4aaf-9f13-f4a9720bcb77/files/zf73/venv` (outside the repo and index); `pip install -e src/core[blob] -e src/importer ruff==0.17.1 mypy==2.4.0`, only actually missing deps; the package index is the only network use, and unavailability is a blocker. Proof: venv python prints `zava_forward.core.__file__` and `zava_forward.importer.__file__` under this worktree, plus `pip list` for ruff, mypy, zava dists. A pin mismatch is a failure. No PYTHONPATH.

## P02 Merge current main

* P02-T01 After Implement activation and re-check that `origin/main` still equals the pin: `git merge --no-ff -m "chore(merge): integrate current main into demo exception workflows parent (#73)" -m "Refs #73, #135. Partial CLI component integration only." -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" 3bc20719803a77490c704f985559720e23aa169d`; no fetch, rebase, force, reset or amend. Post-check `git log -1 --format='%an,%ae,%cn,%ce%n%B'` shows noreply author and committer and the trailer. Research C6 predicts no conflict.
* P02-T02 On conflict: resolve only understood paths preserving both intents; any importer or Core ambiguity stops with a blocker.
* P02-T03 Expected sets: `git diff --name-only a4317567..HEAD` equals main's delta (`git diff --name-only a04668ae9..3bc20719`); `git diff --name-only 3bc20719..HEAD` lists only `src/importer/*` and `.copilot-tracking/*` paths of the parent delta (research C1); `git diff a4317567..HEAD -- src/importer` is empty; both pins are ancestors of HEAD.

## P03 Verification

* P03-T01 From `src/importer` with the venv python: `python -m unittest discover -s tests -v`; pass = 71 ran, 0 skipped, 0 failures. From `src/core`: `python -m unittest tests.test_exception_feeds tests.test_exception_queue tests.test_exception_register` (if the register test module exists; otherwise record absence) with the installed worktree Core, pass = 0 failures.
* P03-T02 From `src/importer`: `ruff format --check .`, `ruff check .`, `mypy` (project config: `files = ["src","tests"]`); pass = 0 findings/errors at pinned versions.
* P03-T03 Separate-process script in the session scratch directory (uncommitted), synthetic data only, each step a fresh `python -m zava_forward.importer` process:

| Scenario | Construction | Command and expected oracle |
| --- | --- | --- |
| Persist and reopen | file with bytes `not a workbook` | `stage` exit 1 twice; a new sqlite connection finds exactly 1 `import_refusals` row with the sha256 of the bytes; source sha256 unchanged |
| Same basename, two dirs | `a/bad.xlsx`, `b/bad.xlsx` with different oversized/unreadable-hash content | two distinct refs |
| Replacement | rewrite the same path with different bytes then `stage` | a new ref, never merged with the first |
| Hashless | file larger than `MAX_SOURCE_BYTES` | exit 1; ref starts with `source:` (opaque), sha256 unset, not the basename |
| Unreadable | path with no read permission or missing file | recorded refusal exit 1 with per-attempt opaque identity; second attempt a new record (skip, with reason, if running as root) |
| First-reason dedupe | same bytes under two names | one row; reason is the first recorded |
| DB open error | `--db` in a non-existent directory | exit 2, stderr has `Cannot`, no `Traceback`, stdout empty |
| DB write error | DB with a `BEFORE INSERT ON import_refusals` abort trigger | exit 2, 0 rows |
| Read-only viewer | `exceptions DB` with `ZF_EXCEPTION_STAFF` naming a steward | exit 0, `items=` count, `eligibility=Unknown`; sha256 of the DB file and any `-journal`/`-wal` sidecars and every source file identical before and after |
| Missing steward | `exceptions DB` without `ZF_EXCEPTION_STAFF` | exit 0, `UNROUTED`, `items=0`, Unassigned/Unknown wording |

* P03-T04 Static assertions: `grep -rn "importer" src/api/pyproject.toml src/api/src` empty; `grep -n NOT_CONNECTED src/core/src/zava_forward/core/exception_register.py` present; `grep -rnE "(requests|httpx|urllib|openai|azure)|replay|auto_correct" src/importer/src` has no model, network or replay use (record any hit with its reading).
* Stop rule: a red result outside importer compat scope means stop and report without history rewrite; a corrective commit is allowed only for a tiny importer compat fix after a recorded red repro.
* Test ownership: no tests added or removed (`none`), existing tests are semantic coverage; a test is added only after a red repro that needs an importer compat fix.

## P04 Tracking and handoff

* P04-T01 Write changes record, review (one Review), state JSON; commit dated tracking with the noreply identity; confirm clean tree; write handoff to `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/handoff-73-cli-integration-1109.md` with head/tree/base, manifest, commands/exits/skips, owner/SHAs, dependency interpretation, limits.
