<!-- markdownlint-disable-file -->
# RPI Plan: Publish staff initializer #360

## Task Metadata

* Task ID: 360
* Task slug: publish-staff-initializer-360
* Date: 2026-10-17
* Planning status: Ready for bounded offline/evidence work; live image blocked
* Details: .copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/publish-staff-initializer-360-plan-critique.md

## Executive Summary

Normal Docker works, but this host cannot reach either existing private ACR
endpoint. Preserve registry and initializer configuration; complete focused
offline contracts, sanitized preservation readback and factual evidence.
Publication and pin remain blocked, not completed. Do not send authenticated
registry requests through the public route or build against a substitute base.
Delivered local packaging correction removes directory-wide ignore exceptions;
native context audit confirms exactly seven intended files. Final 83 focused
tests, source checks, scoped lint/format and mutation guard pass.

### What You May Not Know

The initializer remains Manual with args ["initialize"]. Changing its image
does not authorize starting it; accidental execution would enter the historic
SQL initializer. The retained API base is not among the inspected local API
images. Docker access alone therefore cannot yield the required image smoke.

### Unresolved Decisions or Blockers

An already existing authorized private-connected publisher must reach login
10.40.4.21 and UK South data 10.40.4.20. Both TCP/TLS probes time out here;
public DNS resolves outside the VNet and returns HTTP403. This is not an IAM
denial. Owner approval is sufficient for publication but not network changes.

## User Decisions and Requirements

* Execute full ordered Research -> Plan -> Implement -> Review on specified
  branch based on latest origin/main; commit actual dated phase artifacts/logs.
* Docker group is now usable; use normal Docker, never privilege escalation.
* Publish proof from infra/cutover-proof.Dockerfile with infra/ context and
  retained immutable API base; unique source-SHA tag and digest required if built.
* Only existing private ACR, job and identity; no services, spend, roles,
  network changes, ACR Tasks/import, pools, temporary VM or unrelated upload.
* Image-only pin requires validated package and exact settings preservation;
  never start the job, initialize SQL, use Graph, read secrets or restart API.
* Update runbook, evidence pack, index and append-only KB log; keep d/e UNMET.
* Privacy-safe conventional commit with Copilot trailer; ordinary topic push,
  main PR Refs #360; stop after final push or concrete blocker, no merge/rebase.

## Goals

Establish the actual publication outcome, preserve all current configuration,
and replace the obsolete Docker-denied blocker with fresh precise evidence.

## Scope and Non-Goals

In scope: offline existing tests, source import/help smoke without private
inputs, exact context allowlist/source hashes, sanitized ARM/DNS/route receipt.
No production code changes expected. No source upload or authenticated registry
attempt while the private-route gate fails. No substitute-base build.
All workload/data/secret/network/IAM actions are excluded.
Implementation discovery permits a directly coupled packaging correction:
remove directory-wide .dockerignore reinclusions and extend the existing
BuildContextTests method with explicit unwanted-file exclusions. No runtime
code, new test methods, Dockerfile or retained base changes.

## Functional Requirements

Record live source/base/proof refs and trigger/container shape. Verify
before/after equality without logging env values or secret/tag contents.
Preserve retained base and nonroot proof recipe. Mark image import/CLI smoke,
push, new digest and pin Not run when connectivity blocks the real image.

## Non-Functional Requirements

No secret/data payloads, debug/token output, full ARM dump or docker auth dump.
No broad cleanup, shared-image deletion, system configuration changes or
package installs unless focused tests demonstrate a missing dependency.

## Acceptance Criteria

* Exact private login/data routes probed with normal TLS and no config writes;
  publication runs only if both reachable on existing approved private DNS.
* Packaging/image/transport/proof tests and source import/help checks execute,
  with exact results/skips recorded separately from real image acceptance.
* If blocked, no registry login/build/push/pin/start; no new digest invented.
* Fresh readback preserves initializer image, identity, template, registry,
  trigger/replica settings, env/secrets references; comparisons may operate in
  memory over values but committed receipts must not contain those values.
* Documentation distinguishes historical Docker denial from resolved Docker
  and current route failure. #360 d/e stay UNMET.
* One critique and one post-implementation Review; persistent evidence and PR.

## Sources

.copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md
(C1-C4, W1-W4), exact issue #360, merged #375/#379 source.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Offline contract and live preservation evidence

Dependencies: complete Research, one final-candidate critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Run focused existing packaging/worker/proof contracts

Before tests, create exact task-owned scratch
.copilot-tracking/tmp/publish-staff-initializer-360, bind TMPDIR to its resolved
absolute path before Python starts, assert tempfile.gettempdir() equality and
remove that exact directory after tests. Run unittest test_container_contract, test_staff_azure, test_private_cutover_proof,
test_initialize_workbench_staff. Run no-network source imports/help only;
inspect complete allowlisted packaging set for unexpected files/symlinks.
If native context semantics need verification, a strictly local scratch-only
Docker COPY audit may run with network disabled and no RUN/ENTRYPOINT, no base
pull, no push and no cloud identity. This is not the proof image or image smoke;
delete only its exact task-owned image/container after listing context paths.
No actual worker main, proof initialize or credential/config input.
Completed: final 83 tests pass, zero failures/errors/skips; five source imports
with network forbidden and two isolated --help checks pass. Native corrected
context contains exactly Dockerfile, five scripts and manifest; no unrelated
scripts, .env, pyc or private profiles. Audit containers never started; exact
named container/image cleaned after both local audits. Not real image smoke.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Capture sanitized before/after receipt and outcome

Record source SHA, exact retained immutable API and old proof refs, Docker
version/user, private endpoints/probe outcomes and public DNS. Fresh recheck
must preserve job configuration and registry restrictions. No real image build,
login, push or pin while route gate fails. No image idempotency claim: only
unchanged configuration/no-write evidence is available.
Completed: actual sanitized live receipt, equal read-visible job fingerprints,
unchanged private registry restrictions and demo deny-all; no image or workload
writes. Actual private-route blocker retained, no published tag/digest.

<!-- rpi:phase id=P02 -->
### [x] P02: Durable factual documentation and implementation handoff

Dependencies: P01 actual results or concrete validation limitation.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update runbook/evidence/index/append log and reconcile

Append fresh evidence without rewriting prior logs; clarify stale top-level
Docker-denial wording and historical permission boundaries. Record changes,
amendment (no live attempt because no approved route), checks and unmet gates.
Reconcile markers/details/state before one independent post-implementation Review.
Completed: docs, index and append log current; seven new relative links resolve,
old log prefix exact and diff clean. All bounded implementation markers complete;
actual image delivery remains blocked. Parent owns one Review and publication.

## Test Ownership and Change Budget

Canonical targets: infra/.dockerignore, existing BuildContextTests method,
existing infra/tests and the six Docker COPY assets.
Generated targets: only sanitized receipt under dated changes. Test scratch is
the exact project-relative directory P01-T01 names; verify resolution and clean
only that task-owned directory. A missing-dependency venv may use session files,
never system Python/package changes.
Exact removals: none. Maximum new tests: zero; no code defect identified.
Semantic checks: native no-network scratch context audit and source/import/help contracts; regression coverage:
existing proof/transport/container/staff tests. Real image smoke is blocked,
never represented by source-only proxies. No documentation build exists.

## Dependencies

Private registry login and data connectivity are hard prerequisites for the
actual retained-base build and all subsequent live publication/pin. Do not
route around this prerequisite. No live-build tasks can be marked completed.

## Critique Disposition

Exactly one independent critique executed; verdict Revise, PC-001 Medium,
planning parent. Accepted operational correction: enforce explicit TMPDIR,
preflight its resolution and exact-path cleanup in P01-T01/details; no second
critique. The critic's assertion that runtime forbids all /tmp/session scratch
is not established by the parent instructions; the actual resolving action is
nevertheless compatible bounded fixture isolation, not a new authority.
Resolving evidence: P01-T01 and details; eventual receipt records actual scratch
assertion and cleanup. Zero test additions/removals or production changes.

During Plan handoff, an early test-discovery readiness probe failed before test
execution: missing zava_forward package. This is not a completed Implement test
or image smoke. Restore only missing dependencies in a task-owned venv during
Implement, then run the planned configured runner.

## Implementation Amendment

Native network-disabled scratch/COPY audit proved !scripts/ and !entra/
reinclude entire directories, including unrelated scripts and generated pyc.
This contradicts the intended file allowlist. P01-T01 now removes only those
two directory exceptions, adds exclusions to the existing test method, and
repeats the native context audit plus focused runner. This is immediately
relevant packaging correction within the caller's surgical source allowance,
not a new architecture/owner decision. No secret contents inspected and no
cloud source upload. Exactly one critique remains historical.

## Follow-Up Items

* Existing authorized private publisher must supply working private path,
  build/push new source-SHA image and immutable digest, then validate image-only
  Manual job pin. External route repair is outside current authorization.
* Genuine tenant/browser/roles/SQL/AI verification and later separately
  authorized retirement remain with human operators, #360 d/e UNMET.

## Handoff

Implementation record:
.copilot-tracking/changes/2026-10-17/publish-staff-initializer-360-changes.md.
Bounded implementation complete and ready for one Review; image delivery blocked.
Parent proceeds through one Review and final privacy-safe publication, then stops
under caller's explicit boundary without selecting child work.
