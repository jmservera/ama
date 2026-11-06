---
title: Issue 80 r12 research, harness test isolation and README correction
description: Prospective research for a test-only isolation fix, a README correction and a current-head preservation proof, no deletion
ms.date: 2026-11-06
---

* Task: excel-transition-80-r12-test-isolation, parent r11 harness hygiene. Intake HEAD 5fa4496406b34213675da796901c56ee29f8125f, tree cfe6507aa2f357c221b40c193e781dac1389fa66, main bb3a3b03, parent ead177ef unchanged.
* Disposition: executed (read-only). Planning Readiness: Ready.
* Worktree state at intake is NOT clean: tracked status empty; ignored status lists exactly the three `src/{agents,api,core}/src/zava_forward/*/__pycache__` directories and the empty repo-root `.venv`.
* Chronology qualification: the r11 Research, Plan and Details were created concurrently at 13:46:25.833-.834 (before any test or source edit) and were not serial completed phases. This round does not claim the old strict ordering. r12 Research is written first, then Plan, then Details, each after the previous one finished.

## Findings

* `src/api/tests/test_browser_harness_scratch.py` line 13-15: `test_default_scratch_parent_is_unchanged` clears the environment and calls `harness.scratch_parent()` on the real `harness.ROOT`. With `ZF_BROWSER_SCRATCH` cleared, `scratch_parent()` creates `ROOT/.venv` in the actual checkout, even when the validation caller had chosen external scratch. A test of the legacy default therefore mutates the checkout.
* The same file already uses `unittest.mock.patch` for environment control (`patch.dict`), the existing pattern to reuse. `patch.object(harness, "ROOT", tmp_root)` inside an owned `tempfile.TemporaryDirectory` isolates the default branch without a new helper or production change.
* `src/api/README.md` lines 1312-1316: the new paragraph says the harness "drops the caller's bytecode settings from the server it starts". After r11 `child_env()` passes `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` when set, so the sentence is stale. The correct current statement: the default scratch location stays under the repository `.venv` (legacy); an explicit absolute `ZF_BROWSER_SCRATCH` outside the checkout overrides it; configured bytecode controls reach the server child.
* The harness helpers (`scratch_parent`, `child_env`) need no change for this finding.

## Preservation gap (root finding)

* The r11 archive `/mnt/ama-gates/e80-r11-r64-1106/preservation/snapshot.tar.gz` (sha256 198e5bf5...7487, 8183 members) predates three r11 tracking records (Changes, Review, state) and will predate the r12 records. It is valid for its recorded baseline only and is not a complete current-head snapshot.
* The old external helper's protected check iterated rows present in its own inventory, so a deleted original would not be found, and the index-list hash alone is not byte proof of protected source. It is not reused as proof of current protected bytes.
* The r12 proof will be built after all r12 commits from the frozen final head: inventory every current tracking member (opaque symlinks, no target following), the exact four generated paths, and all tracked source identities obtained from `git ls-files`/`git ls-tree`; archive, full readback, restore into a new empty external location without following links, compare type/mode/size/sha256, detect missing, extra and drifted members, and compare production and harness bytes with `5fa44964`. Location: new `/mnt/ama-gates/e80-r12-r65-1106` (refuse overwrite). No further tracking commit after the snapshot.
* `tools/tracking_retention.py` remains hardwired to the PR 438 manifest; it is policy guidance only and is not modified.

## Limits

* No deletion authorised. No browser, server, SQL, lock, install or FULL. Focused four-test module plus Ruff, format and mypy on the changed test only.
