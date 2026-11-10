<!-- markdownlint-disable-file -->
# Merged-wave 440 correction C3 phase details (2026-11-10)

Plan: `.copilot-tracking/plans/2026-11-10-merged-wave-440-c3-1110-plan.md`.

## P1 merge

`git fetch origin main`; `git merge --no-ff origin/main` with a normal message. Success is a clean merge, parent one the C2 head `678261eda`, parent two `bcc99405c`. Afterwards the diff against `origin/main` shows only the 440 own files. Failure: stop and report.

## P2 environment

Run `python -c` with `env -i` in the venv printing the `__file__` of `zava_forward.core`, `.agents`, `.api`, `.orchestrator`, `.importer` and `playwright`; each must lie under this worktree `src/` tree. Otherwise `pip install -e` the declared own-source distributions into a new venv under the new scratch.

## P3 observation (new scratch `/tmp/i440-c3-1110-*`, no `ZF_*` apart from the data path and the browser flag, `env -i`, `timeout`)

* C1: `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`, `python -m unittest -v test_queue_empty_state`; expect 7 run.
* C2: `src/core`, `PYTHONPATH=tests`, `python -m unittest -v test_scenario_manifest test_needs_inventory`.
* C3: `src/api`, `python -m checks.workbench_browser_check` (synthetic loopback Chromium), expect pass of the 152 additions: seven non-Contractor role empty or non-empty explanations, no-match search statement, reflow 320/390/1280.
* C4: SHA-256 of `src/api/checks/workbench_browser_check.py` against the manifest recipe digest.
* Each run records `date -u` start and end, exit, counts; logs plus `SHA256SUMS` in the new scratch.

## P4 wording

* Evidence pack: replace the distinct-count sentence with execution totals plus disclosed repeats (the five R5/R6 and four R4b/R9c), and the skip wording with the four-way R3 breakdown, marked as a C3 erratum in place with a pointer to the C3 section. Index: same breakdown. Log: append an erratum entry; original entry untouched.
* New C3 section appended at the end of the checkpoint section with own source pin, tree, blob ids, commands and exits.
