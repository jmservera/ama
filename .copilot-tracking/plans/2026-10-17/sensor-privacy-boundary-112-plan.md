<!-- markdownlint-disable-file -->
# RPI Plan: Sensor privacy boundary

## Task Metadata

* Task ID: 112; slug: sensor-privacy-boundary-112; date: 2026-10-17.
* Status: Ready after one critique and direct dispositions.
* Details: .copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/sensor-privacy-boundary-112-plan-critique.md

## Executive Summary

Verify sensor observations are exact synthetic generator output before SQL
admission. Close the recursive chat-home export and refuse malformed nested
values before legacy AI or map serialization. Preserve manual detail and
existing static tiles; add no sensor AI capability or operational approval.

### What You May Not Know

There is no implemented sensor-analysis read model or registered sensor AI
purpose. New derived health indicators would invent an unapproved method.
Replay proves observation construction, not the truth/approval of stock anchors.
Replay requires temporary disk/time and current generator revision; old snapshots
must be regenerated, not silently trusted.

## User Decisions and Requirements

* Full ordered Research, Plan/critique, Implement and one Review, committed artifacts.
* Raw readings/device identifiers excluded from AI/map/cluster/log boundaries.
* Synthetic only, never pseudonymization or filename inference.
* Preserve manual work, all existing safety/quality/finance/current-actor controls.
* No live systems, private data, new deployments or legal/consent/threshold invention.
* Parent #109 hierarchy only; no issue dependency or closing keyword.

## Goals

* Close actual admission and structured export leaks without widening authority.

## Scope and Non-Goals

Core sensor loader, chat projection, legacy AI field validation, map scalar
validation and focused tests/docs. No web, provider/framework changes or broad
security audit. No blanket service hold. Free-prose semantic DLP is not claimed.

## Functional Requirements

* Missing/real/unknown/malformed manifests refuse before schema/register writes.
* Replay from current generator, seed/window and explicit stock Selection;
  exact manifest/payload match required. Load private replay bytes to avoid races.
* Unknown nested home data never enters chat; allowed fields must be scalar.
* Legacy prompt/citation and map display fields cannot stringify containers.
* No raw observation values, source paths, device identifiers or exception payloads
  in loader rejection messages/logs. Success receipt contains bounded counts only.

## Non-Functional Requirements

Reuse existing generator/hash/access helpers. Preserve idempotency and SQL
parameters/schema. No persistence schema changes. Configured Ruff/format/mypy
and relevant core/agents/API tests, using a pip-installed local worktree venv.

## Acceptance Criteria

* Sentinel device/raw values absent in captured assembled chat/legacy AI inputs
  and serialized points/forced clusters/logs.
* Malformed values explicitly refuse; nested unknown diagnostics are excluded
  by field authorization rather than sensor-name matching.
* Relabelled and rehashed real readings, missing/unknown manifests, changed
  revision and register mutations refuse without any SQL operation.
* Valid generated tiny normal/stock fixtures remain loadable and idempotent.
* Original Review retained, adverse findings routed or corrected at most twice.

## Sources

Research C1-C9 in .copilot-tracking/research/2026-10-17/sensor-privacy-boundary-112-research.md.
Component READMEs and actual #112 body; no historical PR accepted as proof.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Boundary regressions and implementation
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Write failing-first exact-boundary tests
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Verify synthetic admission and close exports

<!-- rpi:phase id=P02 -->
### [x] P02: Verification and durable documentation
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute component checks and document limits

## Dependencies and Shared-File Overlap

No issue dependency. #88 overlaps planned store.py, core README, KB index/log;
avoid finance/server/web/projection/resident/workflow edits. #102's branch
production delta is already in this base; store/core README/KB are shared
surfaces. Only surgical boundary changes; do not touch other worktrees. No
history rewrite, automatic merge or issue closure.

## Test Ownership and Candidate Lock

Core owns new test_sensor_privacy.py, maximum 18 test methods; no removals.
Existing test_sensor_stock may pass its explicit Selection to the loader.
Canonical targets are core source/tests, no generated dataset committed.
Semantic coverage: actual captured prompts, map payload/log values and no SQL
before refusal. Regression coverage: current AI/chat/map, synthetic loader and
cross-project API/agents. No MSSQL required unless actual persistence behavior
changes; pre-write admission validation only, existing SQL portable tests apply.
No browser required: no web edits.
Actual task-owned loopback MSSQL admission test was additionally executed:
one pass; UUID database, exact owned container and credential file cleaned.
Full core discovery was killed with exit 137 and cannot be claimed passed.
Focused core selection 143 run/142 pass/one optional MSSQL skip; actual MSSQL
executed separately. Agents 94 pass; API 707 run/500 pass/207 existing skips.
All three configured Ruff/format/mypy checks passed. Agents chat_eval source
binding updated to the closed source contract after full regression caught
its dependency on the removed CASE_KEYS constant; no eval results regenerated.

## Critique Disposition

Single critique execution Complete; original verdict Revise retained.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Rejected, erroneous execution premise | Current parent instructions permit self-owned TemporaryDirectory; they do not prohibit temporary directories or require all scratch inside checkout. Public stock destination guard stays unchanged. Tests already use disposable temporary directories. No guard bypass needed. |
| PC-002 | Applied | Strict integer seed/homes/days/cadence and ISO as_of; default replay budget 2,000,000 nominal rows and steps, explicit positive max_rows override for trusted offline callers. Check before generation. |
| PC-003 | Applied | Race oracle mutates original register/shard inside schema hook, captures inserted values; missing/mismatched stock Selection and unchanged/rehashed manifest mutations tested before any SQL. |

No new user decision, no repeated critique.

## Follow-Up Items

* Real-use inventory, source authority, DPIA/lawful basis, retention and
  scientifically reviewed thresholds remain human-owned OD-43 work, not this fix.

## Handoff

Changes: .copilot-tracking/changes/2026-10-17/sensor-privacy-boundary-112-changes.md.
One original Review Complete / Not accepted retained unchanged. Correction ONE
for RV-001/RV-002 implemented and verified: raw status-input validation at
external context only and pre-dispatch/pre-audit document metadata validation.
Manual status/detail and document content/manual paths preserved. Two new
core methods (16 total, <=18 cap) reproduced six pre-correction failures;
corrected focused core145 run/144pass/one opt-in SQL skip, agents94pass,
focusedAPI86pass; all configured Ruff/format/mypy pass. No second Review or
independent Pass. Ready for normal publication; final-head acceptance remains
coordinator-owned. No legal approval invented; full-core exit137 incomplete.
Published main PR https://github.com/jmservera/ama/pull/393 by normal push;
delivery state records implementation commit and coordinator handoff.
