<!-- markdownlint-disable-file -->
---
title: Issue 159 refusal receipts plan
description: Record a receipt when an unstored ask or a regulatory-thread turn is refused before any model call
ms.date: 2026-11-04
---

## Task Metadata

* Task slug: issue-159-refusal-receipts. Research: .copilot-tracking/research/2026-11-04/issue-159-refusal-receipts-research.md
* Phase details: .copilot-tracking/details/2026-11-04/issue-159-refusal-receipts-details.md
* Critique: executed once on the final candidate. Verdict Approve. Applied directly: reuse the existing audit action and shape for unstored asks, never log the question, leave 401 as residual, keep response codes unchanged.

## Phases

* [x] Phase 1: `ChatPanel.record_rejected_unstored`; call it from `ask_unstored` on current-user refusal and from the POST role gate for `/api/chat/unstored-ask`.
* [x] Phase 2: record `record_rejected` when `_regulatory_access` refuses a `messages` or `ask` turn.
* [x] Phase 3: tests outside the package (core and API); ruff and mypy with `--cache-dir=/tmp/mypy-530`; focused unittest.
* [x] Phase 4: knowledge-base log entry, commit, push, PR with `Refs #159`.

## Acceptance for this slice

* Each refused turn on these paths yields exactly one receipt with outcome `access-rejected`, 0 model calls, no question text; responses and permissions unchanged.

## Unmet after this slice

* Criterion 6: named human screen-reader test and announcement check.
* Tokenomics criterion: not proven for 401 and validation-refused paths; left unticked.
