---
title: Issue 221 live suspension, incident and restart evidence (demo)
description: What a live probe of the synthetic demo showed about suspension, manual fallback and restart denial, including an unintended open suspension and a placeholder-authority gap in the deployed build
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 221
  - RULE-024
  - NFR-014
estimated_reading_time: 5
---

Refs #221. Scope: synthetic desktop demo, owner decisions of 2026-11-18 (live Azure authorised, resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Evidence folder: [operator-suspension-live-221-2026-11-18/](./operator-suspension-live-221-2026-11-18/). Builds on the [repository-test note](./issue-221-restart-authority-and-drill-evidence-2026-11-18.md). No source or Azure resource was changed or created.

## What happened

A probe of `ca-cutover-test-demo-api` (revision `0000031`, image digest `sha256:5368f4e4...c5fb`) was written to prove that placeholder, AI-named, automatic and self-designated restart authorities are refused. The first request, restart authority `TBD` with scope `all`, was accepted (HTTP 200) and created an open suspension `SUS-1` of all AI work, epoch 1, status Suspended. The other four requests (three further suspend requests and one restart proposal for an unknown suspension) failed only with "This scope is already suspended", so they do not prove the authority refusals live. Raw output: [live-probe-1-unintended-suspension.json](./operator-suspension-live-221-2026-11-18/live-probe-1-unintended-suspension.json).

This was not intended and is not a drill. The demo remains suspended: restart needs a proposal with complete incident evidence and a decision by a distinct human holding the OID-bound `ai_restart` capability, which no demo account has (OD-35 unappointed), and the SQL gate state is delete-protected by design. No SQL, ledger or gate tampering was attempted. Owner decision needed: accept the open suspension as demo evidence, or restore the demo database from a point in time before 2026-11-18T11:51Z (see [issue 145 PITR note](./issue-145-live-pitr-restore-evidence-2026-11-18.md)).

## Live observations while suspended

Raw output: [live-probe-2-while-suspended.json](./operator-suspension-live-221-2026-11-18/live-probe-2-while-suspended.json), script [live_probe.py](./operator-suspension-live-221-2026-11-18/scripts/live_probe.py), screenshot [02-signed-in-while-suspended.png](./operator-suspension-live-221-2026-11-18/screens/02-signed-in-while-suspended.png) (synthetic case names visible).

* Register: scope, reason, incident owner, containment, communication (not sent), trigger, evidence, resident impact, remediation, restart authority, affected versions per task (with missing release evidence listed), `restart_rule` RULE-024 and `automatic_restart` false are recorded; `snapshot_complete` is false.
* An AI summary request returned a template (`source: template`, `model: null`) with the reason "Suspended (SUS-1): use the manual route", citing that manual case work, resident challenge and hazard response continue and emergency and statutory hazard duties are never paused. The record carries `continuity_epoch` 1.
* Cases stayed readable (`/api/cases` 200) and the staff briefing loaded (observed; raw output not retained, screenshot only).
* Restart proposal with a constructed passing claim: 403 "Incident evidence, impacted versions and restart authority are incomplete". Restart decision without a proposal: 403 "Restart needs corrective evidence proposed first". Request with an automatic-restart flag: 403 (refused on the claim class before the flag check).
* Attempted without being exercised live: a manual hazard raise (would write an undeletable record on a synthetic case).

## Per-criterion table (unticked criteria of #221)

| Criterion | Proven for the demo? | Evidence and limits |
| --- | --- | --- |
| Guardrail breach record names restart authority per RULE-024 | Partly. Proven in repository code and tests; the live record stores a `restart_authority` field and `restart_rule` RULE-024. Contradicted for the deployed build: it accepted the placeholder `TBD` as authority | Six drill tests OK ([test-core-drill.txt](./operator-suspension-live-221-2026-11-18/test-core-drill.txt)); live probe 1. The deployed image is not shown to contain the current validator |
| Suspension and manual fallback drill is tested (NFR-014) | Repository drill proven (`test_nfr_014_end_to_end_suspension_manual_fallback_hazard_and_restart_drill`). Live: suspension, containment record, AI block with manual route message and restart denial observed; live restart, live hazard route use and a witnessed operator drill unproven | Owner excluded drills; no account can approve a restart; a witnessed drill by named operators is production work (#1905 to #1908) |

Ticked criteria 1 to 4 (block on dispatch and reliance, record fields, manual and hazard routes, restart denial) are consistent with the live observations above but were not re-proven in full: only AI reliance blocking, record fields and restart denial were seen live.

## Follow-ups

* Owner: decide on the open `SUS-1` suspension (accept as evidence or point-in-time restore).
* Check which commit the deployed image was built from; redeploy a build with the placeholder-authority refusal, then re-run the refusal probe against a scope that is not already suspended (needs a restart path first).
* Appoint OD-35 restart authority and an `ai_restart` holder so a live restart can be tested.

## Evidence limits

* The script for probe 1 (the one that created the unintended suspension) was not retained; only its raw output JSON is. Probe 2's script is committed. The probe 2 script redacts synthetic staff names with a title-case pattern; the saved JSON files were redacted at capture.
* Account codes, addresses, OIDs and synthetic staff names in the saved JSON are redacted; sign-in values were read at runtime from files outside the repository and never printed.
* The drill tests ran on the worktree code, not the deployed image; the SQL-server tests were not run. mypy and ruff were not run because no source changed.
