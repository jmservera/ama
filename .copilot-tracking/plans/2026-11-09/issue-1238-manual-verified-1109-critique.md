<!-- markdownlint-disable-file -->
# Critique: issue 1238 F3 manual_verified supersession (1109)

Executed once, 2026-11-09T23:32Z, on the final prospective candidate (research,
plan, details) before any test or source edit. Verdict: Revise (six findings).
No second critique will run for this task. Dispositions are direct unless noted.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | Control owner mapped to service owner without owner confirmation | Partly accepted. No separate control-owner role exists and no role may be invented, so the existing service owner and redress owner (registered, persisted, distinct identities) stay the two gates and unknown identity fails closed. The mapping is labelled an interpretation in code docs, README and handoff; no F3 closure claim rests on it being owner-confirmed. Interactive confirmation is unavailable in this non-interactive run and is not inferred. |
| PC-002 | `_IN_FLIGHT` is per store instance; another instance could supersede during a send | Accepted as a documented limit, with a test. A late outcome for a `Superseded` attempt is refused by the existing `Pending` check, the bounded retry exhausts, and the receipt reference is logged and surfaced as `ResidentCommittedError`; it is never silently lost or applied. No new durable lock or shared-store change is made (owned elsewhere). |
| PC-003 | A receipt found by verification has no recording path | Accepted as an explicit remaining gap. Adding a manual acknowledgement path would be new authority and is not approved. README and handoff state that evidence of a receipt means the attempt must not be superseded and goes to existing reconciliation. |
| PC-004 | A first authorization survives reassignment of its owner | Accepted and applied. On every authorization and at completion each recorded authorization must still match the current owner for its role by code or oid; stale ones move to `withdrawn`, never delete, and do not count. Test both reassigned roles. |
| PC-005 | Exact replay after a lost acknowledgement is refused as a duplicate | Accepted as safe refusal: the duplicate is refused with a reload message and writes no second authorization or audit entry; the existing `_operation` committed-acknowledgement handling covers the lost-ack case. Atomic audit-fault rollback and replay are tested. |
| PC-006 | New free text could outlive retention deletion | Accepted and applied by removing the free-text note. Only `evidence_ref` (a short reference, at most 100 characters) and registered identities are stored; README states it must be a reference, not resident detail. Retention deletion test covers a superseded attempt. |

Plan and details are updated for PC-004 and PC-006 (no `note`, `withdrawn`
list) in the same phase before tests.
