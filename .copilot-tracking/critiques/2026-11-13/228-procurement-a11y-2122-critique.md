---
title: Issue 228 criterion 5 independent critique (2026-11-13)
ms.date: 2026-11-13
---

Executed once by an independent rubber-duck agent on the first implementation. Verdict: changes required.

| Finding | Disposition |
| --- | --- |
| Keyboard entry used `focus()`, bypassing Tab | Applied: `tab_to` presses Tab until the target link has focus, then Enter |
| Table checks derived expected stops from already-labelled regions | Applied: every `table` must sit in a labelled focusable region; expected stops come from table captions |
| DOM text is not visible text | Applied: panels are rendered, `inner_text` is read, then the override is removed before the keyboard checks |
| README overstates; package row values removed | Applied: package and work-order row assertions restored; README narrowed |
| Test at 320 px as well | Applied: keyboard checks also run at 320 px |

Applying the 320 px keyboard check exposed a harness issue (Tab start point stayed on the last focus), fixed by clicking the page heading before tabbing. No product defect.
