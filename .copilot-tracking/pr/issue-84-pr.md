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

PR review correction: only the registered case owner or programme/manager role
may open a query. Separate append-only events let the original raiser or a
manager withdraw it, and let a named human programme-role holder attest
reconciliation with reason/evidence. Effective status clears only that query's
hold; the original assertions, prior events and audit remain unchanged.
Agents cannot resolve or sign off. Source authority, resolution rules and
eligibility remain Unknown/owner-approval-needed; no winning source, home
overwrite or technical approval is inferred. SQL reuses portable case-body
rowversion/audit transactions and rechecks stock holds at sign-off commit.

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
* [x] Authorised withdraw/resolve lifecycle, immutable history/audit, case
  responsibility, independent holds and SQL concurrency evidenced locally.
* [x] New regressions observed failing against the pre-fix JSON/SQLite and
  HTTP implementation before production edits; green after the fix.
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
| core | 357, OK | Pass |
| api | 500, OK, 99 skipped | Pass |

Current correction: 857 discovered methods in the two touched projects;
skipped tests are not passes. The opt-in Chromium test is separately executed
with the real loopback SQL application:
both source groups/values/metadata/owner, Unknown support, heading/keyboard access
and second-case navigation, plus withdrawn status/event provenance with source
assertions preserved. Node syntax checks pass. Existing sensor-test
ResourceWarnings remain unrelated.

Every local command and result, including failed probes and corrective runs,
is recorded in
[the committed changes evidence](../changes/2026-10-15/stock-reconciliation-84-changes.md).
The final commands are:

```bash
cd src/core
PYTHONPATH=$PWD/src:$PWD/tests python3 -m unittest discover -s tests -q
/tmp/zf164/bin/mypy .
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .

cd ../api
PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests python3 -m unittest discover -s tests -q
/tmp/zf164/bin/mypy .
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
node --check src/zava_forward/api/web/panels.js
ZF_STOCK_BROWSER=1 PYTHONPATH=$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests /tmp/zf164/bin/python -m unittest discover -s tests -p test_stock_reconciliation_api.py -q
```

Before implementation, the new JSON-first and SQL-first core runs failed for
missing lifecycle/unrestricted opening; new HTTP methods failed on unauthorized
opening and missing lifecycle route. After the fix, all 18 core stock methods
exercise JSON/SQLite lifecycle, authorization, audit/restart and independent
holds; SQL-specific races prove refused approval/duplicate terminal events do
not commit pending audit. Five API methods include authenticated lifecycle
and the opt-in rendered app. Historical validation of the other src projects
and all intermediate results remain in the full ledger. No dependencies were
installed for this correction; tooling uses the supplied pip environment.
Pre-correction PR checks passed, including image/mssql; new commit CI remains
separate from local evidence and cannot establish live/human acceptance.

## RPI evidence and review

Research executed (Ready), plan authored, exactly one independent critique
(Revise; all four compatible findings applied), implementation completed and
exactly one post-implementation Review completed. Review outcome: Residual
work, not unconditional acceptance. The subsequent owner review identified a
High permanent-query-hold/overbroad-opening defect, now corrected in this
owner-selected bounded follow-up. Changes/review docs retain that finding,
red/green evidence and disposition; no second critique/Review was performed.
Live platform, source-policy and professional/human acceptance remain open.

* [Research](../research/2026-10-15/stock-reconciliation-84-research.md)
* [Plan](../plans/2026-10-15/stock-reconciliation-84-plan.md)
* [Details](../details/2026-10-15/stock-reconciliation-84-phase-details.md)
* [Critique](../reviews/2026-10-15/stock-reconciliation-84-plan-critique.md)
* [Changes and command ledger](../changes/2026-10-15/stock-reconciliation-84-changes.md)
* [Review](../reviews/logs/2026-10-15/stock-reconciliation-84-review.md)
* [Session state](../rpi-sessions/2026-10-15/stock-reconciliation-84-state.json)

The reference index and append-only knowledge-base log link the durable
core/API contracts. No merge or Azure deployment is requested by this PR.
