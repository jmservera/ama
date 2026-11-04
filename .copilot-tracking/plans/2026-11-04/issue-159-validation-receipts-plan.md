<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refused receipts plan
description: Record a receipt for validation and missing-case refusals of unstored asks
ms.date: 2026-11-04
---

## Task Metadata

* Task slug: issue-159-validation-receipts. Research: .copilot-tracking/research/2026-11-04/issue-159-validation-receipts-research.md
* Phase details: .copilot-tracking/details/2026-11-04/issue-159-validation-receipts-details.md
* Critique: executed once on the final candidate. Verdict Approve. Applied directly: reuse the `chat.turn.unstored` action and shape, never log the question, keep responses and permissions unchanged.

## Phases

* [x] Phase 1: `_record_unstored_refusal`; call it when `ask_unstored` validation or case lookup refuses (`rejected` for ValueError, `access-rejected` for ChatNotFound/permission).
* [x] Phase 2: core behavioural test; ruff, mypy `--cache-dir=/tmp/mypy-159`, focused unittest.
* [x] Phase 3: log entry, commit, push, PR with `Refs #159`.

## Unmet after this slice

* Criterion 6 (human screen-reader test) and the tokenomics criterion (401 and route-validation paths).
