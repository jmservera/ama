---
title: Issue 96 live research, 2026-11-19
ms.date: 2026-11-19
---

## Disposition

Research disposition: reused. The 2026-11-18 live probe (`.copilot-tracking/research/2026-11-18-issue-96-live-research.md`, record `docs/reference/research/issue-96-live-demo-evidence-2026-11-18.md`) already established the facts for the only unticked criterion, "Each assisted form has an approved versioned schema".

## Findings

* `forms.register_schema` always writes `approval="Unapproved"`; no source path sets `Approved`. The deployed demo holds an empty `form_schemas` list.
* Building an approval route would create a human-authority control (named template and source-policy approval). That is a human decision and a FULL-tier, security-sensitive change, not an engineering result the demo can prove.
* Offline re-run today: `test_form_staging`, `test_form_review`, `test_form_dependencies` in `src/core`: 50 tests OK.

## Planning Readiness

Ready. Outcome: criterion cannot be proven or built for the demo; docs-only closeout.
