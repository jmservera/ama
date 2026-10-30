<!-- markdownlint-disable-file -->
---
title: Resident AI fallback diagnosis plan
description: Evidence-only completion plan with explicit unresolved runtime cause, Refs #563
ms.date: 2026-10-30
---

# RPI Plan: Resident AI diagnosis

## Task Metadata

* Task ID: 563
* Task slug: resident-ai-diagnosis-563
* Planning status: Ready for evidence/handoff only; single critique Pass; causal correction blocked
* Plan date: 2026-10-30
* Phase details: .copilot-tracking/details/2026-10-30/resident-ai-diagnosis-563-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/resident-ai-diagnosis-563-plan-critique.md

## Executive Summary

Implement a durable diagnostic report, not a speculative runtime fix. The
retained enabled revision proves the configuration names, endpoint and managed
identity matched the code. Its actual unavailable fallback cannot be attributed
to a particular stage because the stopped replica is unavailable and both
historical telemetry queries are denied. Current "AI not enabled" is explained
by the verified deliberate rollback, not the enabled attempt's failure.

The caller's exact root-cause goal remains unmet. Finish the requested local
validation, one independent Review and a local-only commit, preserving B1 and
the precise next diagnostic query for the coordinator. No source defect is
proved, so the conditional source-fix/test authority is not triggered. No
corrective configuration is justified; the two activation settings were already
correct. Never silently substitute evidence packaging for root-cause success.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated tracking artifacts.
* Use this worktree and ops/resident-ai-diagnosis-563 from main d934478fa4b877a17f83773a7f9eb7c2bd37b218.
* Diagnose only, using the specified activation/source evidence and read-only Azure queries confined to ama.
* No Azure resource changes, deployment, sign-ins, credential/.env/secret reads or secret output.
* Fix an established source/doc cause in src/ with outside-package regression coverage; otherwise report the exact corrective config when evidence establishes it.
* Run API discovery, Ruff lint/format and mypy locally with the specified source/test path; heavy work under flock -w 600 /tmp/ama-rpi-heavy.lock; no uv.
* Commit locally with the required Copilot trailer; no push; Refs #563 only.

## Goals

* G1: Distinguish disabled-state explanation from the enabled-runtime failure.
* G2: Establish exact cause if evidence permits, otherwise preserve the smallest concrete blocker without guessing.
* G3: Persist the diagnosis, one-pass phase evidence and requested local validation.

## Scope and Non-Goals

### In Scope

* Seven dated tracking artifacts, existing-source validation and coordinator handoff.
* Exact safe configuration values as verified facts, not an instruction to re-enable.
* One final-candidate critique and one post-implementation Review.

### Non-Goals

* Source, infra, knowledge-base or UI edits without an established causal defect.
* Azure mutations, inference, SQL access, sign-ins, network/RBAC changes, push/PR/issue edits.
* Live acceptance, source-to-image attestation, human approval or publication eligibility claims.

## Functional Requirements

* FR1: Report both observed labels and their different control-flow meanings (C2-C6).
* FR2: Compare all requested candidate causes against positive and missing evidence (W1-W7).
* FR3: Provide an exact bounded historical-query handoff, including what a generic result cannot prove.
* FR4: Preserve original activation evidence and disclose inaccessible telemetry and unknown model dispatch/spend.

## Non-Functional Requirements

* NFR1: Zero cloud writes, sign-ins, credential/secret access or external publication.
* NFR2: Every root-cause statement resolves to research evidence; no unproved "fix".
* NFR3: Heavy validation uses the shared lock with 600-second admission; no foreign process interruption.
* NFR4: Local commit author/committer use the freshly resolved GitHub noreply identity and required trailer.

## Acceptance Criteria

* AC1: Configuration, IAM, endpoint/deployment, code and cold-start alternatives receive explicit evidence-based dispositions.
* AC2: Exact enabled-runtime cause is either proved or plainly Blocked; this criterion is NOT satisfied by an unavailable fallback alone.
* AC3: A corrective code/config change is supplied only if its causal basis is established. Currently unavailable, not zero work assumed.
* AC4: All four caller-specified local commands have actual results or a recorded concrete blocker.
* AC5: One independent critique, one independent Review, full dated artifacts and local-only persistence.
* AC6: Human/live acceptance remains unchecked; issue #563 remains open and unmodified.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Research | .copilot-tracking/research/2026-10-30/resident-ai-diagnosis-563-research.md |
| Plan | .copilot-tracking/plans/2026-10-30/resident-ai-diagnosis-563-plan.md |
| Details | .copilot-tracking/details/2026-10-30/resident-ai-diagnosis-563-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-30/resident-ai-diagnosis-563-plan-critique.md, Complete / Pass for evidence packaging only |
| Changes record | .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md, implementation-owned |
| Readiness | Ready for evidence/handoff only; B1 blocks causal correction |
| Continuation | Explicit full-loop parent, automatic within caller scope |

## Sources

* Research C2-C8 and W1-W7: runtime control flow, retained revision metadata and denied telemetry.
* Caller constraints: no reproduction/sign-in, no cloud writes and no push.

## Test Ownership and Locked Change Budget

* Canonical source/test owners: existing src/api tests, maintained outside src/api/src package.
* Exact removals: none. Maximum added source files/tests: zero, because no causal defect has been proved.
* Canonical changed targets: seven task tracking artifacts only.
* Generated targets: external validation logs only; no generated assets or receipts committed.
* Semantic evidence: retained enabled revision and observed unavailable fallback; not a successful model call.
* Regression evidence: existing local API suite plus Ruff/mypy; no paid/cloud/browser evidence substituted.
* Validation commands: from src/api, with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`, run `python3 -m unittest discover -s tests -q`, `ruff check .`, `ruff format --check .`, `mypy`, all heavy commands serialized under the requested lock.
* Full publication gate: no publication authorized. No eligible full-gate receipt will be claimed; any future publication requires the repository's complete exact-head gate and independent assessment.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve bounded diagnosis and validate locally

* Intent: evidence-based report and actual requested command outcomes.
* Dependencies: Research complete within accessible scope; one critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Write diagnosis and coordinator handoff

* Requirement and evidence: FR1-FR4, C2-C8/W1-W7.
* Expected result: changes record distinguishes confirmed disabled rollback from unresolved enabled failure, includes query and verified settings without re-enablement.
* Detail section: P01-T01 in phase details.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute requested local validation

* Requirement and evidence: AC4/NFR3, caller exact command/path.
* Expected result: actual exit/test/skip outcomes or bounded lock/dependency blocker recorded; no invented pass.
* Detail section: P01-T02 in phase details.

<!-- rpi:phase id=P02 -->
### [ ] P02: Independent Review and local persistence

* Intent: assess the evidence boundary once and preserve it locally.
* Dependencies: P01 finished and plan/details/changes reconciled.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run one independent Review

* Requirement and evidence: caller full loop; original Review outcome must remain intact.
* Expected result: Review execution/outcome and residual causal blocker recorded, not called conformant root-cause delivery.
* Detail section: P02-T01 in phase details.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit artifacts locally and verify boundaries

* Requirement and evidence: AC5/NFR4, no push.
* Expected result: seven artifacts committed with privacy-safe identity and trailer, clean worktree, no source/infra/original-evidence changes.
* Detail section: P02-T02 in phase details.

## Dependencies

* B1: existing authorized private historical telemetry access is necessary for causal correction; not necessary to preserve this blocked diagnosis.
* Local dependencies/tools may be restored with pinned pip tooling only after an actual missing-dependency result.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| Single critique Complete / Pass; zero findings | Accepted | Evidence packaging only, not causal acceptance; B1 remains unresolved. No second critique |

## Follow-Up Items

* Rank 1: coordinator retrieves historical failed-attempt telemetry through existing approved private access; prerequisite to any correction (B1/W4-W6).
* Rank 2, conditional: if historical events contain only the generic fallback marker, separately scope privacy-safe allowlisted stage/reason diagnostics before any independently authorized reproduction (C6).
* Original Review RV-003 disputes shared-lock compliance. Parent does not adopt an unevidenced prohibition contrary to the caller's exact lock requirement; retain the original finding and disposition for coordinator context, without relocating the lock, rerunning checks or inventing a runtime defect.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md.
* Ready task: P02-T02 scheduled local persistence. One original Review executed Complete / Not accepted as causal diagnosis; B1 remains open. P01 and all four local commands complete; original dependency failure preserved, restored rerun passed with318 skips.
* B1 remains an explicit unmet root-cause goal. Do not retry inference or change config to "test" a guess.
