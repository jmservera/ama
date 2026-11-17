---
title: Issue 1844 review
ms.date: 2026-11-17
---

## Review (one pass, self-review by the worker; independent exact-head assessment still required)

Outcome: conformant for the bounded defect, with open items.

* CSS change is scoped to max-width 600px and leaves the expanded dialog rule (higher specificity) intact.
* The test fails without the CSS and passes with it; own-served-byte identity is captured.
* Open: the 600px breakpoint also affects 321-600 px widths, covered only by the existing 390 px checks; the hosted CI, independent review and human approval are not obtained; no axe-incomplete or assistive-technology work done; a pre-existing intermittent filter-focus assertion remains.
* Unmet acceptance criteria: independent exact-head assessment and hosted CI; explicit narrow expand/collapse/reopen assertion in the new test; the issue's parent-topic base was not used (brief says main), so PR targeting is the coordinator's decision. Use `Refs #1844`, not a closing keyword.

## Correction cycle 1 (2026-11-17)

Independent-review findings 1-3 were verified as real and addressed in `map_fullscreen_browser_check.py` (expand/collapse/reopen focus and selection at 320/390, DOM-order keyboard assertion with hit-tests, unused `base` removed, 321-600px limitation recorded). Evidence and commands: changes artifact, correction section. The earlier "Not covered" record is retained. Remaining: the known `filter label and focus fit at 390x568` flake (not fixed, not seen in 2 reruns); assistive-technology testing and human review open; no conformance claim.
