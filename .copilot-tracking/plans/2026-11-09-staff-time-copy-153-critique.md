---
title: Issue 153 staff-time refusal and error guidance critique
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
---

## Execution and verdict

* Executed once on 2026-11-09T22:51Z by an independent read-only rubber-duck agent against the final candidate plan, details and research. Verdict: revise (three High, four Medium findings). No repeat critique for this task.

## Findings and direct dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | High | A 403 can follow a committed write (audit after write, `server.py:1193-1208`), so "Nothing was changed" is unsafe for unrecognised 403 | Applied: only recognised pre-write refusals claim nothing changed; any other 403 is an unknown outcome |
| C2 | High | A 409 is the client pending guard (`app.js:62`); checking records at once can miss a later commit | Applied: 409 text says wait for it to finish, then refresh and check |
| C3 | High | Ambiguous-save test assumed no entry added; the write may have committed | Applied: browser test covers both committed and uncommitted cases; the copy notes My entries lists only the latest 200 |
| C4 | Medium | A mine/report read refusal replaces the view, so checklist guidance may not be visible | Applied: load-failure 403 copy says refresh and contact support, no checklist reference |
| C5 | Medium | Missing-request and same-role refusals were merged | Applied: split into two messages with separate tests |
| C6 | Medium | Notice copy overstated approval | Applied: wording requires an approval reference covering the current wording, no authenticity claim |
| C7 | Medium | Test gaps: mine/report 403, role mismatch, audit failure, announcements, banned words and dashes | Applied: added to the test matrix |

No finding conflicts with a confirmed decision; none rejected.
