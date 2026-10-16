---
title: Issue 212 implementation plan
description: Approved deterministic checks and scoped alerts
ms.date: 2026-10-16
---

Task: 212 / issue-212. Status: implementation-ready candidate.

## Executive Summary

Add immutable executable contracts to newly proposed exercise cards, a bounded
SQL-fact engine, durable per-check alerts/checkpoints and scoped HTTP reads and
owner dispositions. Existing prose-only seeds stay drafts and never acquire
approval. Local proof is not operational legal or Azure acceptance.

## User Decisions and Requirements

* Implement #212 acceptance criteria, architecture 3/4 of ADR 0005 and ADR 0006.
* Code only in src; READMEs, RPI artifacts and append-only knowledge log are
  explicitly requested documentation exceptions.
* Use approved cards only; no inferred approval, clocks, awareness or legal
  interpretation. Future/consulted sources never become active controls.
* pip only; /tmp/zf164 tools; absolute per-project PYTHONPATH. No private
  dataset, env, editor configuration or GitHub-issues tracking reads/writes.
* Push a normal topic branch and open a Refs #212 PR, never close or merge.

## Goals

Make missing evidence and service failure visible while preserving independent
human safety work and deterministic reproducible checks.

## Scope and Non-Goals

Two bounded executable kinds: hazard awareness and significant automated
decision safeguard. No arbitrary expressions, AI-controlled rules, resident
sending, invented statutory durations, operational activation or new UI.

## Functional Requirements

Five cited result states; strict source gating; immutable contract/version
binding; code-owned UTC clocks; three evaluation triggers; SQL persistence;
per-home grouping, deadline/harm sorting; attention publication rate limiting;
owner acknowledgement and outcome; false-positive history.

## Non-Functional Requirements

Atomic checkpoint/check/alert writes, replay idempotency, explicit unavailability,
portable SQL adapters, bounded batches, server-side role and identity checks.

## Acceptance Criteria

Audit each of the nine issue criteria separately with tests and remaining
limits. SQL Server/live Azure and real human approval/trial remain unmet.

## Phase Checklist

<!-- P01 -->
### P01 Core and integration

* [x] P01-T01 Add optional immutable execution specification to new card versions.
* [x] P01-T02 Implement typed bounded SQL engine and durable alert dispositions.
* [x] P01-T03 Add role-scoped API, post-change/transition checks and schedule CLI.

<!-- P02 -->
### P02 Evidence and delivery

* [x] P02-T01 Add core/API tests; update endpoint inventory and READMEs/log.
* [x] P02-T02 Run project tests, ruff and mypy; audit criteria for one Review.
* [ ] P02-T03 Commit, push and publish Refs #212 PR.

## Validation Ownership

Core tests own predicates, source/approval boundaries, all five outputs,
clock boundaries, persistence/replay, rate limits and rollback. API tests own
identity/role denial, owner-only disposition, engine-outage safety paths and
trigger integration. Existing endpoint inventory remains canonical. Removals:
none. Maximum additions: two test modules, one engine module. No generated
targets. Run focused suites first, then core/API regression and lint/types.

## Critique Disposition

Executed once: issue-212-critique.md, verdict Revise. Final readiness: Ready
after the following direct dispositions; no second critique.

* PC-001 rejected: its claimed temporary-directory prohibition is not a
  parent instruction and conflicts with the explicit /tmp/zf164 user direction.
* PC-002 applied: bounded contracts below specify inputs and exact comparisons.
* PC-003 applied: stable data/transition keys use case rowversion and card/source
  fingerprint, never wall time; schedule uses a UTC minute bucket. Check,
  publication and checkpoint commit together. Schedule revisits SQL homes after
  a crash; it does not claim to reconstruct intermediate states never evaluated.
* PC-004 applied: explicit supported audience roles plus exact named owner,
  existing staff case access, default deny unknown/provider roles. Owner actions
  require trusted capability AND exact owner identity. No authority from body.
* PC-005 applied: separate unavailable response/log, not a fake persisted check.
* PC-006 applied: stable risk episodes retain acknowledgement/outcome and open
  breaches; false positives are owner classifications, never suppression.
  Denominator is classified alerts, numerator false-positive classifications,
  with unclassified and total counts returned. Attention publication window is
  24 elapsed hours per home/card/step/evidence item; checks remain retained.
* PC-007 applied: no new replace/ignore/autoincrement/pragma; adapter-specific
  DDL, parameterized DML and explicit keys. Live SQL Server remains untested.
* PC-008 applied: matrix below binds all nine issue criteria to local tests.

| Issue criterion | Work and test ownership | Limitation |
| --- | --- | --- |
| Five cited results | P01-T02; core test_rule_engine | Two supported predicates only |
| Missing is unknown | P01-T02; core missing/invalid tests | No invented facts |
| Future/consulted never active | P01-T02; core source/date tests | No legal currentness claim |
| No model clocks/suppression | P01-T01/T02; core contract tests | No model dependency |
| Safe action/owner/clock; breach acknowledgement/outcome | P01-T02/T03; core/API disposition tests | Fictional approvals only |
| No resident messages | P01; core/API side-effect assertions | No messaging interface |
| Group/rank/rate-limit/false positives | P01-T02; core hygiene tests | No staff precision trial |
| Safety with engine down | P01-T03; API outage tests | Local engineering evidence |
| Idempotent/checkpointed | P01-T02/T03; core retry/rollback/restart tests | Intermediate missed revisions not reconstructed |

## Follow-Up Items

Real Legal/Compliance/DPO approval, staff comprehension/precision trial,
SQL Server/Azure verification and accessible step UI remain separate gates.

Review boundary: P01 and P02-T01/T02 source/documentation candidate. P02-T03
is the authorized post-review publication step, not unimplemented product work.
The core README contains the nine-row acceptance audit: criterion 7 is
explicitly partial end-to-end where home identity is unresolved; local
engineering evidence does not satisfy live approval or trial gates.
