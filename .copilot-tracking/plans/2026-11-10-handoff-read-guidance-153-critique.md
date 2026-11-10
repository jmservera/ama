---
title: Issue 153 pending-handoff read-failure guidance critique
ms.date: 2026-11-10
task_id: 153-handoff-read-guidance-1110
---

## Critique (one pass, author, final candidate plan and details)

Verdict: revise, all findings compatible with confirmed decisions and applied directly.

| ID | Finding | Disposition |
| --- | --- | --- |
| C1 | Silently returning on `AbortError` is a behaviour change beyond the message. | Applied with justification: `priorityPanel` already does this and the brief requires cancellation safety. Test proves nothing is painted. |
| C2 | A 200 response with a non-JSON body makes `api()` return `{}`, so `rows.length` is undefined and the card hides: an unavailable-as-empty path. | Recorded out of scope (not a transport rejection, owner-directed scope). Reported as a follow-up; not changed here. |
| C3 | Source-slice extraction can break silently on a refactor. | Applied: tests assert both slice markers exist and the function is found. |
| C4 | A non-HTTP error thrown while rendering success rows would now show load guidance. | Accepted: still true that the card could not show the queue, never claims empty. Recorded in the changes record. |
| C5 | Browser tests may race the lock or leak servers. | Applied: opt-in, single nonqueued `flock -n`, own server and cleanup, no retry. |
| C6 | Copy must not be read as an empty queue or contain banned words. | Applied: text says "we cannot tell whether any are waiting"; lexical guard checks banned words, ASCII and absence of the raw message. |
| C7 | HTTP/401 paths could regress. | Applied: explicit VM cases for status 500 with server text and status 401 expecting the old text. |

No finding conflicts with a confirmed user decision. Critique is not repeated for this task.
