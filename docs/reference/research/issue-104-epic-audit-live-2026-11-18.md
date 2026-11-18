---
title: Epic 104 bounded AI assistance audit with live demo read (Refs #104)
description: Per-criterion evidence table for epic 104, the exact remaining demo gaps for children 107, 108, 164 and 216, and a fresh read-only live probe of the synthetic demo on 2026-11-18
ms.date: 2026-11-18
---

Refs #104. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive Azure billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. This note ticks nothing in any issue. No source code changed and no Azure resource was created.

## Method and retained evidence

* Issue state read with `gh issue view` for #104, #107, #108, #164, #216 and #440 on 2026-11-18.
* Azure CLI with the existing login, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` limited to revision, image digest and the non-secret `AI_*`, `ZF_*` settings. Result: revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4...c17e5fb` (unchanged from the earlier notes), `ZF_STORE` `mssql`, `ZF_DEPLOYMENT_PROFILE` `demo`, `AI_DEPLOYMENT` `standard`, `AI_MODEL_VERSION` `gpt-4.1-nano-2025-04-14`, `ZF_CHAT_DEMO_ACTIVATION` `approved-2026-11-03`.
* Playwright Chromium, 1366 by 900, signed in as the employee demo account. Driver `live_epic_probe.py` read credentials at run time, never printed or saved them, and scrubbed e-mail addresses and GUIDs; a scan of `live_epic_probe.json` found no `@`. It made six GET calls only (`/api/ai/report`, `/api/assistants`, `/api/assistants/forecast`, `/api/assistants/proposals`, `/api/chat/status`, `/api/ai/priority`), all HTTP 200, and no write.
* Files are in `.copilot-tracking/evidence/2026-11-18/issue-104-live/`: `live_epic_probe.py`, `live_epic_probe.json`, `azure_cli_outputs.json`, `workbench-1366.png`. The screenshot shows the workbench after sign-in and is orientation only; the proof is the JSON.
* Reused from merged notes, not repeated: [#107](./issue-107-live-assistants-evidence-2026-11-18.md), [#108](./issue-108-live-demo-evidence-2026-11-18.md), [#164 first pass](./issue-164-live-chat-grounding-evidence-2026-11-18.md) and [second pass](./issue-164-live-chat-grounding-evidence-r2-2026-11-18.md), [#216](./eval-gates-live-216-2026-11-18.md), [#432 batch](./ai-heldout-batch-432-live-2026-11-18.md), [human review effectiveness](./human-review-effectiveness-live-demo-2026-11-18.md) and the [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md).
* The first login attempt of the probe timed out waiting for the redirect to the app (transient); the second attempt succeeded. No other failure occurred.

## Fresh live observations (2026-11-18, about 13:42Z)

* `/api/assistants`: all five assistants (stock-prioritisation, assessment-preparation, funding-evidence, works-resident-coordination, quality-evidence) report `release.missing = ["approved, unexpired release record"]` and owner "RAI task owner not appointed (OQ-017)".
* `/api/assistants/forecast`: `proactive` false, `call_allowance` 0, rule `synthetic-gaps-2026-10-13-v1`.
* `/api/assistants/proposals`: six retained proposals, every one in state `disabled` with `envelope` null (the earlier #107 note counted five; one further denial was recorded after it, source not examined here).
* `/api/ai/report`: registry tasks include `chat-case-conversation` and `aftercare-concern-pack` with `enabled` false and state `disabled`. Consumption block `ai-consumption-v1`: 16 calls, 0 retries, 1 failure, 1 unknown liability, 0 accepted proposals, `token_cost` and `cost_per_accepted_proposal` Unknown, reconciliation `unreconciled`, coverage `incomplete`, an owned alert `liability-unknown` routing to workflow-only. Briefing runs: 254 total, 0 AI, 253 "Not reviewed", 1 Edited, 0 Accepted.
* `/api/ai/priority`: `recommendation` null. Evaluation block: 11 scenarios, `passed` true.
* `/api/chat/status`: `activation` `demo-only`, storage approved, retention 30 days.

These agree with the earlier same-day notes: the live demo denies model dispatch for every registered capability, no AI output is approved, and no accepted-proposal cost can be computed.

## Epic 104 acceptance criteria

| # | Criterion (state on the issue) | Demo result | Evidence | Tickable now |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Not met | The [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) gives epic 104 the verdict "Continue" and gates it on nothing; #440 itself is OPEN with two unticked criteria (deliver triaged RPI issues with owner approval for pivots and deferrals, and the PR research, plan, changes and review artifacts for the coordinator change). The criterion also states that merged children alone do not satisfy it. | No. Needs #440 closed and the owner's recorded pivot or deferral decisions. |
| 2 | All child features closed or deferred (unticked) | Not met | #105 and #106 are CLOSED. #107 and #108 are OPEN. #164 (under #157) and #216 (under #208) are OPEN and are named by the owner as epic 104 children for this audit. #432 is CLOSED. No owner-approved deferral is recorded for the open four. | No. Needs closure or an explicit owner deferral per child; see the gap tables below. |
| 3 | AI never approves, executes, ranks or mutates controlled records (ticked) | Consistent, fresh | Live: every assistant denied (`release.missing`), all six proposals `disabled`, `proactive` false, `priority` returns no recommendation, 0 Accepted briefings. Offline: `test_epic104_bounded_ai_invariants` ran inside the 115-test and 54-test suites cited in the #108 and #164 notes. PR #1596 and #1779 (per issue comments) tightened the authority-claim filter and proved the boundary across all registered capabilities. | Already ticked; no contradiction found. The 27-test invariant suite was re-run and passes. |
| 4 | Tokenomics: #432 complete or its gap recorded (ticked) | Consistent, fresh | #432 CLOSED. Live report shows cost per accepted proposal and token cost as Unknown with reconciliation `unreconciled`, which is the permitted stated-Unknown form. Missing inputs "dated model price" and "complete review effort" are named in the chat reply. | Already ticked; no contradiction found. |
| 5 | Tokenomics: no capability enabled beyond the exercise without finite owner-approved limits and an owned alert, BRD NFR-012 (ticked) | Consistent, fresh | Live: all registered tasks disabled or release-denied; the consumption block carries an owned alert; `/api/chat/status` states "engineering caps, not spend authorization". Repo-side `ConsumptionLedger` enforcement came from PR #1602 and #1779 per issue comments. | Already ticked; no contradiction found. |

## Remaining demo gaps for the four children

Classes: owner decision (a person with authority decides, no new engineering), person evidence (needs competent people, excluded from demo substitution), production-only (deferred to #1905 to #1908 per the #108 note), engineering or run (can be closed by a further run or code change within the demo authority).

### #107 Five assistants (two unticked)

| Criterion | Exact remaining gap for the demo | Class |
| --- | --- | --- |
| Independent SQL worker and race tests; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven on actual SQL Server 2022 locally (7 tests) and on a SQLite proxy (14 tests). Gap: the old-image change path has no actual SQL Server test, and nothing ran against Azure SQL or across separate container revisions. Open follow-up #1840 (malformed-completion classification) is tracked separately. | Engineering or run: add an MSSQL old-image case and run it on the disposable local service; an Azure SQL or revision-restart drill is excluded by the owner (no drills). |
| Matching approved exercise record permits bounded proposals only; delivered-build acceptance needs real AI, actual SQL and Azure evidence (CON-009/AC-057) | Denial side proven live again today. Approved side unproven: no release approver or residual-risk holder is appointed (OQ-017), so no approved record exists and no real proposal from the delivered image can be shown. | Owner decision: appoint the demo release approver and residual-risk holder, then record a release for one assistant and capture one real proposal. |

### #108 Evaluation harness (eight unticked)

| Criterion | Exact remaining gap for the demo | Class |
| --- | --- | --- |
| Model names, versions and quotas in the chosen region | Names, versions, capacity and rate limits confirmed for `gpt-4.1-nano` 2025-04-14 in uksouth. Subscription quota route returned an empty list. The model is `Legacy`, retiring 2027-04-14. | Engineering or run: obtain the regional quota from another supported route, or record the deployment rate limit as the demo quota. Region choice for production is production-only. |
| Freeze versions, independently labelled held-out split, thresholds | Frozen manifest, seed `demo-seed-432`, 12 cases exist. Labeller and prompt author are not independent; 12 cases are too few for cohort claims; thresholds are demo values. | Person evidence for independence; owner decision for threshold approval. |
| Competent humans detect and block every seeded critical proposal | No participants. | Person evidence. |
| Full effort and cost comparison, Finance validation | Cost components Unknown; no measured effort; Finance not involved. | Person evidence and owner decision. |
| Hashes, split, denominators, serving version, usage, reviewer protocol, outcomes | Hashes, denominator, version and usage recorded; no reviewer protocol or pass/fail/insufficient outcome. | Engineering or run: write the protocol and record an outcome for the measured batch. |
| Finite authorisation, payload handling approval, serving attestation | Authorisation recorded for 12 calls; payload approval and signed serving attestation absent; one earlier stopped call is not reconciled to a renewed authority. | Owner decision. |
| Delivered builds retain real AI, SQL and Azure proof (CON-009/AC-057) | Real batch calls and an `mssql` app exist; no registered generative task has produced a cited output (0 AI outputs, release denied). | Owner decision (same dependency as #107 criterion 2). |
| One routing or caching lever at a time against the same cases | Mechanism proven offline; no live lever measured; cached tokens 0 on all 12 calls. | Engineering or run: run one lever (for example caching) on the frozen 12 cases within a new finite authorisation. |

### #164 Chat grounding (four unticked, one negative constraint)

| Criterion | Exact remaining gap for the demo | Class |
| --- | --- | --- |
| Thresholds approved before enablement; accountable reviewer and enable state | Task registered and disabled; thresholds `proposed`; accountable individual unknown. | Owner decision. |
| Results bound to serving model and control versions with approved thresholds | Versions recorded; no actual-model chat evaluation exists because the live chat made 0 model calls on every ask (`activation-not-approved` or `not-called`, with `liability-unknown` routing to workflow-only). | Engineering or run: clear the unknown liability and run a finite-authorised chat batch; then owner decision on thresholds. |
| Competent humans detect and block seeded critical suggestions | No participants. | Person evidence. |
| Approved payload and provider handling, finite authority, consent and privacy approval | No call made, so no spend; payload and provider approval and human consent absent; DPO and Legal waived for the demo, not granted. | Owner decision. |
| Criteria do not authorise implementation, memory capture, calls or live use | No breach observed: task disabled for dispatch, memory inactive, model not reached. | Nothing to prove. |

### #216 Citation and refusal gates (one unticked)

| Criterion | Exact remaining gap for the demo | Class |
| --- | --- | --- |
| Gates set with owners and measured on a graded and adversarial set | Gates and owner exist in code; 30-prompt set measured: refusals 10 of 10 (rule layer, not model), citations valid 7 of 7 on only 7 model answers (lower Wilson bound 0.646), 13 non-refusal prompts never reached the model. Regulatory chat returned 403 for the test account. | Engineering or run: rerun all 30 prompts through the model after the UTC meter reset and with a `regulatory_chat` account. Named Legal and Compliance gate ownership and an independent grader are production-only. |

## Cross-cutting blocker

Four of the open items share one root: no named release approver or residual-risk holder (OQ-017) and an unknown liability that holds every model dispatch on the deployed demo. A single owner decision to appoint them and a finite authorisation would unblock the approved-side proof for #107, the delivered-build proof for #108 and the actual-model chat evaluation for #164. #216 needs only a later meter window.

## Resources and residue

No Azure resource, role assignment or app state was created or changed. The probe issued GET requests only. No throwaway resource needs deletion.

## Evidence limits

* Azure CLI facts are operator-observed and retained as a filtered JSON; the full command output was not kept.
* Observations of #107, #108, #164 and #216 beyond today's six GETs are reused from earlier notes and carry their limits, including that several of those notes' Azure CLI outputs were not retained.
* The sixth retained proposal's origin was not investigated.
* Only the invariant suite was re-run in this audit (from `src/agents`, `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_epic104_bounded_ai_invariants -q`: 27 tests, OK; observed, raw output not retained); the larger suites cited above were not.
* PR numbers and merge claims for #1596, #1602 and #1779 come from issue comments and were not re-verified against Git history here.
* Independent exact-head review and hosted CI are outstanding.
