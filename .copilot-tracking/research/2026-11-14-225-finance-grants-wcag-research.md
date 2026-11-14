---
title: Issue 225 finance and grants WCAG research
ms.date: 2026-11-14
---

* Source: issue #225 criterion 4 (WCAG 2.2 baseline, textual state, keyboard) is unchecked; stacked on PR #1639 base c9d4204.
* Finding: `role-screens.js` `finance-funding` and `finance-invoices` use `screenTable` with caption, `scope="col"`, labelled `tabindex=0` scroll regions. Global `:focus-visible` exists in `style.css`; scroll-region outline could be clipped by `overflow-x:auto`.
* Gap: eligibility and claim-pack readiness lacked a State prefix; no co-funding cap or variance indicator exists in code or data (grep of src), so they are Unknown by design, not invented.
* Constraints: no new `aria-invalid` (baseline audit counts sites); no second `[role=status]` in `#regulatory-alerts`.
* Planning readiness: Ready.
