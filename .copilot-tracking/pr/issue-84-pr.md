---
title: Issue 84 pull request description
description: Reviewable stock reconciliation engineering slice and evidence boundaries
ms.date: 2026-10-15
---

## Summary

Refs #84

Add owned, append-only stock comparisons in `src/core` and the staff API/view.
Both competing values, source IDs/dates/versions, validation states and the
named query owner stay visible. Authority, resolution and eligibility remain
Unknown; no home value is overwritten or home silently excluded.

Reuse assessment/design/building/coordination sign-offs, affected-only design
returns, building dependencies and hazard holds. Technical decisions require
registered named human staff, separate people and explicit reapproval; neither
an AI proposal nor a client's claimed identity can approve technical work.
Unknown support inputs are explicit across ranking, views, counts and AI
facts, with an idempotent existing-SQL derived-key refresh. Existing governed
AI proposal capability, resident consent and independent safety intake remain.

All new code/tests are under `src/` per Accepted ADR 0006 and the parity
matrix. Core imports no workload; agents gain no SQL/blob dependencies; no
new SQL dialect or deployment is introduced. `mvp/`, `.env`, `.vscode` and
the issue-tracking directory are unchanged. No private operating data was used.
Nomination/challenge and tenure routing remain #130/#131 by owner comment.

## Acceptance

* [x] Both compared stock values and named query owner displayed in API and
  real rendered synthetic workbench.
* [x] Four separate versioned human sign-offs demonstrated with synthetic roles.
* [x] Design change returns only affected sign-offs; explicit reapproval retained.
* [x] Missing support flags are Unknown; safety/waiting/stage/ID still rank homes.
* [ ] Named professional competence/delegation and direct-human task/accessibility
  acceptance; synthetic actors and browser automation do not establish these.
* [ ] Owner-approved source authority, resolution and eligibility rules.
* [ ] Real permitted AI inference/evaluation, SQL Server/Azure workflow evidence
  and image build checks. Local Docker socket access is permission denied.

These checks evidence the local engineering slice, not full operational
acceptance. This PR uses a non-closing issue reference; operational acceptance
remains open.

## Validation

| Project | Full suite | Ruff lint/format and mypy |
| --- | --- | --- |
| core | 340, OK | Pass |
| api | 498, OK, 99 skipped | Pass |
| agents | 70, OK | Pass |
| orchestrator | 17, OK | Pass |
| importer | 39, OK | Pass |

Total: 964 discovered tests; skipped tests are not passes. The opt-in Chromium
test was separately executed and passed with the real loopback SQL application:
both source groups/values/metadata/owner, Unknown support, heading/keyboard access
and second-case navigation. Node syntax checks pass. Existing sensor-test
ResourceWarnings remain unrelated.

Every local command and result, including failed probes and corrective runs,
is recorded in
[the committed changes evidence](../changes/2026-10-15/stock-reconciliation-84-changes.md).
The final commands are:

```bash
cd src/core
../../.venv/bin/ruff format tests/test_stock_reconciliation.py
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
../../.venv/bin/python -m unittest discover -s tests -q

cd ../api
../../.venv/bin/ruff format tests/test_stock_reconciliation_api.py
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
ZF_STOCK_BROWSER=1 PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
node --check src/zava_forward/api/web/app.js
node --check src/zava_forward/api/web/panels.js
PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q
```

Remaining project commands and all intermediate results are in the full ledger.
The root `.venv` was created with pip after missing-tool errors and removed
after validation. Application dependency manifests/pins were not changed;
only narrow existing test-boundary mypy configuration was extended.
CI must supply unavailable image and SQL Server evidence.

## RPI evidence and review

Research executed (Ready), plan authored, exactly one independent critique
(Revise; all four compatible findings applied), implementation completed and
exactly one post-implementation Review completed. Review outcome: Residual
work, not unconditional acceptance. No high-confidence implementation defect
was identified in the bounded local scope; live platform, source-policy and
professional/human acceptance remain routed follow-ups.

* [Research](../research/2026-10-15/stock-reconciliation-84-research.md)
* [Plan](../plans/2026-10-15/stock-reconciliation-84-plan.md)
* [Details](../details/2026-10-15/stock-reconciliation-84-phase-details.md)
* [Critique](../reviews/2026-10-15/stock-reconciliation-84-plan-critique.md)
* [Changes and command ledger](../changes/2026-10-15/stock-reconciliation-84-changes.md)
* [Review](../reviews/logs/2026-10-15/stock-reconciliation-84-review.md)
* [Session state](../rpi-sessions/2026-10-15/stock-reconciliation-84-state.json)

The reference index and append-only knowledge-base log link the durable
core/API contracts. No merge or Azure deployment is requested by this PR.
