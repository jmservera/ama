---
title: Delivery bottleneck plan
description: RPI plan for writing the delivery bottleneck knowledge-base page
ms.date: 2026-10-31
---

## Plan

* [x] Phase 1: write `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md` (frontmatter, no H1, `*` bullets, ASCII, measured table, ranked fixes, separated owner decisions, seven-day plan).
* [x] Phase 2: add the catalog row to `docs/reference/README.md` and append an entry to `docs/reference/log.md`.
* [x] Phase 3: validate links, ASCII punctuation and Git diff. The heavy gate was not run (docs only per task direction).
* [x] Phase 5 (2026-10-31 correction cycle, PR #623): address the 11 Copilot review threads in the page and plan; dataset IDs and commands recorded, causal claims stated as hypotheses, gate and queue assumptions corrected.
* [ ] Phase 4: commit with the noreply identity and trailer, push without force, open PR using `Refs` only.

## Constraints

* No workflow, setting or source change. Savings labelled as estimates.
* Critique: not run as an independent sub-agent critique (docs-only, cost-bounded); a single self-critique was applied (separate measured evidence from estimates and keep owner decisions apart). Independent review remains with the owner.

## Publication blocker (2026-10-31)

* The docs-only exception conflicts with `.github/copilot-instructions.md`, which requires the complete exact-head local gate for every final RPI candidate, including documentation-only work. Relaxing it is undecided owner decision D4. Publication is therefore blocked for merge purposes until the full receipt is run and verified or the owner explicitly amends the rule. Hosted CI does not run for these paths and is not a substitute. The skipped-gate record is preserved.

## Correction (2026-11-01)

* The statement above that publication is blocked solely on a full receipt is historical. The plan was assessed under the owner-selected Focused tier for docs-only work, as recorded in the changes record. The Focused tier applies; the complete local gate is not claimed. Remaining: independent human review and owner decision D4 on whether the repository rule should be amended.
