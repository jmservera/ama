---
title: Resident assistant Azure OpenAI implementation plan
ms.date: 2026-10-27
---

Task: #469. Slug: resident-assistant-aoai. Refs #466.

## Executive Summary

Replace the optional echo adapter at the host composition boundary with a real
Azure OpenAI sentence-selection assistant. The model chooses explanatory text
from an own-case, approved sentence catalogue; arbitrary model text is never
displayed. Preserve the deterministic provider, accessible topic controls and
human routes. Use existing SQL for a lifetime USD20 reservation ledger and
per-resident limits, with managed identity inference on a dedicated small
Standard deployment. Fail closed to rules on any uncertainty.

## User Decisions and Requirements

* Full ordered Research, Plan, Implement, Review; dated committed artifacts.
* RG ama only; no keys, new groups, ingress changes or unrelated Azure roles.
* USD20 inference ceiling; resident USD30 within USD700 through 2026-12-31.
* Own-case status/documents/forms only, never decide or give specialist advice.
* Branch from merged main, PR to main, refs #469/#466, no closing keywords.
* Scoped changed-path gate; timeout-zero shared heavy lock for Docker; no uv.

## Goals

Meaningful real inference without giving the model consequential authority.
Durable atomic spend/rate controls and explicit, usable fallback.

## Scope and Non-Goals

Runtime backend, existing assistant notice, dedicated default-off infra,
accounting SQL, focused tests and evidence. No free text, document ingestion,
identity redesign, case mutations, ingress or production activation.

## Functional Requirements

Session-authorised topic requests bind to own-case mapped facts only.
Model may return only validated IDs from that request's sentence catalogue.
Missing document requests stay explicitly unknown. Mandatory caveats and
source/human notices cannot be removed by the model.
Reserve one cent before credentials/transport, retain all reservations, record
usage counts, limit each resident to five model attempts per rolling hour.
SQL failure, cap, rate limit, expiry and provider failure return labelled rules.

## Non-Functional Requirements

ManagedIdentityCredential only; exact HTTPS host, no redirects/retries/tools.
Prompt <=4096 bytes; output <=256 tokens; bounded timeout/reply.
Ledger uses serializable transactions, global row locking and DB UTC time.
Token logs contain counts and coarse outcome only, no resident identifiers.
Only existing resident identity receives OpenAI User on the dedicated account.

## Acceptance Criteria

Tests demonstrate prompt/data boundaries, refusal of arbitrary prompts and model
output, per-resident rate limiting, exact USD20 threshold, concurrency-safe
reservations, retained failures, explicit fallback and cross-resident isolation.
Bicep compiles and defaults off; only account/deployment/account-scoped role.
Record actual Azure resources, quota outcomes, SQL/live smoke limitations and
cleanup. No inferred success when a required cloud prerequisite is absent.

## Phase Checklist

<!-- phase: P01 -->
### P01 - Runtime and durable controls

* [x] P01-T01: Add atomic SQL accounting and provider host wiring.
* [x] P01-T02: Add bounded sentence-selection inference and labelled fallback.

<!-- phase: P02 -->
### P02 - Infrastructure and documentation

* [x] P02-T01: Dedicated default-off Standard account/deployment and identity role.
* [x] P02-T02: Update the existing design and runbooks; provision only reviewed
  dedicated model resources in ama; attempt safe live verification.

<!-- phase: P03 -->
### P03 - Verification and publication

* [ ] P03-T01: Focused units, infra compilation and scoped gate.
* [ ] P03-T02: One independent Review, committed original evidence, exact-head
  publication gate and PR to main if gate permits.

P01/P02 implementation is present; marking implementation complete is not SQL
or live activation acceptance. P03 remains incomplete: isolated SQL and scoped
publication checks cannot currently acquire the shared heavy lock (timeout 0).
Private SQL public access is Disabled; local DNS resolves the public endpoint.
No private migration or new resident image/config rollout was performed.

## Test Ownership and Validation Contract

Core owns sentence catalogue/fallback semantics. API owns provider, SQL adapter,
auth isolation and transport. Infra owns compiled resource policy and SQL text.
Removals: none. Maximum additions: 30 focused tests across existing/new owning
test modules. Generated targets: none committed. Semantic coverage is explicit,
not inferred from snapshots. Existing browser test remains regression coverage
for the unchanged controls; update its changed explanatory notice expectation.
Run focused tests first, then `tools/rpi-checks.py --changed`; receipts external.

## Critique Disposition

Executed once, original verdict Revise; preserved unchanged in the critique.
All nine findings receive direct planner corrections, no owner decision changed:

* PC-001: Add optional context-sensitive explanatory sentences, with mandatory
  progress/closed/next or documents-unknown/form-limits semantic units appended
  in canonical order by the host. Model chooses optional relevant guidance,
  never omits or reorders mandatory facts. Evaluate open/closed/unknown cases.
  This remains explicitly fixed-topic AI assistance, not free-text generation.
* PC-002: Pin nano regional Standard 2025-04-14 and reviewed tariff through
  2026-11-01 UTC. All messages and response schema serialize within 4096 bytes.
  Conservatively bound input by 8192 tokens including message overhead.
  Maximum cost = 8192*0.000121/1000 + 256*0.000484/1000 =
  USD0.001115136, below the permanent USD0.01 reservation. No diagnostic
  inference outside this ledger. The cap covers this application, not other
  subscription callers; no auto-upgrade or alternate model configuration.
* PC-003: Actual SQL procedures are exercised in opt-in isolated local SQL
  integration, including concurrent ceiling/rate, boundary, completion and
  reapply tests. Missing SQL remains a gate/activation blocker. No retry after
  uncertain commit; reserve returns only after durable autocommit completion.
* PC-004: Extend the existing verifier to exactly the two resident_ai object
  EXECUTEs; retain role/ownership/direct-write restrictions. Migration helper
  reuses existing validated Entra SQL token mechanics, no new Azure role.
* PC-005: Factory uses ZF_DEMO_ASSISTANT_* settings, requires msi SQL identity,
  hardcoded deployment and reviewed endpoint. It supplies trusted SHA256 of
  the server-resolved case ID to SQL; no request selector or session-key hash.
  Missing ledger falls back, missing/unsafe activation config refuses startup.
  HTTP reauthorises after both model success and fallback.
* PC-006: Stable SHA256 of canonical case ID, only in private accounting rows;
  never logged or sent to the model. Synthetic mapping, not real-person proof.
* PC-007: Compiled policy tests assert conditions, types, scope, pinned SKU,
  existing identity, local-auth-off and no app/ingress mutation.
* PC-008: Funding ends 2027-01-01 UTC exclusively; tariff/inference ends
  2026-11-01 UTC; resident access retains its existing earlier configured
  expiry and 2026-11-01 authority ceiling. Funding does not extend access.
* PC-009: Separate local, resource provisioning, SQL/MI readiness and
  authenticated live inference outcomes. Blocked cloud rows stay blocked;
  account creation never establishes live functionality.

Implementation amendment: ARM rejects nano Standard (fine-tune SKU only);
ordinary 4o-mini Standard is retired. Current selected deployment is
gpt-4.1-mini 2025-04-14, `resident-mini`, Standard capacity 1, swedencentral.
Revised full bound: 8192*0.000484/1000 + 256*0.001936/1000 =
USD0.004460544 < USD0.01. The earlier nano calculation is historical critique
disposition, not the current runtime tariff.

## Follow-Up Items

Human approval, actual resident identity, privacy and production acceptance are
not established by this synthetic service. Hosted CI and owner merge remain.
RV-001: actual isolated SQL accounting evidence, highest leverage and first
dependency; RV-002: private migration/new image/config and authenticated MI/
resident inference, after gates. Original Review is Complete / Not accepted,
not repeated; both are High evidence gaps routed to later bounded research.

## Handoff

Implementation and original Review completed with explicit acceptance gaps.
P03 remains incomplete pending real SQL/scoped publication gates and eligible
PR publication. Preserve original critique and Review; do not loop into fixes
or another Review inside this completed assessment task.
