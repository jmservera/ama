---
title: Resident chat review correction changes
ms.date: 2026-10-28
---

Task: 520-review-correction. Execution: Partial; original Review Complete / Not accepted.
Scope: P01/P02 implementation then P03 original Review/publication.
Plan/details/research use the same slug under their dated canonical directories.
Earlier artifacts and original adverse outcomes remain unchanged.

## P01: Protocol and behavior

P01-T01/T02 implemented. Verified codec sid returned by login/session and required
as exactly one canonical X-Resident-Session on view/chat/agenda/logout. Invalid
cookie remains 401; missing/malformed/mismatched binding is explicit 409 with
session_changed before personal reads. Header cannot choose a case. CSRF retained.
Broadcast hints trigger fenced server comparison, not identity/permission adoption;
one transition epoch protects session/login/view/logout/failure continuations.
Clearing disposes callbacks, transcript, permission and personal page together.
Shared chat.words tokenization handles punctuation for both routing and periods.
Manual focus selects visible heading/email/retry, otherwise launcher. Original
untrimmed draft comparison preserves later typing. Closed chat cannot automatically
handoff to callbacks. Critique PC-001/002 applied; PC-003 unsupported restriction
rejected. No material divergence or new user decision. All phases explicitly
requested; automatic session mode has not been inferred.

## P02: Focused evidence

Added three unit methods (within maximum eight), removed none. Existing Client
tracks tab sid independently of cookies and supports actual duplicate HTTP headers.
Tests cover A/B cookie switch, same-resident fresh sid, absent/empty/short/long/
nonhex/nonASCII/duplicate/joined headers, sid without cookie, no personal reads,
and six punctuated morning/afternoon searches with matching offered-slot hours.
Expanded actual Chromium harness covers all five findings with pinned axe, shared
pre-opened pages, late notifications, held old responses, unnotified cookie
replacement and explicit no-focus/no-search assertions. API README updated.

Initial focused HTTP 62 tests passed. Expanded owning HTTP/agenda/check set:
71 tests passed, no skips. JS syntax passed for both changed scripts.
Initial targeted lint found one import-order issue, fixed with existing Ruff.
Initial mypy found six new-test typing errors; fixed using explicit dict/str
guards, no casts or suppressed diagnostics. Final API mypy: 94 files passed;
targeted Ruff/check-format100 and git diff --check passed.
Fresh guideline source retrieved before changed-web review. Native semantics,
existing labels/live regions, focus styling and reduced motion preserved; no new
in-scope guideline issue found. This is not human/AT/WCAG acceptance.

Browser run requested through task-owned nonblocking lock wrapper, retry every
60s up to 40m. First observations: lock occupied; no foreign process interrupted.
Actual browser/axe result is not passed.

First browser admission acquired after 35 occupied-lock retries. The first
execution failed in new harness setup: removing a Playwright handler before
fulfilling its held route caused "Route is already handled", before application
assertions. Corrected one-shot session/view interception using times=1 instead
of premature unroute. This is a test synchronization correction, not weakening
an application assertion. First failed external output directory remains
/tmp/ama-520-review-correction-browser-20261028-1; rerun uses a fresh directory.

The corrected rerun could not acquire the heavy lock in its full 40-minute
nonblocking/60-second admission window and exited 1 without executing Chromium.
External original log:
/tmp/ama-520-review-correction-browser-20261028-2.log.
No owner was interrupted, lock bypassed, tests skipped or false pass asserted.
The corrected harness remains implemented-unverified. Browser/axe and publication
are blocked; do not resolve remote threads before a verified push.
Final focused ChatApiTests rerun: 12 tests passed, including stale book/cancel
bindings. Final eight changed Python files pass Ruff/check-format100; API mypy
passes 94 files; diff/JS syntax checks pass. Generated task-created Ruff/mypy
caches were moved to this session's external files/generated-caches directory,
not deleted; no ignored inputs remain.

Ordinary coupled scope reconciliation: the new protected-view binding also
requires explicit sid headers in the existing SQL browser, sensor-browser
selector and image-check direct HTTP probes. Updated those three canonical
checks rather than weakening runtime binding or their existing isolation
assertions. No new harness, test method, authority or material decision.

## Validation and Remaining Work

Focused units/static/types passed; browser blocked after the bounded lock retry.
One original independent Review completed, canonical outcome Not accepted.
RV-001 High preserves the required browser/full-gate publication evidence gap;
RV-002 Medium identifies the delayed logout response cookie-clearing race.
The source/user-requested fixes are implemented, not accepted or browser-verified.
Route RV-002 to later implementation and RV-001 to evidence completion; do not
repeat the original Review or imply that passing HTTP tests closes its findings.
Full exact-head gate, receipt verification, push and resolution are not performed:
the candidate lacks required browser evidence and has an open Review finding.
Do not consume a full heavy gate for this known non-final candidate or bypass
publication requirements. The bounded lock retry has already been exhausted.
Human/AT/native zoom/real-model acceptance remains unperformed and separate.

## Local Commit Handoff

The owner requested a local Conventional Commit with original RPI evidence.
Authenticated account resolved afresh using gh api user: id 8036360, login
jmservera; local author/committer email derived as
8036360+jmservera@users.noreply.github.com. Include the exact requested Copilot
trailer. Commit this blocked handoff, not a purported passing candidate.
Remote topic remains 685547ed; fetched origin/main remains
413ccaf253fce4566e855bae9d0a924b2a82b506. Earlier artifacts are untouched.
No push, thread mutation, PR body change, Azure operation, .env or private dataset
read occurred. Original PR body digest captured during the cycle:
bc9673e9670eb68be7b5c57b601b27d81d4d96d990bd3b7a56a2b7d1ebedfc5e.
