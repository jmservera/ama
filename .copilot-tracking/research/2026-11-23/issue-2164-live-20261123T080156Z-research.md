---
title: Research for issue 2164 r6, audit of identity.verified staff paths
ms.date: 2026-11-23
---

## Scope

Follow-up from the r5 loop: audit every other `identity.verified(user)` caller for the same gap
that #2164 closed in `assistants.authorize`: a roster-bound Entra principal (`user["bound"]`)
carries no `case_ids`/`areas`, so roster scope, view-only and row revocation are skipped unless the
caller re-reads the bound row. Issue #2164 lists no acceptance checkboxes; its decision question
(inherit bound-row scope; test `view_only` and scope bypass) is the criterion set.

## Evidence

* Roster scope fields (`case_ids`, `areas`) are read in exactly two places:
  `assistants.authorize` (fixed by #2164) and `sensor_review_draft._gate`
  (`grep -rn "case_ids\|areas" src/core/src`).
* `identity.bind` runs on every request in `api/server.py::_user` and `identity.matches` excludes
  disabled rows, so a revoked roster row yields an unbound derived principal on the next request.
* Callers of `identity.verified` were read and classified:

| Caller | Uses roster scope | Result |
| --- | --- | --- |
| `assistants.authorize` | yes | Fixed by #2164; row re-read, oid/tid, view-only, scope tested |
| `sensor_review_draft._gate` | yes | Gap: does not call `verified`; reads row by email only |
| `bulk_edits._fresh_actor`, `forms._actor`, `change_provenance._actor` | no scope field | No scope gap; `change_provenance` re-resolves the bound row by oid/tid |
| `chat_isolation.current_user`, `chat_privacy._admin`, `resident_decisions` (2 sites), `coordinator` | no scope field | No scope gap; role from verified principal |
| `regulatory_chat.admit`, `regulatory_privacy` (2 sites), `simulator_admin` | no scope field | Verification and view-only checks only; no roster scope |

## Gap found: sensor_review_draft

`_current_staff` looks up the roster row by `user["email"]` with no check that the row belongs to
the same tenant and object id, and the gate has no view-only refusal. Probe against a JSON store
(roster row oid changed to another person, then `view_only=True` on a bound principal): both
`read_drafts` calls passed the gate and returned `consent-withheld` instead of `PermissionError`;
the row scope (`case_ids=["ZF-2"]`) was applied correctly, so scope bypass does not occur while the
oid matches. Real flow impact is limited (view-only principals are never bound; a rebinding needs a
roster edit), so this is defence in depth that makes the gate match `assistants.authorize`.

## Planning Readiness

Ready. Disposition: executed. Fix `sensor_review_draft._gate` to verify Entra principals, refuse
view-only, and require the bound row to carry the same oid and tid; add tests.
