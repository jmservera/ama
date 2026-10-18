---
title: Zava Forward source projects
description: Index of the isolated src projects, the dependency rule, local commands and image properties defined by ADR 0006
author: AMA programme
ms.date: 2026-10-18
ms.topic: reference
---

Skeleton projects created for issue #290 (ADR 0006 phase 1). They contain a version module, a `python -m` entry point that prints the version, and tests. Move-not-copy migration happens in #199: M1 moved `profile`, `rulecards` and `ai` into `core` (tests in `core/tests`, plus `agents/tests/test_ai_identity.py`). M2 moved the core hub (`store`, `sqlstore`, `mssqlstore`, `factory`, `ledger`, `continuity`, `chatthreads`, the document, finance, grants, governance, sign-off, workflow, quality, procurement, insights, projection and ranking modules, `ai_tasks`, `ai_registry`, `assistants`, `assistant_release` and `policies/ranking-v1.json`) into `core`, with the shared test fixtures in `core/tests/dataset.py` and `test_content_standard` in `api/tests`. M3 moved the synthetic tools (`scale_fixture`, `sensor_backfill`, `loadcheck`) into `core/synthetic`, `chat_fixture` into `agents/tests`, and the eval fixtures into the owning project's `evals/` folder (`core`, `agents` registry, `importer`), with their tests. M4 moved `chat_privacy`, `chat_isolation` and `recovery` into `core` (tests `test_chat_privacy`, `test_chat_memory`, `test_recovery` in `core/tests`), and `ai_eval` with `evals/ai_priority_golden.json` and `test_ai_eval` into `agents`; M5 moved `server`, `auth`, `timecapture` and `web/` into `api` (the web assets are package data under `zava_forward/api/web/`), `lawstore` and the law source register into `core`, `digest_blob` and `token_store` into `orchestrator`, the image build and hashed requirements into `api`, the browser checks into `api/checks`, and the remaining tests into `api/tests` (job tests in `orchestrator/tests`). Those suites import shared fixtures from `core/tests` and `agents/tests`, so run them with `PYTHONPATH=../core/tests:../agents/tests` (api) or `PYTHONPATH=../core/tests` (orchestrator). M6 split `mvp/README.md` into the per-project READMEs ([api](./api/README.md), [core](./core/README.md), [agents](./agents/README.md), [orchestrator](./orchestrator/README.md), [importer](./importer/README.md)), keeping the dated evidence sections unchanged, and left only a pointer README in `mvp/`; `mvp/` is deleted at cut-over (ADR 0006 phase 5). The decision record is [ADR 0006](../docs/adrs/0006-src-layout-and-cutover.md).

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

Targeted commands above support development; they do not replace the complete
pre-push gate, including for documentation-only issues. Finish implementation
and the original RPI Review, commit the candidate and dated evidence, then run
from the repository root with Python 3.12, Node, Docker, Azure CLI/offline Bicep,
actionlint and Trivy 0.76.0 available on PATH:

```bash
git fetch origin main
BASE_SHA=$(git rev-parse origin/main)
python3 tools/rpi-checks.py --all --base "$BASE_SHA" --out /tmp/rpi-ISSUE-final
python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-ISSUE-final/receipt.json --base "$BASE_SHA"
```

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
port, never a configured database. It serializes heavy work with the shared
`/tmp/ama-rpi-heavy.lock` and cleans only its owned resources.

Install missing prerequisites from trusted pinned sources after an actual
missing-tool/dependency result; preserve project pins. No uv, remote model or
cloud fallback is part of this command. Browser/system-library or scanner/DB
failures block the gate. General-discovery opt-in skips and the one inherited
JSON-only SQL non-applicability are enumerated by test ID and reason; unexpected
required integration skips fail. Existing private-data, real AI, Azure/OIDC,
reviewer protection, privileged what-if and deployment acceptance remain
separate controls, not local successes.

For issue-specific additional unit contracts, repeat a reviewed selector such
as `--extra-test api:test_module.Class.test_method`; the module must be tracked.
This is an argv-based unittest interface, not a shell-command dispatcher.
Receipts are inert evidence: their command arrays are never replayed.

Keep the authoritative receipt outside git to avoid self-reference. It binds
HEAD/tree/base, matrix/helper/tool/package identities, command logs, images and
fresh scan DB metadata. A committed evidence copy is historical. Every later
commit, correction or rebase requires a full new run, as does a changed base or
relevant tool/image identity. Dirty, untracked and ignored candidate inputs are
refused. Fetch main again and verify immediately before independent exact-head
review and push; if it moved, reconcile under the issue's approved RPI scope
and rerun. Preserve original adverse findings. Local verification is not a
replacement for independent review, owner publication permission or retained
hosted checks, and it does not authorize changing required contexts.

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
be resolved in one deliberate PR. `mvp/README.md` is retained pending #201/#202
owner sign-off; this path update does not complete the Azure deployment or private
data copy/encrypted-backup gates.

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
