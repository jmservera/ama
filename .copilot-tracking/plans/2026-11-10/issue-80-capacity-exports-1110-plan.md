---
title: Issue 80 capacity page export controls, plan
description: Plan for two contextual CSV download anchors on the Capacity page with focused regression assertions
ms.date: 2026-11-10
---

## Objective

Add exactly two native download anchors to `capacityView`, one beside the Packages heading and one beside the Work orders heading, pointing at the existing fixed routes `/api/packages.csv` and `/api/workorders.csv`. Advances issue 80 criterion 2 for these two lists only. Does not prove "every list", does not touch the progress variant, thresholds or other registers. Refs 80 and 73 only.

Research: [research](../../research/2026-11-10/issue-80-capacity-exports-1110-research.md). Details: [details](../../details/2026-11-10/issue-80-capacity-exports-1110-details.md). Critique: [critique](./issue-80-capacity-exports-1110-critique.md).

## Phases

* [ ] Phase 1: UI change in `src/api/src/zava_forward/api/web/ops.js` (one local helper, two conditional anchors).
* [ ] Phase 2: focused regression assertions in the existing `src/api/checks/capacity_browser_check.py` (seeded and empty scenarios).
* [ ] Phase 3: focused validation: `node --check` on the changed JS, ruff on the changed check if configured, `test_list_export_api.py`, then one run of `capacity_browser_check.py` with the pinned axe asset under its own non-blocking heavy lock.
* [ ] Phase 4: reconcile changes record, native self-review (not independent review), commit locally, handoff.

## Validation tier

Focused demo tier. Rationale: two UI affordances for already authorised existing routes; no dependency, workflow, permission, security control, deployment, SQL or gate change. Strictest applicable tier is still focused. No blanket or full gate, no `--changed` run claimed as a receipt, no hosted CI claim. Independent exact-head review and hosted CI remain required before publication and are not performed here.

## Boundaries

* No change to `server.py`, `core`, `projection.py`, serializers, store, routes, defaults, filters, retention or roles.
* Fixed hrefs only; no page, `case` or `view` parameters.
* Controls withheld when `total` is 0; no control on a load failure (the view never renders then).
* Labels state the breadth: all visible records, not only this page, and the one-way read-only meaning.
* No new dependency, no network, owned synthetic data only.

## Stop conditions

Any targeted validation failure blocks and is preserved with its exit; no retry until green. A busy heavy lock is reported as BLOCKED, not queued.
