# Demo direct ingress plan

Task ID: issue-360. Slug: demo-direct-ingress. Date: 2026-10-16.
Status: Ready, single critique corrections incorporated.

## Executive Summary

Add a demo-only external environment with separately named workloads/subnet,
retain private backing services and existing identities, branch Entra setup
before edge discovery, and provide secret-free acceptance probes and a gated
migration runbook. No Azure changes or live acceptance are authorized.

## User Decisions and Requirements

* Implement only offline a, b, f and a written plan for c of issue 360.
* Do not deploy, change Azure, delete resources, touch MVP/prototype or private data.
* Preserve production/default behavior and the optional Front Door path.
* Reuse dependencies and identities; new environment/apps/jobs have distinct names.
* Produce RPI evidence, commit, push and open a PR using Refs references.
* Owner approval, tenant authority and live testing remain independent gates.

## Goals

Make direct demo HTTPS a reviewable opt-in without opening private services.

## Scope and Non-Goals

Infra templates/scripts/tests and directly related docs only. No web UX edits,
live deployment, identity provisioning, cost commitment, or resource retirement.

## Functional Requirements

* Separate external demo environment/subnet/NSG; private dependencies unchanged.
* Reject demo plus edge, production, public backing access or unsafe demo auth.
* Direct Entra mode selected explicitly or by demo tag; callbacks use app FQDN.
* Existing registration/role/roster/secret lifecycle remains shared and idempotent.
* Strict direct probes include public content, API denial, browser login and roles.

## Non-Functional Requirements

No credentials or identity IDs in output/evidence. Reuse existing helpers and
test patterns. Default compiled resource names and controls remain unchanged.

## Acceptance Criteria

a/b/f need offline tests and updated documentation. c remains proposed, pending
owner review/approval. d/e are Not run and out of scope. No issue-body edits.

## Sources

See .copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md,
issue 360 and owner task constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Offline infrastructure

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Demo infrastructure and compiled guard regressions

<!-- rpi:phase id=P02 -->
### [x] P02: Offline Entra and probes (independent of P01)

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Direct Entra discovery and strict probe regressions

<!-- rpi:phase id=P03 -->
### [x] P03: Documentation (parent owned)

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Migration, history and architecture reconciliation

<!-- rpi:phase id=P04 -->
### [x] P04: Validation and delivery

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Offline checks, one review, commit/push/PR

## Validation Ownership and Boundaries

Infrastructure lane owns infra/tests/test_bicep_policy.py and related compiled
tests; auth lane owns setup tests and proof-runner tests. No test removals.
At most one new direct-mode test module per lane if existing files cannot fit.
Canonical sources are infra Bicep/Python; compiled JSON is temporary, not committed.
Run az bicep build (local compiler only), relevant unit suites, Ruff and mypy;
run local API on a generated temporary fixture when installed packages permit.
Semantic tests exercise compiled modes and actual fake CLI/HTTP interactions,
not merely source string matches. No network to deployed services.

## Dependencies

Main merged before setup edits; PR 359 remains open, device prompt is not owned
by this task. Review migration with the owner before any live action.

## Critique Disposition

One critique executed, verdict Revise, all compatible corrections applied.

| Finding | Disposition | Resolving requirement |
| --- | --- | --- |
| PC-001 | Applied | Stage all queue/scheduled consumers inactive; drain and activate one generation only, reverse on rollback |
| PC-002 | Applied | Explicit public probe mode, retained private defaults, exact status/redirect matrix and adversarial tests |
| PC-003 | Applied | Direct NoProxy reconciliation with explicit browser-mode opt-in and preserved default bearer behavior |

## Follow-Up Items

Owner/coordinator: approve migration and cost; tenant/browser/SQL/AI proof;
then authorize selective retirement. Browser JSON API 302 gap remains explicit.

## Handoff

## Owner-directed continuation: one resilient command

The 2026-10-16 follow-up extends this existing task, without repeating its
completed research, critique or historical Review. Reuse the active branch/PR.
Implement only offline; do not call Azure or directory services.

<!-- rpi:phase id=P05 -->
### [ ] P05: Resilient authentication onboarding

<!-- rpi:task id=P05-T01 -->
#### [x] P05-T01: Discover credential dependencies, onboard private roster, coordinate and orchestrate SQL

Default setup creates missing credentials, discovers vault/attached identity,
permits app-local fallback only for direct demo, records storage selection,
rechecks Entra and checks/applies SQL with one confirmation and replica restart.
Missing roster creates a private placeholder template and stops before cloud
writes. Read-only modes report every step. Deployment/revision/advisory locks
block concurrent mutations. No usable in-VNet staff/roster transport exists in
the proof initializer; provide an exact authorized-host command instead.

<!-- rpi:task id=P05-T02 -->
#### [ ] P05-T02: Protect app-local credentials and prove the offline contract

Bicep/store guard, mocked Azure/SQL regressions, scoped lint/type checks,
runbook/evidence/KB log and acceptance audit. Preserve unmet live/human gates.
Commit/push existing branch and update PR 362 using Refs #360 only.

P05 source/test/documentation implementation is complete. Final candidate:
260 infra tests passed without skips (local Bicep compiler included), four-script
scoped mypy and focused Ruff passed, no introduced Ruff baseline diagnostics,
32 responsive loopback API auth tests passed, local Markdown targets and diff
hygiene passed. Bounded continuation acceptance audit is appended to the
existing review artifact; historical Review/critique verdicts are unchanged.
Absolute simultaneous-start exclusion is not established by advisory tags,
and raw unguarded deployments remain outside the supported wrapper boundary.
Live/human c/d/e gates remain unmet. Delivery is the remaining P05-T02 step.

Details: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-16/demo-direct-ingress-changes.md.
P01-P04 completed. One Review executed, Complete / Not accepted for its assessed
candidate. RV-001/RV-002 were routed to distinct subsequent implementation,
corrected and tested; no second Review or rewritten verdict. Current main,
including merged device-code/missing-tool changes, integrated without rewriting
history. Final infra suite 238 passed. Pushed feat/demo-direct-ingress and opened
https://github.com/jmservera/ama/pull/362. Owner PR/migration approval and c/d/e
remain outstanding; no issue checkboxes changed.
