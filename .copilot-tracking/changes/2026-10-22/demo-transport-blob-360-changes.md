<!-- markdownlint-disable-file -->
# Changes: demo-transport-blob-360

Refs #360, PR #423, branch docs/demo-transport-plan-360. Owner decisions DN1 to DN5 (2026-10-22).

## Related Files

* Plan: .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/demo-transport-blob-360-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-22/demo-transport-blob-360-plan-critique.md
* Research: .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md

## Implementation Summary

### P01 Controller, worker and codec

* Added infra/scripts/staff_blob.py: AEAD paged codec, strict account URL, no-overwrite writes, preflight, fail-closed read, shared StaffJobError (PC-004, PC-005, PC-009).
* Rewrote infra/scripts/staff_azure.py: removed tag/chunk transport and ZF_STAFF_RELAY; discovery verifies the storage account via ARM (private, keyless, no anonymous access, container public access None); execute runs preflight before any job, reads only after Succeeded, checks image drift (PC-003, PC-008).
* infra/scripts/staff-azure-worker.py writes pages with ManagedIdentityCredential; no detail logged.

### P02 Infrastructure and tests

* infra/modules/storage.bicep: staff-results container appended last, lifecycle rule deleting blobs and versions after one day (PC-007).
* infra/staff-initializer-rbac.bicep and infra/role-assignments.json: tag role replaced by a container-scoped write-only data role, includeResultBlob default false (PC-006).
* Added staff_blob.py to Dockerfile, .dockerignore, tools/rpi-checks.py and CI lint lists (PC-002).
* Tests rewritten with a fake container: round trip and paging, tamper, swap, gap, extra, stray, expiry, future, binding, preflight, failed job skips read, image drift, storage properties, URL grammar, worker overwrite refusal, retired-token grep, storage contract (PC-010).

### P03 Documentation

* infra/README.md: superseded note, new Private Blob Result Transport section with DN1 to DN5, live prerequisites and NOT RUN list; stale runbook paragraph updated.
* docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md updated (append-only).
* DN4: no code change; existing role-assignment behaviour is unchanged (PC-011).

## Validation

* infra tests: 378 tests OK (cd infra/tests with PYTHONPATH=../../src/core/tests:../../src/agents/tests).
* ruff check and format on the four Python files, mypy on scripts: clean.
* bicep build of main, storage and RBAC templates: OK.
* Full tools/rpi-checks.py gate: see PR body for receipt (run after commit).

## Not Run

Live private routing, deployment, role grants, real job, Entra/browser, signed attestation, screen-reader acceptance, real size measurement.

## Divergences

* Worker role is a custom write-only data role instead of Storage Blob Data Contributor (narrower; matches the least-privilege intent).
