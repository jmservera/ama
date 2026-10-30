---
title: Both demo sites redeployment plan
ms.date: 2026-10-30
---

## Task Metadata

Task f09558e0-64f4-4440-856f-8e9a302dbb6f; slug demo-sites-redeploy.
Pinned origin/main ffd8f35e63b24905b9aeb937dbf2a7fe9968747f.

## Executive Summary

Rebuild and roll resident then employee using the successful #545 route,
initialize sensor tables and reconcile the resident SQL view, preserve full
configuration and registry policies, and record actual live browser results.
Only evidence is committed locally; no source change, push or approval claim.
Implementation result: Partial / blocked. Both local images built and exact
hub-scoped role granted. Financial admission did not establish all-in headroom,
so no registry push, SQL initialization or app rollout occurred. Both old live
sites remain Healthy; latest-main delivery and authenticated UX are unmet.

### What You May Not Know

Creating sensor tables does not start telemetry ingestion. Authenticated UX
checks may be blocked by owner-held resident credentials and Entra login.
Public health is not proof of target revision or feature acceptance.

## Sources

Research: .copilot-tracking/research/2026-10-30/demo-sites-redeploy-research.md.
Prior details: .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md.
Operations notes: infra/README.md, IoT and resident SQL sections.

## User Decisions and Requirements

* Redeploy both sites from current origin/main to ama; follow #542/#545.
* Authority through 2026-11-15; preserve min0, eight Manual jobs, ACR policies
  and live digests; never delete RG, print secrets or read .env.
* Grant minimum IoT data-plane role and create sensor tables using existing
  in-VNet initializer; counts only, no endpoints or broad roles.
* Use nonblocking shared lock for heavy work; defer if busy.
* Verify named UX with Playwright/curl and record blocked steps honestly.
* Complete one full RPI loop and local Conventional Commit with exact trailer,
  Refs only; coordinator pushes.

## Goals

Both named sites run immutable images built from the pinned tracked source.
SQL schema/view compatibility is proven without exposing rows or changing
resident access boundaries.

## Scope and Non-Goals

Only two app images/revision suffixes, scoped hub Registry Contributor for
verified current operator, additive sensor schema and optional view reconciliation.
No datasets, seeds, policy/control rows, secrets, model activation, devices,
new endpoints, job image refresh, infrastructure redeploy or unrelated app.

## Functional Requirements

Use local Docker with src context, unique tags, OCI source labels, remote
manifest/config binding, old-manifest presence and raw ARM template PATCH.
Execute finite SQL once with no automatic retries and restore initializer.

## Non-Functional Requirements

Private backups0600 under current session files; command journal has unique
invocation names and redacts token-bearing calls. ACR max600s, forward420s,
reserve180s; private-first exact restore. Detect concurrent drift before writes.
No heavy build or gate without flock -n admission.

## Acceptance Criteria

Target latest=ready Healthy/Provisioned, active100%, exactly one forward revision
each, retained history/digests, full protected app/auth equality and min0.
All eight job definitions restored Manual, complete ACR stable equality.
Sensor tables exist, counts only, no data/policy/permission expansion beyond
the exact approved role. Resident view principal/SID/narrow rights unchanged.
Feature result matrix distinguishes live pass, static availability and blocked.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Preserve and prepare
<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Capture complete backups and preflight; grant exact role
<!-- rpi:phase id=P02 -->
### [ ] P02: Build, initialize and roll
<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Build both images under nonblocking lock and push privately bounded
<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Initialize schema/view once via existing in-VNet job
<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Roll resident then employee with preservation and recovery contracts
<!-- rpi:phase id=P03 -->
### [ ] P03: Verify, review and persist
<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Live curl/Playwright checks and invariant readback
<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: One independent Review and local evidence commit

## Current Work Disposition

| Task | Actual execution |
| --- | --- |
| P01-T01 | Backups and narrow role complete; financial admission blocked, not checked complete |
| P02-T01 | Both local builds pass; push blocked, not checked complete |
| P02-T02 | SQL initialization stopped before any job/schema write |
| P02-T03 | Both app rollouts stopped before write; no new revision |
| P03-T01 | Public curl/browser and full invariant readback pass; named authenticated UX blocked/unavailable |
| P03-T02 | Independent Review Complete / Not accepted; original eight-file evidence committed locally as e05183b6, no push |

## Test Ownership and Targets

No source or canonical test changes; removals none, additions zero.
Generated private executors/evidence remain external. Existing deployed health,
asset hashes, exact Azure comparators and browser checks own validation.
Semantic UX acceptance is not replaced by static/regression evidence.
Complete publication gate is coordinator-owned before push, not claimed here.

## Critique Disposition

One independent critique executed Complete / Revise, original preserved at
.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-plan-critique.md.
All four planner-owned corrections applied directly, no second critique:

| Finding | Disposition and resolving contract |
| --- | --- |
| PC-001 High | Accepted; details cleanup compares expected owned deltas; only retry field restored, seven untouched jobs read-only; drift blocks dependent writes. |
| PC-002 Medium | Accepted; SQL success requires worker/input hash, one execution/attempt and bound post-COMMIT marker with terminal success. |
| PC-003 Medium | Accepted; recovery600s remaining-time bound, sanitized private diagnostics and no repeat recovery. |
| PC-004 Medium | Accepted; RG-only aggregate cost preflight, existing USD700 all-in ceiling and external-liability Unknown admission refusal. No broader scope or role requested. |

Implementation-ready with conditional admission. If financial evidence remains
Unknown, paid push/job/rollout steps stop; local builds, read-only browser and
the approved no-charge scoped role can proceed independently.

## Follow-Up Items

* Authenticated owner acceptance if credentials/session unavailable.
* Publication full gate, independent exact-head assessment and hosted/human
  approval remain coordinator-owned; no push is authorized here.
* Highest priority: coordinator supplies current bounded all-in cost evidence
  under existing envelope, including U/commitments/reserve, then resume a later
  authorized deployment task. RG totals alone are not all-in headroom.

## Handoff

Details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-phase-details.md.
Changes target: .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-changes.md.
