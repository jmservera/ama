---
title: Zava Forward source projects
description: Index of the isolated src projects, the dependency rule, local commands and image properties defined by ADR 0006
author: AMA programme
ms.date: 2026-10-27
ms.topic: reference
---

The projects began as skeletons in issue #290 (ADR 0006 phase 1). The
move-not-copy migration in #199 completed M1-M6: core/domain/storage modules
and synthetic tools moved to `core`, assistant evaluation to `agents`, HTTP,
auth and web assets to `api`, jobs to `orchestrator`, and import fixtures to
`importer`. Tests and evals belong to their owning project outside the package.
M6 split the former README into the per-project guides
([api](./api/README.md), [core](./core/README.md), [agents](./agents/README.md),
[orchestrator](./orchestrator/README.md), [importer](./importer/README.md)),
preserving their dated evidence sections.

The owner signed off #201 on 2026-10-27. The remaining `mvp/` pointer is now
retired; `prototype/` was already absent. Archive `v0.21.0` and the owner-only
tag push command are recorded in the [repository README](../README.md#source-cut-over-archive).
The decision record is [ADR 0006](../docs/adrs/0006-src-layout-and-cutover.md).

## Projects

| Project | Distribution | Import root | Image | Provisional core extras |
| --- | --- | --- | --- | --- |
| [core](./core/) | `zava-forward-core` | `zava_forward.core` | none | declares `sql` and `blob` |
| [api](./api/) | `zava-forward-api` | `zava_forward.api` | [Dockerfile](./api/Dockerfile) | `sql` |
| [agents](./agents/) | `zava-forward-agents` | `zava_forward.agents` | [Dockerfile](./agents/Dockerfile) | none |
| [orchestrator](./orchestrator/) | `zava-forward-orchestrator` | `zava_forward.orchestrator` | [Dockerfile](./orchestrator/Dockerfile) | `sql`, `blob` |
| [importer](./importer/) | `zava-forward-import` | `zava_forward.importer` | [Dockerfile](./importer/Dockerfile) | `blob` |

`zava_forward` is a PEP 420 namespace: there is no `__init__.py` at that level, so the five distributions install side by side. The extras column is provisional and is reassessed as modules move; the `agents` image must never install `core[sql]`, `core[blob]` or any SQL or blob client (ADR 0001 identity).

## Dependency rule

The #213 offline [source-change job](./orchestrator/README.md#offline-source-change-job-213)
uses the shared [monitor and owner-review contract](./core/README.md#source-change-monitoring-and-review-213).
No API endpoint, deployment, live scraping or legal approval is added.

* `api`, `agents`, `orchestrator` and `importer` may import `core`.
* `api` may also import `agents` until #144 deploys `agents` as its own workload.
* No project imports `api`, and `core` imports no workload.

Each project has `tests/test_dependency_rule.py`, which parses every source and test file and fails on a forbidden `zava_forward.<project>` import.

## Commands

Run from a project folder (for example `src/agents`), in a virtual environment, with pip only:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ../core -e ".[dev]"        # api also needs -e ../agents; core needs neither
python -m unittest discover -s tests -v
ruff check . && ruff format --check . && mypy
```

Regenerate hashed requirements with `pip-compile --generate-hashes --no-emit-index-url --no-emit-trusted-host --output-file=requirements.txt requirements.in`. Pins are never loosened. `build-requirements.txt` holds the hashed build tools used only in the image build stage.

### Local RPI gate

Owner policy (2026-10-27): small issues, tooling and documentation use planned
unit and focused tests, with hosted CI still required. Big features, releases,
infrastructure, deployment, SQL and security changes require the complete gate.
Do not treat a partial receipt as full-tier evidence. Finish implementation
and the original RPI Review, commit the candidate and dated evidence, then run
from the repository root with Python 3.12, Node, Docker, Azure CLI/offline Bicep,
actionlint, ShellCheck and Trivy 0.76.0 available on PATH:

```bash
git fetch origin main
BASE_SHA=$(git rev-parse origin/main)
python3 tools/rpi-checks.py --all --jobs 3 --base "$BASE_SHA" --out /tmp/rpi-ISSUE-final
python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-ISSUE-final/receipt.json --base "$BASE_SHA"
```

For small issues, the conservative changed-path tier maps the committed
`base...HEAD` diff to checks and transitive prerequisites. Unknown paths fall
back to the full matrix; inspect the selection before execution when full work
is not authorized. Documentation selects static checks plus their namespace
bootstrap; runner/tests also select focused tooling lint/types. Runtime/build
inputs select consumer images, and store/schema/SQL inputs select real SQL.
Core/API dependency manifests also select their real SQL consumer. API extra
suites run after selected browser/SQL environment mutations. Worker capacity
intersects effective cgroup-v2 membership and all visible limiting ancestors;
unresolvable membership fails closed.
All selected checks retain their original contracts.

```bash
python3 tools/rpi-checks.py --changed --jobs 3 --base "$BASE_SHA" --out /tmp/rpi-ISSUE-fast
python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-ISSUE-fast/receipt.json \
  --required-scope partial --base "$BASE_SHA"
python3 tools/rpi-checks.py --resume /tmp/rpi-ISSUE-fast/receipt.json \
  --jobs 3 --base "$BASE_SHA" --out /tmp/rpi-ISSUE-retry
```

Resume is only for a failed receipt at the exact same clean commit/base and
tool identity, not for a fix committed afterward. It verifies successful
parent groups in their original external directories and reruns failed/unrun
groups through trusted dispatch, with fresh prerequisite setup where needed.
Keep all parent directories, logs, environments and images unchanged. A new
attempt records the parent receipt hash; prior adverse evidence is immutable.
Missing checkpoints, changed evidence or failed cleanup block resume.
Schema-4 receipts bind their full/partial scope and recomputed path selection.
Verification defaults to requiring full coverage; `--required-scope partial`
explicitly accepts partial coverage and never upgrades it to a full claim.

#### Measuring full-gate scheduling

Compare the existing serial baseline (`--all --jobs 1`) with parallel scheduling
(`--all --jobs 3`) at the same clean committed HEAD and reviewed main base.
Use a new external output directory for each run, with no `--changed`, resume
or differing extra selectors. The runner already owns
`/tmp/ama-rpi-heavy.lock`; use its `--lock-timeout 600`, not an outer `flock`
around this self-locking command. Other heavy validation must use the same lock.

```bash
python3 tools/rpi-checks.py --all --jobs 1 --lock-timeout 600 \
  --base "$BASE_SHA" --out /tmp/rpi-ISSUE-serial \
  > /tmp/rpi-ISSUE-serial.log 2>&1
python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 600 \
  --base "$BASE_SHA" --out /tmp/rpi-ISSUE-parallel \
  > /tmp/rpi-ISSUE-parallel.log 2>&1
```

For each run, record the command exit, receipt path, HEAD/base, selected
groups/extras, requested jobs and admitted `receipt.jobs`. Measure the same
execution interval in both logs: from the runner's `Lock ... acquired`
timestamp to `receipt.sealed`. Report queued-to-acquired time separately.
This interval includes setup, checks and cleanup but excludes lock queueing
and final receipt verification; summed command durations are not parallel
wall time. Independently verify each receipt with the default full scope.

Only two passing, verified full runs with serial admission of one worker and
parallel admission above one support a full serial/parallel comparison.
Compare tool/package versions, CPU/memory admission conditions and selected
inputs; disclose scanner-database, download/cache and serial-first order
effects. Fresh output directories do not make Docker or host caches cold.
Material uncontrolled differences make the observations noncomparable, not
proof of a scheduling speedup. A single ordered pair is descriptive, not a
statistical performance guarantee. Failed or incomplete runs, partial receipts,
lock timeouts or parallel admission capped at one leave the parallel timing
criterion unproven; preserve their evidence without substituting historical
partial timings. Record successful full timings and these qualifications in
the delivery PR. Later evidence commits invalidate these receipts for final
publication, but do not erase their historical benchmark observations.

Use a new external output directory for every run; never overwrite a failed
receipt. The runner tests a fresh detached exact-HEAD checkout, installs each
project's existing dev dependencies with pip into isolated external venvs and
installs all five namespace distributions side by side. It runs their existing
unit/dependency/Ruff/mypy suites, infrastructure/Bicep/actionlint, JS/compile/
tracked-data guards, migration, actual Chromium/design-system/regulatory/axe,
real SQL Server selectors, four Docker contracts and a separate logo-mode
stress build, fixable HIGH/CRITICAL Trivy gates, full reports and SPDX.
No app data or credential environment is inherited. SQL tests drop tables:
the runner accepts only its own labelled local container and random loopback
port, never a configured database. It serializes gates with the shared `/tmp/ama-rpi-heavy.lock`, bounds independent
workers by CPU affinity/quota and host/cgroup memory (two CPUs/four GiB per
worker plus one GiB headroom), and serializes SQL/image work and shared-venv
mutations. Editable setup precedes snapshot readers. It cleans only its owned
containers and checkout; retain verification images until receipt verification
has succeeded.

Install missing prerequisites from trusted pinned sources after an actual
missing-tool/dependency result; preserve project pins. No uv, remote model or
cloud fallback is part of this command. Browser/system-library or scanner/DB
failures block the gate. General-discovery opt-in skips and the one inherited
JSON-only SQL non-applicability are enumerated by test ID and reason; unexpected
required integration skips fail. Existing private-data, real AI, Azure/OIDC,
reviewer protection, privileged what-if and deployment acceptance remain
separate controls, not local successes.

The required local `browser` group also runs
`test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log`
with `ZF_BROWSER_TESTS=1` and the API/core/agents test paths. Its verbose unittest
log and executed/skipped counts are required receipt evidence. Only that exact
test ID with reason `opt-in local Chromium` is accepted during non-integration
`project-api` discovery; its skip remains recorded, not counted as execution.
The dedicated browser command must actually execute: missing/changed command
identity, zero execution, dependency failures and unexpected skips block the
gate and receipt verification. Execution and verification also require exactly
one verbose successful result for that test ID, one reported test and zero skips.
An unrelated, missing, duplicated or additional result cannot substitute for the
named case, even when aggregate counts and log hashes match.
This local coverage adds to, not changes, the
hosted workflow coverage inventory.

General discovery also recognises the exact reason
`Chromium is installed by the later browser-check step` from the browser asset
URL regression when the executable is not yet installed. Both Chromium reasons
are enumerated explicitly; the chat-panel reason retains its narrower test-ID
and `project-api` boundary above. Recognised skips remain visible in receipt
counts, never count as execution and still fail in required integration commands.
Unknown or changed reasons fail closed. Recognising the asset discovery skip
does not prove that its browser regression subsequently executes.

Runner contract tests capture only their synthetic skip transcripts so enclosing
static-suite counts remain truthful. Journey route callbacks bind iteration
fixtures explicitly; neither repair relaxes browser or skip acceptance.

ShellCheck is a required preflight dependency, not an optional actionlint
enhancement: native workflow lint must analyze shell scripts as hosted lint
does. Its version is logged and its binary identity is receipt-bound; a missing
or changed ShellCheck blocks the complete gate or receipt verification.

For issue-specific additional unit contracts, repeat a reviewed selector such
as `--extra-test api:test_module.Class.test_method`; the module must be tracked.
This is an argv-based unittest interface, not a shell-command dispatcher.
Receipts are inert evidence: their command arrays are never replayed.
Verification hashes bounded environment configuration, interpreter files/link
identities, distribution metadata and startup files as data. It never launches
receipt-adjacent Python/pip or imports `.pth`/customization code. Missing,
symlinked package/startup metadata, exceeded bounds or changed identities block
verification; a matching receipt sidecar does not establish executable trust.

Keep the authoritative receipt outside git to avoid self-reference. It binds
HEAD/tree/base, matrix/helper/tool/package identities, command logs, images and
fresh scan DB metadata. A committed evidence copy is historical. Every later
commit, correction or rebase requires a new selected-tier run, as does a changed base or
relevant tool/image identity. Dirty, untracked and ignored candidate inputs are
refused. Fetch main again and verify immediately before independent exact-head
review and push; if it moved, reconcile under the issue's approved RPI scope
and rerun. Preserve original adverse findings. Local verification is not a
replacement for independent review, owner publication permission or retained
hosted checks, and it does not authorize changing required contexts.

### Stabilization validation ladder

For the coordinator's recurring checkpoints (#440), select checks by the
affected requirements, contracts and journeys; this is not an unconditional
full suite after every edit. Use the owning project READMEs and existing
Source CI selectors rather than inventing another command matrix:

1. Run the smallest failing reproduction and focused regression/unit/static
   checks first. After each correction, repeat that reproduction before
   widening validation; preserve the original failure evidence.
2. Run affected-package suites, dependency boundaries, lint and type checks
   using the installed `src/` distributions and documented shared test
   fixtures, never a `PYTHONPATH=mvp` workaround.
3. Exercise relevant local cross-package HTTP/browser journeys, actual
   disposable SQL Server persistence and Docker/non-root contracts. Use
   constructed synthetic data, not default/private `ZF_DATA`, a configured
   real database or paid model calls. Preserve auth/role isolation, resident
   consent and human-approval controls, explicit model failure/unavailable
   states and usable manual paths. Mocks, SQLite and worker skeletons do not
   establish SQL Server, real AI, deployed workloads or live approval.
4. List any Azure-only residuals explicitly. Admit them only when all relevant
   local checks pass, action-specific authority is valid, complete all-in
   cost headroom is evidenced (including accrued charges, outside-group
   liabilities, remaining resources, tranches and reserve), and the approved
   plan has finite commands/scope, budget, time window, stop conditions and
   exact owned-resource cleanup boundaries. All conditions are required.
   Unknown or partial evidence blocks Azure-dependent work only; independent
   local work continues. A budget ceiling is not spending permission or
   incremental headroom. Use the current
   [owner budget decision](../docs/case_study_48_addendum.md#revised-owner-budget-decision-2026-10-22),
   not historical forecasts: USD 700 is replacement all-in, authority expires
   2026-10-25T16:02Z, and complete headroom remains Unknown until its refresh
   gate is met. This guidance grants no Azure or real-model authority.

Before heavy validation, check the actual shared-lock holder/process, not
just whether the lock file exists. Use the existing runner with
`--lock-timeout 0` for nonqueued admission; do not launch duplicate or waiting
gates, interrupt a foreign owner, inspect/reuse its output, or poll for its
release. If busy, record the affected validation as blocked with its exact
source, remaining checks and resume condition, then continue independent
lightweight work. Resume only on a later explicit coordination event after
ownership is free. Each admitted run owns its evidence and cleanup; remove
only its exact owned resources, not foreign sessions, containers or data.

Record actual commands/exits/skips and source/environment identities in the
checkpoint evidence; distinguish local/Azure observations from
implemented-unverified, deferred, blocked and unknown outcomes. Missing
relevant prerequisites or failed local checks stay unmet, not cloud fallbacks.
Once corrections and the original RPI Review are stable, require the selected
tier's evidence under the [local RPI gate](#local-rpi-gate) policy for the
committed final candidate before publication. Full-tier candidates require the
complete gate and its current-main, exact-head receipt; focused-tier candidates
require relevant unit and focused checks, not a full receipt. Neither tier
replaces human/hosted approval gates.

## Images

The [cut-over evidence pack](../docs/architecture/cutover-evidence-pack.md)
records the source-image build attempts, image digests, remote runtime checks
and failed Azure bootstrap for #200/#201. With no local Docker, the tested
remote alternative is
`az acr run -r <registry> -f acr-cutover.yaml --timeout 1800 src` from the
repository root. [acr-cutover.yaml](./acr-cutover.yaml) enables BuildKit for
the existing `RUN --mount` instructions, tests UID/read-only/capabilities/data
paths (and agents dependency isolation), then pushes run-ID-specific tags.
This is not a deployment or vulnerability scan. The context retains only the
API's explicit runtime golden-file exception; other evals/tests/data stay out.
This historical remote route is not a fallback for a failed local RPI gate.

The build context is this `src/` folder, because a workload image also needs `core`:

```bash
docker build -f src/agents/Dockerfile -t zava-forward-agents:local src
```

Each image pins the `python:3.12-slim-bookworm` base by digest, runs an in-image
`apt-get upgrade`, uses UID/GID 10001:10001, copies named packages only and
contains no working data. The latest same-tag digest was checked on 2026-10-16
and is unchanged. Dockerfile alone cannot configure kernel mount flags or
capability bounding sets: supply them at launch. Images retain their direct
Python CMD with no fail-closed ENTRYPOINT guard, so Container Apps can start
them despite lacking these kernel controls. Non-root does not imply a
read-only root, dropped capabilities or NoNewPrivs.

```bash
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  zava-forward-agents:local
# From repository root, after building each image:
python src/check-container.py agents zava-forward-agents:local
```

Working data is mounted read-only at `/data` and writable state at `/state`;
the location follows `ZF_DATA` and is never under `src/`. `src/.dockerignore`,
the API's allow-list `Dockerfile.dockerignore`, and the
`/src/**/data/` gitignore entry keep data out of images and git.
The [hosting limitation](../infra/README.md#hardened-source-image-rollout-118)
means hosted hardening acceptance remains Partial. Runtime flags are enforced
by local/CI Docker contracts, not claimed as available on Container Apps.

## CI

The [deployment pipeline](../infra/README.md#github-deployment-pipeline-refs-138)
adds a separate manual, protected-environment release from `main`: four fresh
images, hardened startup, the same fixable/full Trivy policy, run-versioned
registry tags and immutable deployment digests. Build/test jobs have no cloud
credentials; publication and deployment use separate OIDC identities on private
ephemeral runners. Source CI now filters image builds by project paths and
transitive dependencies without renaming any existing checks. Application unit,
lint and type checks still run for every project. No Azure workflow was run for
this implementation; federation, approvals, quarantine release and live checks
remain setup/acceptance gaps.

The `src-api` browser step also runs the
[regulatory alert/chat UX regression](./api/README.md#local-engineering-checks)
with hash-verified axe 4.10.3. A failed pinned download or integrity check
blocks the browser gate; it is not silently reduced to non-axe assertions.
The job uploads JSON evidence with explicit axe execution status.
API unit discovery also works with runtime-only installations: importing the
regulatory harness does not load Playwright. Pure target-size and axe-integrity
tests remain enabled without a browser; an isolated regression blocks accidental
eager Playwright imports even in dev environments. Playwright stays in the API
dev extra for typed browser checks, which still run in the dedicated CI step.

[`.github/workflows/src-ci.yml`](../.github/workflows/src-ci.yml) retains the checks
`src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`,
`src-namespace` and `src-no-working-data`, and now independently owns the
legacy `mssql` job with its exact selectors. It also retains the legacy
compile/migration/JavaScript/data guards, separate unreadable-logo build and
SPDX coverage. The new local runner/tests and migration tool/requirements
trigger Source CI. Its normal cadence is one consolidated workflow per
eligible PR update, not one run per PR lifetime; ordinary main-push repetition
is removed. Both legacy workflow files remain dispatch-only for rollback.
Their duplicate `test`, `image` and `validate` contexts are not fabricated;
the owner/coordinator must verify required-context mapping before merge,
especially where protection APIs are unavailable. No remote workflow state or
repository protection is changed by these files. Restore the previous triggers
and explicitly re-enable a disabled workflow only under owner direction if
transition coverage or enforcement regresses. Manual release and the privileged
Source CI workflow_run what-if boundary are unchanged.

API packages only core, agents and API; Bicep selects the separate orchestrator
image. The API entry point is `python -m zava_forward.api`; CI version probes
import its version instead of starting the server. Runtime/generated data
default to the per-user `ZF_DATA` folder, never under `src/`. Existing temporary
Ruff/mypy migration exemptions remain; general cleanup is separate work.

Workflow/check naming remains unchanged for branch-protection continuity, following
the issue #200 owner decision of 2026-10-15. The post-cut-over naming question must
be resolved in one deliberate PR. The owner-authorized directory retirement is
recorded in the [2026-10-27 cut-over note](../docs/architecture/cutover-evidence-pack.md#owner-authorized-directory-retirement-2026-10-27);
it does not assert new Azure deployment, private backup, full-suite parity or
rubric acceptance evidence.

### Hardened image CI (#118)

Each of the four image matrix entries runs [check-container.py](./check-container.py)
with `docker run --read-only --cap-drop ALL --security-opt no-new-privileges`.
It verifies root mount flags, an actual EROFS
write failure, writable `/state`, UID/GID, all capability sets, NoNewPrivs, and no
baked working data. Five negative probes per image independently omit
read-only-root, capability dropping or NoNewPrivs, or change UID/GID; the
external contract must reject them, not the shipped image entrypoint.
Both hardened and plain non-root launches run each image's default command.
The API starts its real HTTP server on an empty constructed fixture and checks
health and PNG delivery in both modes. The other default CLIs still print a
version; this does not prove a queue worker or actual Azure startup.

Trivy gates only HIGH/CRITICAL OS and library findings that have a fix, using
the scanner option `ignore-unfixed: true`, not a vulnerability ignore list.
[trivy.yaml](./trivy.yaml) explicitly uses `/dev/null` as the ignore file: no
ignore lists, baselines or repository-discovered config suppressions.
Each workflow also runs a non-gating scan (`exit-code: "0"`,
`ignore-unfixed: false`) and uploads `trivy-*-all.json`, retaining all
HIGH/CRITICAL findings including unfixed packages alongside the fixable gate
JSON. Scanner execution errors still fail visibly. Reports and SPDX upload
even when the gate fails. A runtime failure after a successful build does not
skip its scan. Source CI generates SPDX for all four source images; disabled
legacy workflows are not coverage for a PR. No workflow deploys as part of this change.
The initial 2026-10-16 full scans found 61 HIGH and two CRITICAL package findings
per image (16 unique CVEs, all unfixed in Debian 12.15). A green fixable-only
gate is not a vulnerability-free image or hosted-hardening acceptance. See the
[acceptance audit](../docs/architecture/cutover-evidence-pack.md#deployment-hardening-audit-118-2026-10-16).
