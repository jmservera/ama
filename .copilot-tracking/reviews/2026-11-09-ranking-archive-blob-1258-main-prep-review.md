# Issue 1258 main preparation review (2026-11-09)

Refs #1258. One original Review of the main preparation, executed once after implementation by the implementing agent. It does not replace the independent exact-head Functional closure or hosted CI.

Execution: executed. Outcome: conformant with findings (documentation limits only).

## Assessed boundary

Merge commit `8033379faa83238892092a33b8b4e353776eac0b` against the plan, addendum and critique dispositions.

## Checks against plan

| Item | Result |
| --- | --- |
| Prospective records committed before the merge | Met (`c2920241`, `e54b6f2f` precede `8033379f`) |
| Immutable pin and re-fetch guard | Met; the guard fired once, recorded, re-pinned prospectively |
| No rebase, force, push, PR, board | Met |
| Delta equals pinned paths, no src/infra/tools change | Met (37 paths) |
| Equivalence limited to application trees | Met; `.github` exception named |
| Identity and trailer on merge | Met |
| #1292 not imported | Met (merge-tree forecast only, no ref or file change) |
| Unique output paths | Met |
| Source defect or ambiguous conflict | None found; no sixth cycle used |

## Findings

* RV-1 Minor: tests were not re-run; results are inherited by tree identity. Documented in the changes record; not a defect.
* RV-2 Minor: the first pin check failed because main moved by a rubric score record. Documented with the addendum; the plan stop rule worked as designed.
* RV-3 Minor: `main` can move again before publication; the coordinator must re-fetch and plan again.
* Hosted CI on this head is unobserved and must not be treated as passing.

No material finding remains open for this task. Open work is the unmet criteria listed in the changes record, owned by later user-selected tasks.
