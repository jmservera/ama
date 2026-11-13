---
title: Issue 96 saved export check amendment independent Review
description: One independent Review of the saved export check at exact head ad37cb113, run in a separate agent context
ms.date: 2026-11-12
---

## Execution and outcome

Review executed once by a separate `code-review` agent context (not the author) after the corrections, against exact head `ad37cb113` (tree `8528e5360`). Outcome: Conformant with qualifications; no open material (Critical, High or Medium) finding. Not repeated. This is the independent Review the required loop needs; the earlier author self-review stays unchanged and non-independent.

## Reviewer-stated limits (preserved)

* Ran `test_form_held_download_api` (14) and `test_role_endpoint_inventory` (24), all OK, worktree clean afterwards.
* Did not run the new tests against the pre-fix code; the fails-without-fix claim for the mixed-type copy rests on code reading. The author separately reproduced the 503 before the fix with a throwaway script outside the repository (not independent evidence).
* Did not open the three mandatory context documents or the changes file and plan; README accuracy was judged from the new section only.

## Findings and routed work

* RV-A1 (Low): the `TypeError` fallback also converts any other core `TypeError` into `Invalid`, which could mask a real core bug. Destination: later core fix or narrower handling.
* RV-A2 (Low): a body nested deep enough to parse but not re-serialise could still reach the generic 503 (`RecursionError`); not exercised, nothing disclosed. Destination: note only.
* RV-A3 (Low): tests are looser than the README: revocation accepts 401 or 403; `no-store` is asserted only on the 400 empty-body error; CSRF, administrator view-only and oversized-body paths are not asserted on this route (shared suites ran instead). Destination: later focused tests.
* Nuance: `unaffected_fields` echoes client-supplied field ids; no values are returned.
* CR-1 to CR-4 genuinely addressed; CR-5 partially addressed (as RV-A3).

## Boundaries unchanged

No reviewed or approved state, no UI, no core change, no acceptance tick, no push, PR, merge, issue or human approval. C1, C5 and C6 remain unproven. Independent coordinator exact-head assessment, hosted checks and human approvals remain required before publication.
