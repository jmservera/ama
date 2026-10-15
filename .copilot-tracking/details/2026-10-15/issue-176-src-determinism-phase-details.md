---
title: Issue 176 src determinism phase details
description: Test ownership, compatibility constraints and completion evidence
ms.date: 2026-10-15
---

## P01: Generator contract and regression coverage

### P01-T01

Modify only existing core/synthetic writers plus one typed helper. Fingerprint
scale, its shared helper and STAGE_ORDER's source; sensor also fingerprints
scale and shared dependencies. Use explicit stable names and source bytes,
not absolute paths. Preserve historical defaults and existing manifest keys.
Version bump records new metadata/refresh contract. Sensor date means exclusive
end of a fixed-days window. Low-level existing function calls keep START as
default; write() computes and passes the requested start. Omitted as_of
preserves START even when days/cadence are customized; explicit as_of is an
exclusive UTC end. Scale as_of is metadata, not an event cutoff.

Typed boundaries: annotate scale.write, sensor.write and each revision_sources
helper with concrete path/int/date inputs and dict[str, object] or tuple[Path,
...] returns; new tests call those boundaries and typed shared helpers only.
No new ignores or type exemptions. Dependency inventory uses logical basenames:
scale_fixture.py, provenance.py, synthetic/__init__.py (logical __init__.py),
insights.py; sensor additionally includes sensor_backfill.py. This tracks
generator source, not the standard library or every core transitive import.
Hash sorted names plus length-delimited bytes. Test each dependency mutation
using mocked source reads and path/order independence.

Resolve full representable UTC start/end before any directory creation,
including date underflow/overflow and excessive timedelta ranges. Require
YYYY-MM-DD syntax. Propagate start into estimate, outdoor and readings;
estimate-only CLI uses the same days/as-of/cadence validation and window.

Reject non-positive homes/days/cadence, cadence not dividing 1440, non-positive
events-per-home and invalid dates before creating outputs. Refuse nonempty
destinations so old shards cannot leak into loader globbing. Existing empty
TemporaryDirectory calls must continue working. No force overwrite flag.
Do not change source physics, sensor IDs, SQL loader or approval/consent code.
Protection is not a concurrent transaction or rollback for disk failure.

### P01-T02

One new core test file owns typed helper semantics, writer provenance/hash
checks, full-directory byte equality and parameter/overwrite regressions.
Use small outputs and patch shard size to exercise multiple shards cheaply.
Demonstrate seed and as-of sensitivity, preserved default start, file set
equality, dependency-fingerprint sensitivity, and old-output preservation.
Retain all existing tests without removals. Pre-change payload hashes captured with 12 homes/3 events or 3 sensor days
before editing are the historical compatibility oracle; manifests intentionally
change. Hash every non-manifest file, including estimate and CSV headers.
Check every shard's timestamps within the half-open window and cadence.
Do not count equality alone as
semantic coverage: assert bounds, dates, metadata, hashes and explicit errors.

## P02: Documentation and local validation

### P02-T01

Correct stale "no sensor generator" claim in existing synthesis. Describe
bounded sensor evidence separately from absent private register. Add exact
CLI recipe, proposed policy status, named owner approval boundary and new-path
refresh behavior. Update core README, reference index and append-only log.
Do not rewrite generated/published data or owner memory.

### P02-T02

Use per-project READMEs and existing src-ci commands. Test core, agents, api,
orchestrator, importer, including required test fixture PYTHONPATH. Use pip
only if dependency failure requires it. Run existing ruff and mypy per project.
Local API uses wholly fictional synthetic fixture under a unique ZF_DATA
temporary path, ZF_AI=on, normal draft/human gates; report missing real model
honestly. Probe Docker without privilege escalation. Never read private
working data or secrets. Record commands, exit outcomes, counts and blockers
in the changes artifact, summarize the same in PR.

## P03: Review and delivery

### P03-T01

Invoke rpi-review exactly once after implementation. Assess plan, source diff,
tests, doc consistency, private-data and dependency boundaries. Residual findings are future work, never fake AC closure or repeated Review.
Any in-scope blocking finding prevents a ready-for-delivery/accepted claim;
record it as a blocker for a distinct later invocation rather than silently
deferring it as accepted scope. Private-source and owner-approval limitations
are already declared residuals, not engineering defect acceptance.

### P03-T02

Resolve GitHub identity, local privacy-safe author/committer email, conventional
commit with required Copilot trailer. Stage explicit paths including all new
RPI artifacts. Push only feat/src-synthetic-determinism-176 and open main PR
using Refs #176. Do not merge or amend. Record local evidence/CI boundary.

## Implementation reconciliation

P01 and P02 completed. One helper and one test file added; no removals or new
exemptions. Related scale-fixture registry version updated in agents/evals
to avoid stale metadata after v1.2.0. This is metadata, not a dependency change.
Seven new contract tests and existing five sensor tests pass; historical hashes
are unchanged. All five component suites and strict gates pass. Smoke app uses
980 generated fictional cases, ZF_AI=on, explicit ZF_DATA and SQLite; template
fallback is labelled unapproved, no actual model configured. Docker access
denied. Changes artifact records failures, recovery and exact commands.
P03 Review completed Complete/Residual work, implementation commit 774137a
pushed and PR #309 opened to main. All eleven implementation-commit CI checks
passed, including image and mssql. Evidence-only handoff commit follows.
Issue-wide ACs stay unticked; no operational acceptance or merge.
