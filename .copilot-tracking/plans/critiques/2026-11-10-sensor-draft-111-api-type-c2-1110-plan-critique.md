---
title: Issue 111 API typing C2 plan critique
ms.date: 2026-11-10
task_id: 111-api-type-c2-1110
---

One pass by the planning agent (no new agents); verdict compatible with changes; not independent.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Module-level stanza is the dominant precedent but wider than needed. | Applied: exact-call ignore (precedent `scale_load.py:102`), no config edit. |
| 2 | A typed helper or `Any` wrapper would hide the same untyped call. | Rejected per the grant. |
| 3 | Local run lacks CI `PYTHONPATH`. | Accepted; error identical on reproduction; re-run after fix with the same environment and note it. |
| 4 | MSSQL carry-forward needs proof. | Applied: diff shows only the typing line changes; runtime and dependency inputs unchanged. |
| 5 | Browser failure could be unrelated. | Stop for Root, no repair, no retry. |
