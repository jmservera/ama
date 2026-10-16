---
title: Source change monitoring implementation evidence
description: Full-plan changes and validation evidence for issue 213
ms.date: 2026-10-16
---

## Starting state

Full plan P01-P03 authorized by the user's implementation request. Executable
write boundary is src/; READMEs, knowledge index/append-only log and requested
RPI artifacts are supporting changes. First boundary P01-T01. No blockers.
Initial installed-package probe failed; installed local core, orchestrator,
agents and API editable packages using /tmp/zf164/bin/python -m pip --no-deps.
No dependency versions changed.

## Planning reconciliation

One critique executed. Accepted PC-001/002/003/004/005/007 as detailed in
phase details. Rejected PC-006 because its temporary-directory prohibition
is unsupported and conflicts with the user's explicit /tmp/zf164 instruction.
This is an immediately relevant safety refinement preserving the offline
scope, not a new user decision. No second critique.

## Validation intent

Local fixture-driven unittest suites for core/orchestrator/API, then project
ruff/mypy. No network scraping, paid calls, private dataset reads, deployment,
new endpoints or claimed legal approval.

## P01 and P02 implementation

Added core/source_monitor.py with four append-only tables, local observations,
content/metadata/retrieval-failure classification, capped visible diffs,
content-addressed candidate snapshots and exact source/card impact binding.
Candidates do not enter reg_version/provision/index. Existing review records
include candidate/config identity and configured journeys/communications.
Configuration validates cadence and High/Medium/Low with retained rationale.

Added the bounded orchestrator local-JSON job, per-source due checks,
pagination, nonzero retrieval-failure outcome and no activation capability.
No new endpoints or role-inventory entries.

Owner approval freezes exact source/configuration/card histories, test cases,
ENGINE_VERSION and clock. Regression runs after approval and only the latest
passing result can authorize activation. Runtime-equivalent citation checking
is shared with RuleEngine, not duplicated or weakened. Replacement activation
cannot supersede holds; explicit no-change review/regression can release the
captured hold. Atomic rollback restores captured active cards or holds without
overriding later decisions. Existing activate/release cannot bypass monitoring.
Ordinary future/expired activation now fails without retiring the prior card;
updated the existing engine regression to assert this intended correction.

26 new core tests and four new orchestrator tests (30 total, within the maximum
30), plus the existing engine regression. Fixtures are outside packages,
wholly constructed and visibly simulated. Concurrent independent SQLite
adapters, restart, source/config/card/test freshness, multi-card injected
failure and SQL Server DDL/ledger contracts are covered.

## P03-T01 validation and documentation

Observed local results:

* Core full suite: 462 run, 1 opt-in skip; ruff, format and mypy (89 files)
  passed. Existing sensor tests emit ResourceWarnings; not changed.
* Orchestrator full suite: 21 run; ruff, format and mypy (10 files) passed.
* API law-store tests: 34 run, 16 SQL Server opt-in skips; rule tests:
  5 run, passed. No network scraping or live SQL/Azure test was attempted.
* Missing local packages installed editable using pip --no-deps in /tmp/zf164.
  Narrow typed adapters call migrated untyped core interfaces; orchestrator
  mypy locates sibling source/test modules and retains migrated fixture skips.

Updated core/orchestrator/source READMEs and knowledge routing; appended the
knowledge log. The six-criterion README audit explicitly separates bounded
local outcomes from unmet official retrieval, hosted scheduling, exhaustive
impact, source promotion, actual legal approval and communication delivery.
No protected/private files or immutable regulatory snapshots were read/edited.

## Current handoff

P01/P02 and P03-T01 complete. Final post-documentation rerun and one Review
precede the authorized commit/push/PR portion of P03-T02.

## Final readiness preflight

New card IDs referencing a previously changed source now join the guard and
refresh the candidate identity/impact snapshot. Overlapping changed sources
fail closed, rather than allowing one source approval to stand for another.
Coordinated multi-source release is an explicit residual limitation, not an
invented operational capability. The new boundary test brings additions to
the allowed maximum 30. This is a conservative current-state clarification
within the requested bounded offline slice; no user approval was inferred.

Post-documentation core monitoring rerun: 26 passed; project ruff/format and
mypy (89 files) passed. Orchestrator pagination now exercises a second
configured source and next_after boundary; all 21 tests and project
ruff/format/mypy (10 files) passed. State JSON, README local file links and
git diff whitespace checks passed.

## P03-T02 Review and publication handoff

One post-implementation Review executed, outcome Residual work. No material
defect is established inside the bounded slice; RV-001 coordinated multi-source
release, RV-002 verified new-source publication/actual human approval and
RV-003 live monitoring/operational regression/communications remain distinct
follow-ups. No issue closure or operational conformance claim.

Final complete core rerun after all executable changes: 463 tests run,
1 opt-in skip, passed. Orchestrator 21 tests passed; core/orchestrator
Ruff/format/mypy and targeted API law/rule regressions passed as recorded.
Authenticated GitHub account rechecked: id 8036360, login jmservera,
matching the requested privacy-safe commit identity. Commit/push/PR is the
remaining authorized publication action.
