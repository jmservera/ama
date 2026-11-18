---
title: Issue 215 live demo UX re-verification, research (run 3)
ms.date: 2026-11-18
---

## Opening

Issue #215 unticked criteria: (A) WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode; (B) comprehension tested with staff.
Prior live evidence on this base: `docs/reference/research/issue-215-live-alert-chat-ux-evidence-2026-11-18.md` (run 1) and `issue-215-live-populated-states-evidence-2026-11-18.md` (run 2, mocked populated states).
Opening facts: deployed API image still `zava-forward-api@sha256:5368f4e4...` (revision 0000031), resident image `zava-resident-demo@sha256:65481780...`.

## Plan of research

* Re-check live `/api/me` and `/api/law/alerts` for a changed law-store state.
* Capture the home chat open (run 1 screenshots were defective) and characterise the axe incomplete item.
* Record per-criterion proven/unproven. No Azure changes.

## Findings (research disposition: executed)

* Law store still not loaded (`services.law_alerts` false, `/api/law/alerts` 503 unknown); image sha unchanged, so criteria 2, 3a and 3c cannot be proven live beyond runs 1 and 2.
* Chat axe incomplete is `color-contrast` overlap uncertainty on three elements; manual ratios 15.52, 15.52, 10.05.
* New adverse observation: employee chat helper line clipped at 1366x900.
* Criterion 5 needs real staff; not provable for the demo.
* Planning Readiness: Ready. Evidence note: `docs/reference/research/issue-215-live-rerun3-evidence-2026-11-18.md`; evidence dir `.copilot-tracking/evidence/2026-11-18/issue-215-live-r3/`.
* Note: the state file path mandated for this run was already tracked from an earlier run (`task_slug` issue-215-live); the earlier content is preserved in git history (commit 1a79804d1) and was overwritten in the working file.
