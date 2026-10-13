---
title: Public Welcome and Entra Account Menu Implementation
description: Secure explicit workbench entry and real own-user profile photo
ms.date: 2026-10-12
---

## Task Metadata

* Task ID: zava-workbench-entry-2026-10-12.
* Mode: Confirmed automatic.
* Research: .copilot-tracking/research/2026-10-12/zava-workbench-entry-research.md.
* Details: .copilot-tracking/details/2026-10-12/zava-workbench-entry-phase-details.md.

## Executive Summary

Provide a public Zava Forward welcome with the supplied logo and an explicit
sign-in button. Keep /app and every data API protected. Replace the text-only
sign-out control with an accessible account panel showing the current Entra
account and its real Microsoft photo when available, plus sign-out and switch.

### What You May Not Know

Microsoft photos require a delegated Graph token, not an ID-token picture
claim. Container Apps supplies that token through its private Blob token
store. A small, narrowly scoped maintenance job renews its five-day
user-delegation SAS daily; account keys remain disabled. Users may need a fresh
sign-in and normal User.Read consent. No username/password is shared with the
assistant, and the existing app registration/roles are not recreated.

## Sources

Research C1-C4/W1-W5 and the current MVP, infrastructure and initializer.
The owner's isolated --login --check completed successfully and reported the
existing callback already initialized on 2026-10-12.

## User Decisions and Requirements

* Workbench sign-in works; improve entry rather than describe it as broken.
* Show app name/logo and an explicit sign-in button without prompting merely
  for visiting the main page.
* Show the Entra user picture on an account control with sign-out/change-profile.
* Keep working autonomously through the full implementation.
* The owner completed the isolated tenant login/check. Never collect or record
  its device code, passwords or tokens.

## Goals

Public branding with deliberate protected entry; clear current-account UX;
real delegated own-photo integration; safe reproducible deployment.

## Scope and Non-Goals

Scope: MVP entry, account UI/auth/profile modules/tests, optional token-store
infrastructure and renewal command, deployment, related guides/index/log.
Non-goals: Broad Graph grants, app recreation, changed resident workflows,
shared storage keys, new model/agent behavior, or bypassed human consent.

## Functional Requirements

* Root serves welcome only; /sign-in redirects to Microsoft with /app return.
* /app serves the existing workbench and retains all API role controls.
* Exact public exemptions include root, welcome assets and /sign-in, not /api.
* Account details use authenticated Entra claims without persisting them.
* Server photo endpoint fetches only Graph /me/photo/$value with the
  platform-injected token, no browser token payload or arbitrary user URL.
* No-photo and error states show initials plus an explicit status.
* Logout returns home; switch clears the app session and selects an account.

## Non-Functional Requirements

Native keyboard-operable details/summary, Escape/outside close, visible focus
and mobile containment. Photo requests have timeout/size/type/signature limits
and no redirects. No secrets or real user photo artifacts in Git/logs.
Token renewal fails explicitly and never overwrites a valid secret on failure.
Keep Azure SQL, AI configuration and continuing synthetic data unchanged.

## Acceptance Criteria

* Anonymous live / returns 200 with name/logo/button and no auth redirect or
  protected data requests; /app redirects and anonymous /api/me remains 401.
* Public logo/styles load, including at 375 CSS pixels.
* Local regression covers existing password development and production
  denial without a second shared-password form.
* Account menu, logout/switch and server photo success/failure are tested.
* Shared keys disabled; private token container; renewal job actual execution
  writes a live bounded SAS without printing it; token store activates only
  after bootstrap success.
* Actual signed-in photo is a real-user acceptance gate, not a simulated
  proxy-header claim. Record any human/session/consent limitation explicitly.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Welcome and account behavior

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Public welcome, protected route and explicit sign-in

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Own-account metadata/photo and accessible logout/switch menu

<!-- rpi:phase id=P02 -->
### [x] P02: Supported private token store

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Identity-only storage, least-scope renewal and staged auth config

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Test SAS bounds, failure/preservation and no credential output

<!-- rpi:phase id=P03 -->
### [ ] P03: Validate, deploy and publish

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Unit/API/Bicep/browser checks and real image build

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Deploy, bootstrap token store, activate and verify live boundaries

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Update guidance/index/log and publish to continuing #65

## Test Ownership and Candidate Lock

Primary owns all tests. No removals. Maximum 40 additions across MVP/API/auth,
photo and renewal tests; reuse existing suites and installed dependencies.
Canonical source: mvp and infra. Generated browser/image evidence remains
outside Git in the session; never save a real user photo or token.
Semantic coverage: auth boundaries, Graph delegation and SAS lifecycle.
Regression coverage: prior role projection, local login, lists, branding,
real SQL/model configuration and read-only/non-root image behavior.

## Critique Disposition

Final candidate ready for exactly one independent critique. Execution/verdict
and each compatible correction will be recorded before Implement.

Critique executed once, verdict Revise, five findings. All dispositions are
resolved for implementation; no second critique or user decision is needed.

* PC-001: Apply explicit Container Apps globalValidation.excludedPaths changes
  in P01, not just application routing. Live anonymous checks own acceptance.
* PC-002: Add a new container-scoped Contributor resource and a separate
  account-scoped Delegator. Do not reuse account-wide Contributor grants.
* PC-003: Clarify a separate token-only account, not the existing evidence
  account. Retain researched isolation: existing evidence API/import identities
  already hold account-wide Blob Contributor and must not read other users'
  authentication tokens. Reuse private-endpoint/diagnostic patterns.
* PC-004: Prioritize credential bounds/failure/redaction and photo/auth boundary
  coverage over cosmetic assertions within the existing 40-addition cap.
* PC-005: Verify supported refresh/secret rotation behavior in deployed config
  and platform documentation; record any real-user expiry limitation rather
  than assert live authenticated acceptance from a mock.

## Follow-Up Items

* Prior tenant naming/role migration is outside this UX task; the original
  owner/provisioning follow-up remains distinct.
* Human workbench/consent/photo acceptance may require a real user session;
  owner acceptance remains separate from source and server checks.

## Handoff

After critique, execute P01-P03 and maintain the changes record. No source
changes during Plan; one post-implementation Review only.
