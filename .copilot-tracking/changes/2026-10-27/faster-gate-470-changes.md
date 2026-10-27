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

Broader tools unittest discovery initially exposed missing local application
distributions, then pytest in the external focused environment. Installed
core/agents/API from an external `git archive` of the committed source and
restored pytest there (no editable metadata in this checkout). The subsequent
`cd tools && PYTHONDONTWRITEBYTECODE=1 <external-python> -m unittest -q`
passed all 123 discovered unittest cases. Pytest-style function tests are not
claimed as executed by unittest.

## P02 measured partial execution

The trusted selector was inspected before execution and confirmed exactly
preflight, namespace, static and tooling. No full fallback was executed.
A clean detached checkout of the branch's committed implementation
`da2969b894b1457c6648bc807312d9f414608c01` allowed independent policy evidence
generation to continue without dirtying the measured candidate. Its base was
`2fbb42f0ed80b84429fc7962eda1e04e3265e15e`.

Actual `--changed --jobs 3` wall time: 62.668 seconds, exit 0.
Resource admission reduced requested 3 workers to 2. All 28 commands passed,
and the runner verified the receipt explicitly as partial. Command-duration
sums: preflight 3.595 s, namespace 32.611 s, static 10.545 s, tooling 7.243 s.
Wall time also includes checkout/setup/verification/cleanup overhead.

External receipt:
`/mnt/ama-rpi-gates/issue470-fast-da2969b8/receipt.json`.
External measurement:
`/mnt/ama-rpi-gates/issue470-fast-measurement.json`.
The auxiliary clean source worktree was removed; original adverse and
measurement evidence was retained. Later evidence commits invalidate this
receipt as a final-head claim and require a fresh final partial run.

Before: supplied analysis measures 17 historical full runs at 23-26 minutes,
representative command-duration sum 1547 seconds. After: measured small tooling
tier 62.668 seconds, not a like-for-like full benchmark. Parallel full timing
remains unmeasured, explicitly prohibited here. Hosted CI and owner merge are
separate gates. The issue's full-before/after benchmark criterion is therefore
not claimed complete; publication must use Refs #470.

## Remaining work

Independent Review, policy behavior gate completion, final exact-head partial
verification and topic PR publication. No source corrections are currently
pending; any Review findings will be preserved and routed, not erased.

## Original Review and routed continuation

The single independent Review executed Complete / Not accepted. Original
RV-001 through RV-003 identify direct SQL-manifest closure, extra-API shared
environment exclusion and nested cgroup admission defects. RV-004 retains
the explicitly unmeasured full benchmark as later owner-controlled work.
The original review is immutable and is not rerun or relabelled Pass.

A separate later `rpi-implement` invocation executes P03 under the original
owner instruction to deliver working code before publication. These are
compatible corrections to accepted requirements, not new design decisions.
Focused regressions and an independent exact-head publication assessment will
provide later evidence without replacing the original Review.

Policy-only simulation completed: seven scenarios independently graded Pass,
static Pass and mechanical Pass. Evidence is harness-default model proxy
simulation, not native coordinator/CI execution or intended-profile assurance.
The original mechanical failure and its parent-concurrency explanation are
preserved in the policy report; human-review checkbox remains unchecked.

## P03 routed implementation evidence

RV-001: Core/API dependency manifests now select mssql and its API prerequisite.
RV-002: API extra suites are serialized after selected browser/SQL writers and
other API extras, including when API setup was recreated during resume.
RV-003: capacity resolves `/proc/self/cgroup` against cgroup-v2 mount metadata,
walks the effective directory and all visible ancestors, and intersects their
CPU/memory limits with host affinity and available memory. Unresolvable inputs
fail closed. The actual host's session/user/user-slice/root ancestry resolves
and admits two workers for a request of three.

Added direct manifest-consumer assertions, deterministic shared-API exclusion
coverage including resumed setup, and nested/current/ancestor CPU/memory and
unresolvable-mount/membership fixtures. All 126 tools unittest cases pass;
the focused gate suite now contains 30 methods (16 new, within budget).
Pinned Ruff/format and strict mypy pass. The original 184 full command contracts
were independently confirmed unchanged by the original Review; P03 alters
selection/scheduling/admission only, not those command contracts.

No second RPI Review was run. Publication requires a fresh committed-head
partial receipt and an independent exact-head assessment. The 62.668-second
measurement remains historical implementation evidence; final-head timing and
receipt will be retained externally and recorded in the PR without another
self-invalidating evidence commit.
