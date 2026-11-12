---
title: Handoff waiting screen feature-wave checkpoint details (Refs #440 #83)
description: Exact commands, prerequisites, static expectations and recording rules for the later admitted observation
ms.date: 2026-11-11
---

## Admission-gated prerequisites

* RAW is a new directory outside the repository under the session `files/` area, for example `.../files/waiting-checkpoint-440-observation-1111/` (one file per command: command, start and end UTC, exit, stdout and stderr).
* Private venv `/tmp/ama-440-waiting-venv-1111`: `python3 -m venv`, then `pip install -e src/core -e src/agents -e src/api -e src/importer` and `pip install playwright==1.64.0` (the `dev` extra pin in `src/api/pyproject.toml`; re-read at the admitted main; `ruff==0.17.1` only if S1 is admitted). This deliberately differs from the component README line (`--no-deps`, orchestrator instead of importer) because whether the selectors need importer helpers was not verified here; if the narrower README install suffices, use it and record that. The package index is contacted; record it. Preflight first: record the import result in the fresh venv, restore only after an actual import failure, then prove each `zava_forward.*` module origin lies under this worktree (the host's editable installs point at the primary checkout) and that `import playwright` works with the same interpreter that runs W1 to W3. Record a missing Playwright, a private `HOME` hiding a user-site install or a missing browser cache as blocked; do not hide it.
* `ZF_DATA` unset, `~/.zava-forward` absent before and after, no `.env`, no credential, no provider variable, `TMPDIR` an owned `mktemp -d` removed at the end. Run every command under `env -i` with an explicit allow-list: `PATH`, `HOME` (an owned directory with the Playwright cache reached by a symlink to the existing cache, or the real `HOME` only if the cache needs it and the `~/.zava-forward` state is proven before and after), `LANG`, `PYTHONDONTWRITEBYTECODE=1`, the `PYTHONPATH` named below and the variables a row names.
* Cached Chromium matching the installed Playwright and `node` must already exist; otherwise W1 to W3 browser cases are blocked, not installed here. The Node source cases of W1 to W3 need `node`.
* Lock: `/tmp/ama-rpi-heavy.lock` free (`fuser` exit 1) and `MemAvailable` at least the 8 GiB headroom rule. The W1 and W3 browser classes take the lock themselves with a non-blocking `flock` and raise a skip when it is busy; do not wrap them in `flock`. The W2 browser class takes no lock (critique WC-01): the lock-free and memory check is its only protection, and W2 runs only after it passes and never concurrently with W1 or W3. A busy lock is recorded as blocked, not a pass.

## Selectors, in order (existing tests only; `PYTHON` is the venv interpreter)

Directory for all rows: `src/api`. Environment for all rows: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests` (the shape the component README uses). Static expectations are re-derived on the actual merged main before the first run; a difference is recorded with its cause, never forced.

| Id | Command | Static expectation | Notes |
| --- | --- | --- | --- |
| W4 | `PYTHON -m unittest tests.test_unaccepted_handoff_csv_api -v` | 13 ran | CSV projection of the same rows |
| W5 | `PYTHON -m unittest tests.test_handoff_api -v` | 7 ran | Roles `sam` (rows), `rex` (valid empty), `kim` (403), bad limit (400), POST (404) |
| W6 | `PYTHON -m unittest tests.test_role_endpoint_inventory.RoleEndpointInventory -v` | 24 ran (14 own, 10 inherited from `Matrix` in `tests/test_role_matrix.py`) | Role matrix includes both routes and the CSV |
| W7 | `PYTHON -m unittest tests.test_accessibility_baseline -v` | 12 ran, the table inventory equals 13 | The coupling that failed on hosted CI; whole module |
| W8 | `PYTHON -m unittest tests.test_workbench.WorkbenchNavigation -v` | 5 ran | Header navigation and `route()` |
| W9 (optional) | `PYTHON -m unittest tests.test_content_standard.CopyAudit -v` | 18 ran | Admit only if Root names it; a failure belongs to #83, #153 or #149, not to a fix here |
| W2 | `ZF_BROWSER_TESTS=1 PYTHON -m unittest tests.test_handoff_read_guidance -v` | 9 ran, 0 skipped if Chromium is available (no lock involved) | Personal pending card, its transport failure guidance and the `Served` helper |
| W3 | `ZF_BROWSER_TESTS=1 PYTHON -m unittest tests.test_unaccepted_handoff_download_ui -v` | 6 ran, 0 skipped | Existing CSV links, copy distinct from the screen |
| W1 | `ZF_BROWSER_TESTS=1 PYTHON -m unittest tests.test_handoff_waiting_view -v` | 10 ran (`WaitingViewText` 6, `WaitingViewBrowser` 4), 0 skipped | New screen: one unscoped read-only GET, rows by keyboard, valid empty versus alert states, rejected and malformed responses, recheck, abort and ended-session render nothing beyond loading |
| S1 (optional) | `node --check src/zava_forward/api/web/app.js`, then `ruff check` and `ruff format --check` on `tests/test_handoff_waiting_view.py` with the repository configuration | exit 0 | Repeats Root's candidate checks on main; mypy only if the pinned version is already present, otherwise recorded not run |

Sequence: W4 to W8 (and W9 if admitted) without the browser variable, then W2, W3, W1, never concurrently, none retried. Root's own 81 command list, supplied at admission, replaces or augments this table only with a named affected surface. Pairings with the PR 1444 numbers are static: W1 to W5 = 45; with W6 = 69; with W7 = 81.

Not selected: whole API suite, full gate, SQL Server, Docker, scanners, `role_screens_browser_check`, whole `test_role_screens`, `test_role_screens_conformance` (unchanged `role-screens.js`), services, cloud, provider, model, default or private datasets.

## Cross-feature contract checks recorded from the runs (no new test)

* Staff screen versus personal card: W1 asserts reach when the personal list is empty or its load fails; W2 asserts the card's guidance and hidden-when-empty behaviour; W3 asserts the card's CSV copy states it is not the personal list.
* Guarded route and projection: W5 and W6 for roles and refusal; W1 for exactly one unscoped GET and `approved_limit_hours` null.
* Valid zero versus failure and navigation: W1 text cases for `empty`, `forbidden`, `server`, `transport`, `notArray`, `badRow`, `nullRow`, `badFlag` and the abort and ended-session cases.
* Manual case links and recheck: W1 browser cases (keyboard reach of the encoded case link, recheck repeats the read, no mutation request).
* Existing CSV and JSON: W3 and W4; no CSV, JSON or API source changed by PR 1444 (verified by the actual diff at admission).
* No automatic escalation and no global OD-09 threshold: W1 policy copy assertion and the unscoped GET assertion; this is a source and test statement, not an operational acceptance.

## Recording rules for the later documentation step

* Append one section to `docs/architecture/cutover-evidence-pack.md` with the headings and contents of the plan's pack section contract. Quote raw output from RAW; correct nothing earlier in place; the witness and model label are asserted, not attested.
* Carry candidate-side evidence (PR 1444: 69 at `dd3c3291`, Root-reported 81 with Chromium and no skips at `441fd7ed`, JS, Ruff and mypy results, hosted API job `run 42984858029 / job 130403684801` with 2850 tests, 603 skips and one failure of 13 versus 12, the original adverse records and the independent assessments with their stated limits) only in a labelled "candidate history, not main evidence" paragraph, marked UNMERGED where applicable.
* Qualify every requirement id by document path, version, status and blob re-read at the admitted main (the research lists the base values). Mark FR-066 and AC-120 as partial (no urgency, next-update or accountable-reviewer column) and record the #83 BRD source-reference drift as a finding owned by #83.
* Append one entry to `docs/reference/log.md` (never edit earlier entries); touch `docs/reference/README.md` only if an index pointer is genuinely needed.
* No API, store, permission, architecture, ADR or requirement change; ADR 0007 stays Proposed; draft and proposed stay so. State that actual OD-09 times, operational acceptance, manual assistive-technology and reflow and zoom checks, and large-queue performance remain unproved, and that a local run is narrow integration evidence, not broad user acceptance. State that this checkpoint performed no fresh web-interface review: it changes no web file.
* The #83 criterion, #81 and #440 are not ticked or closed by this record; merged children alone do not satisfy epic or whole-issue criteria.

## Resume steps (for Root)

* Wait for the dependency: PR 1444 actually merged, matching tested feature tree, coordinator confirmation.
* Commit the admission amendment (`.copilot-tracking/plans/2026-11-11/waiting-checkpoint-440-1111-admission-amendment.md`) before any test, then merge the admitted main ordinarily into `docs/handoff-waiting-checkpoint-440-1111`.
* Resume this task from state `.copilot-tracking/rpi-sessions/2026-11-11/waiting-checkpoint-440-1111-state.json`, Implement phase, Phase 1.

## Source-unchanged proof (plan launch)

At freeze: the planning commit descends from `7880b95b19525ff465cab27870ba9d55b57110a3`, `git diff --name-only 7880b95b19525ff465cab27870ba9d55b57110a3 HEAD` lists only `.copilot-tracking/` paths, and the `src`, `docs`, `infra`, `tools` and `.github` tree ids of the planning commit equal the base ids recorded in the research.
