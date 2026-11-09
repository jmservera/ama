# Issue 1258 main preparation critique (2026-11-09)

Refs #1258. One critique of the final candidate plan, executed by a rubber-duck agent. Not repeated.

Execution: executed. Verdict: Revise. Dispositions: all compatible, applied directly in the plan and details; no user decision required.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-MP-1 | Blocking | Moving merge target (`origin/main` could gain #1292) | Applied: merge the immutable SHA after re-fetch equality check |
| PC-MP-2 | Significant | Equivalence overclaim ("all executable paths"); docs hold Python and JSON | Applied: limited to `src`, `infra`, `tools`, `.github`; delta equals the pinned 36 paths; docs tooling not claimed |
| PC-MP-3 | Significant | Future #1292 textual work vs spent cycles | Applied: new issue-specific authorization required |
| PC-MP-4 | Significant | Tracking history protection and path collisions | Applied: unique `-main-prep` paths, stop rather than overwrite |
| PC-MP-5 | Minor | Merge commit identity and trailer | Applied: verify after merge |

Hosted CI is carried as unperformed, not inherited.
