---
title: Epic 73 child disposition audit with live demo read, second pass (Refs #73)
description: Per-criterion and per-child disposition table for epic 73 on 2026-11-19, with the residual of each open child and a read-only live check of the synthetic demo
ms.date: 2026-11-19
---

Refs #73. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18. This note ticks nothing in any issue. No source code changed, no Azure resource was created (nothing to delete) and no demo record was written. It follows the [first pass](./issue-73-epic-live-2026-11-19.md).

## Method

* Issue state read with `gh issue view` on 2026-11-19 for #73 to #80, #135, #183 and #440, and `gh api repos/jmservera/ama/issues/73/sub_issues` for the registered children.
* Azure CLI, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` returned revision `ca-cutover-test-demo-api--0000033`, image digest `sha256:5368f4e4...c17e5fb` (the digest the other 2026-11-18 notes record), provisioning `Succeeded`.
* Reused, not repeated: the [#76 live notes](./issue-76-live-r3-2026-11-18.md), the [#79 publication evidence](./issue-79-live-ranking-publication-evidence-2026-11-18.md), the [#80 thresholds note](./issue-80-live-transition-thresholds-evidence-2026-11-18.md) and the [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md).

## Epic 73 acceptance criteria

| # | Criterion (state on the issue) | Demo result | Evidence | Tickable now |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Not met | #440 is OPEN with two unticked criteria (triage into independent issues with owner approval for pivots and deferrals, and the review artifacts for the coordinator change). Merged children alone do not satisfy it. | No. Needs #440 closed and the owner's recorded pivot or deferral decision. |
| 2 | All child features closed or deferred (unticked) | Not met | Six children CLOSED, three OPEN (#76, #79, #80). No owner deferral of an open child is recorded. | No. Needs each open child closed or an explicit owner deferral. |
| 3 | Each requirement traces to a passing check or a recorded deferral (unticked) | Not met | Traceability for the three open children is incomplete; see the residual table. | No. |

## Child disposition

| Child | State | Unticked criteria | Disposition |
| --- | --- | --- | --- |
| #74 | CLOSED | 0 | Closed |
| #75 | CLOSED | 0 | Closed |
| #77 | CLOSED | 0 | Closed |
| #78 | CLOSED | 0 | Closed |
| #135 | CLOSED | 0 | Closed |
| #183 | CLOSED | 0 | Closed |
| #76 | OPEN | 1 | In progress |
| #79 | OPEN | 2 | In progress |
| #80 | OPEN | 1 | In progress |

## Residual of each open child

| Child | Remaining criterion | Class |
| --- | --- | --- |
| #76 | Hazard and safeguarding items show a clock and named owner | Hazard clock and owner seen live with value Unknown; no safeguarding item exists on the demo and the API has no endpoint that writes one, so seeding would change the shared record. A local HTTP test covers both kinds. Owner decision: seed a synthetic item or defer. |
| #79 | Named policy owner signs the first rule order | Human signature by a named person; `ranking-v1` owner is still "to be named". Cannot be proven for the demo. |
| #79 | Ranking snapshot publication scheduled and retained | The scheduled job's orchestrator image lacked the entry point and the infra job was not provisioned; Blob immutability was not observed. Deployment and owner decision. |
| #80 | Owners set the staged transition thresholds | Owner decision recorded nowhere in the repository. |

None of the residuals is closable by code in this repository. Each needs a named owner decision or a deployed run.
