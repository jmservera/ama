---
title: Research for #74 home case browser evidence slice
ms.date: 2026-11-04
---

* Research disposition: executed against origin/main d8b755d. Planning Readiness: Ready.
* Delivered: #907 (core versions, links, building context) and #1038 (API routes, read-only `#/case-home/{id}` screen). Issue comments 2026-11-03 and 2026-11-04 tick criteria 1, 3 and 4.
* Unmet: criterion 2. The screen exists but has no browser, WCAG or reflow evidence, and the allocation list printed raw JSON (not plain language).
* Not in scope: version-recording form, building record versioning, hosted evidence, independent review, owner closure.
* Smallest slice: a browser check for the screen, plain-language allocation wording, README note. Web-only; not security, infrastructure, SQL or deployment, so focused tier.
* Environment note: pip-installed zava packages point at another worktree, so runs used PYTHONPATH to this worktree's src.
