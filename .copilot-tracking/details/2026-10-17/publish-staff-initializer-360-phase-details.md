<!-- markdownlint-disable-file -->
# RPI Phase Details: Publish staff initializer #360

## Metadata

* Task ID: 360
* Task slug: publish-staff-initializer-360
* Date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md
* Research: .copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Offline contracts and live preservation | Complete; live image blocked | P01-T01, P01-T02 |
| P02 | Factual evidence/handoff | Complete; Review handoff ready | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Offline contract and live preservation evidence

Context: Docker 29.9.0 now works, but actual existing private ACR endpoints time
out. Context/retained base/nonroot/worker copies remain exact merged source.
No private route means no authenticated login, base pull, build, push or pin.
Intent: bounded useful validation and a precise non-success receipt.
Targets: existing infra tests/scripts; dated changes receipt.
No secrets, dataset, worker main, proof initialization or live setup command.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Focused tests, source imports/help and package allowlist

Set TMPDIR to the resolved exact project-relative directory
.copilot-tracking/tmp/publish-staff-initializer-360 before the Python runner
starts. Assert tempfile.gettempdir() equals that path. Remove only this exact
task-owned scratch directory after all validation (including failures);
record preflight and cleanup. Use one runner with four relevant existing unittest modules, then no-input
imports of proof/worker/roster/transport/initializer, and proof/initializer
--help. Help/import must be checked from source with environment cleaned of
application variables and no network; never worker main. Check exact Docker
COPY set and explicit dockerignore allowlist, regular files only, no symlinks,
no extra included configuration/data files. A local FROM scratch / COPY-only
native Docker context audit, network disabled with no RUN/ENTRYPOINT or execution,
may verify actual ignore semantics; it is not a substitute proof image. Remove
only the exact task-owned audit container/image after path listing.
Record immutable API base reference
but do not claim image import/help success without building the real image.
Dependencies: critique disposition. Completion: actual pass/fail/skips and
source-only caveat in changes. No new test methods. Native audit found
directory reinclusions transmit unrelated scripts/pyc into local context;
remove only !scripts/ and !entra/ from infra/.dockerignore and extend existing
context test exclusions, then rerun focused tests and native audit. Dockerfile,
base, runtime code and all cloud restrictions unchanged.
Completion: 83 focused tests pass after correction, no skips; five source
imports and two isolated help calls pass. Corrected native context lists seven
regular files exactly (Dockerfile + five scripts + manifest). Task-owned audit
container/image removed after each run, no container started.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Sanitized preservation readback and concrete route blocker

Use az job show metadata only (never listSecrets); compare complete read-visible
job identity/configuration/template in memory if necessary, emitting only equality
and sanitized names/refs. Do not persist raw reads or environment values.
Capture registry private restrictions unchanged and exact source/base/image
digests. Preserve manual args ["initialize"], one container proof, identity
id-cutover-test-init, MI registry pull, retry=1, timeout=600, parallelism=1,
completion=1, no declared secrets/volumes. No job start. No image update may be
sent because there is no new validated digest. Record image-pin idempotency
Not run, not success. Before/after comparison covers this no-write task window,
not a claim of historic equivalence beyond available evidence.
Dependencies: existing research live endpoints; P01-T01 independent.
Completion: precise sanitized dated receipt and explicit unperformed operations.
Completed: receipt stores equal before/after fingerprints and reference/shape
metadata only, unchanged registry restrictions and API deny-all. No settings/
secret values, image-pin idempotency or workload execution claim.

<!-- rpi:phase id=P02 -->
## P02: Durable factual documentation and implementation handoff

<!-- rpi:task id=P02-T01 -->
### P02-T01: Reconcile evidence, documentation and handoff

Update infra/README.md and docs/architecture/cutover-evidence-pack.md; add
current index route and append only to docs/reference/log.md. Keep historical
observations dated, distinguish resolved Docker/IAM from remaining private
route and human acceptance. No new acceptance or permission inferred.
Update plan/details/changes/state and ordered phase log. One independent full
post-implementation Review follows; it must not trigger another implementation
or review loop in this task. Parent owns privacy-safe commit/push/main PR and
verified remote head, then explicit stop. No separate legacy phase-log files:
canonical changes/review logs satisfy caller's phase-log requirement.
Dependencies: P01 results/limitations. Completion: reviewed diff and truthful
handoff; image publication blocked, #360 d/e UNMET.
Completed: all four documentation targets updated; seven new local links pass,
append-only prefix exact, scoped Ruff/format and diff pass. Current changes
record reconciled; parent owns one Review and terminal publication.
