---
title: Role task queues 76 research
ms.date: 2026-10-16
---

## Brief and controls

Task #76, slug role-task-queues-76. Focused internal acceptance audit for a
bounded offline implementation. Read #76 with `gh issue view 76 --comments`
and its JSON body. Code writes only in src; supporting docs and RPI artifacts
are requested. No deployment, private dataset, environment-file changes, new
identity provider, perspective picker or owner approval. Existing clean topic
branch feat/src-task-queues-76 has no prior PR.

## Prior knowledge and extensions

ADR 0006 and parity matrix require the installed five-project src layout.
Original/addendum, reference index/memory and housing primer were consulted.
Repository instructions and the RPI research/implementation skills apply.
No specialist lane is necessary for this continuous local trace. Existing
navigation, Entra provider, permission projection and technical/resident
decisions are prior art, not work to rebuild.

## Cycle 1: Wider

| Evidence | Source | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/workbench.py:15 | Server describes existing role-authorized navigation; it does not define task queues. |
| C2 | src/api/src/zava_forward/api/web/app.js:293 | Own-case list, list filtering/sorting, full-screen case and one reset already exist; next action is a generic prompt. |
| C3 | src/core/src/zava_forward/core/projection.py:39 | Existing default-deny endpoint/contractor field lists and role-based free-text withholding must cover additions. |

## Cycle 1: Deeper

| Evidence | Source | Finding |
| --- | --- | --- |
| C4 | src/core/src/zava_forward/core/store.py:175 | Summaries and detail derive status but lack one shared task context. Detail already contains separate handoff/history, hazard observations and blockers. |
| C5 | src/core/src/zava_forward/core/sqlstore.py:594 | Limited SQL paging bypasses Store.page_cases. Queue filtering must happen before counts/paging, with parity for CSV and JSON stores; no SQLite-only SQL is needed. |
| C6 | src/core/src/zava_forward/core/workflows.py:42 | Receipt is not acceptance. Handoff view separates current/proposed/confirmed/chase/resident-update owners and preserves unknown due dates. |
| C7 | src/core/src/zava_forward/core/workflows.py:77 | Hazard awareness, response/update due dates and follow-up owners already exist; do not start or classify a statutory clock from stage dates. |
| C8 | src/api/checks/workbench_browser_check.py:80 | Existing live synthetic loopback browser checks cover roles, responsive case, cancellation and reset. Extend, do not replace. |

## Cycle 1: Contrarian

Ranking policy `src/core/src/zava_forward/core/policies/ranking-v1.json:5`
explicitly has no named approving owner and is draft. Accepted AI priority
advice must not be relabelled approved programme priority. Newly-arrived
window is not owner approved; show a versioned engineering definition and
open ratification. Missing dates are Unknown, not fresh or overdue. Existing
technical sign-off requirements name roles, not necessarily individuals:
show named owner Unknown rather than inventing an assignment. Hazard service
clock authority stays external. No added scheduling, approvals or writes.

## Acceptance audit before changes

| #76 acceptance | Existing delivery | Gap |
| --- | --- | --- |
| Own list, plain status/next action | Own list and status delivered | Replace generic next-action prompt with current shared recorded context. |
| No picker/simulator | Delivered | Preserve and regression check. |
| Six visible queue definitions | General flags only | Add versioned definitions and filters, including visibly unavailable approved priority. |
| Blocked step reason/owner/action | Several domain checks have prose and responsible roles | Make shared structured context visible in list and detail; do not fabricate named owners. |
| Hazard clock and named owner | Expanded case safety panel has external observations/owner | Surface recorded clock and owner in queue too; missing values explicitly Unknown. |
| FR-034 | Detailed handoff/return/source records exist | Reuse one projected context in list, detail, current history and suggestion context; preserve historical snapshots. |
| FR-032 | Single reset, own scope/order/page/focus exists | Add server version/default contract and clear the new queue filter with it. |

## Synthesis and readiness

Research disposition: executed. Planning Readiness: Ready for the bounded
offline slice. All three waves completed inline; a further wave is redundant
for the identified gaps. Open decisions: OQ-005 role/field rights, OD-14/19
redaction/operational delegation, queue definition ratification and ranking
policy owner approval. These block operational acceptance, not the requested
offline engineering slice. Live Azure/SQL Server/AI and direct human
acceptance are not claimed.
