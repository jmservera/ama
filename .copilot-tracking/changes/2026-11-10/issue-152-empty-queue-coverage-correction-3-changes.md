<!-- markdownlint-disable-file -->

# Changes: issue-152-empty-queue-coverage-correction-3

Plan: .copilot-tracking/plans/2026-11-10/issue-152-empty-queue-coverage-correction-3-plan.md
Details: .copilot-tracking/details/2026-11-10/issue-152-empty-queue-coverage-correction-3-phase-details.md
Scope: full plan (P01). `Refs #152`; correction 3 of 5 total (two remain). Targeted DEMO tier.

## Adverse evidence preserved

The coordinator's failed API suite receipt (`/tmp/ama-g152-c1-1109/0024-project-api.log`: 2038 tests, 1 failure, 363 skips) and the C2 statement that final browser/current-source qualification was unperformed are original, unmodified and not a Pass. The full API suite was not rerun here, so that receipt is neither confirmed nor cleared.

## P01-T01 Integration

* Pre-merge records committed first as `dc2447cba58c145a4d00196ea31e03ab003a4099` (parent of the merge).
* `git fetch origin main` at 2026-11-10T01:43:21Z: `origin/main` = `0385ad6a50d25c98cc902f199186c4fd1b50eca7` (coordinator preview named `e9c98eb2...`; main advanced since).
* Ordinary `git merge --no-ff origin/main`: clean, no conflicts, merge commit `01e3824ef4d61bdbba7e5fe2af22e8bf6e71b6e6`, parents `dc2447cba` and `0385ad6a5`. No rebase, reset, stash, amend, cherry-pick or force.

## P01-T02 Both intents preserved

* `git diff origin/main --name-only -- . ':!.copilot-tracking'` after the merge listed exactly the four slice paths (app.js, test_queue_empty_state.py, workbench_browser_check.py, README.md): 183 insertions, 1 deletion; main's other app.js code (account label, simulator navigation, priority history controls) is therefore byte-equal to main outside the slice hunks. `queueEmptyExplanation` at app.js:466 and the `listView` empty render at app.js:821 are present. No `server.py`, navigation, intake, persistence, finance or resident_decisions change relative to main. No overlap with the 132 reservation.

## P01-T03 Recipe hash binding

* Integrity code: `src/core/src/zava_forward/core/synthetic/scenario_manifest.py` lines 92-101 compare each recorded source `sha256` with `hashlib.sha256` of the literal file bytes.
* Only occurrence of the stale value: `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` source `recipe`. Changed `4bd825e9...a320` to `56409ec2b962aab0b7ae88c092f4c299d2e1b61a88d3f0547d178279a7ac0df9` (`sha256sum src/api/checks/workbench_browser_check.py`). The workbench, fixture and navigation-test hashes already matched and are unchanged. Source set, expected data, audit, permissions, version and Proposed/unapproved status untouched.
* `docs/reference/log.md`: appended one dated correction entry following the 2026-11-07 recipe-digest precedent. No index change. The pre-fix stale-hash failure was not separately executed (not run); the comparison code and the digest mismatch are the evidence.

## P01-T04 Validation (Python 3.12.3, Node v24.21.0, venv /tmp/ama-c3-venv, editable installs of this worktree src/core, src/agents, src/api[dev]; mypy 2.4.0, ruff 0.17.1, playwright 1.64.0)

| Check | Result |
|---|---|
| `pip install -e src/core -e src/agents -e "src/api[dev]"` | RUN, ok; distributions resolve to this worktree |
| From `src/api` with `PYTHONPATH=../core/tests:../agents/tests`: `python -m unittest tests.test_queue_empty_state tests.test_content_standard tests.test_workbench` | RUN, 30 tests OK, exit 0 |
| `node --check src/zava_forward/api/web/app.js` | RUN, exit 0 |
| `mypy` (strict, project files src/tests/checks) in src/api | RUN, "no issues found in 213 source files" |
| `ruff check .` and `ruff format --check .` in src/api | RUN, all checks passed; 136 files formatted |
| From `src/core/tests`: `python -m unittest test_scenario_manifest test_needs_inventory` | RUN, 19 tests OK. A first attempt from `src/core` could not import the modules (path error), recorded and rerun correctly |
| Served `python -m checks.workbench_browser_check` from `src/api` (loopback server, committed public fixtures, `ZF_STORE=json`, no ZF_DATA or credentials) | RUN, exit 0, 108 PASS lines, Chromium 156.0.8078.4, manifest 152-ia-v1, no uncaught JavaScript errors; log `/tmp/c3-browser.log` |

Browser PASS lines of interest: empty-explanation check passed for Resident Liaison Officer, Retrofit Programme Manager, Retrofit Coordinator, Building Safety Liaison, Grants and Evidence Officer, Quality Inspector and Programme Support Officer (nonempty queues assert no empty element; empty queues assert "unknown" and no "declared gap"); "no-match is a search result, not a coverage statement"; own queue reflow at 320, 390 and 1280 px; keyboard skip link; reset focus/announcement. Contractor is excluded from the new check by the harness design.

Limits: the 320/390/1280 reflow checks cover the harness's existing queue and safety content; the empty-state text itself is asserted by content at the default 1280 viewport, not rendered at 320/390. Not run: `--changed` or complete gate, full API suite, SQL, Docker, hosted CI, independent review, assistive technology, usability, contrast measurement.

## Final commit

Recorded in the delivery response and handoff (the commit that carries this file cannot name its own hash).

## Follow-Up Items

* Two corrections remain of five total; none is inferred.
* Coordinator: independent exact-head assessment and hosted checks.
* Owner decision on a trusted coverage producer (original F1).
