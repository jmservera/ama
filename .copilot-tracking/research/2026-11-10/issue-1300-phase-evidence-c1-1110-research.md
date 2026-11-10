---
title: Issue 1300 C1 correction research
description: Research for first source review-correction C1 of candidate d07812a2
ms.date: 2026-11-10
---

## Opening

* Task: `issue-1300-phase-c1`, parent `issue-1300-phase-initial` (candidate `d07812a23a5803a1a2a6bcdbc68081931816f503`, tree `a3bd26047ad3be8e699cefc093a62737b8a65f92`).
* Research opening state written at tool clock 2026-11-10T03:23:08Z, before the findings were read. The phase witness helper did not witness this task's phases (the helper under correction is the candidate itself).
* Original d078 research, plan, critique, changes and Review records are preserved unchanged.

## Correction consumption (C1)

* Authority: the owner's existing FIVE TOTAL default for this fresh issue. This is C1 of five, not five additional, not an extension or reset, and not authority for another issue.
* Basis: d078 received its first independent review (REQUEST_CHANGES, 1 High and 3 Medium as originally reported). Coordinator reconciliation of issue, PR, session, worktree and history found no earlier #1300 source candidate or debit.
* Residual uncertainty: this is reconciliation evidence, not a proof of zero historical correction consumption. If an earlier actual #1300 debit is discovered, stop and reconcile before further corrections.
* Not authorized here: C2, any other issue, budget, D5, approval or #1296 clauses. #185 remains UNKNOWN; #132 remains 5/5 spent.

## Findings and dispositions (read ledger, not only the summary)

| Original finding | Original severity | Later disposition | C1 action |
| --- | --- | --- | --- |
| 1 Missing launch excluded from verify | High | Confirmed by actual run | Fix |
| 2 Staged rename origin dropped | Medium | Default rename probe PASSED (tool1064 case 2); `diff.renames=false` probe PASSED (tool1067, 0.158s); reviewer withdrew the unconditional claim | Do not implement. No speculative rename or classification change |
| 3 verify follows substituted symlink; tracking-root symlink bypass | Medium | Confirmed; the hash attempt was intercepted before reading an owned dummy target | Fix |
| 4 Clean committed source change before implement-start unqualified | Medium | Confirmed | Fix |

Confirmed defects are three (1 High, 2 Medium), not four. No actual external secret read is claimed.

## Retained adverse reproductions on unchanged d078

Run at tool clock 2026-11-10T03:23:14Z in this worktree with the external reviewer script (owned temporary repos only):

* `test_initial1300_functional_repros.py`: 4 tests in 0.528s, FAILED (failures=3): tests 01 (missing launch), 03 (external symlink hash) and 04 (early source commit). Test 02 (rename) passed. Exit 1.
* `test_rename_config_repro.py`: 1 test, OK (0.157s).
* Root's separate runs (reported, not re-run as evidence): tool1064 4 cases 0.606s, failures 1/3/4, case 2 passed; tool1067 rename case passed; original 18 unit tests OK in 1.269s. Passing suites do not waive the failing safety repros.

## Root causes (source read at d078)

* Defect 1: `verify` iterates `EVENTS[1:]` so `launch` is never required, and `record_event` skips the missing-predecessor check for `research-open` (`ORDER > 1`).
* Defect 3: `inside_tracking` resolves the tracking root without requiring it to stay under the resolved repo. `verify` and the log/lock path code use `repo / path` and `is_file()`/`sha256_file` without re-checking containment, so a replaced artifact or tracking-root symlink is followed.
* Defect 4: only the dirty-source set at `implement-start` is checked. Earlier recorded HEADs are never compared with the opening HEAD, so a clean commit changing source before opening is invisible.

## Planning Readiness

Ready. Research disposition: executed (bounded reads of known target files and supplied findings; no open-ended exploration).

## Limits

* The witness remains a local writable record, not tamperproof, not host or model attestation. Invisible edit and revert activity between observations is not claimed detectable.
* HVE remains Major. Original static, behavior (Deferred) and Review results stay preserved; C1 additive stages follow.
