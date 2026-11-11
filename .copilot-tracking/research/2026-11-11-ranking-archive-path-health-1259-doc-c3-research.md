---
title: Issue 1259 documentary C3 research
description: Audit of four documentary truthfulness findings in the 1259 failing-first replay record (documentation only)
ms.date: 2026-11-11
---

## Scope

* Task `1259-ranking-archive-path-health-doc-c3`. Initial head `ca352d7a8c90ff076f27770fe96f884726fdffff` (tree `673132067e7600f7efaf7918e552656f67c3f39e`, base `077ad5ad2`) stays unchanged in history; this work is additive commits above it.
* Admission: one documentary correction, C3 of the default five. C1 and C2 stay spent and at most two remain afterwards. No reset, no source grant, no C4. Research disposition: executed (read of the complete independent report `independent-1259-proof-2122.json`, the native log `rpi-1259-failing-first-2122.log`, the exit file and the committed records).

## Findings confirmed against evidence

1. Old red stops at the first verify tuple assertion. In `check_unknown` the verify, schedule, publish and exercise calls run before any assertion, but only the verify tuple assertion (test file line 712) failed on old source. The four subtests therefore prove verify `('problem', None, True)` against `('problem', None, None)` only. Schedule, publish and exercise returned-value assertions were not reached on old source. Separate old failures: regular-file schedule CLI exit `0 != 1`, Store problems `[]`, and the path in verify JSON. The committed changes record (lines 40-41, mapping section) and review overstate this.
2. Today's run is `Ran 8, FAILED (failures=7)`: six methods of `UnusableArchivePathTests` plus two pre-existing tests. The seven failure records come from three standalone methods (path leak, schedule exit, Store status) and four subtests of one method. Two pre-existing tests and both absent-directory controls passed. The historical `Ran 6, failures=7` and the 90-test post-fix count are historical summaries. The changes record's heading "6 tests and 7 failures" and "Counts agree" conflate them.
3. The plan and details promised `manifest.txt`; it was never created. `run.sh` hardcodes the scratch root and assumes exports, replaced tests, `HOME`, data, tmp and logs already exist. Its last command echoes `unittest_exit`, so it exits 0 even when unittest fails. The export and blob-check commands live only in the native session log. The native receipt `native=0 tee=0` reports orchestration, not test success (old-source unittest exit 1 is expected and logged inside the log).
4. Native log facts: one command ran `sed -i` over `.copilot-tracking/rpi-sessions/2026-11-11/*-state.json`, modifying 13 other tasks' tracked state files in this worktree (plus the intended own file). `git status` showed them, then `git checkout -- .copilot-tracking/rpi-sessions` restored tracked files for the whole directory before any commit, and my own state file was re-edited by explicit path. A broad `sed` over the plan and changes globs, and `git add -A` in three chains, were used; the first chain stopped at a failed `json.tool` before its `git add -A`. `ruff` created `src/core/.ruff_cache` (ignored), removed with `rm -rf`. The committed red log had trailing whitespace stripped on one line. The post-commit plan checkbox edit changed the prospective plan after its commit. These are out-of-scope or non-conformant actions; the clean final state does not prove the absence of other transient writes.

## Limits

No new observation, rerun, script, manifest or runtime is authorized. Missing facts stay missing. The native log shows collapsed outputs, so a forensic list of every touched file is not available beyond the 13 listed in `git status`.

## Superseded in part (2026-11-11 documentary C4)

The "13 other tasks" count and the first-chain `json.tool` stop above are the author's account, not exposed native output; see [the C4 changes record](../changes/2026-11-11-ranking-archive-path-health-1259-doc-c4-changes.md). The text above is otherwise preserved.
