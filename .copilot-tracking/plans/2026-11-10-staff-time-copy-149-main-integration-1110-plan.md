---
title: Parent 149 component-only main integration plan
ms.date: 2026-11-10
task_id: 149-copy-main-integration-1110
---

## Plan (authored 2026-11-10T00:45Z, before the merge)

Objective: ordinary-merge pinned main `ddeebd01694ddb46b456451d9ac6390347e51aaa` into the owned parent `feat/demo-content-workflows-149-1109` (head `befe28e48`), then verify the staff-time component still passes on the merged tree and record the evidence.

* [ ] Phase 1: Record research, plan, details and one critique, commit them alone (own records only) before the merge.
* [ ] Phase 2: `git merge --no-ff ddeebd016...` with the repository privacy noreply identity. No rebase, amend, reset, force push, push or PR. STOP with exact evidence on any conflict, unexpected unrelated parent source or shared-hook overlap.
* [ ] Phase 3: Verify the merge result: parents, tree, that `timecapture.js` and `test_timecapture_copy.py` blobs equal the parent blobs, and that the non-tracking diff of the merge against pin shows only the two product files.
* [ ] Phase 4: Focused validation with the matching venv (details file lists exact commands). Browser under one nonqueued heavy-lock admission.
* [ ] Phase 5: Changes record, one Review, state file, freeze commit with a clean tree, handoff file.

Done means: every selected check ran with no skip in required scope, or the exact pending step is recorded and no ready claim is made.

Out of scope: any product edit, other UX issues, whole 149 or 153 claims, knowledge-base edits, full API suite or full gate, SQL, cloud, provider, private data, push, PR, issue or board changes, primary checkout changes.

Gates: independent exact-head assessment precedes publication. Citations are `Refs 149` and `Refs 153`; no closing keyword and no criterion ticked.
