---
title: Issue 1300 C1 correction changes
description: Changes record for C1 of candidate d07812a2
ms.date: 2026-11-10
---

## Opening

Changes record opened at tool clock 2026-11-10T03:25:07.885814+00:00, before the first C1 source edit. Source edits follow it; edit order inside the session is otherwise not provable.

## Planned source edits

* `tools/rpi_phase_witness.py`: defects 1, 3 and 4 per the plan and details.
* `tools/test_rpi_phase_witness.py`: focused regressions.

## Changes

(appended below as work proceeds)

* `tools/rpi_phase_witness.py`: `verify` now requires `launch`; any non-launch boundary without a preceding successful launch is qualified. `inside_tracking` requires the tracking root under the repo and the target under the root; `log_contained` checks directory, `events.jsonl` and `events.lock` before any open in record (refused, exit 2, no write) and verify (finding, log not read); verify skips hash/open for an artifact path outside tracking; `dirty_identities` does not hash an outside-tracking path. `early_source_changes` qualifies committed source changes between the earliest observed HEAD and the HEAD at implement-start (explicit ancestor check, `diff -z`), or reports inability to compare. Rename handling untouched.
* `tools/test_rpi_phase_witness.py`: fixture `observe_launch`/`launched_run` (the `full_run` contract kept without launch so the reviewer's external script still runs); new tests for no-launch qualification, early clean source commit, tracking-only commit and non-ancestor comparison, substituted external artifact symlink, replaced tracking root, log and lock symlink targets; positive launch run verifies 0.
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` step 5: qualification list adds missing launch, committed source change before start and path outside the tracking root; one wording fix ("at later boundaries, the canonical artifacts") from the static Low.
* Mistake recorded: a whole-`tools/` `ruff check --fix` touched 12 unrelated tracked files; they were restored with `git checkout --` (own worktree, only those files) before any commit. Not in the delta.

## Validation (focused tier)

* d078 adverse (before edits, 2026-11-10T03:23:14Z): external script 4 tests FAILED (failures=3: 01, 03, 04); rename probe test 02 passed; `test_rename_config_repro.py` OK.
* After: external script 4 tests OK (0.859s); rename config probe OK; `python3 -m unittest tools.test_rpi_phase_witness` 24 tests OK; ruff check and format --check on the two files pass. Earlier mid-run external failures (1 fail, 1 error) were my fixture rename collision, fixed by keeping `full_run()` unchanged.
* HVE: see `.copilot-tracking/hve-builder/2026-11-10/issue-1300-c1-behavior-report-1.md` (static Pass, behavior simulation Revise with Low gaps, native not available).
* Not run: full gate, `rpi-checks`, AC3 native exercise (Deferred to coordinator).
