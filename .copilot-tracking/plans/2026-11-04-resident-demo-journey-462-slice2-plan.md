---
title: Plan for #462 slice 2, 320px resident journey fixes
ms.date: 2026-11-04
---

* Slice 2 (this PR, stacked on PR #1042): fix gaps 1 to 5 in the research. Later (not started): assistant panel length, deployment of both slices to ca-resident-demo, owner-run authenticated live checks.
* Phase 1: shorten the banner, make the sign-in lede signed-out specific, name the missing field in login errors with `aria-invalid`.
* Phase 2: show sensor times as UK time, enlarge chart axis labels, shorten the sign-out failure message.
* Phase 3: static unit tests and one browser-check assertion.
* Validation tier: focused (unit tests, loopback Chromium sensor check, ruff, mypy with `--cache-dir=/tmp/mypy-530`). No gate, benchmarks or full suites.
* Critique: executed once, inline. Compatible findings applied: keep the Legal and Data Protection Officer sentence verbatim (existing tests depend on it); keep `datetime` attributes in UTC so the exact alternative remains; set the signed-out lede only on the sign-in view so a signed-in user does not see it while loading. No significant or divergent issue.
* Details: [details](../details/2026-11-04-resident-demo-journey-462-slice2-details.md).
