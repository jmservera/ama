---
title: Personal handoff HTTP guidance checkpoint details (Refs #440 #153)
description: Exact commands, prerequisites, static expectations and recording rules for the later admitted observation
ms.date: 2026-11-11
---

## Admission-gated prerequisites

* RAW is a new directory outside the repository under the session `files/` area, for example `.../files/http-handoff-checkpoint-440-observation-1111/` (one file per command: command, start and end UTC, exit, stdout and stderr). Never overwrite a file; a second run, if Root directs one, gets a new file.
* Environment: `env -i` with an explicit allow-list: `PATH`, an owned `HOME` from `mktemp -d` that exposes the existing user-site Playwright and existing Chromium cache by explicit path variables or symlinks, `LANG`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUSERBASE` only if needed to reach the existing user site, the `PYTHONPATH` named below and the variables a row names. `ZF_DATA` unset; `~/.zava-forward` absent before and after; no `.env`, credential or provider variable. If the first import shows the isolated HOME hides Playwright, that is a preflight `blocked`, a Root pause and not a self-repair (the waiting checkpoint hit exactly this and retried natively).
* Interpreter: the existing `python3` that imports Playwright; no venv creation, `pip install`, `uv`, browser download or image pull. A missing tool is recorded raw and pauses for Root.
* Lock: `/tmp/ama-rpi-heavy.lock`. H1 only: acquire the non-queued outer lock with `flock -n /tmp/ama-rpi-heavy.lock <command>` (exit 1 on busy is a recorded pause, not a queue, a `-w` wait or a retry loop). Verify before and after that the lock holder is the H1 process (`fuser` or `/proc/locks`), and that `MemAvailable` meets the repository headroom rule. H2 and H3 take the lock themselves through `heavy_lock_or_none()` with a non-blocking flock and skip when busy: no outer lock, and a nonzero skip is a pause.
* Never wrap the combined selection in one outer lock; H1, H2 and H3 never run concurrently.

## Preflight commands (record raw, no edits)

From the repository root: `pwd`, `git branch --show-current`, `git rev-parse HEAD HEAD^{tree}`, `git status --short`, the five directory tree ids, the admitted-main comparison. From `src/api` with the explicit `PYTHONPATH`: print `__file__` of `zava_forward.api.server`, `zava_forward.core.store`, `tests` helper `dataset` and the three browser test modules, and `playwright.__version__`; assert each lies under this worktree or the existing user site. `node --version`, `python3 --version`, `ruff --version` (a missing Ruff is found here and pauses S1 before the first test), memory and lock state.

## Selectors, in order (`PYTHON` is the existing `python3`; directory for all rows `src/api`)

Environment for all rows: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`. Static expectations are re-derived on the actual merged main before the first run (class test counts, lock use, skip decorators); a difference is recorded with its cause and pauses for Root if unexplained, never forced.

| Id | Command | Static expectation | Notes |
| --- | --- | --- | --- |
| H4 | `PYTHON -m unittest tests.test_handoff_api -v` | 7 ran | Roles, refusal, bad limit, projection |
| H5 | `PYTHON -m unittest tests.test_unaccepted_handoff_csv_api -v` | 13 ran | CSV of the unaccepted rows |
| H6 | `PYTHON -m unittest tests.test_role_endpoint_inventory.RoleEndpointInventory -v` | 24 ran (14 own, 10 inherited from `Matrix` in `tests/test_role_matrix.py`) | Role matrix with the touched routes |
| H7 (optional, off by default) | `PYTHON -m unittest tests.test_content_standard.CopyAudit -v` | 18 ran | Only if Root explicitly admits it; reads `app.js` copy; a failure belongs to #153 and is not fixed here |
| H1 | `ZF_BROWSER_TESTS=1 flock -n /tmp/ama-rpi-heavy.lock PYTHON -m unittest tests.test_handoff_read_guidance -v` | 15 ran (`HandoffReadGuidanceText` 8, `HandoffReadGuidanceBrowser` 7), 0 skipped | Personal card; the browser class has no internal lock |
| H2 | `ZF_BROWSER_TESTS=1 PYTHON -m unittest tests.test_unaccepted_handoff_download_ui -v` | 6 ran, 0 skipped | No outer lock |
| H3 | `ZF_BROWSER_TESTS=1 PYTHON -m unittest tests.test_handoff_waiting_view -v` | 10 ran (`WaitingViewText` 6, `WaitingViewBrowser` 4), 0 skipped | No outer lock |
| S1 | `node --check src/zava_forward/api/web/app.js`, then `ruff check tests/test_handoff_read_guidance.py` and `ruff format --check tests/test_handoff_read_guidance.py` with the repository configuration | exit 0 | Existing tools only; mypy only if already installed, otherwise recorded not run; no install |

Sequence: H4 to H6 (H7 only if admitted) without the browser variable, then H1, H2, H3, then S1, one run each. Total static expectation 7 + 13 + 24 + 15 + 6 + 10 = 75 tests (93 with H7), zero skips, zero failures; the observation does not equal the coordinator's candidate combined commands and no reconciliation is forced.

Not selected: whole API suite, the 149-module set, full or `--changed` gate, `test_accessibility_baseline`, `test_workbench`, whole `test_role_screens`, SQL Server, Docker, scanners, services, cloud, provider, model, default or private datasets, acceptance or assistive-technology testing.

## Cross-feature contract checks recorded from the runs (no new test)

* Personal card states: H1 Node cases for 403, other HTTP, malformed success, transport, abort, 401 and empty or rows; H1 browser for constructed 403, 500 and malformed, and the manual reload recovering real backend rows. Constructed means a `page.route` response, not a backend status.
* Coexistence: H2 for the unchanged CSV links and distinct helper text; H3 for the staff screen reachable and unchanged beside the personal card.
* Route and projection: H4 to H6 for roles, projection and inventory.
* Copy: H7 for the audited `app.js` copy.

## Recording rules for the later documentation step

* Append one section to `docs/architecture/cutover-evidence-pack.md` per the plan's contract; quote raw output from RAW; correct nothing earlier in place; the witness and model label are asserted, not attested. Link the log entry in the append-only `docs/reference/log.md`.
* Carry candidate evidence (PR 1449 frozen head `2db08d8e2`, Root's raw 149 with 13 skips, 15, 16, the 153 native counts, the independent Functional and Readiness approvals with zero findings and the Root verification comment `https://github.com/jmservera/ama/pull/1449#issuecomment-6793048206`) only in a labelled "candidate history, not main evidence" paragraph. Never relabel a candidate log as main execution; state tree equality separately from the actual commands.
* Qualify every requirement id by document path, version, status and blob re-read at the pin. Keep BRD `draft`, PRD `in-review`, ADR 0007 `Proposed`, the named-human wording review, OD-09, operational, assistive-technology, reflow, zoom, large-queue, remaining AC-120 and whole 83, 81, 153 and 440 gaps. State that no fresh web-interface review is performed unless a web file changes and that the browser 403 and 500 are constructed responses.
* Record process history as qualified outcomes without rewriting it: the 153 native correction of its test after five assertion failures and its rerun of lock, format and `PYTHONPATH` steps without a Root pause; the waiting checkpoint's unauthorized native environment retry and Root publication-sequencing and end-of-file check error; fresh Root verification authorised separately, not retrospective permission.
* No issue, PR, branch, remote or board action; no tick or closure.

## Resume steps (for Root)

* Wait for the dependency: PR 1449 actually merged and a Root pinned-main amendment (`.copilot-tracking/plans/2026-11-11/http-handoff-checkpoint-440-1111-admission-amendment.md`).
* Commit the amendment before any test, then merge the admitted main ordinarily into `docs/handoff-http-checkpoint-440-1111`.
* Resume from state `.copilot-tracking/rpi-sessions/2026-11-11/http-handoff-checkpoint-440-1111-state.json`, Implement phase, Phase 1.

## Source-unchanged proof (plan launch)

At freeze, the planning commit descends from `ab44d42faae8dc3e69d2a149a067a29aca59f5e0`, `git diff --name-only ab44d42faae8dc3e69d2a149a067a29aca59f5e0 HEAD` lists only `.copilot-tracking/` paths, and the `src`, `docs`, `infra`, `tools` and `.github` tree ids equal the base ids in the research.
