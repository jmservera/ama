---
title: Issue 133 implementation review
ms.date: 2026-11-13
---

Executed once by code-review. Outcome: two findings, both fixed in this task, no open material findings.

* High: the uncertainty exemption erased text up to the next stop, hiding a claim after "Unknown, but ...". Fixed: exemption limited to a whether/if phrase ending at a comma, conjunction or stop; regression cases added.
* Medium: patterns missed plurals, auxiliaries and was at fault. Fixed and tested.

The fixes were rechecked by the targeted tests, ruff and mypy listed in the changes artifact.

Follow-up: api `mypy` needs playwright installed locally to be clean; hosted CI covers it.
