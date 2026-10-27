<!-- markdownlint-disable-file -->
---
title: API minimum replicas phase details
description: Bounded implementation and validation expectations
ms.date: 2026-10-27
---

# RPI Phase Details: API minimum replicas

## Metadata

* Task ID: aca-api-min-replicas-2026-10-27
* Task slug: aca-api-min-replicas
* Plan: .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md
* Evidence: .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md C1-C9

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Parameterize and document | Complete | P01-T01, P01-T02 |
| P02 | Validate and reconcile | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Parameterize and document

Context: main is the sole shared module caller. Production profile governs
security, not a requirement for minimum 2. Intent: cost-safe defaults plus opt-in.
Boundaries: shared API minimum only; standalone resident template stays unchanged.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add and forward bounded minimum

Targets: infra/modules/containerapps.bicep, infra/main.bicep,
infra/main.bicepparam, infra/main.test.bicepparam,
infra/main.pilot.example.bicepparam.
Add `apiMinReplicas int = 0`, description, min 0/max 4 decorators in module and
parent. Forward in apps.params and use in API scale. Examples explicitly set 0.
Dependency: critique disposition. Completion: compiled schema/forwarding tests,
no resource/property changes outside API minimum and parameter schemas.
Unresolved: none for implementation.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile documentation and regression contracts

Targets: infra/README.md, infra/tests/test_bicep_policy.py,
infra/tests/test_resident_demo_deploy.py. Evidence C6-C7 identifies stale assertions.
Describe default 0, valid range, cold starts and private production `param
apiMinReplicas = 2`; retain production security controls. Correct stale fixed-two
resident separation wording while retaining its jobs/isolation warning.
Replace the old policy assertion with parameter expression and evaluate default/
production input through compiled parent forwarding. Check both parameter schemas,
example compiled values, unchanged HTTP/max/agent scale. Resident separation
test must still enforce no resident wiring into main/wrapper. Dependency: T01
schema intent. Completion: source assertions and compiled tests cover behavior
without changing standalone resident scale.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile

Context: component commands operate offline and compile nested templates.
Boundary: no Azure deployment/what-if and no full gate. No generated ARM in git.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run infra checks and record changes

Run REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -q;
az bicep build/lint across infra/*.bicep and infra/modules/*.bicep. Existing
fake CLI wrapper tests supply offline what-if coverage. Build parameter examples
via existing CLI for semantic tests. Run existing Ruff on changed policy tests.
Install with pip only following a missing dependency failure; use external
disposable environment, editable src distributions as documented if needed.
Use a task-owned directory under the session files area for TMPDIR and any
conditional venv, outside tracked source. Parent execution has no prohibition
on this storage; the critique's worker-local restriction is not applicable.
Record exact commands, results, unexpected skips, amendments and divergences in
changes. Update markers/details after success before one independent Review.
Completion: scoped commands succeed and evidence reconciled. Publication remains
blocked; no full receipt, live observation or deployed state is inferred.

## Completion Evidence

P01-T01/P01-T02: bounded main/module input and explicit 0 in all three
parameter examples; compiled tests exercise 0/1/2/4, parent forwarding, HTTP
and agent invariants, plus unchanged standalone resident 0..1 scale.
P02-T01: 447 offline infra tests passed with no skips after installing missing
documented dependencies using pip in the task-owned external venv. All 24
Bicep templates built and linted; both changed Python test files passed
Ruff lint/format. Complete command history/results are in the changes record.
