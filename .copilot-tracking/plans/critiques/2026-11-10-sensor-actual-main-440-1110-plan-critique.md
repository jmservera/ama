# Plan critique: sensor-review wave actual-main observation (2026-11-10)

Executed once, by the author (self-executed, not independent; no nested author). Verdict: proceed with amendments applied directly.

* C1 (compatible): the staged-tree qualification must be stated beside every result so no figure reads as a run on `4c1b4099`. Applied: the section says candidate validation ran on staged `d45426bd`, not post-commit and not on main.
* C2 (compatible): the `.github` exception must be exact. Applied: name `.github/rubric/scores/latest.json` blobs `b0bc2db354d0` (reviewed) and `b9c8b5d9e978` (main) and state no workflow file differs.
* C3 (compatible): hosted all-19 SUCCESS belongs to PR head `6fe2218c`, not to the merged main commit. Applied: reported as PR-head metadata; the main-commit push runs are not read here and not inferred green.
* C4 (compatible): keep the PR 1405 aftercare section out. Applied: only a neutral statement that it is OPEN and not main.
* C5 (compatible): preserve adverse items (role-inventory first failure, 22 and 13 opt-in skips, unforced `ConflictError` and `CommittedReloadError`, node checks only in handoff, witness notes). Applied.
* C6 (compatible): no new defect or refactoring claim. Applied; #1297 and #1298 cited only as existing owners.

No significant or divergent issue; no user decision required.
