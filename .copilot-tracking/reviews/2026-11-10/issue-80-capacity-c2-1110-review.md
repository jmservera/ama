---
title: Issue 80 capacity browser check aftercare route, review
description: Native review (not independent) of the C2 checker hunk, written after implement-done
ms.date: 2026-11-10
---

Executed once after the `implement-done` marker from the diff and `browser-run3.log`; native author review, not independent. Boundary: the checker hunk (+38) and run 3. Outcome: **OPEN FINDINGS**.

* C2-R1 (Medium, open): the whole check still exits 1, now at `capacity_browser_check.py:754` in `delayed sibling 401 after packages refresh failure` (`#app > [role=status]` stayed empty for the 60 s timeout waiting for "We could not load packages"). The `empty capacity` assertion (line 885) is still not reached, so withholding on empty is source-read only. Publication stays blocked. Cause undetermined: no baseline run, no app-defect claim, not repaired or retried by instruction.
* C2-R2 (Info, closed): the `#/aftercare` blocker is resolved at runtime. Run 3: `Manager route #/aftercare: PASS`, with exactly one 403 on the form read, the exact error text, the read-only status line, no `#ac-form`, no submit button, no POST, and no other failure or console error on the route.
* C2-R3 (Low): the allowlist marks the request expected only for scenario `#/aftercare`, GET and the exact URL; the recorder keeps every response for that URL, so a 200, a second call or a different status fails the `== [403]` assertion. Any other path, method or status stays fatal. The console filter drops errors only when located at that exact URL; no such console event was separately verified in this run.
* C2-R4 (Info): scope is the manager read-only boundary only; not aftercare acceptance, held #1401/#1402 mapping or real approvals. C2/C4/#73 and owner thresholds stay open. C1 chain remains local phase verification only (batched preflight disclosed).
* C2-R5 (Info): process disclosure of the early review draft is in the changes record.

Ranked follow-ups: 1. Root decides whether to diagnose the line-754 stage (one observation first; may be pre-existing or timing). 2. Independent exact-head review only after a targeted pass.
