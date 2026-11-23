---
title: Critique, issue 149 live r3
ms.date: 2026-11-23
---

Executed once. Verdict: proceed.

* Risk: `has_not_text` also matches a status node that is empty; intended, since the tile note is empty until a tile fails. Direct disposition: keep.
* Risk: the count-notice regex anchors the full text, so a count notice with other text would be treated as the tile note. Disposition: the existing test asserts the count pattern; the check also asserts the tile note text in the failure state.
* Scope: a check-script fix does not touch the page or the workbench recipe SHA (verified by grep). Owner-gated criteria are not ticked.
