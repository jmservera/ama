---
title: Regulatory security and privacy implementation plan
description: Bounded synthetic implementation for issue 217
ms.date: 2026-10-16
---

Task: 217 / regulatory-security-privacy-217. Scope: full plan.

## Executive Summary

Extend the merged regulatory assistant without claiming live approval. Add a
separate trusted regulatory-chat capability and matching registration contract,
metadata-only retention visibility with unknown periods kept explicit, atomic SQL
turn/referral audit, and recorded-reason requirements for consequential-decision
checks. Reuse existing projections, privacy settings, tables and human owners.

## User Decisions and Requirements

* Implement issue 217 in src/ and infra/ only for executable changes.
* ADR 0005 is accepted for synthetic development only.
* Draft, never approve, the DPIA for Juan Manuel Servera's DPO review.
* No private datasets, environment files, tenant identifiers, paid calls or Azure
  changes. No changes to mvp/ or prototype/.
* Produce RPI evidence, update READMEs/log, push and open a PR with Refs #217.
  Leave issue checkboxes to the merge coordinator.

## Goals

Demonstrate server-side separation, minimum necessary retrieval, tamper-evident
audit and explicit human/retention gaps using constructed local fixtures.

## Scope and Non-Goals

Source changes belong to core, API/auth and infra Entra configuration/tests.
The existing agents composer is exercised, not replaced. No generative model,
new SQL authority, destructive retention worker or operational activation.

## Functional Requirements

* Map RegulatoryChat separately from author and owner roles, granting it only
  from claims bound to one provisioned Entra principal. Existing thread ownership
  stays unchanged; add capability denial to direct and generic thread reads.
* Expose own-thread retention status using existing CHAT_RETENTION settings;
  distinguish simulated references, unknown periods and review-due records.
* Include checks/alerts/source/audit retention classes without inventing periods.
* SQL turn and referral writes and metadata audit must commit or roll back
  together. Keep question, answer, excerpt and health text out of audit metadata.
* A significant-decision check cannot be clear without reasons.

## Non-Functional Requirements

Portable parameterised queries; tests outside packages; no new dependencies.
Reuse existing lint/type settings. Preserve independent emergency routes,
author/owner separation, source immutability and offline-only admission.

## Acceptance Criteria

Local evidence must cover trusted role denial, direct/generic read denial,
minimum fact bundles, injected source/question containment, retention unknown
and simulated-period boundaries, SQL audit rollback and named human reasons.
Issue criteria requiring live/DPO evidence remain explicitly partial or unmet.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Controls

* [x] P01-T01: Implement role, retention, audit and reason controls.

<!-- rpi:phase id=P02 -->
### P02: Evidence and delivery

* [x] P02-T01: Add at most 20 focused tests across existing/new core, API and
  infra test files; remove none. Core owns retention/audit/reason semantics;
  API owns HTTP disclosure/auth; agents owns extractive injection regressions;
  infra owns registration parity. No generated fixture/eval changes planned.
* [x] P02-T02: Run targeted suites, ruff, mypy and loopback app; update draft DPIA,
  READMEs, index/log and changes evidence.

<!-- rpi:phase id=P03 -->
### P03: Publication

* [x] P03-T01: Record one post-implementation review, then commit, push and open
  the requested evidence-qualified PR. Source review assesses P01/P02; publication
  is tracked separately, not prematurely claimed.

Publication evidence: implementation commit f5ebc5e pushed to the topic branch;
PR 353 opened against main with Refs #217 and all seven criterion dispositions.
Source Review execution Complete, outcome Residual work. Full bounded plan
complete; issue-wide human/deployed acceptance remains open.

## Critique Disposition

One final-candidate critique executed; verdict Revise. Findings disposition:

* PC-001: Rejected on direct evidence. `evidence="SYN-HUMAN"` is an evidence
  identifier, not a recorded reason. The existing significant-decision test
  returns clear without a reasons field. Retain the narrower, explicit
  nonempty `reasons` requirement and engine-version invalidation.
* PC-002: Applied. Clarified Entra principal binding versus existing per-thread
  ownership; new tests target capability denial, not a new ownership design.

Planning readiness: Ready. No additional critique or user decision required.

## Follow-Up Items

* DPO completion and approved per-class retention/rights/hold policy.
* Tenant role provisioning and live ingress/Azure SQL evidence.
* Real Foundry minimisation and provider terms if generative chat is introduced.
