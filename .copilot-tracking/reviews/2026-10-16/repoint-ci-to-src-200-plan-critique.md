---
title: Issue 200 source cut-over plan critique
ms.date: 2026-10-16
---

## Metadata

* Task ID: #200 / repoint-ci-to-src-200
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/repoint-ci-to-src-200-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent critique; no further critique requested.

## Inputs and Criterion Boundary

* Caller requirements: assess the supplied plan once, write only this artifact,
  preserve mvp/, workflow/check names, image identities and private-data boundaries.
  The parent has authority for the full RPI sequence and subsequent push/PR.
* Primary inputs: the plan and phase-details paths above, plus
  .copilot-tracking/research/2026-10-16/repoint-ci-to-src-200-research.md.
* Source evidence: .github/workflows/src-ci.yml,
  .github/workflows/mvp-ci.yml, .github/workflows/mvp-validation.yml,
  src/api/Dockerfile, src/orchestrator/Dockerfile,
  src/api/src/zava_forward/api/__main__.py,
  src/api/src/zava_forward/api/version.py, src/api/tests/test_version.py,
  src/core/src/zava_forward/core/factory.py,
  src/core/src/zava_forward/core/synthetic/__init__.py,
  src/core/tests/test_synthetic_output_dir.py,
  infra/modules/containerapps.bicep, tools/rename-zava.py,
  tools/rename-zava-tests.py and docs/adrs/0006-src-layout-and-cutover.md.
* Repository context: original case study, addendum, knowledge-base index,
  owner memory and housing-association primer. No regulatory interpretation
  or business-scope change is assessed.
* Decisions and acceptance: src build context and installed packages; named
  Docker copies; unchanged workload identities and SQL/blob grants; local
  synthetic validation; five unit suites and existing checks; maximum ten
  new focused test methods with no removals and ownership locked by the plan.
* Boundary: requirements, research C1-C9/W1, all phases/tasks, dependencies,
  acceptance criteria, decisions and risks. This is implementation-readiness
  assessment, not implementation acceptance or Azure deployment approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2 / P01-T01: entry point and CI | Partial | Socket-free delegation test and trigger coverage are credible; version execution needs PC-002 correction. |
| C3-C4 / P01-T02: isolated images and jobs | Covered | Existing orchestrator image and parameter support the narrow retarget; compiled image/command assertions preserve identities and grants. |
| C5 / P01-T03: runtime data paths | Covered | Reuse existing folder resolver while retaining explicit filenames; mocked Store avoids private input reads. |
| C6 / P01-T03: branding targets | Covered | Packaged web/policy/logo targets and no-mvp-output regression address the live stale references. |
| C7-C9: already migrated guards/tools | Covered | Verification rather than repeated migration; no private generator execution is authorized. |
| W1 / scope and non-goals | Covered | Caller preservation decisions control; no check renaming, mvp retirement or cloud deployment added. |
| P02-T01: validation prerequisites and execution | Partial | Five suites, lint/type/format, Bicep, app and four-image checks are identified; tool/scratch paths need PC-001 correction. |
| Test ownership and maximum additions | Covered | Retain the named owners, ten-method ceiling and zero removals; neither finding requires extra tests. |
| P02-T02: documentation and acceptance status | Covered | Current commands/index/log are updated while historical evidence is preserved; unmet gates remain explicit. |
| P02-T03: review and publication | Covered | One implementation review, safe GitHub-derived email, intended-path commit, topic push and main-targeted PR with Refs #200. |
| Dependencies and residual acceptance | Covered | Runtime/probe edits must land together; job retarget accompanies API isolation. Azure/new-tag health, real SQL/model/human acceptance and private backup remain unmet. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: The scoped mechanical cut-over is credible, but one validation
  instruction conflicts with the execution boundary and another is not
  executable as specified against the current version module. Both are direct
  planner corrections, not reasons to widen scope or seek new user decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation tool and scratch paths violate the execution boundary

* Related IDs: P02-T01; local validation acceptance criterion.
* Evidence: .copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md:46
  explicitly directs creating/restoring tools under a system temporary path.
  The active execution constraint forbids that location and requires
  workspace-relative file creation. Existing tools/rename-zava-tests.py and
  src/core/tests/test_synthetic_output_dir.py use tempfile.TemporaryDirectory,
  so correcting only the virtualenv path does not control test scratch output.
* Concern: Following the phase literally violates the permitted filesystem
  boundary. Unconfigured test and pip scratch paths can do the same indirectly.
* Impact: The planned local validation cannot be executed compliantly as written,
  irrespective of whether application changes are correct.
* Smallest useful change: Replace the external tool path with a unique
  workspace-local virtualenv and scratch/cache locations. Explicitly configure
  TMPDIR and relevant installer caches for local commands, use synthetic inputs
  only, and exclude/clean task-created scratch artifacts before staging.
  Keep missing-tool/package failure as the prerequisite for installation.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 names only permitted workspace-local tool,
  scratch and cache locations and their environment setup; implementation
  command evidence later records that setup and task-only cleanup.
* Decision route: Direct planner correction; no user response required.
* Direct disposition: Revise phase details before implementation; preserve
  the locked test owners/count and do not modify existing tests merely to
  redirect their standard temporary-file mechanism.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Version-module execution does not satisfy the image probe

* Related IDs: C1-C2; P01-T01; coordinated CI validation.
* Evidence: .copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md:16-17
  directs replacing version probes with version-module execution.
  src/api/src/zava_forward/api/version.py:1 only assigns __version__.
  .github/workflows/src-ci.yml compares the API image probe output with
  zava-forward-api 0.1.0 and separately invokes package entry points in the
  namespace job. A read-only runpy execution of the version source captured
  empty stdout during this critique.
* Concern: A literal switch to python -m zava_forward.api.version exits
  without printing the expected version. Avoiding server startup alone
  is insufficient for the existing image check.
* Impact: The image project check fails after the entry-point fix even
  though the server itself may work; leaving the namespace invocation
  unchanged instead causes a long-running server in that job.
* Smallest useful change: Specify an explicit non-serving command that imports
  the API version and prints the existing distribution/version string.
  Apply the coordinated replacement to both the API image RUN_CMD and
  namespace API invocation, preserving check/job names and other workloads'
  current behavior. No new public version CLI is necessary.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 contains the explicit command and identifies
  both invocation sites; later validation captures exact expected stdout,
  successful exit and namespace completion without a listening server.
* Decision route: Direct planner correction; no user response required.
* Direct disposition: Clarify the existing task before implementation;
  use its existing validation budget rather than adding test methods.

## Strengths and Residual Risk

* Updated ADR src context, package installation and named-copy isolation are
  honored; no obsolete project-context recommendation is reintroduced.
* Compiled Bicep assertions check semantics rather than text-only proxies;
  token-maintenance and API ledger identities remain unchanged.
* Historical branding assertions, deployment identifiers, pins, non-root and
  read-only/no-data checks are retained.
* Local-only evidence is intentional. New immutable image deployment/health,
  operational SQL/model/human acceptance, private backup and mvp retirement
  remain owner/cloud follow-ups, not findings against this scope.

## Questions or Blocking Evidence Gaps

* None requiring a user decision. Resolve both findings directly in planning.

## Limitations

* No private datasets, properwarm.json, .env, .vscode or private inputs were read.
* No source, plan, phase-details or research files were changed. Existing
  untracked parent planning artifacts were left intact.
* Workflows, Docker builds and test suites were not executed during critique.
  The sole runtime check executed only the public version source with bytecode
  writing disabled and captured its empty stdout.
* Issue-comment provenance is supplied by research W1; no new external
  research or independent remote acceptance claim was added.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct P02-T01 workspace paths and P01-T01 version
  probe specification, then record both direct dispositions and finalize
  planning without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/repoint-ci-to-src-200-plan.md](.copilot-tracking/plans/2026-10-16/repoint-ci-to-src-200-plan.md) | Assessed plan and locked validation ownership |
| [.copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md](.copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md) | Two direct planner corrections |
| [.copilot-tracking/research/2026-10-16/repoint-ci-to-src-200-research.md](.copilot-tracking/research/2026-10-16/repoint-ci-to-src-200-research.md) | Supplied evidence and scope decisions |
| [.copilot-tracking/reviews/2026-10-16/repoint-ci-to-src-200-plan-critique.md](.copilot-tracking/reviews/2026-10-16/repoint-ci-to-src-200-plan-critique.md) | Complete single critique and actionable finding set |

## Next Steps

The active planning parent resolves PC-001 and PC-002 directly, records their
dispositions and proceeds through the authorized RPI gates. No user action or
second critique is required. This critique stops here.
