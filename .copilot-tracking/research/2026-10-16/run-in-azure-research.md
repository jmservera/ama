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
