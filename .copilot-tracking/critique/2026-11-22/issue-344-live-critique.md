---
title: Issue 344 critique (2026-11-22)
description: One final-candidate critique of the ninth-pass plan
ms.date: 2026-11-22
---

Refs #344. Critique executed once on the final candidate plan. Verdict: proceed with the dispositions below.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | A probe-only run could be mistaken for a source change; the tier must be explicit | Applied: focused tier, no `src/` edit, no `rpi-checks.py --all` |
| 2 | Claiming parity from 13 clean pages overstates; the MVP is retired and the walk used one role (a Retrofit Programme Manager) | Applied: criterion 5 stays unproven and the note names the single-role limit |
| 3 | The ageing-fix deployment is inferred from a 200, not from an image digest comparison | Applied: wording says "consistent with" |
| 4 | Criterion 1 could be declared proven from the curl 401 | Rejected as unsafe: browser User-Agent still gets a redirect; stays partly proven |
| 5 | Screenshot `walk-10.png` shows a stale loading state | Applied: kept and explained, with the settled recheck screenshot |
| 6 | Issue checkboxes must not be edited | Applied: no checkbox change; none of the unticked criteria is fully proven |

No conflict with a confirmed owner decision. No significant or divergent issue needs a user decision.
