---
title: In-VNet staff initialization research
description: Offline evidence and implementation readiness for Refs #360
ms.date: 2026-10-16
---

## Brief and controls

Implement the requested SQL-only Azure job continuation; directory writes remain
under the operator's authorized login. Focused, internal convergence research.
No Azure commands, image builds, private datasets, network changes or issue edits.
The user explicitly requests research, plan, implementation, review and a PR.
No interactive intake is available; the supplied scope is sufficient.

## Cycle 1

### Wider

* C1: `infra/scripts/setup-entra.py:596` and `:898` run candidate lookup and
  check/apply locally, capture output, and currently stop on private SQL failure.
* C2: `infra/scripts/initialize-workbench-staff.py:154` preserves SQL positions,
  immutable bindings and historical actors; `:199` provides atomic installation.
* C3: `infra/README.md:277` describes the existing manual initializer job,
  SQL-admin identity and private environment. These are deployed proof assets,
  not Bicep-managed initializer resources.

### Deeper

* C4: `infra/cutover-proof.Dockerfile:1` inherits the source API image.
  `src/api/Dockerfile:35` installs core, agents and API wheels plus the hashed
  runtime dependencies. The proof image lacks the staff initializer and helpers.
* C5: `src/api/requirements.txt` already pins cryptography, azure-identity and
  mssql-python. A narrow COPY extension suffices; no Azure CLI in the image.
* C6: `infra/scripts/setup-entra.py:126` already sends sensitive ARM bodies using
  private temporary files with CLI logging disabled and deletes those files.
* C7: `infra/scripts/setup-entra.py:1078` resolves/validates people and
  `:1114` reconciles app roles locally. Roster generation is independently
  implemented and need not change.

### Contrarian

* Private blob transfer still requires laptop data-plane connectivity, so it
  cannot solve the stated problem without another transport.
* Plain candidate/roster results in job logs violate the codes-free requirement.
  Use a random per-execution AES-GCM key in a job secret; only authenticated
  ciphertext enters logs. The operator captures and decrypts it in memory.
* Granting the SQL-admin identity ARM rights just to restart the API is
  unnecessary privilege. The job verifies SQL; the authorized operator performs
  the existing management-plane replica restart after job success. Treat the
  complete orchestration as the staff step was the initial proposal; the
  independent critique rejected that split against the literal requirement.
  Implementation instead authors an API-only custom restart role for the
  existing identity, without operator credentials.
* Read-only SQL checks require a transient job/secret control-plane write.
  `--dry-run` must not create jobs; `--check`/`--list-staff` may explicitly use
  transient jobs without SQL writes. Explain that distinction.

## Dispositions and readiness

Selected: clone only the validated existing `job-<prefix>-init` image, registry
configuration, SQL-admin identity and API environment into a uniquely named
manual job in ama. Transfer input and result-encryption key as one secret via
private ARM body file; delete the job (including its secrets) in finally.
Never forward Graph credentials or entire existing job environments.

Shared SQL preparation/installation remains canonical; the worker receives
operator-resolved people and has no Graph client. The worker uses its own MI
to restart/verify serving replicas after verified SQL completion. Missing image/assets,
permissions, failure or timeout fail closed with a private-host fallback.

Research disposition: executed. Planning Readiness: Ready.
Extensions: repository instructions and ADR 0006 selected; RPI skills selected.
No specialist or research delegation needed for this continuous local trace.
No external evidence used; no legal or operational acceptance inferred.
Another cycle is not needed: all material implementation surfaces are identified.
Live image availability, Azure authorization, log delivery, private SQL and
browser/human acceptance remain unverified and must be reported as unmet.

## Interface evidence added during critique disposition

W1: Azure CLI extension public source, retrieved 2026-10-16:
https://github.com/Azure/azure-cli-extensions/blob/main/src/containerapp/azext_containerapp/_params.py
and custom.py, stream_job_logs/list_replica_containerappsjob. Explicit
execution/replica/container, JSON-line Log fields, tail limit 300. The client
gets a job auth token via ARM, then streams from the environment log endpoint.
This is not ARM-only access. The CLI request has no internal HTTP deadline,
so the parent enforces a subprocess deadline. Replica disappearance is
documented; worker holds the encrypted result for 60 seconds before exiting.
Actual endpoint reachability remains Not run. Failed retrieval fails closed.

## Correction cycle 1 intake (2026-10-17)

Status: In progress. Existing task identity and artifact paths are retained.
Explicit caller direction requests all four phases in order, then publication
on `feat/run-in-azure-360` and stop; no continuing automatic session.
Research posture: focused, bounded CI dependency correction. Evidence root is
the existing `.copilot-tracking/research/2026-10-16/` directory.
Source baseline: `296037b239d20179de4048f0bc9f837b4704bb86`.
Worktree was clean; branch matches open PR #370 targeting main.

Questions: which workflows execute the full infra tests; which declared
dependency supplies real AES-GCM; do the prior image-context and timeout
corrections survive; which deployment blockers remain?

Prior-knowledge gate: prior research, plan, details, changes, critique, state
and Review read. Prior 304-test offline evidence predates the failing clean
CI and must not be treated as current acceptance. RV-001/RV-002/RV-003 remain
unmet. User-supplied run 38983585607 is the primary failure evidence.
Repository instructions and RPI phase skills selected; no UI/security-audit
skill or delegated lane applies to this tightly coupled trace.

Caller exclusions: no Azure writes, deployments, images, roles, secrets,
Graph work, private data or primary-checkout environment reads; no uv, test
skips, crypto mocks, weakened guards, merge or force-push. Resource group ama
must never be deleted; services remain private and no spending is authorized.

### Correction cycle 1: Wider wave

* C8: `.github/workflows/mvp-validation.yml:30,44-45` installs source with
  `--no-deps` and only PyYAML before full infra discovery.
* C9: `.github/workflows/src-ci.yml:175,192-193` installs source transitively,
  then only explicitly declares PyYAML before the same discovery.
* W2: https://github.com/jmservera/ama/actions/runs/38983585607,
  retrieved 2026-10-17 with `gh run view 38983585607 --log-failed`: 14 failures,
  four errors; real AESGCM import fails before job lifecycle/cleanup assertions.

Reflection: both executing workflows need the same explicit dependency
installation; transitive availability in src CI is not a reliable declaration.

### Correction cycle 1: Deeper wave

* C10: `src/api/requirements.txt` pins and hashes cryptography 50.0.2 and its
  dependencies; `infra/scripts/staff_azure.py:33,50` uses actual AES-GCM.
* C11: `infra/tests/test_pipeline.py:106-147` already validates prerequisite
  ordering and mutates PyYAML removal/unpinning/late installation in both
  workflows. Extend this existing contract, not a separate test framework.
* C12: `infra/.dockerignore:5-10` retains all staff COPY sources including
  `entra/app-registration.json`; `infra/tests/test_staff_azure.py:636` checks
  every proof Dockerfile source against context rules.
* C13: `infra/tests/test_staff_azure.py:300` advances a fake execution clock
  after polling and asserts multiple polls plus deletion with a decoded result
  but Running status. Preserve this non-vacuous timeout regression.

Reflection: install the existing hashed runtime requirements before discovery
in each workflow; retain PyYAML and add removal/unhashed/late-install mutations.
Validate on Python 3.12 in a new /tmp pip venv with no system site packages.

### Correction cycle 1: Contrarian wave and synthesis

Rejected: relying on src CI's incidental transitive crypto, duplicating an
independent cryptography version pin, skipping tests, mocking AES-GCM, or
weakening lifecycle guards. The existing operator/runtime lock is the single
declared source and already matches the dependency error's remedy (C8-C11).
The context test's local rule evaluator is offline evidence, not an image
build: independently remove the parent/file allowance pair for each staff COPY
source in memory and require test failure. Mutate execution-timeout handling in memory and require the new
decoded-result test to fail, without editing runtime source (C12-C13).
No further research cycle is needed for this bounded correction.

Research disposition: executed, Complete. Planning Readiness: Ready.
Live blockers RV-001 through RV-003 are unchanged; passing offline tests cannot
prove image publication, role activation, private logs/SQL/restart/browser,
real tenant authority, cross-host serialization or hard-kill recovery.

Implementation evidence refinement: removing only `!scripts/staff_roster.py`
survived the existing context test's coarse prefix matcher because `!scripts/`
still matches its prefixes. The final negative controls therefore remove both
parent and file allowances for each of five staff sources, including the
manifest. These prove omitted-source detection, not complete Docker ignore
semantic equivalence. Existing corrected rules/tests remain unchanged; no
image build or live image availability is implied.
