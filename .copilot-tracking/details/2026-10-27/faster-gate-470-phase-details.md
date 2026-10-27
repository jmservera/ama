---
title: Faster local gate phase details
ms.date: 2026-10-27
---

## P01 implementation

P01-T01: Centralize ordered selected-group closure and map changed names from
base...HEAD with rename detection disabled so old and new paths are covered.
Documentation/tracking/agent Markdown is static tier; tooling gets focused
lint/types. Unknown input fails closed to full. Bind schema-4 scope/selection
and recompute it on verification.

P01-T02: Split grouped methods into dispatchable units while preserving their
commands. Thread-local group/process state, synchronized command reservation,
per-group verification, install lock and dependency scheduler protect shared
state. One Docker-resource exclusion covers SQL and all image groups.
Namespace-derived groups run in order; API/browser/SQL run in order.
Keep the fixed host lock around execution/verification. Cap requested workers
using affinity/cgroup CPU and available host/cgroup memory.

Resume uses a new external directory and an immutable parent receipt reference
and digest. Recursively verify successful parent groups in their original
evidence/environment directories; never replay their commands. Fresh trusted
setup-api/setup-namespace groups prepare prerequisite interpreters where the
corresponding successful parent project group is not executed again. Final
coverage is the union of verified parent successes and current successes.
Missing successful environment checkpoints block resume; failed/incomplete
environments need not be reused. Every parent file, image and tool identity
must still match. No prior output is overwritten. Limit provenance depth.

P01-T03: Keep every existing full-tier check. Add tests within the plan's
18-method budget. Update source commands and coordinator policy in place.

## P02 validation/publication

P02-T01: Unit fixtures simulate concurrency and resume without Docker/Azure.
Measure actual --changed after committing implementation and evidence; keep
receipt external and verify explicit partial scope before publication.
Historical full baseline is 23-26 min, representative command sum 1547 s.
No after-full timing will be fabricated or measured.

P02-T02: One independent post-implementation Review preserves findings and
routes later work rather than rewriting the original review. Commit all
dated phase artifacts with privacy-safe identity and Co-authored-by trailer.
Fetch main and validate exact final candidate before ordinary topic push/PR.
Hosted checks and owner merge remain separate approvals.

## Concrete selection and verification contracts (critique amendments)

| Input | Selected groups before dependency closure |
| --- | --- |
| docs/, tracking/, support/, Markdown including agent policy | static |
| tools/rpi-checks.py and tools/test_rpi_checks.py only | static, tooling |
| core | all project groups; SQL for store/schema/SQL inputs; all images for runtime/build inputs |
| agents | agents, api; consumer images for runtime/build inputs |
| api | api; browser for web/checks; SQL for stores/assistants; image for runtime/build inputs |
| orchestrator/importer | own project and runtime/build image |
| infra | infra |
| workflows, shared image/build/gate inputs, unknown tools/paths | full fallback |

Union mixed paths; disable rename detection and parse NUL-delimited names to
cover deleted and old/new renamed paths including unusual names. Empty diff
still runs static. All tiers include preflight. Namespace is the existing
bootstrap for static/infra/migration/images/tooling; API is required by
browser/SQL. Full closure does not add the partial-only tooling group.
Tooling uses pinned Ruff 0.17.1 and mypy 2.4.0, existing tool targets.

Verification first recomputes selected groups/scope from trusted source and
base, then verifies each group's ordered commands, environment names, selected
files/results and live images. Only SQL checks require SQL identity; only
browser requires axe/browser outputs; only infra requires workflow inventory;
only scanned images require Trivy/SPDX. Missing/invalid scope is rejected.
Schema 3 remains historical and is not promoted. Partial opt-in is explicit.

Schedule project installs/namespace first under the setup lock, then independent
project suites. Images wait for all mutable install-bearing groups; serialize
namespace consumers and API consumers. SQL and all image/scanner work share an
exclusion lock. On cancellation stop tracked children, join all workers, then
clean owned snapshot/containers. Failed prerequisites block descendants.

Resource admission: positive jobs only; effective workers <= requested jobs,
floor(available affinity/cgroup CPUs / 2), and
floor((host/cgroup available memory - 1 GiB) / 4 GiB). Admit at least one only
when the reservation fits; otherwise fail explicitly. Unlimited cgroups defer
to host limits; malformed available limits fail rather than assume capacity.

Before any real measurement, inspect the committed diff selection using the
trusted selector. Abort rather than execute if it selects full. Expected
branch selection: preflight, namespace, static, tooling.
