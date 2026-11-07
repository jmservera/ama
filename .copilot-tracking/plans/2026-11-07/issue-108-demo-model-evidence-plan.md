---
title: Issue 108 demo model evidence plan
description: Plan for a bounded documentation-only configured model/limits/evidence-gap record
ms.date: 2026-11-07
---

## Scope

Documentation only. Files: `docs/reference/resources/ai-tokenomics.md`, `docs/reference/README.md` (index row), `docs/reference/log.md` (append) and `.copilot-tracking/` RPI evidence. Excluded: original case study, memory, architecture, experimental design, code, infra, tests, any Azure change, push, PR or merge.

## Phases

* [x] Phase 1: Add dated section "Configured Demo Model, Limits and Evidence Gaps" to the existing synthesis before its Gaps table; bump `ms.date`.
* [x] Phase 2: Update the index row and append the log entry.
* [x] Phase 3: Critique once; apply compatible findings.
* [x] Phase 4: Validate, commit, review once. Focused gate blocked by the shared heavy lock (review R-001).

Details: [phase details](../../details/2026-11-07/issue-108-demo-model-evidence-details.md).

## Constraints

* Cite source commit, retrieval dates and sanitized commands; no credentials, tokens, private data.
* Keep resource location, configured version and capacity distinct from serving region, attestation, budget and benefit.
* No invented quotas for other candidates; keep historical mini/nano observations dated.
* Focused tier. Heavy groups are not acquired; if selected, stop with the exact blocker.
