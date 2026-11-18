---
title: "Task Research: infra-144-container-load"
description: "Primary evidence artifact for Issue #144 container hosting completeness: versioned worker/job images, deployed container hardening, declared-scale load test, and single-replica restart audit persistence"
ms.date: 2026-11-15
---

| Field | Value |
| --- | --- |
| Date | 2026-11-15 |
| Researcher / agent | `rpi-research` (via `RPI Agent`, automatic mode) |
| Status | Complete |
| Artifact path | `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` |

## Research Brief

* What to research: Current repository state and gaps across Issue #144's four unticked acceptance criteria: (1) real, versioned worker and job images deployed through the pipeline; (2) container hardening (non-root, read-only root filesystem, dropped capabilities, no-new-privileges) enforced in the deployed app/runtime spec, not only in CI; (3) declared-scale (60,000-home) fixture load test execution and durable recording without claiming production scale; and (4) single-replica and restart behaviour verified with audit persistence.
* Why it matters: Issue #144 has scale rules, probes, resource limits, revision rollback, and tokenomics driver fields ticked, while the four criteria above remain unticked and need concrete deployed-spec enforcement where missing, verified test coverage in `infra/tests/test_container_hosting_144.py`, and accurate evidence documentation without overclaiming live Azure or production acceptance.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases for branch `feat/infra-144-container-load`.
* Scope: `infra/` (`modules/containerapps.bicep`, `main.bicep`, `main*.bicepparam`, `resident-demo.bicep`, `live-*.bicep`, `scripts/pipeline.py`, `scripts/deploy.py`, `README.md`, `tests/`), `.github/workflows/src-deploy.yml`, `.github/workflows/src-ci.yml`, `src/*/Dockerfile`, `src/check-container.py`, `src/api/tests/scale_load.py`, and restart/audit persistence tests in `src/api/tests/` and `src/agents/tests/`.
* Non-goals: Live Azure subscription mutation, claiming production scale or live Azure SLA acceptance, editing workflow permissions/pinned actions that would alter security controls unnecessarily, or pushing to remote.
* Criteria: Every codebase claim carries a stable `C#` ID with workspace-relative `path:line`; contrarian wave explicitly checks whether Bicep / Azure Container Apps ARM schemas and runtime startup actually enforce non-root, read-only root filesystem, and dropped capabilities in deployed specs vs CI-only `docker run` flags.
* Requested outputs: Converged design and verification plan inputs for `rpi-plan`.
* Output mode: `convergence`

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q5 covering worker/job image pipeline wiring, deployed app container hardening, 60,000-home scale fixture load run & recording, single-replica restart + audit persistence, and `test_container_hosting_144.py` + docs contract |
| Codebase scope | `infra/`, `src/`, `.github/workflows/`, `docs/` |
| External scope | None required unless Azure Container Apps Bicep schema details cannot be verified locally via `az bicep build` |
| Initial internal candidate areas | `infra/modules/containerapps.bicep`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `infra/README.md`, `src/api/tests/scale_load.py`, `src/check-container.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_container_contract.py` |
| Initial external candidate areas | none |
| Research posture | `focused` |
| Posture provenance | caller-specified (bounded internal issue #144 criteria, named target module `infra/tests/test_container_hosting_144.py`, Focused validation tier) |
| Explicit limits / deadline | Focused validation tier; commit locally and do not push |
| Posture-specific completion basis | `focused` scope and materiality: all four unticked AC surfaces, Bicep compilation/schema behavior, load test execution, restart persistence, and existing test contracts verified |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Never read private datasets; preserve existing workflow/check names; do not claim production scale or unexecuted live Azure acceptance |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; `rpi-research` contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence paths | Enforces KB conventions, validation tiers, honest evidence claims, ASCII Markdown style | Selected: mandatory repository governance |
| Skill | `rpi-research` | Explicit RPI phase skill | Three-wave read-only research artifact | Selected: active phase |
| Research specialist | `hve-core-all:rpi-researcher` | Host-registered research worker | Delegated independent lane artifact | Skipped: tightly coupled internal `infra/` + `src/` trace fits direct inline inspection in <=5 parallel read batches |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive execution with explicit user instructions specifying all 4 unticked criteria, target test module, validation commands, and commit-without-push boundary | No interaction needed / unavailable | Proceed with `focused` posture in `convergence` output mode |
| Direction change | None at intake | N/A | N/A |
| Convergence | Cycle 1 completed across Wider, Deeper, and Contrarian waves; evidence supports a single non-breaking convergence design | No user prompt required in confirmed automatic mode | Converged on deployed Bicep `EmptyDir` + `ZF_CONTAINER_HARDENING=enforced` spec paired with `zava_forward.core.container_hardening` runtime enforcement, `pipeline.py` `rank-publish` maintenance check, fresh 60,000-home scale/restart recording, and `infra/tests/test_container_hosting_144.py`; `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: Verify what already exists vs what is missing or CI-only across the four unticked Issue #144 acceptance criteria, and converge on exact code, Bicep/runtime, test, and evidence-documentation changes.
* Assumptions:
  * Earlier Issue #144 slices may have already implemented parts of worker/job images, scale load harness, or restart tests, or left gaps between CI (`src/check-container.py`) and the deployed app/Bicep spec. Must verify directly in code.
* Success criteria:
  * Every research question Q1-Q5 answered with `path:line` `C#` evidence.
  * Contrarian wave tests whether ACA Bicep / container runtime actually enforces hardening in deployed apps vs CI-only flags, and whether `az bicep build` accepts any proposed Bicep properties.

## Task Research Requests

* Explicit requests: Inspect `infra/` container app/job definitions, hardening properties, scale fixture load test, and single-replica restart + audit persistence tests; prepare to add `infra/tests/test_container_hosting_144.py` and evidence documentation.
* Inferred research questions: How images are built/tagged/digested and passed to Bicep in `pipeline.py`/`deploy.py`/`src-deploy.yml`; how ACA hardening is represented in Bicep and/or container image/runtime; how `scale_load.py` runs against the 60,000-home fixture and records results; how single-replica and restart audit persistence is implemented and verified across `api` and `agents`.
* Caller constraints and non-goals: Do not claim production scale; do not push; keep Focused validation tier clean.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| narrow | Focused validation tier; target module `infra/tests/test_container_hosting_144.py` + evidence docs + any required `infra/`/`src/` hardening/hosting gap fixes | User prompt / Intake | Constrain scope to Issue #144's 4 unticked criteria without unrelated refactors |
| exclude | Do not claim production scale; do not push commits | User prompt / Intake | Enforce non-production framing on load test recording and local-only git commit |

## Research Questions

| # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How are API, worker (`agents`), and job (`orchestrator`, `ledgerVerify`, `importJob`, plus any auxiliary jobs/apps) images built, versioned (SHA/digest), and deployed through `src-deploy.yml`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, and Bicep? Are any placeholder images remaining? | depth | H | answered |
| Q2 | How is container hardening (non-root user/group, read-only root filesystem, dropped capabilities, privilege escalation) currently enforced in CI vs in deployed Container Apps/Jobs Bicep specs and application runtime? What does ACA Bicep/runtime support or require so hardening is enforced in the deployed app, not only in CI? | depth | H | answered |
| Q3 | How does `src/api/tests/scale_load.py` (and any companion load script/record) generate and exercise the declared 60,000-home / 600,000-event scale fixture, what metrics/tokenomics drivers does it record, and has a 60,000-home run actually been executed and recorded (vs smaller smoke parameters)? | depth | H | answered |
| Q4 | How are single-replica mode (`minReplicas`/`maxReplicas`, `activeRevisionsMode: Single`) and restart behaviour with audit persistence implemented and tested across the API store, SQL/file persistence, and worker/queue runtime? | depth | H | answered |
| Q5 | What prior Issue #144 tracking artifacts and existing tests (`test_container_hosting_completeness.py`, `test_container_contract.py`, `test_pipeline.py`, `test_deploy.py`) exist, and what exact gap must `infra/tests/test_container_hosting_144.py` + evidence docs close? | breadth | H | answered |

## Executed Research Cycles

### Cycle 1

#### Wave 1 — Wider (Inline)

* Investigated all infrastructure templates (`infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/modules/guard.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`), Dockerfiles (`src/*/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`, `infra/*.Dockerfile`), release workflows and scripts (`.github/workflows/src-deploy.yml`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `src/check-container.py`), load/restart harnesses (`src/api/tests/scale_load.py`, `src/api/tests/test_scale_fixture_load_and_restart.py`, `src/api/tests/test_restart_audit.py`), and existing tests (`infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_container_contract.py`, `infra/tests/test_bicep_policy.py`).
* Wave 1 reflection: Identified that earlier slices delivered scale/probe/rollback rules (`C1`, `C9`), worker `serve` + `SIGTERM` drain (`C11`, `C12`), and initial load/restart harnesses (`C16`, `C17`), while leaving specific gaps in `pipeline.py` maintenance-job validation (`C4`) and deployed-app container hardening (`C8`, `C10`).

#### Wave 2 — Deeper (Inline)

* Examined every container entrypoint (`zava_forward.api.server:main`, `zava_forward.agents.worker:main`, `zava_forward.agents.runtime:build_runtime`, `zava_forward.orchestrator.__main__`, `token_store:main`, `digest_blob:main`, `ranking_publish:main`, `source_monitor:main`, `document_rescan:main`, `zava_forward.importer.__main__:main`, `resident_demo`, `live_receiver`, `live_simulator`).
* Verified how `pipeline.py` tags `sha-<40hex>-r<run_id>-a<attempt>`, resolves `@sha256:<64hex>` repo digests, checks pull-only admission, and forwards `apiImage`, `agentImage`, `orchestratorImage`, and `importImage` into `main.bicep` -> `modules/containerapps.bicep` (`C2`, `C3`, `C4`). Found that `pipeline.py` PR-plan maintenance image consistency check covers `auth-renewal` and `ledger-verify` but omits the seventh workload container `job-forward-{env}-rank-publish` (`C4`).
* Verified `scale_load.py` and `test_scale_fixture_load_and_restart.py` against `docs/architecture/scale-load-2026-11-01.json` and `docs/architecture/scale-restart-2026-11-13.json`: `make_cases(60000, seed=11)` produces 60,000 synthetic homes and 53,821 events in SQLite `SqlStore`, explicitly records `meets_declared_workload: false` because the 1,800 s open-loop 600,000-event run is not executed, and verifies `SIGKILL` hard restart + `/api/audit-check` SHA-256 hash-chain continuity (`C16`, `C17`, `C18`).
* Wave 2 reflection: Narrowed the crucial design tension to Criterion 2 — how to enforce non-root, read-only filesystem, and dropped capabilities in the deployed app rather than only in CI `docker run` checks.

#### Wave 3 — Contrarian (Inline)

* Tested `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` against `az bicep build` (`Bicep CLI v0.48.1`):
  * Adding `securityContext` (`runAsNonRoot`, `readOnlyRootFilesystem`) fails Bicep type validation with `Warning BCP037: The property "securityContext" is not allowed on objects of type "Container". Permissible properties include "args", "command", "env", "probes", "resources", "volumeMounts"` (`C14`).
  * Adding `volumes: [{ name: 'tmp', storageType: 'EmptyDir' }, { name: 'state', storageType: 'EmptyDir' }]` and matching `volumeMounts` compiles cleanly (`rc=0`) on both `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` (`C15`).
* Investigated Git history (`commit 3698de8d96f55c64b3dca974b37ca7a005162c71`) and `infra/tests/test_container_contract.py`:
  * Previously, a `container-entrypoint.py` wrapper that unconditionally asserted `os.statvfs('/').f_flag & os.ST_RDONLY` and `CapBnd == 0` broke Azure Container Apps startup because ACA's hypervisor guest does not set `ST_RDONLY` on `/` and keeps the standard non-root bounding set `CapBnd`, which is why `test_container_contract.py` explicitly forbids `ENTRYPOINT` and `src/container-entrypoint.py` (`C10`).
  * Contrarian challenge also caught `test_bicep_policy.py:1015-1060` (`C13`), which explicitly requires `main.bicep`'s `orchestratorImage` empty-string fallback to `mcr.microsoft.com/k8se/quickstart:latest` for `deploy.py` dependency-only/bootstrap workflows — meaning versioned `@sha256:` enforcement belongs in `pipeline.py` (including `rank-publish`) rather than mutating `main.bicep` parameter defaults.
* Wave 3 reflection: Solved the ACA vs Docker runtime hardening tension cleanly without violating `test_container_contract.py` or ACA startup:
  1. In Linux OCI containers started as `USER 10001:10001` (`uid=10001, gid=10001`) with no file capabilities, `execve(2)` zeroes `CapEff`, `CapPrm`, `CapInh`, and `CapAmb` (`0000000000000000`), and `prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` works unprivileged inside the process to enforce `NoNewPrivs: 1` in ACA just like `--security-opt=no-new-privileges` in Docker.
  2. In `src/*/Dockerfile`, `/` and `/app` are owned by `0:0` (`0755`/`0644`), so `UID 10001:10001` receives `EACCES` (in ACA) or `EROFS` (in Docker `--read-only`) on any write attempt to `/` or `/app`, while Bicep `EmptyDir` `volumeMounts` explicitly isolate `/tmp` and `/state` as the sole writable ephemeral directories.
  3. Implementing `zava_forward.core.container_hardening` and setting `ZF_CONTAINER_HARDENING: 'enforced'` + `EmptyDir` mounts in the deployed Bicep app/job specs enforces non-root (`10001:10001`), dropped capabilities + `NoNewPrivs=1`, bytecode write suppression (`PYTHONDONTWRITEBYTECODE=1`), read-only `/` and `/app` write rejection (`EROFS`/`EACCES`), and bounded `/tmp` + `/state` scratch mounts inside the deployed application at startup and `/healthz` without adding a Docker `ENTRYPOINT`.

## Evidence Log

| ID | Source (`path:line`) | State | Summary |
| --- | --- | --- | --- |
| C1 | `infra/modules/containerapps.bicep:250-715` | Verified fact | Declares 2 Container Apps (`api`, `agents`) and 5 Container Apps Jobs (`orchestrator`, `tokenRenewal`, `ledgerVerify`, `rankingPublish`, `importJob`) with `activeRevisionsMode: 'Single'`, explicit CPU/memory limits, startup/readiness/liveness probes on `api`, queue scale on `agents`, and parameterised images (`apiImage`, `agentImage`, `orchestratorImage`, `importImage`). Currently lacks `EmptyDir` scratch `volumes`/`volumeMounts` and `ZF_CONTAINER_HARDENING` env wiring. |
| C2 | `.github/workflows/src-deploy.yml:65-195` | Verified fact | Builds all 4 `PROJECTS` (`api`, `agents`, `orchestrator`, `importer`) from `src/{project}/Dockerfile` with context `src/`, runs `python src/check-container.py`, gates fixable HIGH/CRITICAL vulnerabilities via Trivy, exports SPDX SBOMs, publishes versioned ACR tags, and deploys immutable `@sha256:` digests via `infra/scripts/pipeline.py`. |
| C3 | `infra/scripts/pipeline.py:21-215` | Verified fact | `PROJECTS = ("api", "agents", "orchestrator", "importer")` maps to `apiImage`, `agentImage`, `orchestratorImage`, `importImage`; `release_tag()` formats `sha-<40hex>-r<run_id>-a<attempt>`; `publish()` captures the exact `@sha256:<64hex>` digest; `release_images()` validates SHA/tag/digest and verifies `docker pull` under AcrPull-only identity. |
| C4 | `infra/scripts/pipeline.py:345-378` | Verified fact | `deployment()` enforces existing `@sha256:` images across `ca-forward-{env}-api`, `ca-forward-{env}-agents`, `job-forward-{env}-orchestrator`, and `job-forward-{env}-import` during PR `what-if`, and checks `auth-renewal` and `ledger-verify` maintenance jobs for matching `orchestratorImage`, omitting `job-forward-{env}-rank-publish`. |
| C5 | `src/api/Dockerfile:18-35` | Verified fact | Digest-pinned `python@sha256:34386ef0...`, root-owned `/app` and site-packages, `10001:10001`-owned `/state`, `USER 10001:10001`, `PYTHONDONTWRITEBYTECODE=1`, `CMD ["python", "-m", "zava_forward.api"]`, no `ENTRYPOINT`. |
| C6 | `src/agents/Dockerfile:15-26` | Verified fact | Digest-pinned `python@sha256:34386ef0...`, installs `core` + `agents` only (no SQL or Azure SDK packages), `USER 10001:10001`, `PYTHONDONTWRITEBYTECODE=1`, `CMD ["python", "-m", "zava_forward.agents"]`. |
| C7 | `src/orchestrator/Dockerfile:16-30` | Verified fact | Digest-pinned `python@sha256:34386ef0...`, `USER 10001:10001`, `PYTHONDONTWRITEBYTECODE=1`, `CMD ["python", "-m", "zava_forward.orchestrator"]`; `src/importer/Dockerfile:14-28` follows the identical hardened contract. |
| C8 | `infra/README.md:1298-1365` | Verified fact | Documents prior Issue #144 status: marks worker/job images and deployed container hardening as `Partial` because `Microsoft.App/containerApps@2025-07-01` lacks `securityContext` and `pipeline.py`/deployed runtime had not yet enforced runtime container hardening in deployed specs. |
| C9 | `infra/tests/test_container_hosting_completeness.py:1-225` | Verified fact | Existing 11-test contract suite verifying scale bounds, HTTP probes, CPU/memory limits, `activeRevisionsMode: 'Single'`, job retry/timeout limits, and `scale_load.py` driver keys. |
| C10 | `infra/tests/test_container_contract.py:72-115` | Verified fact | Enforces `USER 10001:10001`, `CMD ["python", "-m", "zava_forward...."]`, absence of `ENTRYPOINT` and `src/container-entrypoint.py`, `agents` `serve` command without `ZF_AGENT_RESULT_ROUTE` in `containerapps.bicep`, and absence of HTTP/TCP probes on `agents`. |
| C11 | `src/agents/src/zava_forward/agents/worker.py:70-137` | Verified fact | Standalone worker `main()` supports `serve`, `health`, and version output; stays in healthy standby when `ZF_AGENT_RESULT_ROUTE != "enabled"`, fails closed (`NOT_CONFIGURED=2`) if enabled with incomplete settings, and drains in-flight work on `SIGTERM`/`SIGINT` (`DRAIN_SECONDS=20.0`) before releasing unposted tasks for redelivery. |
| C12 | `src/agents/tests/test_worker.py:312-375` | Verified fact | `ReplicaRestartTests` proves single-worker crash before post redelivers and processes once, and crash between post and ack redelivers and reposts with identical `(task_id, fence)` for receiver idempotency. |
| C13 | `infra/tests/test_bicep_policy.py:424-480` | Verified fact | Verifies all 7 workload container images and maintenance job commands in `modules/containerapps.bicep`, `apiMinReplicas` (0..4), and at lines `1015-1060` enforces `main.bicep` `orchestratorImage` empty-string fallback for `deploy.py`. |
| C14 | `infra/bicepconfig.json:1-26` | Verified fact | Core Bicep analyzer rules are errors; `az bicep build` on `Microsoft.App/containerApps@2025-07-01` emits `BCP037` rejecting `securityContext` on `Container` (`Permissible properties include "args", "command", "env", "probes", "resources", "volumeMounts"`). |
| C15 | `infra/live-receiver-job.bicep:85-92` | Verified fact | Demonstrates `volumes` and `volumeMounts` in ACA Jobs (`mountOptions: 'ro'` on `device-certs`), and `az bicep build` verified `storageType: 'EmptyDir'` compiles cleanly on both `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01`. |
| C16 | `src/api/tests/scale_load.py:29-310` | Verified fact | Defines `DECLARED = {"homes": 60000, "events": 600000, "sessions": 20, "requests_per_second": 5.0, "duration_seconds": 1800, "inference_per_home": False}` and `API_LIMITS = {"vcpu": 0.5, "memory_gib": 1.0, "max_replicas": 4}`; runs synthetic SQLite `SqlStore` load and records latency percentiles, RSS, CPU, SQL statement counts, and `meets_declared_workload: False` with explicit non-production-scale scope text. |
| C17 | `src/api/tests/test_scale_fixture_load_and_restart.py:180-360` | Verified fact | Launches a separate API OS process over SQLite `SqlStore`, runs concurrent closed-loop HTTP load, performs acknowledged audit-writing mutations, kills the server abruptly with `SIGKILL`, restarts a single replacement process on the same DB file, and verifies `/api/audit-check` SHA-256 chain integrity before and after a post-restart write. |
| C18 | `docs/architecture/scale-restart-2026-11-13.json:1-92` | Verified fact | Recorded 60,000-home (53,821-event) separate-process load and `SIGKILL` restart evidence (`entries_before_kill: 3`, `entries_after_restart: 3`, `entries_after_new_write: 4`, `chain_intact_after_new_write: true`, `meets_declared_workload: false`); paired with `docs/architecture/scale-load-2026-11-01.json`. |
| C19 | `infra/modules/guard.bicep:118-135` | Verified fact | Enforces `publicSimulationRequiresSingleReplica` (`apiMinReplicas <= 1`) and `containerapps.bicep` sets `maxReplicas: enablePublicSimulationLane ? 1 : 4`; `resident-demo.bicep:161` sets `minReplicas: 0, maxReplicas: 1` with `activeRevisionsMode: 'Single'`. |

## Synthesis and Findings

### Q1 — Worker and job images real, versioned, and deployed through the pipeline

* **Accepted finding**: All four application images (`api`, `agents`, `orchestrator`, `importer`) are real multi-stage non-root wheels built from `src/*/Dockerfile` (`C5`-`C7`), gated by `src/check-container.py`, Trivy, and SPDX SBOM generation in `.github/workflows/src-deploy.yml` (`C2`), version-tagged `sha-<40hex>-r<run_id>-a<attempt>` and pinned by immutable `@sha256:<64hex>` repo digest in `infra/scripts/pipeline.py` (`C3`), and wired into all 7 Container App / Job containers in `infra/modules/containerapps.bicep` (`C1`, `C13`).
* **Gap to fix**: Add `f"job-forward-{environment}-rank-publish"` to the maintenance-job `orchestratorImage` consistency set in `infra/scripts/pipeline.py` (`C4`) so PR planning enforces digest consistency across all three scheduled maintenance jobs (`auth-renewal`, `ledger-verify`, `rank-publish`), and prove both `pipeline.py` and compiled Bicep wiring in `infra/tests/test_container_hosting_144.py`.

### Q2 — Container hardening enforced in the deployed app, not only in CI

* **Accepted finding**: Because `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` do not support `securityContext` (`C14`) and `test_container_contract.py` forbids Docker `ENTRYPOINT` wrappers (`C10`), deployed-app enforcement must combine **Bicep container/volume specification controls** with **in-process Python startup & health runtime enforcement**:
  1. **Deployed Bicep spec (`infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`)**:
     * Inject `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, and `TMPDIR: '/tmp'` (plus `ZF_STATE: '/state'` on state-writing containers) in every deployed container's `env`.
     * Mount explicit `EmptyDir` ephemeral volumes (`tmp` -> `/tmp`, `state` -> `/state`) in `template.volumes` and `container.volumeMounts` so writable scratch paths are explicitly declared and bounded in the deployed ARM resource specification (`C15`).
  2. **Deployed application runtime (`src/core/src/zava_forward/core/container_hardening.py`)**:
     * Invoked at process startup across `api` (`server.main`, `resident_demo.app.main`, `live_receiver.main`, `live_simulator.main`), `agents` (`worker.main`), `orchestrator` (`__main__`, `token_store.main`, `digest_blob.main`, `ranking_publish.main`, `source_monitor.main`, `document_rescan.main`), and `importer` (`__main__.main`), and checked on `/healthz`.
     * When `ZF_CONTAINER_HARDENING=enforced` (active in every deployed Container App and Job):
       * Enforces non-root UID/GID (`uid == euid == 10001` and `gid == egid == 10001`, rejecting `0`/root) and sets `os.umask(0o077)`.
       * Calls `prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` on Linux to actively enforce `NoNewPrivs: 1` inside the deployed container process, then parses `/proc/self/status` and fails closed if any of `CapEff`, `CapPrm`, `CapInh`, or `CapAmb` is non-zero or `NoNewPrivs != 1`.
       * Enforces `PYTHONDONTWRITEBYTECODE=1` / `sys.dont_write_bytecode`, actively probes `/` and `/app` to verify filesystem writes are rejected (`EROFS` or `EACCES`, unlinking and failing closed if a write succeeds), and verifies declared ephemeral scratch directories (`/tmp`, and `/state` when configured) are writable.

### Q3 — Declared-scale fixture load test run and recorded without claiming production scale

* **Accepted finding**: `src/api/tests/scale_load.py` (`C16`) and `src/api/tests/test_scale_fixture_load_and_restart.py` (`C17`) generate the deterministic 60,000-home (`SEED = 11`, 53,821 events) SQLite `SqlStore` fixture, exercise `list`/`detail`/`dashboard` routes at 20 concurrent sessions / 5.0 target req/s, record latency (`p50`/`p95`/`p99`), RSS, CPU, SQL statement drivers, and explicitly set `meets_declared_workload: false` and `Not production scale` scope caveats. We will execute and record fresh dated `2026-11-15` runs (`docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`) on the hardened code path and assert both live bounded execution and recorded 60,000-home report invariants in `infra/tests/test_container_hosting_144.py`.

### Q4 — Single-replica and restart behaviour verified with audit persistence

* **Accepted finding**: Single-replica and revision boundaries are enforced in Bicep (`activeRevisionsMode: 'Single'`, `apiMinReplicas` default `0`, `maxReplicas: 1` on `enablePublicSimulationLane` and `resident-demo.bicep`, `parallelism: 1` on jobs; `C1`, `C19`), worker restart/drain task-lease safety is proven by `ReplicaRestartTests` and `DrainTests` (`C11`, `C12`), and API single-replica hard `SIGKILL` restart with durable SHA-256 audit hash-chain continuity across process death and subsequent writes is proven by `test_scale_fixture_load_and_restart.py` and `test_restart_audit.py` (`C17`, `C18`). `infra/tests/test_container_hosting_144.py` will directly verify all three surfaces end-to-end.

### Q5 — Scope of `infra/tests/test_container_hosting_144.py` and evidence documentation

* **Accepted finding**: Add `infra/tests/test_container_hosting_144.py` covering all four unticked Issue #144 acceptance criteria with positive and negative/mutation assertions, update `infra/README.md` (status table + deployed container hardening architecture + dated `2026-11-15` load/restart evidence without claiming live Azure deployment or production scale) and `docs/reference/log.md` if any `docs/reference/` file is touched (keeping `infra/README.md` and `docs/architecture/` truthful about local vs live Azure verification boundaries).

## Alternatives Considered

| Option | Summary | Disposition | Rationale |
| --- | --- | --- | --- |
| Option 1 (Selected) | Combine Bicep deployed-spec controls (`ZF_CONTAINER_HARDENING=enforced`, `EmptyDir` `/tmp` & `/state` mounts, `PYTHONDONTWRITEBYTECODE=1`, `pipeline.py` `rank-publish` check) + `zava_forward.core.container_hardening` in-process startup enforcement (`UID/GID 10001`, `prctl(PR_SET_NO_NEW_PRIVS)`, `CapEff/Prm/Inh/Amb == 0`, `/` & `/app` write-rejection probe, writable scratch check) + dated 60,000-home load/restart JSON artifacts + `infra/tests/test_container_hosting_144.py` + `infra/README.md` evidence | **Accepted** | Genuinely enforces hardening in the deployed app (not only CI), compiles cleanly in `az bicep build`, preserves ACA startup compatibility (`C10`, `C14`, `C15`), and keeps all existing `infra` and `src` test contracts intact. |
| Option 2 | Add `securityContext` (`runAsNonRoot`, `readOnlyRootFilesystem`, `capabilities.drop`) in `containerapps.bicep` | **Rejected** | `Microsoft.App/containerApps@2025-07-01` rejects `securityContext` (`Warning BCP037`, `C14`). |
| Option 3 | Add a Docker `ENTRYPOINT ["python", "/app/container-entrypoint.py"]` asserting `ST_RDONLY` and `CapBnd == 0` | **Rejected** | Violates `test_container_contract.py` (`C10`) and crashes in Azure Container Apps where the hypervisor root mount omits `ST_RDONLY` and retains non-root `CapBnd`. |
| Option 4 | Replace `main.bicep` default `quickstart:latest` parameters with empty/failing strings | **Rejected** | Breaks `test_bicep_policy.py:1015-1060` (`C13`) and `deploy.py` bootstrap/dependency-only staging; `pipeline.py` already enforces `@sha256:` digests for release and PR plan flows (`C3`, `C4`). |

## Decisions and Risks

* **Confirmed decisions**:
  * Enforce runtime container hardening opt-in via `ZF_CONTAINER_HARDENING=enforced` set on every deployed Container App and Job in Bicep, while keeping unset local developer test environments non-breaking.
  * Enforce `CapEff == 0`, `CapPrm == 0`, `CapInh == 0`, `CapAmb == 0`, and `NoNewPrivs == 1` (after calling `prctl(PR_SET_NO_NEW_PRIVS, 1)` on Linux) and read-only write-rejection (`EROFS` or `EACCES`) on `/` and `/app`, so the check succeeds in both hardened Docker (`--read-only --cap-drop=ALL`) and Azure Container Apps (`USER 10001:10001`) while failing closed on root, elevated capabilities, or writable code directories.
  * Frame all load and restart recordings explicitly as local synthetic SQLite `SqlStore` measurements over the 60,000-home fixture (`meets_declared_workload: false`), never claiming production scale, live Azure rollout, or 600,000-event 1,800-second open-loop completion.
* **Residual risks / honest boundaries**:
  * Live Azure Container Apps revision rollout, queue scale-out in Azure, and Azure SQL Server persistence remain deployment-time live checks outside offline repository tests; `infra/README.md` must preserve that distinction explicitly rather than overclaiming live cloud execution.

## Potential Further Research

* None required for Issue #144 scope; cycle 1 reached saturation across all four acceptance criteria (`Q1`-`Q5`).

## Readiness and Handoff

* **Research execution status**: Complete (Cycle 1: Wider, Deeper, Contrarian waves completed and synthesized).
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Blocking items**: None.
* **Pointer handoff to `rpi-plan`**: Primary evidence in `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C1`-`C19`).

