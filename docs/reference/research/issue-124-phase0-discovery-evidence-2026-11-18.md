---
title: Phase 0 retrofit-flow discovery evidence for the demo (issue 124)
description: Recorded 2026-11-18 evidence for what the repository contract and synthetic demo data show for Phase 0 discovery, what only human workshops and an approved company extract can prove, and a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 124
  - phase 0 discovery
  - BG-011
  - constraint register
estimated_reading_time: 7
---

Refs #124. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Nothing here is a company finding: every figure comes from the synthetic pack in [retrofit-synthetic-data](./retrofit-synthetic-data/README.md) or from the offline contract, and all of it stays `candidate_hypothesis_not_company_finding`.

Issue #124 has three unticked criteria (owner nomination and endpoint; lifecycle and event dictionary validated; constraint register with supporting and contradicting evidence). The fourth, that findings are not company findings until owners validate, is ticked and is re-checked below.

## Method

* Code under test: `src/core/src/zava_forward/core/discovery_contract.py`, `discovery_flow.py`, `discovery_register.py`. The probe imports the worktree copy by path.
* Offline tests: `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` from `src/core`, 59 tests, all OK (output retained in `.copilot-tracking/evidence/2026-11-18/issue-124-live/unittest.txt`).
* Probe: `.copilot-tracking/evidence/2026-11-18/issue-124-live/probe.py` with output `probe.json`. It exercises the contract with placeholder human names (they are not nominations) and counts the synthetic CSVs. No network, no credentials, no Azure call.
* Live Azure: not applicable. A search of `src/api`, `src/orchestrator`, `src/agents` and `src/importer` finds no runtime consumer of the discovery modules, so the deployed apps (`ca-cutover-test-demo-api`, `ca-resident-demo`) expose nothing to probe. No Azure resource was created or changed, so there is nothing to delete. No source changed (Tier FOCUSED).

## Observations

| Observation | Result |
| --- | --- |
| Default owner record | `NOT_NOMINATED` |
| Nominating an AI actor | Refused: "Discovery owner must name a human actor, not a blank, placeholder or AI actor" |
| Sponsor and owner the same person (case-insensitive) | Refused: "must be distinct people" |
| Nomination only | `ENDPOINT_NOT_AGREED` |
| Endpoint other than `accepted handover` (tried `installation`) | Refused |
| Nomination plus agreed `accepted handover` endpoint with human sponsor | `ENDPOINT_AGREED` (placeholder names, rule check only) |
| Default dictionary | 15 stages (10 flow stages plus 5 exception states), 15 events, 8 timestamp specs, 7 wait states, 4 return-loop kinds; 49 open validation gaps; `owner_validated=false` |
| Dictionary validation without a ready owner | `GovernanceViolationError`: readiness `NOT_NOMINATED` |
| Dictionary validation by an AI actor with a ready owner | `GovernanceViolationError`: 49 gaps open (gaps block before the actor check matters) |
| Seed register | 5 ranked hypotheses (CAP, HANDOFF, RESIDENT, DEPEND, QUALITY), each with 0 supporting and 0 contradicting evidence, each reporting two gaps, all `owner_validated=false` |
| Add supporting evidence only to CAP | One gap remains: contradicting evidence still required |
| Add both sides | No evidence gap for that hypothesis (five-part test and owner validation remain separate) |
| Default pack and `validate_discovery_pack` without an owner | Candidate status kept; validation refused |

## Synthetic demo data against the dictionary

The pack holds 992 candidates, 991 distinct properties, 9,859 lifecycle event rows (980 candidates have events), 322 candidates with an `ACCEPTED_HANDOVER` event, and every row flagged `is_synthetic`.

| Contract event | Synthetic event type | Rows |
| --- | --- | --- |
| candidate selection | `CANDIDATE_IDENTIFIED` | 992 |
| retrofit assessment completed | `ASSESSMENT_COMPLETED` | 857 |
| design approved | `DESIGN_APPROVED` | 801 |
| resident works decision recorded | `RESIDENT_WORKS_DECISION` | 634 |
| work release | `WORK_ORDER_ISSUED` | 534 |
| installation / practical completion | `INSTALL_STARTED`, `INSTALL_COMPLETE` | 946 / 465 |
| physical acceptance | `QA_PASSED` | 410 |
| evidence acceptance | `EVIDENCE_ACCEPTED` | 349 |
| resident handover | `RESIDENT_HANDOVER` | 332 |
| accepted handover | `ACCEPTED_HANDOVER` | 325 |
| ready to install, appointment, invoice, documentary completion | none in `lifecycle-events.csv` | 0 |

Four of the 15 contract events have no event type in the lifecycle log; appointments and finance sit in separate files (`appointments.csv`, `grant-and-finance.csv`). Other findings that a real extract would also need to survive:

* Mixed date formats: 8,818 event rows are ISO (2025-03-11 to 2026-10-07) and 1,041 are `dd/mm/yyyy`. A naive sort or min/max gives a wrong window, so the contract's strict date parsing matters.
* Return-loop signals: `DESIGN_RETURNED` 243, `DESIGN_RESCOPED` 28, `DESIGN_VARIATION_REQUESTED` 36, `INSTALL_ABORTED` 21, `CASE_REOPENED` 17.
* Delay coding: top candidate codes `DLY-SUP-CAP` 84, `DLY-RES-ACCESS` 49, `DLY-OTHER` 28, `DLY-RES-DECISION` 28, `OTHER` 22, `DLY-FUND` 21; 425 rows carry free-text delay notes. Capacity leads, which is a hypothesis-supporting signal in synthetic data only, and a generated pack cannot supply the contradicting evidence the register requires from a real extract.

## What needs human workshops and cannot be proven here

| Item | Why the demo cannot prove it |
| --- | --- |
| Sponsor nominates a named discovery owner; owner and sponsor agree `accepted handover` as endpoint | Needs a real executive sponsor decision. The contract only enforces the rule; placeholder names are not nominations. |
| Each stage, event, timestamp, wait state and return loop is validated by its operational owner | Needs owner workshops. 49 gaps are open by design; the guard refuses validation until each is closed by a named human in the role. |
| Twelve-month baseline population, queue owners, supplier references, pauses and reopens | Needs an approved company extract. The synthetic pack is generated and must not be treated as the population. |
| Constraint register with real supporting and contradicting evidence, five-part constraint test, domain-owner and discovery-owner validation | Needs the extract plus owner review. The contract shows the two-sided evidence rule works; it cannot create company evidence. |

## Per-criterion result

| Criterion in #124 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Discovery owner nominated and endpoint (accepted handover) agreed (UNTICKED) | Rule enforced (proven offline); company nomination cannot be proven | Probe shows human-only, distinct-person and endpoint refusals and the `ENDPOINT_AGREED` state with placeholder names. A real sponsor nomination is a human decision outside the demo. Stays unticked. |
| Lifecycle and event dictionary validated (UNTICKED) | Dictionary schema proven offline; validation cannot be proven | 15/15/8/7/4 counts match the brief; 49 owner-validation gaps are open and the guard refuses sign-off. Operational-owner workshops required. Stays unticked. |
| Constraint register records supporting and contradicting evidence (UNTICKED) | Two-sided rule proven offline; company evidence cannot be proven | Seed register has 0/0 evidence and two gaps per hypothesis; one-sided evidence leaves a gap, two-sided closes it. Real evidence needs the approved twelve-month extract. Stays unticked. |
| Findings are not company findings until owners validate (ticked) | Re-confirmed offline | All outputs show `owner_validated=false` and `candidate_hypothesis_not_company_finding`; pack validation without a ready owner is refused. |

## What this does not prove

* Any company finding, baseline, constraint ranking or owner decision.
* A live or deployed discovery surface: none exists, and persistence, a screen and extract import are not built (see the brief's delivery status).
* That the synthetic data distribution resembles a real extract.
