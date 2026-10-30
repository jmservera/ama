---
title: Rebuild 148 refresh final-candidate plan critique
description: Independent bounded critique of the PR 511 local refresh plan
ms.date: 2026-10-30
---

## Metadata

* Task ID: pr-511-refresh-2026-10-30
* Slug: rebuild-148-refresh
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/rebuild-148-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/rebuild-148-refresh-phase-details.md
* Critique execution status: Complete
* Execution: One independent final-candidate assessment; no additional agents.

## Inputs and Criterion Boundary

* Caller requirements: Rebase draft PR 511 locally onto origin/main, preserve
  both conflict intents and main rubric/manifest copies, retain src-only
  executable code and external tests, use the requested existing environment
  for lint/format/mypy and relevant unittests, condition full API discovery on
  a successful heavy-lock probe, perform no Azure operations or push, and use
  a Conventional Commit with the required trailer.
* Research considered:
  .copilot-tracking/research/2026-10-30/rebuild-148-refresh-research.md,
  including C1-C4 and W1-W2. Supplied local evidence pointers inspected:
  src/README.md, src/orchestrator/pyproject.toml and
  src/core/tests/test_scenario_manifest.py. W1-W2 are supplied research
  observations, not independently refreshed hosted results.
* Decisions and dependencies: Existing topic branch; explicit local-rebase
  authority; P01 integration precedes P02 checks; P03 original Review and
  candidate commit precede the complete local gate. Hosted/human approval and
  coordinator publication remain separate.
* Acceptance boundary: Refresh correctness, preservation, bounded validation,
  provenance and local handoff only. Original RV-001, new application behavior,
  workflow permissions, deployment and issue acceptance are excluded.
* Worktree inspection found feat/rebuild-148 with untracked dated task inputs;
  those inputs were neither moved nor edited. Only this critique is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01; rebase and both conflict intents | Covered | Explicit ours/theirs warning, preserve prose, compare original source/test blobs and verify main ancestry. |
| P01-T01; main rubric and manifest authority | Covered | Byte-identical acceptance criterion and explicit prohibition on regenerating main's manifest. |
| C2; src-only source and external tests | Covered | Existing ownership retained; no new production or test modules allowed. |
| P02-T01; lint, format, mypy and focused tests | Covered | Existing project configuration, orchestrator discovery, core manifest/dependency and API dependency/workbench coverage are specified. |
| C3-C4; typing and changed source pins | Covered | Configured strict mypy and actual-source manifest regression are required even without conflicts. |
| P02-T01; full API resource boundary | Covered | Explicit successful nonblocking heavy-lock probe prerequisite; default is no full API discovery. |
| P02-T01/P03-T01; complete local gate | Partial | Post-commit attempt and failure reporting exist; successful-receipt verification and base freshness are not specified. See PC-001. |
| P03-T01; original evidence and independent Review | Covered | Preserve original adverse evidence, perform one independent Review and do not silently fix afterward. |
| P03-T01; commit identity and trailer | Covered | Authenticated id/login-derived author and committer address, Conventional Commit, Refs #148 and required trailer. |
| W1-W2; RV-001 and hosted rubric outcome | Covered | Existing RV-001 stays open; hosted permission failure is not treated as an application failure or locally repaired. |
| No Azure, push, private data or publication | Covered | Explicit prohibitions and coordinator-only publication boundary. |

## Verdict

* Verdict: Revise
* Rationale: The integration and focused-validation plan is credible. One
  planner-owned correction is needed to close the successful complete-gate
  evidence path, without expanding implementation or authorizing publication.
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Specify verification of a successful complete-gate receipt

* Related IDs: C1, P02-T01, P03-T01; exact-head publication receipt acceptance.
* Evidence: .copilot-tracking/plans/2026-10-30/rebuild-148-refresh-plan.md
  requires attempting the complete gate after commit and reporting missing
  evidence. .copilot-tracking/details/2026-10-30/rebuild-148-refresh-phase-details.md
  specifies external output and prerequisite/lock failure treatment, but
  neither document specifies receipt verification on success.
  src/README.md, Local RPI gate, requires the receipt verifier, binds the
  candidate/base/tool identities, and invalidates evidence after later
  commits, rebases or relevant input changes.
* Concern: The failure path is clear, but the successful path stops at a gate
  run. A generated receipt is not yet a verified receipt. The plan also lacks
  an explicit fresh-main/base check for that post-commit run.
* Impact: Local handoff could describe full evidence as complete without
  proving its validity for the committed candidate and current main, leaving
  the coordinator to discover a stale or unverifiable receipt.
* Smallest useful change: Add the post-commit sequence to the existing phase
  details: fetch main, bind the reviewed base, run
  `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>`,
  then on success run
  `python3 tools/rpi-checks.py --verify-receipt <receipt.json> --base <current-origin-main-sha>`.
  Record both outcomes. If main moved or any candidate/input identity changed,
  report invalidation and reconcile within authorized scope before a fresh
  gate; otherwise report the blocker. Preserve the existing heavy-lock,
  no-Azure and no-push restrictions. Leave the final immediately-prepublication
  verification and exact-head assessment to the coordinator.
* Action owner: Planning parent.
* Exact resolving evidence: Updated P02/P03 details explicitly require the
  fresh-base, run, verification and invalidation sequence, while retaining
  failure-as-blocker and coordinator-only publication. Subsequent execution
  evidence must record actual outcomes, not promise a passing receipt.
* Decision route: Direct planner correction. No significant or divergent user
  decision is needed; this implements the existing complete-gate requirement.

## Strengths and Residual Risk

* Conflict resolution protects both branch intent and main authority rather
  than mechanically choosing a rebase side.
* Source-hash validation is required even for a conflict-free rebase.
* Focused tests are not misrepresented as a full gate or hosted success.
* Original RV-001, hosted rubric permissions and formal approvals remain
  explicitly outside refresh acceptance.
* Complete-gate prerequisites or shared-host contention may still block
  publication. That disclosed boundary does not authorize a cloud fallback,
  protection change or push.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is required. Actual test and gate results are
  implementation evidence, not facts established by this planning critique.

## Limitations

* No rebase, tests, gate, hosted refresh or receipt verification was performed.
* Preservation and implementation correctness remain to be demonstrated by
  the planned execution and independent Review.
* Background project context was read as required; no domain or regulatory
  claim is reassessed and no open-ended research was performed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the receipt-success verification sequence and
  directly disposition PC-001 before implementation; do not commission
  another critique for this supplied boundary.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/rebuild-148-refresh-plan.md](.copilot-tracking/plans/2026-10-30/rebuild-148-refresh-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/rebuild-148-refresh-phase-details.md](.copilot-tracking/details/2026-10-30/rebuild-148-refresh-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-30/rebuild-148-refresh-research.md](.copilot-tracking/research/2026-10-30/rebuild-148-refresh-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/plans/2026-10-30/rebuild-148-refresh-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/rebuild-148-refresh-plan-critique.md) | This independent critique |

## Next Steps

The active planning parent should directly resolve PC-001 and finalize the
plan, retaining this original verdict. No user action, additional critique,
Azure operation or push is required or authorized.
