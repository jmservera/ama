---
title: Issue 96 UI implementation plan amendment independent critique
description: Independent critique of the plan amendment, executed once in a separate read-only rubber-duck context against commit 38ea41f18
ms.date: 2026-11-12
---

## Execution and verdict

Executed once by a separate read-only `rubber-duck` context against committed amendment `38ea41f18`. It edited no file and ran no test. Verdict: Revise. All findings are compatible with the root G4 decision and are applied directly; none rejected; none needs a user decision. Not repeated for this task.

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-1 | Blocking | `mutationKey(path)` throws without a body argument | Accepted: `mutationKey(path, {})`, acquire before read, release in `finally` if acquired |
| PC-2 | Blocking | `routeController` is replaced on navigation; signal read after the async read could send on the new route | Accepted: capture signal and session at press; recheck before POST and after response |
| PC-3 | Blocking | Numeric fixture lacks an `area` candidate with source evidence | Accepted: stage an `area` candidate from a source span and correct through the real API, twice |
| PC-4 | Non-blocking | Obsolete-selection filtering could swallow a valid 401 | Accepted: 401 for the current session handled first; old session never replaces a newer login |
| PC-5 | Non-blocking | `file.text()` replaces malformed UTF-8; pre-read size check missing | Accepted: `file.size` first, fatal UTF-8 decode, encoded size check |
| PC-6 | Non-blocking | Log or CSS edits outside the fixed scope | Accepted: removed |

## Limits

Read-only critique of a plan; no code run. It does not approve the implementation; Review remains a later separate step.
