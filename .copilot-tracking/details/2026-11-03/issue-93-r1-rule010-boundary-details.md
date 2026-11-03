---
title: Issue 93 R1 RULE-010 boundary phase details
ms.date: 2026-11-03
---

## Phase 1 test design

* `StaticBoundary`: action names carry no automatic bid, match funding, certify or cash term; AST scan of `agents`, `orchestrator`, `importer` and AI/chat/assistant core modules finds no reference to `grant_action`, `finance_action`, `funding_step`, `_financial_authority`; `api` reaches them only in `server.py`; finance, grants, forms, form_review and signoffs import no network client.
* `BoundaryProbes` (file-backed store, synthetic designation): walk every grant state to Cash received; at each approval an undesignated user, the proposer and an approver lacking that exact `grant:<state>` permission are refused with the record unchanged; grant approvals never alter `funding` or add finance ledgers; offline AI draft leaves no Approved, Submitted or Confirmed state; application steps refuse without designation and in order.

## Phase 2 validation

Focused tests, `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-93`.
