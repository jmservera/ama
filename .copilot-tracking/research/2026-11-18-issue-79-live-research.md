---
title: Issue 79 live research (opening)
ms.date: 2026-11-18
---

Refs #79. Demo scope (owner decisions 2026-11-18). Prior note on main: docs/reference/research/issue-79-live-ranking-publication-evidence-2026-11-18.md, whose live raw output was not retained.

Unticked criteria: C3 named owner signs first rule order; C4 snapshot publication scheduled and retained.
Plan: re-run repo ranking tests with retained logs; live demo API ranking determinism and reason codes (Playwright); live publication with throwaway Blob container, retained redacted output; delete throwaways.
Research disposition: executed (opening).

## Findings (closing)

Planning Readiness: Ready. Existing live note on main lacks raw output; ACR build blocked (403, private registry), so the shipped `ranking_publish` job cannot be redeployed for the demo. Storage is network-denied from outside, so Blob work runs in a throwaway job. Disposition: executed. See docs/reference/research/issue-79-live-ranking-2026-11-18.md.
