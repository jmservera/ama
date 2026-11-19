---
title: Service Continuity Audit on the Live Demo (Issue 122)
description: Per-criterion proven and unproven status for the one unticked acceptance criterion of issue 122, with constructed-drill test runs and a read-only live continuity probe
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). Azure billing reconciliation, DPO and
Legal approval and person-run assistive-technology testing are not needed for
the demo. Credentials were read from the owner's files at run time and never
printed; a literal scan of the retained evidence for each value found no match.

Issue #122 has one unticked criterion: "A witnessed authorized drill exercises
suspension, owned communication responsibility and restart. Constructed
templates do not send live notices or contact residents automatically." The
other 10 criteria are ticked and were not re-opened.

This is a second pass after the earlier
[live continuity evidence](./issue-122-live-continuity-evidence-2026-11-18.md),
which covers the ticked criteria; this pass concentrates on the unticked drill
criterion and re-reads the live state.

Target: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`
(read with `az containerapp show`). The probe was two `GET` requests behind
Entra sign-in (Playwright Chromium, employee test account, role `Retrofit
Programme Manager`). No state was changed and no Azure resource was created, so
nothing needs deleting. Scripts and redacted outputs are under
`.copilot-tracking/evidence/2026-11-18/issue-122-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Constructed suspension, manual fallback, hazard and restart drill (core) | `test_operator_suspension_drill`: 6 tests OK, covering JSON and SQL variants, restart authority and multi-actor separation (Observed; raw output not retained) | `python3 -m unittest tests.test_operator_suspension_drill -q` from `src/core` |
| Constructed HTTP incident and restart drill (api) | `test_operator_suspension`: 20 tests OK (Observed; raw output not retained) | same style command from `src/api` |
| Code boundary | `continuity.py` states that a distinct OID-bound manager permits "only a constructed drill", that actual OD-35/RULE-020 restart "remains unavailable", and that a witnessed authorised drill "is an owner activity and is not claimed here"; restart records carry `evidence_class: constructed-fixture` | `src/core/src/zava_forward/core/continuity.py` lines 14 to 20 and 820 to 827 |
| Release-gate deferral | `rai_control_plane.py` AC-072 is `verified_with_live_deferral`: a witnessed live drill with appointed duty staff is still required before live pilot release | `rai_control_plane.py` AC-072 |
| Live `/api/continuity` | 200; `epoch` 1; one persisted suspension `SUS-1`, scope `all`, status `Suspended`, `restart` null, `actual_hold` true, `restart_authority` `TBD`, `actual_authority` "Unavailable: OD-35 and RULE-020 acceptance not established", `history_valid` true | `api-continuity.redacted.json` |
| Live change register | `CHG-1` (v0 to v1, evaluation attached) reversed by `CHG-2`; effective version back at `v0` | same file |
| Live export | 200; format `zf-evidence-export/1`, registry hash present, 317 AI records, 6 assistant proposals | `api-continuity-export.redacted.json` |
| Anonymous access | 401 to `/health`, `/api/health`, `/api/continuity` (Easy Auth) | curl status codes in the session |

`SUS-1` (reason "Demo probe: negative test", evidence `SYN-221-PROBE`, recorded
2026-11-18 11:51) is a leftover of an earlier probe on the same demo. It is
kept as adverse evidence: the demo release is currently suspended with no
restart, and this audit did not restart it because the owner prohibits drills
and restart authority is declared unappointed.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Witnessed authorized drill exercises suspension, owned communication responsibility and restart; templates send no live notices | Unproven | Owner decision forbids drills on live; no appointed duty staff, restart authority (OD-35) or witness exists, and the live `SUS-1` shows authority unavailable. Constructed drills (26 tests above) prove the mechanism and the no-send boundary only, and the source labels them as not a witnessed drill. Needs: appointed restart authority and named communication owner, then an owner-authorised witnessed drill. |

Ticked criteria, for reference only: live reads show the suspension record
persists with incident owner and containment, the change register records a
version change with evaluation and a reversal, and the export is a
self-describing bundle. These are observations, not new acceptance of those
ticks.

## Limits

* No suspension, restart, change or export-signing action was performed live.
* Export digest verification was not re-run offline in this pass.
* The existing `SUS-1` suspension remains in the demo state.
