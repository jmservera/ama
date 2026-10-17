---
title: Issue 358 phase details
description: Evidence-grounded implementation expectations
ms.date: 2026-10-17
---

## Metadata

Task ID: 358. Slug: entra-credential-preservation-358.
Plan: .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md.
Research: .copilot-tracking/research/2026-10-17/entra-credential-preservation-358-research.md.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Behavioral regressions and minimal reconstruction/readback fix | Not started |
| P02 | Mutation, existing gates and honest docs | Not started |
| P03 | Single Review, commits and push/PR | Not started |

<!-- rpi:phase id=P01 -->
## P01: Regression and preservation

Context: research C2-C5/W6. Ordinary configuration reads may omit secret values;
listSecrets may not provide all KV metadata. Neither source alone establishes a
safe replacement array. Use current read-visible configuration KV refs and list
values; no external secret reads or values printed. Do not touch #360 job logic.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add tests before source changes

Use the existing FakeAzure/invoke harness, fixed clock and synthetic mixed
inventory. Test generated and legacy selected names, old/boundary/missing/future
expiry in check/dry-run/apply; expired credentials remain for owner cleanup.
Test full KV rows, sparse name/value rows, omitted KV rows, config name-only/full
list refs, ordinary empty/nonempty values, environment secretRef and tokenStore.
Inspect exact PATCH payload as well as persisted state. Malformed list, duplicate
names, missing app value and failed list/PATCH/readback must not activate auth.
Use a scenario-local GET projection that removes ordinary values, while the
backing store and captured PATCH retain exact empty/nonempty values. After
persisted missing/altered name/KV URL/identity failures, reruns still block auth;
transient readback errors recover only after a matching inventory is observed.
Capture baseline assertion failures; existing expiry/delegate tests may already
pass and are not misrepresented as preexisting bugs.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Minimal inventory reconstruction/readback

Validate outer object/array and named dict rows; reject duplicates. Reconcile by
name without silent loss. Known KV metadata takes precedence over resolved
values; incomplete pairs/unrecoverable ordinary values produce sanitized errors.
Never return a success-shaped fallback. Validate before password creation.
Readback verifies presence of all retained names and exact KV URL/identity, not
app values that are write-only. Poll using existing wait_for; mismatch must stop
auth switch with a sanitized preservation-specific error. Existing secret creation,
credential-store discovery and verified-pair reuse stay unchanged.
Atomically tag the rebuilt inventory with a SHA-256 of sorted names and KV
URL/identity metadata (never values). Before any reuse, validate a pending tag
against current reference metadata; mismatch fails closed for human repair.
Clear the tag only after matching readback; a matching rerun can recover without
creating a duplicate credential. Do not persist values or delete credentials.

<!-- rpi:phase id=P02 -->
## P02: Validate and document

<!-- rpi:task id=P02-T01 -->
### P02-T01: Mutation and existing checks

In-memory mutations exercise both expiry paths, dropping KV fields independently,
and app-value loss; each must fail expected assertions, with no import/runner
error. Own venv under session workspace only; install editable src projects as
guided after missing-dependency evidence. Run setup/legacy, then full infra with
REQUIRE_AZ_BICEP=1, relevant Ruff/mypy/compile and existing offline Bicep commands.
No Azure account, token, secret, SQL or Graph call executes live.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Durable acceptance audit

Update existing infra runbook and cutover evidence with proof/limits, KB index and
append-only log. State non-production test Not run and exact unmet criterion.
No owner memory edit. Describe #360 shared-file overlap and sequencing.
Mark plan/details only for actual completed offline work, not live acceptance.

<!-- rpi:phase id=P03 -->
## P03: Review and publish

<!-- rpi:task id=P03-T01 -->
### P03-T01: One Review and PR

Read final diff and evidence once under rpi-review; separate execution/outcome.
Route any remaining finding to follow-up, not another review/fix loop.
An unresolved in-scope correctness/safety finding means unready/draft publication,
not a passing review. Only accepted nonblocking/out-of-scope limitations may be
deferred with offline-ready status; live proof remains UNMET either way.
Resolve gh api user for local author/committer noreply email; commit evidence and
source with Conventional Commit plus required Copilot trailer. Push only topic,
open main-targeted Refs #358 PR with criterion audit, SHA and validation.
No merge/force push, cloud change or live acceptance claim.

## Explicit Phase Log

* 2026-10-17 Details established from research; all work bounded to offline preservation.
* 2026-10-17 Single critique corrections applied: pending-handoff gate, realistic GET projection and review-outcome publication gate.
