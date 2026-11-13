# Details: demo-chat-validation-parent-891-0945 (2026-11-13)

* Phase 1: `git checkout b05d927 -- .copilot-tracking` then compare `git rev-parse :path` with the source blob for each of the 15 paths; expect 15 equal.
* Phase 2 section content (heading `## Qualified local chat validation observation (2026-11-13, Refs #891)`):
  * Source `b05d927`, original failed candidate `e01ae77`, base `347962dac`; local only.
  * Table: original (36 of 37 ok, 1 error, exit 1, retrospective critique reject), recovery (37 of 37, 0 skips, exit 0, prospective critique approve_with_comments).
  * Finding: noneditable install resolved the GOLDEN fixture under site-packages and the report path failed; documented editable install resolved the worktree fixture. An environment observation, not a code defect or fix.
  * Limits: no bitwise replay (dependencies differ from `8c735ae`), probe separate from run, source-before-critique order of the original is historical, no provider/Azure/UI/privacy/per-call acceptance, #891 whole issue and AI criteria unmet, no ticks, Refs only.
* Phase 3: one index row after the role-screen row in `docs/reference/README.md`; one log entry appended to `docs/reference/log.md`.
* Phase 4: link-target check by grep for the new anchor; `git diff --stat` shows only the three docs plus 15 tracking files plus own RPI files.

## Critique amendments (applied before implementation)

* Cause wording: supported but unconfirmed; probe separate from the run; a defect is not ruled out.
* Copy exactly the 15 enumerated paths (no tree-wide checkout); verify working-tree bytes (`cmp`) and blobs against `b05d927`.
* Say "previously recorded"; `b05d927` is the evidence commit (adds only tracking files over `347962dac`), not a claim of the tested code pin; the original review passed the record, not the validation.
* Verify every new relative link and the README anchor.
