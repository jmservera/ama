---
title: Issue 191 sensor plausibility review
ms.date: 2026-10-15
---

Outcome: conformant with the acceptance criteria, one open item.

* Fail on out-of-bounds or flat-line: covered, with negative self-tests of the checkers.
* Ranges from #178 or labelled exercise values: exercise values, labelled; open item until #178 retrieves a source.
* Fault and missing rates match injection: covered by tolerance tests on profile mix, dropout and outlier rates.
* Risk: tolerances are statistical but the seed is fixed, so results are deterministic.
