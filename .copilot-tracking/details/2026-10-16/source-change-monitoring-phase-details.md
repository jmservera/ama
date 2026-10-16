---
title: Source change monitoring phase details
description: Completion evidence and implementation boundaries for issue 213
ms.date: 2026-10-16
---

## P01

P01-T01: reuse LawStore.sql/blobs and RuleCardStore.transaction. Store
candidate bytes outside reg_version/provision/index so current law retrieval
is unchanged. Compare content hash and canonical metadata, record retrieval
failures and explicit unknown impact. Configuration is append-only and
explicitly maps requirements, journeys, tests and communications; no cadence
or authority is guessed from register prose.

P01-T02: orchestrator accepts explicit local config/observation JSON files,
with a bounded source page, due checks and nonzero failure outcome. It may
retrieve/compare/flag but has no approval or activation command. Tests use
temporary source fixtures and no network or private data.

## P02

P02-T01: owner principal is Juan Manuel Servera with rule_owner capability;
this is a trusted local callable, not authenticated HTTP identity. Every card
still needs separate author/owner approval. The human source assessment
records interpretation, provenance/completeness evidence, notification and
rollback decisions. Regression cases are an immutable approved plan, not
executable expressions or shell commands. Existing evaluate handles the two
bounded rule kinds. Required test IDs and cards must be covered. Activation
rechecks candidate baseline, latest test outcome, date, owner and prior
active/held state under one transaction. Existing activate cannot bypass
the release gate. Rollback is owner-only with retained history.

P02-T02: new tests own detection, metadata-only/retrieval failure,
idempotence, per-source cadence, approval refusal, full-card/test coverage,
regression failures, effective boundaries, rollback, retention, direct
activation denial, concurrency/staleness and SQL dialect contract coverage.
Existing rule-card/engine/API suites cover preserved behaviour. No removals
or generated fixtures. Maximum 30 new test methods; semantic assertions
must test actual observed state, not just command success.

### Accepted critique refinements

All new evidence is exercise-only, with simulated labels on approval,
regression, activation and rollback. Match canonical source IDs exactly,
including provision IDs, rather than substring LIKE alone. Preserve
candidate/config IDs and exact matched card versions/states in impact records.
Candidate content remains outside the current law-store index.

Bind approval to candidate ID, baseline version/hash, configuration revision,
current per-card version/event heads, immutable fixture plan/digest,
ENGINE_VERSION and evaluation clock. New material observations, source
versions, config revisions or card lifecycle changes invalidate the release.
Harmless duplicate observations do not. Activation checks the latest run
for that approval; failed reruns cannot reuse an earlier pass. Card release
from held and alternate-version activation cannot bypass monitoring.

Use RuleEngine._citations eligibility in addition to evaluate; unavailable,
partial, stale or unreviewed citations block activation. Positive fixtures
use visibly synthetic reviewed sources, not promoted monitor candidates.
Capture exact prior active heads under the activation transaction. Rollback
compares all activation heads, rejects intervening holds/retirements and
expired/ineligible prior versions, and restores no card when none was active.
Test atomic rollback failures and separate-connection stale evidence. SQL
Server uses the existing transaction-scoped exclusive sp_getapplock boundary
(`zavaforward_write`) supplied by the SQL adapter, not an inferred isolation
level.

Safety preflight refinement: new card IDs citing an already changed source
join the activation guard and change candidate identity on a refreshed
observation. If a target cites multiple changed sources, refuse activation
until a future coordinated multi-source release exists; one approval never
stands for another source. No-change dispositions can regress/release an
exact captured hold, with rollback restoring that hold. This conservative
offline limitation is explicit in the acceptance audit.

## P03

P03-T01: use /tmp/zf164/bin/python with absolute PYTHONPATH per project,
then project ruff and mypy. Install editable local projects with pip only
because the initial import probe reports packages missing. No uv. Add a
narrow disallow_untyped_calls exemption only for migrated store calls.
Review links/diff and append log; no regulatory snapshot edits.

P03-T02: preserve research/plan/critique/changes/review/state artifacts.
Review once after implementation; route any genuinely remaining work
honestly. Confirm gh api user id/login before configuring the requested
privacy-safe repository email. Commit with supplied Copilot trailer and
Refs #213, push without force and open a main-based PR. Never merge.
