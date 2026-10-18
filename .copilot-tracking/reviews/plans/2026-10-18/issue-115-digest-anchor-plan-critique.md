---
title: Issue 115 digest anchor final-candidate plan critique
description: Single independent assessment of the bounded recognized-anchor correction
ms.date: 2026-10-18
---

## Metadata

* Task ID: 115
* Task slug: issue-115-digest-anchor
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue-115-digest-anchor-research.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique; no nested reviewers or second critique.
* Observed branch: fix/digest-anchor-evidence-115
* Observed HEAD and local origin/main: c803614e8ca7c604e509f1c088f8b8f90f3063ef
* Existing untracked plan, details, research and RPI state were left untouched.

## Inputs and Criterion Boundary

The supplied plan, phase details, research and full caller requirements define
the assessment boundary. Direct source inspection covered
src/orchestrator/src/zava_forward/orchestrator/digest_blob.py,
src/orchestrator/tests/test_digest_blob.py,
src/core/src/zava_forward/core/ledger.py,
src/core/src/zava_forward/core/store.py,
src/core/tests/test_recovery.py,
src/orchestrator/README.md,
src/orchestrator/pyproject.toml and .github/workflows/src-ci.yml.
Required project context was read from the original case study, addendum opening,
knowledge-base index and memory; none was changed.

Criteria are the fail-closed absence of recognized remote head/year evidence,
explicit report and CLI alert/nonzero behavior, genuine failing-first evidence,
preservation of either-anchor success and existing negative/publication tests,
truthful empty-ledger semantics, bounded test ownership, local configured gates,
immutable independent assessments and authorized publication safeguards.
No issue ordering dependency is introduced; #114 is hierarchy only. The base
commit identifies merged PR #403, whose loadcheck paths remain out of scope.

The assessment does not authorize implementation, commit, push, cloud access or
operational acceptance. This worker writes only this critique artifact. Research
probe results are supplied evidence, not independently rerun test receipts.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, FR2, C1, C4, P01-T01/T02, AC1 | Covered | The current verifier tests all listed names for absence despite reading only recognized prefixes. The planned replacement and explicit problem preserve the report/CLI contract. Failing-first completion excludes setup/import errors. |
| FR3, C5, AC2 | Covered | Head-only and completed-2024-year-only matrices include direct verification and CLI checks, with/without unrelated invalid JSON and download assertions. No both-types requirement or stricter filename grammar is introduced. |
| FR4, C6, AC2 | Covered | Local-only evidence cannot populate remote collections. Genuine empty entries are distinguished from missing fixtures; absent anchors fail, zero-count GENESIS head retains existing success, nonempty head/year evidence fails against empty entries. |
| FR5, AC3 | Covered | Existing truncation, rewrite, broken-chain, year-mismatch, unreachable-container and create-only/idempotent tests remain unchanged and run in the canonical suite. Unrelated bytes are ignored, not a bypass around chain/year checks. |
| Locked candidate and scope | Covered | At most eight new methods, no removals or shared-fixture edits, canonical existing fake/test file, no generated targets, no core changes, and a narrow existing README edit are explicit. Subtests make the bounded matrix feasible. |
| NFR sanitized fixtures, C8, P01-T01, P02-T01 | Partial | Credential isolation is specified, but the sanitized runner does not bind the existing tempfile fixtures to an allowed workspace directory; PC-001. |
| AC4, C7, P02-T01 | Covered with PC-001 | Focused digest/coupled recovery checks, full orchestrator discovery, configured Ruff check/format, mypy and diff check are planned. Digest formatting exclusions and mypy ignore_errors are explicitly disclosed. |
| AC5, P02-T02 | Covered | One original independent Review, frozen originals, at most two separate correction cycles, actual receipts and a distinct final-head coordinator review are required. |
| Publication and dependencies | Covered | Main-target PR uses Refs #115 without closing keywords; privacy-safe local identity, clean committed delivery and remote-head evidence are required. Advancing main causes a stop, not unauthorized integration. |
| Operational/non-goal boundary | Covered | Private inputs, credentials, services, policy choices, deployment/spend, web/KB/loadcheck edits and new mvp work remain excluded. SQL/Docker/cloud/browser acceptance is not inferred from offline tests. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The source correction and semantic test matrix are credible and
  appropriately bounded. One execution-path omission must be corrected before
  running the required failing-first and subsequent tests under the stated
  filesystem restrictions. This is a direct planner correction, not a new user
  decision or justification for a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Bind sanitized test processes to an allowed workspace fixture root

* Related IDs: NFR sanitized fixtures; P01-T01; P02-T01; AC1; AC4; research C8.
* Evidence: .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md:33
  calls for a task temp directory but does not configure its location.
  Lines 64-67 specify `env -i` with PATH and public-fixture PYTHONPATH.
  src/orchestrator/tests/test_digest_blob.py:43-45 uses
  `tempfile.TemporaryDirectory()` without `dir`; the required coupled harness
  likewise does so in src/core/tests/test_recovery.py:63-65.
  The supplied runtime boundary prohibits /tmp and /var/tmp writes and requires
  scratch file operations within the working project.
* Concern: Naming a task temp directory does not redirect the canonical existing
  fixtures. A sanitized process without an explicitly supplied workspace
  temporary-file root can select a prohibited system directory. An inherited
  TMPDIR would also be removed by `env -i`. This affects the first regression
  before any production change as well as the full validation suite.
* Impact: The prescribed validation path can violate the filesystem boundary or
  fail during fixture setup, yielding neither a valid failing-first result nor
  usable acceptance receipts.
* Smallest useful change: Specify a pre-created task-owned scratch root beneath
  this worktree, pass its absolute path as TMPDIR inside every sanitized Python
  test invocation, and check the selected tempfile root before running tests.
  Apply this to P01-T01 as well as focused/coupled and full-discovery commands.
  Clean up only task-owned scratch content after use and leave generated
  fixtures untracked. Preserve the existing fake, shared fixtures, method limit
  and source scope; do not modify tests merely to redirect their directories.
* Action owner: Planning parent for the plan/details correction; implementation
  parent for execution and receipts.
* Exact resolving evidence: Updated P01/P02 runner instructions explicitly
  provide the workspace TMPDIR after `env -i`; the implementation changes
  artifact records the actual sanitized commands and a fresh-process
  `tempfile.gettempdir()` result beneath the worktree. The first unrelated-only
  regression then reaches the expected behavioral assertion against the
  unchanged digest source, followed by successful planned checks using that
  same root and task-owned scratch cleanup.
* Decision route: Planner-direct correction. Current user/runtime restrictions
  already resolve the choice; no significant/divergent user decision is needed.

## Strengths and Residual Risk

* The plan correctly distinguishes listing arbitrary JSON from possessing
  recognized remote evidence. It changes only the absence predicate and
  problem wording rather than transport, report shape or schema.
* Source inspection supports the either-anchor contract: core verification
  accepts an intact chain without supplied digests, and year verification
  checks supplied sealed years without demanding a current-year seal.
* Empty-ledger assertions remain deliberately narrow. Core verification does
  not authenticate zero-count head fields; preserving an explicitly published
  zero-count GENESIS control is not a claim of schema validation or
  pre-first-publish authenticity.
* P01-T01 requires direct report assertions and injected CLI marker/exit
  assertions, with a behavioral failure before the guard edit. Existing tests
  alone do not prove that regression; the later actual receipt is mandatory.
* Coupled recovery tests include local SQLite fixtures. Running those existing
  unit tests is not external SQL-service validation or production persistence
  acceptance. The N/A declaration must retain that distinction.
* Configured Ruff/mypy gates do not establish strict coverage of exempt digest
  files. The plan already acknowledges this limitation.
* One original Review cannot independently accept later source corrections or
  a receipt-only final commit. The planned coordinator exact-head review
  preserves that boundary and must not be relabeled as this original Review.
* Real immutability/retention lock, hosted scheduling/monitoring, recovery
  acceptance and independent initial publication remain outside local evidence.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap or unresolved user choice was identified
  within the supplied boundary.
* PC-001 is resolvable directly without widening scope or delegating another
  planner/reviewer.

## Limitations

* No tests, lint, formatting, typing, network checks or publication were run by
  this critique worker. This assessment checks planning credibility, not
  implementation acceptance.
* Local origin/main matched the pinned base during inspection; no fresh remote
  query was made. The publishing parent must perform its planned remote-main
  check at delivery time.
* Source files and all supplied planning/research/state records remain unchanged.
  This original finding set must remain byte-exact after handoff, including its
  Revise verdict, even when the parent resolves PC-001.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Specify the allowed workspace TMPDIR in the P01/P02
  sanitized runners and record disposition outside this frozen critique.
* User response required: No.

## Next Steps

The active planning parent should disposition PC-001 directly, freeze this
original artifact with its SHA-256 receipt, and proceed to the failing-first
implementation task after correcting the runner instructions. Do not commission
another critique. No user action is required.
