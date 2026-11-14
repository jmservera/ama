---
title: "Research: #135 conflict view and controlled recovery"
ms.date: 2026-11-14
task_slug: 135-conflict-recovery-1844
research_disposition: executed
planning_readiness: Ready
---

## Scope

Issue #135 remaining criteria: conflict values with source, date, version and named owner; controlled audited recovery with no automatic replay or release; preserved unresolved eligibility and original source; scoped visible operator access and honest outage state. `src/api/src/zava_forward/api/web/role-screens.js` is out of scope (in-flight UX PRs).

## Evidence

* `src/core/src/zava_forward/core/exception_queue.py` (#1704): in-memory `ExceptionQueue` already carries `values` (value, source, date, version), named `owner`, `eligibility: Unknown`, `original_source`, a `recovery_policy` with automatic replay and release false, a `request_recovery` action with owner check, scoped `queue` and `access_report`, and an honest `outage_banner` (stale or missing check is Unknown).
* `exception_register.py`: the served register rebuilds that queue from stored records on every GET, so `request_recovery` results were never durable. The register note said recovery is "made elsewhere"; no API endpoint made it.
* `GET /api/exceptions` in `server.py` is the only route; `projection` gates POST to staff roles; the role inventory test requires every route to be listed.
* Item ids (`EX-001`) are sequence-based and unstable across rebuilds. Feed `ref` values are stable (`stock:case:query`, `file:digest`, `handoff:...`, record id).
* Audit ledger (`audit_entries`) is tamper-evident in both stores with `who`, `action`, `case`, `detail`. A new `DOCS` document would touch SQL schema and merge paths (full-tier risk).

## Gap

Criterion 3 (controlled, audited recovery) lacks a durable, served action. Criteria 1, 2 and 4 are met in core and the GET register; they remain subject to named-role and operational acceptance.

## Decision

Record each recovery request as an audit-ledger entry keyed by `kind:ref` and overlay the latest request onto rebuilt items. No new persisted document, no SQL change. Request only: no replay, correction, re-send or release.

## Open items

Named steward and operator roles, runbooks and operational acceptance remain with the owner. Source correction history exhausted; no change to that allowance.
