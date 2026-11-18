---
title: Live service continuity, versioning and export evidence for issue 122 (demo)
description: Recorded run on 2026-11-18 against the demo API covering version change and reversal, independent export verification, default-disabled assistants and template fallback, with a per-criterion record (observed, raw output not retained, or unproven)
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 122
  - service continuity
  - versioning
  - evidence export
estimated_reading_time: 6
---

## Scope and authority

Refs #122. Target: `ca-cutover-test-demo-api` revision `--0000031`, synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Sign-in used the employee demo account (role `Retrofit Programme Manager`) through Playwright Chromium; credentials were read at runtime and never printed. No Azure resource was created, so none needs deleting. Only counts, versions and public hashes are recorded below.

## Live observations

| # | Observation (2026-11-18, UTC) | Result |
| --- | --- | --- |
| 1 | `GET /api/continuity` before the run | 200; epoch 0, no suspensions, `history_valid` true, no changes |
| 2 | `POST /api/continuity/change` kind `configuration`, subject `zf-demo-continuity-probe-122`, `v0` to `v1`, evaluation `pass`, `synthetic` true | 200; `CHG-1` Applied; effective version `v1` |
| 3 | `POST /api/continuity/change-reverse` for `CHG-1` | 200; `CHG-1` Reversed, superseded by `CHG-2` (`v1` to `v0`); effective version back to `v0` |
| 4 | `GET /api/audit-check` after the run | 200; intact, 1609 entries, head `51929075977af04e077ca8f4ed93e9c5b76b0685c343e58a3b06e87ef7320fcf` |
| 5 | `GET /api/continuity/export` before the change | 200; format `zf-evidence-export/1`, complete, 1581 ledger entries, digest `c2c0264de7b28aa9b4eed25d5b5dea89ff3b8935df3ffbb105e186e6630823b9` |
| 6 | `GET /api/continuity/export` after the reversal | 200; complete, 1608 ledger entries, both changes present, registry version `2026-10-15.1`, digest `6a704c258ee1ef17f7edd833dc46324ba17a64eb16a4455d56f490e3a433ec2d` |
| 7 | `zava_forward.core.continuity.verify_export` run locally on the saved bundles, no network and no AI service | both: `valid` true, `complete` true, no problems |
| 8 | Same verifier on bundle 6 with the last AI record removed | `digest mismatch`, so tampering is detected |
| 9 | `GET /api/assistants` | `disabled`: "Operator authority, finite allowance and expiry are required."; `proactive` false; `manual`: "Use the ordinary case controls; proposals never approve or change the case." |
| 10 | AI records inside export 6 (199) | all 199 have source `template` and a recorded `fallback_reason`; 191 mode `ai`, 8 `workflow-only`; no external model output depended on |

The export states its own independence: "Plain JSON with its own digest and ledger chain. Provider, deployment and model appear only as recorded data; reading, verifying or re-importing it needs no AI supplier or live service." Observation 7 confirms it by verifying with the repository code alone. The probe row is an append-only register entry that no runtime path reads; the two rows (`CHG-1`, `CHG-2`) remain in the demo database by design, and they are labelled synthetic.

## Restore evidence reused

The point-in-time restore of the demo SQL database, with audit-chain prefix match, is recorded in [issue 145 live PITR note](./issue-145-live-pitr-restore-evidence-2026-11-18.md) from the same day. It was not repeated (about one hour per restore). Suspension and restart behaviour is covered by the repository drill tests in [issue 221 note](./issue-221-restart-authority-and-drill-evidence-2026-11-18.md).

## Per-criterion status

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| Disable mechanism and tested manual fallback exist | Observed; raw output not retained (read only) | Observation 9 shows assistants disabled by default with the manual path named; observation 10 shows template fallback on every recorded AI output; repository tests in the #221 note cover suspension and manual fallback. No live suspension was exercised (drills excluded) |
| Model, rule and configuration changes are versioned, evaluated and reversible | Observed; raw output not retained | Observations 2 and 3: evaluated (`pass`), versioned (`v0` to `v1`), reversed with a linked record; effective version read at each step. A `fail` evaluation path (status Blocked) was not run live |
| Export tests retain evidence independent of the AI supplier | Observed; raw output not retained | Observations 5 to 8, 10 |
| Persist suspension, owner, containment, communication, restart decision | Not re-proven live | Suspension changes live state and counts as a drill; covered by repository tests only |
| Recheck epoch at invoke, scan, claim, dispatch, complete and reliance | Not re-proven live | Repository and SQL tests only; the live epoch reads 0 |
| Independent SQL connection, race and old-image restart tests | Not re-proven live | Needs concurrent suspend and a second image; drills excluded |
| In-flight calls complete but late results quarantined | Not re-proven live | Assistants are disabled on the demo, so no in-flight call exists |
| Corrective evidence and distinct human approval gate restart | Not re-proven live | See #221 note; live restart is a drill |
| Preserve reconstructable history without current reliance | Observed; raw output not retained | Export 6 holds the reversed change, ledger chain and AI records, and verifies offline |
| Manual case work, challenge and hazard response remain during suspension | Partly proven | The continuity view states it (`note`); no live suspension was exercised |
| Witnessed authorised drill of suspension, communication and restart | Unproven | Excluded by the owner for the demo; production work (#1905 to #1908) |

## Limits

* The two synthetic change rows are permanent in the demo register.
* Observation values come from this worker's run; the raw JSON is not committed because the export carries about 1.2 MB of demo audit data.
* Restore evidence is by citation, not a second restore.
* A restored database was not compared with the export, and document blobs were not tested.

## Evidence limits

* Observations 1 to 10 were read from this worker's live run. The raw responses and the saved export bundles were not retained, so none of them can be re-checked from this repository. The criteria above are therefore labelled "Observed; raw output not retained", not "Proven".
* Observations 7 and 8 (offline `verify_export`, tamper test) used the saved bundles; without them the commands cannot be re-run here, and their output was not captured.
* No Playwright screenshot of the continuity view was taken.
* The digests and counts in the table are transcribed values, not retained output.
