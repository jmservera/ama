# Plan: issue 954 C3 strict mypy on the photo-flag checker (2026-11-09)

Task `issue-954-c3-types`; research `.copilot-tracking/research/2026-11-09-issue-954-c3-types-research.md`; details `.copilot-tracking/details/2026-11-09-issue-954-c3-types-details.md`.

Tier: owner-selected DEMO focused. Selected: reproduce the five hosted errors with mypy 2.4.0 under the CI install profile (from `src/api`, `mypy`), then the same mypy command after the fix, Ruff 0.17.1 check and format covering the file, `test_photo_availability` (1 test), Core `test_scenario_manifest` and `test_needs_inventory` (19 tests), and ONE actual synthetic Chromium run covering both status receipts, the 13 detector fixtures and the expected negative control. Shared heavy holder check, then ONE nonqueued `flock -n` admission on `/tmp/ama-rpi-heavy.lock`; if busy, retain unadmitted and stop (no waiter, poll, sleep loop or kill). No `rpi-checks --all`, SQL, cloud, credential, model, accessibility-tool or web redesign work.

## Phases

* [ ] Phase 1: commit research, plan, details and the one critique BEFORE any merge, source edit or validation (this commit).
* [ ] Phase 2: fetch and resolve `origin/main`, then an ordinary `--no-ff` merge of it into this branch, preserving both dated append and RPI intents; no conflict shortcuts.
* [ ] Phase 3: reproduce the five errors under the CI install profile (before the source edit, on the merged head).
* [ ] Phase 4: edit only `src/api/checks/photo_flag_stale_browser_check.py` with typed aliases and callbacks.
* [ ] Phase 5: mypy, Ruff, unit selections, holder check and one nonqueued browser admission; record commands, stdout, stderr, exits, tool versions, import paths and checker SHA before and after outside the repository, with the raw manifest.
* [ ] Phase 6: changes, one review, state, handoff; commit with the privacy email and trailer; freeze a clean local head.

## Boundaries

* Checker only; product UI/API, `pyproject.toml`, workflow and `test_auth` untouched. No `Any`, `cast` or `type: ignore` added, no config exclusion, no CI weakening.
* Preserve actual HTTP 400/503/403 behavior, assertions, the exact negative control, the overlay detector, the owner quiet definition and receipts.
* Budget: C3 of five total; two remain after C3; no reset or extra grant.
* Earlier failures, reviews, C1 and C2 evidence stay unchanged; `Refs #954`. No push, PR, issue or board write, amend, stash or rebase.
