---
title: Public browser access implementation plan
description: Bounded private-origin public edge for issue 344
ms.date: 2026-10-16
---

Task ID: 344. Slug: public-browser-access-344. Status: implemented and reviewed,
publication pending; real-user and full feature acceptance Blocked.

## Executive Summary

Add Front Door Premium, WAF Prevention and Private Link to the existing internal
proof environment. No environment replacement or deletion. Retain private data
services. Restore browser redirect configuration without pretending that the
invalid existing client or missing credentials permit real-user acceptance.
Audit all historical visible features and file prerequisite/feature gaps.

## User Decisions and Requirements

* Refs #344 #143 #200, never auto-close issues.
* Public browser entry, health 200, protected API 401, sign-in redirect to Entra.
* SQL publicNetworkAccess Disabled, no bypass, ama only, no group deletion.
* Source/infra only; preserve legacy/private files and workflow/check names.
* Honest tenant and feature acceptance; owner alone approves operational use.
* Local-first tests, RPI evidence, README/log updates, push topic branch and PR.

## Goals

Public transport to the unchanged src API without exposing any data service;
reproducible additive configuration and precise acceptance boundaries.

## Scope and Non-Goals

Infra edge, callback initialization, auth boundary and focused tests; evidence
pack/JSON/matrix, reference index/log. No tenant object creation, credentials,
staff fabrication, private datasets, production-profile conversion or teardown.

## Functional Requirements

Forward HTTPS with correct origin host/TLS, health probe /healthz, explicit /*
route, WAF all routes, no caching of authenticated content. Forwarded-host
authentication and edge-aware callback initializer. API responses stay 401,
welcome public and browser entry redirects. Preserve current ingress auth
settings except reviewed browser-mode/proxy changes.

## Non-Functional Requirements

Private origin and SQL remain Disabled. No resource deletions, policy changes
or secret output. Mark completed redirect separately from successful login.
Independent critique once, postimplementation Review once.

## Acceptance Criteria

Audit each #344 criterion: public URL and browser entry (Partial until real
login), edge choice, health/API responses, private SQL, full feature inventory
with filed gaps, honest browser smoke. Only observed facts receive Passed.
Do not tick issue criteria; coordinator owns ticks at merge.

## Phase Checklist

<!-- P01 -->
### P01: Implement and validate infrastructure

* [x] P01-T01: Add additive existing-stack edge entry point and correct edge
  health/routes; validate private origin and authenticated ingress prerequisites.
* [x] P01-T02: Support edge-host callback repair and protect exact anonymous
  boundaries, adding narrowly owned tests.
* [x] P01-T03: Run Bicep/infra tests, scoped ruff/mypy and local app smoke.

<!-- P02 -->
### P02: Deploy and capture honest public evidence

* [x] P02-T01: What-if ama-only additive resources; apply, approve only this
  edge's pending Private Link request. Preserve all existing resources.
* [x] P02-T02: Configure browser redirect/proxy, curl public welcome, health,
  API denial and Entra redirect; retain tenant blocker and SQL state.
* [x] P02-T03: Audit historical visible features against deployed app, file
  gaps, update README/evidence JSON/matrix/index/log.

<!-- P03 -->
### P03: Review and publish

* [x] P03-T01: Reconcile evidence and perform one postimplementation Review.
* [ ] P03-T02: Resolve account, configure repo-local noreply email, commit with
  trailer, push and open PR; no merge.

## Locked Test and Change Ownership

Removals: none. No legacy files or private data reads. Maximum additions:
one Bicep entry point and two focused test files, if existing tests cannot hold
coverage. Reuse edge/auth tests first. Canonical code: infra modules and existing
initializer; generated evidence: existing JSON and parity TSV (only if changed).
Semantic tests: exact status/location, forged-header denial and private origin;
regression tests: existing auth and compiled profile controls. No proxy count
claims or successful browser login inferred from redirects.

## Follow-Up Items

Tenant registration, secret, callbacks and staff prerequisite; full real-user
feature audit with continuing synthetic dataset; other gaps only if observed.

Execution amendment: Standard trusted a client RFC Forwarded host; both
entry points and callback initializer now use exact Custom X-Forwarded-Host/
Proto settings, verified by repeated public hostile probes. Azure rejected a
reserved-header removal trial; only its empty unused owned rule set was deleted,
as precisely recorded in details/changes/JSON. No pre-existing deletion.
Native public API curl 401 Passed; browser User-Agent API 302 remains a filed
#350 gap, not completed API-coexistence acceptance. Checkmarks record executed
tasks and filed blockers, not satisfaction of unmet acceptance criteria.

## Critique Disposition

One independent critique executed, verdict Revise, all four corrections applied
directly; no user decision or repeat critique.

* PC-001: sole fixed API origin/host header/TLS and endpoint domain; no alternate
  origins or rewrite rules; compiled and live hostile-host/callback gates.
* PC-002: no API exemption without trusted-header provenance and positive
  contract evidence. If unavailable, retain blocked coexistence, not a bypass.
* PC-003: capture non-secret auth baseline, restore it and disable only the new
  endpoint if critical smoke fails. No deletion; retained resources recorded.
* PC-004: historical asset names come solely from the supplied parity matrix;
  current src paths/image manifest are separate from auth intercept/rendering.

## Handoff

Research: .copilot-tracking/research/2026-10-16/public-browser-access-344-research.md.
Details: .copilot-tracking/details/2026-10-16/public-browser-access-344-phase-details.md.
Changes owner: .copilot-tracking/changes/2026-10-16/public-browser-access-344-changes.md.
