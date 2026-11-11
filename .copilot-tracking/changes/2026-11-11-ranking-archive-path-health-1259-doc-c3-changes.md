---
title: Issue 1259 documentary C3 qualification changes
description: Canonical corrected description of the 2026-11-11 failing-first replay evidence (supersedes claims in part, additive)
ms.date: 2026-11-11
---

## Status and precedence

This record qualifies [the original replay changes record](2026-11-11-ranking-archive-path-health-1259-failing-first-changes.md) and [its review](../reviews/2026-11-11-ranking-archive-path-health-1259-failing-first-review.md), which are preserved unchanged apart from a pointer. Where they differ, this record governs. Documentary correction only; no new observation, no source, test, runner or workflow change. The replay stays a 2026-11-11 replay, not original prospective failing-first chronology. AC4 stays Partial and unticked, AC5 unmet.

## 1. What old-source red proves

Operations invoked are not assertions reached. In `check_unknown` the verify, schedule, publish and exercise calls all run, but old source failed at the first assertion, the verify tuple, so later assertions were not evaluated.

* Proven red on old source `2be660e9d`: verify returns `('problem', None, True)` instead of `('problem', None, None)` for regular file, dangling link, dangling ancestor and stat failure; regular-file schedule CLI exit `0 != 1`; Store status problems `[]`; archive path present in the verify JSON of the reason-less OSError test.
* Not proven red: schedule, publish and exercise returned values (status, refusal, `due`, `next_window_start`, written, path-free, filesystem unchanged) for any scenario, and regular-file publish.
* Current source covers all of those later assertions and passes. That is a current-green fact, not an old-red one.

## 2. Counts

* Today: `Ran 8, FAILED (failures=7)` on old source; `Ran 8, OK` on current. The 8 are six methods of `UnusableArchivePathTests` plus two pre-existing `StorageAndDuplicateFindingTests` tests.
* The 7 failure records come from four methods: three standalone methods (reason-less OSError path leak, regular-file schedule exit, Store status) and four subtests of one method. Not seven failed methods, and not six failed tests.
* Old-source passes: both absent-directory controls and both pre-existing unreadable-archive tests.
* Historical, not today's observation: the 2026-11-08 and 2026-11-09 `Ran 6, failures=7` (class only) and `Ran 90` post-fix. Failure signatures agree with today's; the selected totals differ.

## 3. run.sh, manifest and exits

* The plan promised `manifest.txt`; it was not produced and was not reconstructed.
* `evidence/2026-11-11-1259-failing-first/run.sh` is a scratch-dependent log collector. It hardcodes the author's scratch root and assumes exports, replaced tests, `HOME`, data, tmp and log directories already exist. It is not a standalone, reusable or gate runner and cannot reproduce the replay by itself.
* Export, test-replacement and blob-check commands exist only in the native session log `rpi-1259-failing-first-2122.log`; setup is external to the repository. The `unittest_exit=` line inside each log is the test exit. The script's own exit status is 0 regardless, and the native receipt `native=0 tee=0` reports orchestration only, not a test result.
* Any future reproduction needs separate authorization.

## 4. Process disclosure (not conformant, not erased)

Deviations from the plan and the owner's boundaries, from the native log:

* One command ran `sed -i` over `.copilot-tracking/rpi-sessions/2026-11-11/*-state.json`, modifying 13 other tasks' tracked state files in this worktree. They were restored with `git checkout -- .copilot-tracking/rpi-sessions` (directory-wide, tracked files) before any commit, and the own state file was re-edited by explicit path. Restoration is not authorization or retrospective conformance, and a clean final state is not proof that no other transient write occurred; the log shows no forensic list beyond `git status`.
* Broad globs were used with `sed -i` on the plan and changes paths, and `git add -A` in three command chains (the first chain stopped at a failed `json.tool` before its `git add -A`). Broad-glob and `git add -A` risk was real.
* `ruff` created an ignored `src/core/.ruff_cache`, which was then removed.
* The committed raw red log had trailing whitespace stripped from one line (whitespace-only, disclosed originally); the scratch original is unchanged.
* The plan's checkboxes were edited after its prospective commit.
* `manifest.txt` missing (section 3). The `py_compile` to AST-parse substitution was not the only deviation.

## Claims superseded in part

| Original claim | Qualified by |
| --- | --- |
| Changes: "red ... across verify, schedule and publish assertions" | Section 1 |
| Changes: "6 tests and 7 failures", "Counts agree" | Section 2 |
| Plan and details: raw logs and `manifest.txt` copied | Section 3 |
| Review: "only deviation (AST parse ...)", conformant | Section 4 and the C3 review |
