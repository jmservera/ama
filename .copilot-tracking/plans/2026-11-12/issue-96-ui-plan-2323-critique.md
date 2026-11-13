---
title: Issue 96 Funding screen saved Held copy checker UI plan independent critique
description: Independent critique of the prospective UI plan, run once in a separate agent context against committed plan b8702f97b
ms.date: 2026-11-12
---

## Execution and verdict

Critique executed once by a separate `rubber-duck` agent context (not the author), read-only, against committed plan `b8702f97b` (head `b8702f97ba9effa21f8a23816ac207938d1fe305`) before any revision. The critic edited no file and ran no test. Verdict: Revise. Every finding is compatible with the confirmed constraints; none needs a user decision except CR-1, which needs the root decision already named as gate G4. The critique is not repeated for this task.

## Findings and dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CR-1 | High | `api()` re-serialises parsed JSON (`app.js:69`), so a float `12.0` or an integer above 2^53 in a genuine copy changes the digest (`form_export.py:37`) and is falsely `Invalid`. A raw fetch bypasses the required shared helper; documenting it is unsafe. | Accepted. D4 and G4 rewritten: only a numerically faithful corrected backend or an explicit root-recorded panel-local raw-text exception is acceptable; "document the limit" is rejected, which supersedes option 3 in the research. Task stays blocked until the root decides. |
| CR-2 | High | "The saved copy matches the working review" overstates; the comparator checks selected client-supplied data and accepts self-consistent forged metadata (`form_export.py:124`, `:163`). | Accepted. D7 Current wording now says the details checked match and that the file is not shown to be genuine. |
| CR-3 | Medium | Status table inexact: empty body becomes `{}` and reaches the mismatch 400; further 403 causes; other `ValueError` 400 texts; 404 can be a missing case. | Accepted. D8, G3 and the details checklist corrected; UI shows its own 400 text and no longer promises the control hides after every 404. |
| CR-4 | Medium | M1 closure test too narrow: core also catches `TypeError` around the digest and saved-input block (`form_export.py:124-129`). | Accepted. Repin checklist item 4 adds injection inside that block. |
| CR-5 | Medium | `h()` wraps `onclick` in `AsyncAction.handler`, which already owns `disabled`, `aria-busy` and restore (`app.js:21`, `async-action.js:54`); focus restore inside the handler would run while disabled; body focus cannot prove the user did not move focus. | Accepted. D5 and D6 rewritten to use the wrapper unchanged, test the focus behaviour first, restore only after re-enable and only from `body`, and test deliberate focus moves. |
| CR-6 | Medium | A user can change file while pending or after a result, leaving Current beside the wrong file; whole-page render replaces the "stable" region. | Accepted. New D11 clears results on selection change, ignores obsolete responses, and states that a re-render builds a fresh empty region. |
| CR-7 | Medium | Pending key is built from path and chosen body fields, not the read; the 8 MB limit applies to serialised bytes too; `e.generic` exists only for parsed HTTP errors; 401 follows JSON parsing. | Accepted. D8 and D11 add a local in-flight flag, the serialised size limit, and network, unparseable and abort handling; Phase 1 tests added. |
| CR-8 | Medium | The existing request listener attaches after reload (`held_form_download_browser_check.py:143`, `:160`, `:192`), so it cannot prove no POST on load; one global allowance does not prove one per press. | Accepted. D10 rewritten: attach before navigation, exact path and per-action count. |

## Noted without change

`textContent` rendering, native labelled input, default-off gating, the carried budget and the implementation gates were assessed as sound. `accept` is a picker hint only (recorded in D11).

## Limits

Read-only critique of a plan; no code, test or browser run. It does not approve the plan for implementation: the backend is unapproved and G1 to G5 are open.
