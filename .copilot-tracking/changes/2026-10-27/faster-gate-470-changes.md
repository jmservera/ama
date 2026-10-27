---
title: Faster local gate implementation evidence
ms.date: 2026-10-27
---

## Scope and state

Implementing P01 and P02 of the ready issue #470 plan after one independent
critique and direct PC-001 through PC-006 dispositions. Source changes are
restricted to runner/tests, coordinator policy and directly related commands.
No full gate or Azure execution is authorized.

## P01 completed

Schema 4 records and independently recomputes full/partial selection.
Default verification rejects partial scope. Changed-path mapping unions
transitive consumers/setup, handles rename/deletion with NUL-delimited Git
paths, and falls back to unchanged full coverage on unknown inputs.

Independent suites use thread-local process/group state and unique logs.
Shared editable setup precedes readers; API/namespace chains and SQL/image
exclusion prevent resource races. Workers are capped after acquiring the
fixed host lock, using CPU affinity/quota and host/cgroup available memory.
Cancellation stops children and joins workers before owned cleanup.

Resume references immutable failed parent receipts from new output directories,
reuses only verified successes at the same exact source/base/tools, and creates
trusted setup environments for remaining groups. Full coverage can combine
verified parent successes and current successes without rerunning successful
test groups or replaying receipt argv. Missing/changed evidence, environments,
images or unsafe cleanup checkpoints block reuse. Provenance depth is bounded.

Coordinator policy and source commands now describe risk tiers, deliberate
parent/sub-issue stacks and image retention through verification. The runner
base remains origin/main even for child PRs targeting a parent.

## Validation

`cd tools && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q test_rpi_checks`:
27 tests passed, including 13 added methods within the 18-method plan budget.
Existing full-command mutation rejection tests remain intact.
Pinned Ruff 0.17.1 lint/format and mypy 2.4.0 strict checks passed. The system
Python lacked Ruff; installed only those pinned tools in an external venv.
No application dependency manifests changed.

Measured partial execution and independent Review remain pending. Inspect
selection first and abort if it would select full. External receipts remain
exact-HEAD bound; subsequent evidence commits require refreshed verification.

## Remaining work

Implementation, validation, independent Review and topic PR publication.
