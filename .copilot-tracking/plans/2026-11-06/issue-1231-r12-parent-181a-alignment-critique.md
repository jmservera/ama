---
title: Issue 1231 r12 plan critique
ms.date: 2026-11-06
---

## Execution

One independent read-only critique (rubber-duck subagent) of the r12 research and plan, run before any merge commit or edit. Not repeated.

## Verdict

Pass with changes.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | The child test that accepts an edited record contradicts parent validation | Accepted; expect `PublicationError` and unchanged bytes (the parent version) |
| 2 | Blocking | An existing record can be returned before the winner's directory sync, or after it failed | Accepted; sync the directory before returning a validated existing record; test race and retry |
| 3 | Blocking | Syncing the directory before removing the stage can leave a stage alias after a crash | Accepted; remove the owned stage first, then sync; keep `stage_retained`; test ordering |
| 4 | Blocking | Post-link directory sync failure reported as "Nothing was published" | Partly accepted: reword the Store message to "could not be confirmed" and test it; no new return state and no new audit path, because the critique's "uncertain outcome" state would add behaviour beyond the parent contract; the missing audit on that rare path is recorded as a residual finding |
