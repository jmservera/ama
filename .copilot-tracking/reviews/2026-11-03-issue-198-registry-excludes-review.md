# Issue 198 review: drop dead mvp excludes (2026-11-03)

* Review execution: executed once, self-review of the diff against `origin/main`.
* Outcome: conformant for the slice; the issue is not complete.

## Findings

* The diff is two files plus RPI evidence; no `.py`, workflow or lock change.
* The registry change applies only after merge and reopens every criterion. It adds no scored input (the directories do not exist). The README states a no-change expectation, not a measured result.
* Independent exact-head review, hosted CI and the owner decision remain required.

## Unmet acceptance criteria

* AC 3: per-PR dip records for the dual window (historical, not provable).
* AC 4: the old-registry-scores-the-deletion-PR sequencing cannot be proven retroactively; the registry itself now has no `mvp/` or `prototype/deploy` string.
* AC 7: no sign-off-time before and after comparison beyond #499's 77 vs 77.

## Routed follow-up

* Owner decision: accept ACs 3, 4 and 7 as historical and close #198, or supply evidence.
* Repair the 17 pre-existing rubric test failures (separate issue).
