---
title: Issue 619 live research (2026-11-23)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

## Findings

* #619 has one body with unticked criteria: person-run screen reader, keyboard and zoom testing; consent proven by a real resident journey; #550 consent step; #552 Fluent 2 and WCAG baselines. Owner comments park AT testing for production (#1907).
* Live revisions 0000054 (api) and 0000026 (resident) were created 2026-11-22 23:14 UTC; the last web or resident `src/` change on main is `a6ba1956db` (23:05 UTC); the only later src commit touches tests. Main equals live for these criteria.
* The 2026-11-22 note flagged one candidate code gap: a cramped resident chat entry area at 200 percent text. Re-probed on live; a style experiment shows only a 29 px gain, the consent block is 765 px of required wording, and content stays reachable. Not a defect.
* Consent gate is covered by `test_resident_assistant_api` (no model call without consent) and a live no-request refusal. A consented AI answer cannot be observed while the AI guard holds.

Evidence: `docs/reference/research/issue-619-live-at-consent-evidence-2026-11-23.md`, `.copilot-tracking/evidence/2026-11-23/issue-619-live/`.
