---
title: Explicit Microsoft Account Selection
description: Scoped account-switch repair and safe diagnostic evidence
ms.date: 2026-10-13
---

## Task Metadata

Task zava-account-switch-2026-10-13; automatic child of zava-tenant-staff.
Continuing branch docs/zava-north-homes-challenge, open PR #65.

## Executive Summary

Separate Switch account from Sign out. Switching goes directly through a
fixed public /sign-in?switch=1 route to Easy Auth with prompt=select_account,
not through provider logout. Ordinary sign-in/sign-out stays unchanged.
Add constant auth-flow console events collected by existing Azure Monitor
routing. Validate synthetic routes and deployed Microsoft account chooser,
without claiming a personal session changed. Owner retry of the specified
rubric run already succeeded; no workflow or credentials change justified.

## User Decisions and Requirements

* Owner confirms tenant role access.
* Fix Use another account, which currently only signs out.
* Read Azure logs; ensure useful diagnostics for the next attempt.
* Inspect failed job and owner-started retry without launching a duplicate.
* Continue automatic RPI and publish on the existing coherent branch.
* Once finished, integrate all learning into its proper PRD, ADR or addendum
  sections, not only chat/operator instructions.

## Goals

Offer deliberate account selection while preserving safe app access and
providing privacy-safe operational traces for future reports.

## Scope and Non-Goals

mvp/zavaforward_mvp/auth.py, server.py, tests/test_auth.py; directly related
infra/MVP guide and knowledge-base routing/log; existing app image rollout;
dated learning in PRD review-learning disposition, ADR 0002 identity decision
and addendum exercise evidence. No BRD business change is implied.
No auth exemptions, Entra roles/permissions, generic URL logging, new logging
resources, MSAL dependency, forced global logout or rubric workflow edits.

## Functional Requirements

* Trusted-proxy switch response targets /sign-in?switch=1; normal logout keeps
  /.auth/logout?post_logout_redirect_uri=%2F.
* Parse only exact switch=1 (single value); append only fixed select_account,
  not caller-supplied prompt/return destinations, to fixed /app login.
* Existing JS already follows server response redirects; no unnecessary UI edit.
* Fixed flow events for explicit switch request, chooser start, ordinary
  sign-in/sign-out and authorized workbench arrival.
* Password development mode remains local and does not invoke Microsoft.

## Non-Functional Requirements

Do not log names, ids, cookies, principals, query values, tokens or callback
URLs. No full access logging. Existing tenant/role/oid/CSRF gates preserved.
New image changes runtime only, preserving SQL staff, AI, scopes, secrets and
token-store configuration. No directory or user session credentials needed.

## Acceptance Criteria

* Normal sign-in/sign-out/password behavior and existing access tests pass.
* Explicit switch targets fixed local route and Entra select_account with no
  logout-first dependency; untrusted/duplicate flags cannot override targets.
* Synthetic valid-principal switch and arrival events contain constants only.
* Local Docker validation (sudo existing access) passes before ACR upload.
* Deployment ready; real HTTPS switch route reaches tenant authorize with
  prompt=select_account, correct callback and /app destination preserved.
* Browser shows Microsoft account-selection/sign-in surface, no authentication
  bypass. Actual already-authenticated replacement is explicitly owner-owned.
* New flow events visible in console and existing centralized table.
* Private before/after configuration comparison preserves env/secret references,
  identity, registry, ingress and Easy Auth scopes/token-store settings; only
  tested image and platform-owned revision fields differ.
* Original job cause and successful retry recorded; publish through #65.
* Knowledge compounds in canonical project docs with dates, source links,
  observed versus proposed/owner-reported distinction and unverified gates.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Repair, validate, deploy and publish
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement explicit chooser and fixed-event diagnostics
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate local image and live flow/log ingestion
<!-- rpi:task id=P01-T03 -->
#### [ ] P01-T03: Document and publish

## Candidate Test and Target Lock

Primary owns tests/test_auth.py. Existing switch expectation intentionally
changes; all other existing expectations remain. Removals none, maximum three
new test methods, with subcases for input/capture/password. No generated test
source. Source modules above are canonical. Existing auth/full MVP plus
JavaScript syntax and image live checks are regressions; real Entra prompt
and constant event captures are semantic checks. Private deployment evidence
stays in session workspace, no tokens or names in Git.

## Critique Disposition

One final-candidate critique executed, verdict Revise. Both findings directly
disposed; no significant owner choice or repeated critique.
PC-001: details enumerate all five fixed events; synthetic subcases assert
complete messages and denied requests emit no successful-flow markers. Live
normal/picker GET markers collected; authenticated markers remain owner-pending.
PC-002: private before/after app/auth configuration and tested image digest
comparison required before completion; unexpected drift/readiness/route
failure triggers prior-image rollback. No secret values or SQL writes.
Exact flag parsing retains blanks so duplicate switch=1&switch= is rejected.

## Follow-Up Items

Owner actual signed-in account replacement after deployed chooser; cannot
manufacture remembered accounts or authenticate using CLI credentials.
Retained tenant naming remains separate previously routed work.

## Handoff

Research executed and Ready; single critique directly disposed, plan Ready.
Proceed automatically to P01. No blockers.
