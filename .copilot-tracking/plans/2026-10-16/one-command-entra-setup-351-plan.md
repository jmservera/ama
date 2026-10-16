---
title: One-command Entra setup plan
description: Issue 351 implementation contract
ms.date: 2026-10-16
---

Task ID: 351. Slug: one-command-entra-setup-351. Status: Implement complete.

Owner continuation (2026-10-16): merge origin/main first, resolve RV-001 through
RV-003 with mutation-proven tests, reproduce all infra CI with installed source
distributions, preserve pending PR #352 Custom forwarded-header compatibility,
update evidence and existing PR #356, push without force and mark ready.
Historical critique and independent Review remain unchanged; this is the
explicitly selected later implementation of routed findings, not a review loop.

## Executive Summary

Implement `python3 infra/scripts/setup-entra.py` as a standard-library tool.
Discover the actual ama API and origin-linked edge, converge additive directory
objects and roles, preserve auth controls, and explain/poll human prerequisites.
Never interpret a managed identity sentinel as an app registration.

## User Decisions and Requirements

* Expanded owner request for issue 351 is authoritative; coordinate read-only with 344.
* Default ama; isolated device-code profile; no identifiers, emails or secrets in logs.
* Build only infra/src, preserve SQL/network policy, no private datasets.
* Produce RPI evidence, offline tests, docs, commit/push and PR; use Refs references.
* Synthetic development only; no inferred legal or operational approval.

## Goals

Reliable one-line setup with explicit drift/check outcomes and safe reruns.

## Scope and Non-Goals

Infra script, API/edge role tags, tests and directly related documentation.
No SQL migration, staff creation, B2B invitations, network changes, automatic
directory-wide consent or Azure deployment in this task.

## Functional Requirements

* Discover API by role tag, legacy workload tag, then API name; fail ambiguity.
* Discover Front Door profiles/endpoints/routes/origins linked to the selected API,
  including associated custom domains; never select an unrelated environment.
* Honor UUID auth client first; otherwise uniquely find registration by exact name
  or app tag; create missing registration/SP and additive manifest roles.
* Preserve prior redirects, unrelated roles, credentials, auth paths and token store.
* Parse a private roster with explicit role and userId/groupId; deduplicate and
  validate all rows before writes. Existing code/userId-only roster reports action.
* Assign missing app roles only; verify, never silently swallow forbidden/partial reads.
* Browser credentials optional: reuse existing reference, otherwise request explicit
  `--create-secret` with Key Vault or Container App storage. No rotation on rerun.
* Use fixed Graph/ARM hosts, redact failures and validate resource scope.
* Human admin consent portal instructions and bounded polling, no broad grants.
* --check/--dry-run perform no remote writes or login; return drift distinctly.

## Non-Functional Requirements

Python >=3.10, standard library, az extension preflight, friendly installation
commands and isolated profile 0700. Use bounded propagation retry for reads,
never blindly retry object-creating POSTs. Full tenant/SP failures are explicit.
Secret body transfer uses a 0600 temporary file under isolated profile, removed
on completion, no secret in argv or output. Disable CLI file logs/telemetry.

## Acceptance Criteria

Offline mocked tests prove tags/ambiguity, edge association, sentinel handling,
tools, reruns, dry run, roster and redaction. Additional negative tests cover
permission denial, malformed continuations, preservation and profile isolation.
Live tenant authority, browser sign-in, admin consent and private SQL staff
binding remain unexecuted and must not be ticked as accepted.

## Phase Checklist

<!-- P01 -->
### P01: Setup implementation
* [x] P01-T01: Implement CLI, discovery, directory convergence, private roster and auth wiring. Routed safeguards now implemented and mutation-proven locally.
* [x] P01-T02: Add minimal Bicep role tags and old CLI compatibility routing.
<!-- P02 -->
### P02: Evidence and delivery
* [x] P02-T01: Add infra/tests/test_setup_entra.py; preserve old callback helper tests. Full 177-test infra suite and three safeguard mutation checks pass.
* [x] P02-T02: Update infra README, knowledge index/log and run targeted validation.
* [x] P02-T03: Execute one independent review; record audit and publish draft PR #356. Historical review retained; owner-selected later implementation resolves its source findings.
* [x] P02-T04: Reproduce and repair full infra CI, mutation-prove routed findings,
  publish updated acceptance audit and mark existing PR ready. All eight hosted
  checks pass at source commit 90da083; PR #356 marked ready.

## Test Ownership and Change Bounds

Canonical targets: infra/scripts/setup-entra.py, existing initializer CLI,
containerapps/edge modules, infra README and knowledge index/log.
Generated targets: none. Exact removals: none. Maximum new production files:
one script; maximum new test files: one. RPI artifacts are explicitly requested.
Tests owned by infra unittest; semantic scenarios plus legacy regression tests,
ruff and mypy on new code; Bicep existing tests for changed module tags.
Local CLI --help and mocked full-run are the applicable local app run.
P02-T04 also covers the parameter-aware inventory assertion and exact workflow
formatting; compiled policy checks continue to verify default/forwarding/use.

## Critique Disposition

One independent critique executed, verdict Revise. All eight corrections applied
directly; no divergent owner decision and no second critique.
* PC-001: bind management subscription/tenant and Graph tenant; preflight token
  permissions and directory reads. Reads do not establish directory authority.
* PC-002: credential create/store/activate order; app-bound stable secret name;
  existing named credential without matching storage blocks regeneration with
  exact portal recovery instructions. Failed storage never changes auth client.
* PC-003: explicit typed principals, enabled member users/security groups,
  matching enabled SP role propagation, direct/group effective conflict checks.
* PC-004: exclusive local run lock, no POST retry, explicit unknown-write outcome
  with rerun discovery; concurrent cross-host runs unsupported/documented.
* PC-005: only enabled routes linked to origin, eligible custom domains;
  allowlist identity/HTTPS/proxy fields, preserve action/exclusions/token store,
  no implicit bearer-to-browser conversion.
* PC-006: capture successful and failed CLI output; allowlist device-code prompt,
  fixed mode-0700 profile outside repo, no inherited debug or CLI file logging;
  tests cover invalid output, launch failure, timeouts and cleanup.
* PC-007: default private roster path; missing roster is incomplete exit 2.
  Read-only modes do not log in, create profile or take lock. Missing auth,
  discovery or permissions is blocked exit 1; dry-run drift exit 2.
* PC-008: review blockers prevent ready delivery; draft PR if material findings
  remain. Current task does not perform a second review or silently claim closure.

## Follow-Up Items

Live authorized tenant execution, human consent, SQL binding/restart and real
browser sign-in after 344 are separate operator acceptance gates.
The historical independent Review remains Complete / Not accepted at its
assessed boundary. The owner explicitly selected its later implementation:
RV-001, RV-002 and RV-003 are now resolved with targeted and mutation evidence.
No second critique/Review is required or performed. Live tenant/consent/SQL/
browser acceptance remains unmet, separately from source readiness.

## Handoff

Research: .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md.
Details: .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md.
Changes destination: .copilot-tracking/changes/2026-10-16/one-command-entra-setup-351-changes.md.
