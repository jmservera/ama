---
title: PR 423 review corrections independent plan critique
description: One final-candidate assessment of transport corrections and integration evidence
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr423-review-corrections-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/pr423-review-corrections-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and Review; address
  PR #423 comments; integrate main d986c4c4; preserve the score-only remote
  child; obtain actual API unit, Ruff, format, mypy and local Playwright
  evidence; use pip-installed src distributions; respect heavy-command
  serialization, offline boundaries and local-only commits.
* Primary research:
  .copilot-tracking/research/2026-10-30/pr423-review-corrections-research.md,
  including W1-W5, C1-C6, the three research waves and their dispositions.
* Decisions and dependencies: remote child 32cc1f81 before pinned main;
  transport and active guidance corrections before validation; one original
  independent Review before commit; a clean committed candidate before the
  complete gate; hosted scoring and publication remain coordinator-owned.
* Acceptance boundary: FR1-FR4, all non-functional requirements, AC1-AC8 and
  P01-T01 through P02-T03. Historical hosted 77/100 PASS is not a score for
  unpublished corrections.
* Targeted primary-source inspection: infra/scripts/staff_blob.py;
  infra/tests/test_staff_azure.py; current operations in infra/README.md;
  src/api/pyproject.toml and relevant API guide commands; src/README.md local
  gate contract; .github/rubric/README.md scorecard contract; the gate
  runner's lock and external-output references.
* Required project context: original case study, addendum, knowledge-base
  index and owner memory were consulted. They do not establish live transport
  or deployment acceptance.
* Read-only git inspection confirmed branch
  docs/demo-transport-plan-360-fix at bda7975f. The supplied plan, details,
  research and workflow-state files are currently untracked parent artifacts;
  they were not treated as unrelated work or changed by this assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, AC1, W1, C1/C2, P01-T02 | Covered | Explicit offset and MAX_BLOB + 1 range, pre-decode refusal, slicing fake, range capture and controller cleanup address the replacement-allocation defect. |
| FR2, AC2, W2, C1/C2, P01-T02 | Covered | Exact compact serialization, complete wrappers, comma accounting, initial head retention, final validation and page-count refusal address intermediate-page overflow without truncation. |
| FR3, AC3, W3, C3, P01-T03 | Covered | Active tag prerequisites and cleanup are separated from dated receipts; private Blob routing, default-off writer approval and retained ciphertext are explicit. |
| FR4, AC3, W4, P01-T03/P02-T03 | Partial | Historical run9 is correctly qualified, but the final handoff has no explicit post-gate evidence boundary; PC-002. |
| AC4, C4, P01-T01 | Covered | Remote-child-first integration, pinned main, retained KB additions and trusted baseline, ancestry/content verification and no history rewrite are specified. |
| AC5, C6, P02-T01 | Partial | Requested checks and existing synthetic browser ownership are covered; install-first verification can be bypassed by source imports; PC-001. |
| AC6, P02-T02 | Covered | One critique and one independent original Review, with adverse outcomes retained and later findings routed rather than erased. |
| AC7, C5, P02-T03 | Partial | Clean committed full gate, external receipt and changed-base refusal are specified; the subsequent evidence handoff needs an explicit immutable-candidate procedure; PC-002. |
| AC8, W5, C5 | Covered with external dependency | Existing 77 PASS is historical; a fresh hosted result for the final published candidate remains unavailable locally and must remain unmet here. |
| Non-functional and safety boundaries | Covered | No cloud operations, deployment, actual sign-in, model use, secret access, remote writes or altered scoring contracts are authorized. Existing deadlines, cleanup and DN1-DN5 are retained. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 2; Low 0.
* Rationale: The proposed transport algorithm and ancestry strategy are
  credible. Two directly actionable validation/evidence sequencing gaps
  should be made explicit before implementation. Neither requires new
  research, changed scope or a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Verify installed distributions before source-assisted checks

* Related IDs: AC5; non-functional package-layout requirement; C6; P02-T01.
* Evidence:
  .copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md:67-79
  runs API discovery with the three application source directories on
  PYTHONPATH, then permits pip restoration after actual import/tool failures.
  It explicitly requires installed src packages for infra discovery, but
  does not establish that prerequisite before the earlier API/browser
  checks. The repository instructions require distribution installation
  before application or infrastructure scripts; infra/README.md documents
  the editable src distribution installation.
* Concern: Source-assisted imports can succeed when a required distribution
  is absent, so missing-import detection alone cannot establish the
  install-first requirement. This finding does not object to the requested
  API discovery command itself.
* Impact: AC5 could be reported as pip/src validation even though the direct
  checks ran only through source-path imports. The later isolated full gate
  would not retroactively establish the environment used by those earlier
  commands.
* Smallest useful change: Add a lightweight distribution/interpreter
  preflight before P02-T01. Verify the required local src distributions and
  dev dependencies belong to the selected task environment. Restore through
  pip only after an actual missing-dependency result, then rerun the
  preflight before the requested commands. Preserve the requested discovery
  command and existing dependency pins.
* Action owner: Planning parent; implementation owner executes the preflight.
* Exact resolving evidence: Revised P02-T01 specifying the preflight order,
  followed during execution by the selected interpreter identity and
  installed-distribution metadata/editable-project paths for required
  packages, any actual missing-dependency result and pip restoration log,
  and the subsequent API/static/browser command exits from that environment.
* Decision route: Direct planner correction; no user decision needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Separate committed handoff text from final external gate status

* Related IDs: FR4; AC3; AC6/AC7; W4; C5; P01-T03; P02-T02/P02-T03.
* Evidence:
  .copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md:58-59
  prepares a body describing current candidate/gate status;
  lines 89-102 reconcile evidence, perform the original Review, commit all
  dated evidence and only then run the complete gate. The plan's AC3 expects
  a coordinator-ready body. src/README.md requires the authoritative receipt
  outside git and invalidates it after another commit or dirty candidate
  input.
* Concern: The plan does not say where the final successful or adverse
  outcome and its exact candidate binding are handed off after the gate.
  Updating the committed proposed body or changes record afterward would
  invalidate a successful clean-candidate receipt; leaving the earlier body
  untouched without an external supplement could send the coordinator stale
  gate status. This is the same evidence-currentness risk that W4 asks this
  workstream to address.
* Impact: A valid gate could be invalidated while reporting it, or a proposed
  PR description could again misidentify earlier evidence as current.
  Pre-commit Review evidence also must not be relabelled as a post-gate
  exact-head assessment.
* Smallest useful change: Specify two explicit outputs: committed proposed
  body/changes evidence with an as-of status and final gate still pending,
  and a task-owned external final handoff after gate execution and receipt
  verification. Bind the external handoff to full HEAD/tree/base values,
  receipt/log paths and actual status. Do not edit the committed candidate
  after a successful gate. If any tracked correction is necessary, make a
  new local commit and a fresh gate attempt. Name the coordinator as owner
  of later exact-head publication assessment and hosted scoring without
  repeating this task's original Review.
* Action owner: Planning parent; implementation owner produces the external
  handoff; coordinator owns later publication assessment.
* Exact resolving evidence: Revised P01-T03/P02-T03 defining the committed
  as-of text and external handoff destination; during execution, a final
  external handoff with full commit/base identifiers, receipt verification
  outcome or preserved failure paths, unchanged clean git state after the
  successful gate, and explicit remaining coordinator gates.
* Decision route: Direct planner correction; no user decision needed.

## Strengths and Residual Risk

* The range limit is applied before readall rather than merely checking the
  downloaded length afterward. The fake must model the range, not swallow
  arbitrary keyword arguments.
* Exact serialized-page measurement addresses oversized first/intermediate
  pages and wrapper overhead. Empty-head retention, item ordering,
  measured totals and many-page round trips protect existing semantics.
* The remote score child and main integration are ordered to preserve
  ancestry; score preservation is not confused with new scoring evidence.
* Current runbook corrections do not authorize deployment or rewrite
  historical activation/gate records.
* Shared-lock admission, missing browser/SQL/scanner prerequisites and a
  moved base can still block the complete gate. The plan correctly rejects
  bypasses and fabricated success.
* Fake-client and synthetic browser checks cannot establish actual SDK
  service behavior, private routing, IAM activation, live job behavior,
  accessibility acceptance or a fresh hosted score. Those boundaries remain
  explicit and acceptable for this local-only workstream.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required.
* No additional research is needed for the two findings. Actual dependency,
  test and full-gate outcomes remain execution evidence, not assumed facts.

## Limitations

* This critique inspected only supplied materials and directly relevant
  source. It did not retrieve PR threads again or independently refresh
  remote ancestry/score evidence; those facts are attributed to the supplied
  research.
* No tests, builds, dependency installation, heavy commands, merges,
  commits, cloud operations or remote writes were performed.
* No further agents were invoked. Plan, phase details, research, source and
  parent workflow-state files were not edited.
* The assessment is a plan credibility judgement, not implementation
  verification or publication authorization.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: Planning parent.
* Smallest next action: Define the external final evidence handoff and
  install-first preflight in the existing plan/details, disposition both
  findings and finalize planning without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/pr423-review-corrections-plan.md](.copilot-tracking/plans/2026-10-30/pr423-review-corrections-plan.md) | Assessed plan |
| [.copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md](.copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-30/pr423-review-corrections-research.md](.copilot-tracking/research/2026-10-30/pr423-review-corrections-research.md) | Primary research |
| [.copilot-tracking/reviews/plans/2026-10-30/pr423-review-corrections-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/pr423-review-corrections-plan-critique.md) | This independent critique |

## Next Steps

The active planning parent should apply the two direct corrections, retain
this original verdict and continue the ordered RPI work after recording
dispositions. No user action or second critique is required. This critique
stops here.
