---
title: Employee single case view plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 552
* Task slug: employee-single-case-view-552
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-single-case-view-552-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-single-case-view-552-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique.
* Original verdict: Revise. Preserve this verdict after direct corrections; no second critique is required.

## Inputs and Criterion Boundary

* Caller requirements: ordered RPI for issue #552, branch feat/employee-single-case-view-552 from supplied base 721ba973, local commit only with Refs #552 and Copilot trailer. No push, Azure, deployment, live sign-in, credentials, secrets, source edits by this critic, nested agents or further critique/Review.
* Supplied research: .copilot-tracking/research/2026-10-30/employee-single-case-view-552-research.md, including Q1-Q3, C1-C7, W1-W2 and the decision to preserve the implementation already delivered through merged PR #554.
* Primary assessment: the supplied plan and phase details, both dated 2026-10-30.
* Supporting source inspection: src/api/checks/case_view_ux_browser_check.py; src/api/checks/case_journey_browser_check.py, especially scan; src/api/checks/regulatory_ux_check.py, especially AXE_SHA256; src/api/src/zava_forward/api/web/case-workspace.js; src/api/tests/test_case_journey.py; src/api/README.md; src/README.md; tools/rpi-checks.py.
* Historical outcome inspected: .copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md. Its Partial execution, Residual work outcome and RV-001 remain unchanged.
* Repository context read: docs/case_study_48_original.md, relevant opening context in docs/case_study_48_addendum.md and docs/reference/README.md, and docs/reference/memory.md. Memory is context, not evidence.
* Criterion boundary: all six supplied acceptance criteria; phase/task feasibility; locked ownership and zero-new-unit-method budget; browser evidence integrity; dependency and safety constraints; Review/local-commit/full-gate sequencing.
* Decisions already resolved by current direction: no gratuitous runtime rewrite; use the existing dedicated browser script and canonical pinned axe only; no Azure even for a nominally offline command. These are not unresolved user choices.
* This is planning credibility assessment, not implementation execution, an accessibility audit, a new runtime review, rendered acceptance or a publication approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1/C1-C4; acceptance 1 | Covered | Runtime declares six named icon/label pairs; existing unit regressions check the expected names, icon order, package data and byte-exact presentation assets. Dedicated browser check verifies loaded decorative images and records rendered labels. Fresh screenshots remain required. |
| C2/C5; acceptance 2 | Covered | Existing actual-browser geometry and unchanged <=132px/<=116px ceilings are retained. Historical baseline is explicitly distinguished from a new before/after claim. |
| C1/C4/C5; acceptance 3 | Covered | Existing checks retain native keyboard activation/dismissal/focus return, touch scrolling to final action, missing-field recovery, viewport bounds and 200% root text. Unit evidence retains complete safe disclosure text. |
| C2/C3/C5; acceptance 4; P01-T01 | Covered | Proposed responsive loop explicitly measures shared-surface/scroll ancestry and actual panel scrolling with stationary tabs at 1280/390/320px; retains field state and keyboard operation. |
| C6; acceptance 5; P01-T01 | Covered | Canonical hash verification before app startup; reused scan routine; explicit rejection of every recorded violation, not just the reused routine's serious/critical threshold; retained incomplete results and failure JSON. No comprehensive conformance claim. |
| C7; acceptance 6; P02-T01/P02-T02 | Partial | Fresh desktop/narrow raw JSON and images plus independent inspection are correctly required. Artifact/tool/lock locations must first be reconciled with the active file-operation restriction, PC-001. |
| Locked test ownership/budget | Covered | Existing dedicated real-server script only; no removed checks, new unit methods, dependencies, scanner or replacement fixture app. Baseline-only capture stays optional-axe without weakening normal verification. |
| P02-T01; prerequisites and heavy checks | Partial | Full discovery, exact requested PYTHONPATH, Ruff check/format and mypy are specified, but the stated /tmp tooling and lock cannot be used in this environment, PC-001. |
| P02-T02; no-Azure/full gate | Covered with known blocker | The plan correctly rejects prohibited Azure CLI execution. Direct source inspection confirms the full runner invokes az and uses a forbidden lock location. Record the blocked gate without executing it; never substitute focused results for a complete receipt. |
| P02-T02; original evidence, Review and local persistence | Covered | One independent Review precedes local commit; privacy-safe local identity, Refs #552 and trailer are required. No push, no rewritten historical outcomes and no second Review are planned. Record blockers and the actual Review disposition before committing. |
| Residual risks/follow-ups | Covered | Full Fluent adoption, cross-browser/AT/human acceptance and hosted approval remain outside this bounded engineering evidence and are not represented as delivered. |

## Verdict

* Verdict: Revise.
* Rationale: the technical scope and semantic validation design are credible, and no new runtime rewrite is justified by the supplied evidence. One concrete execution-safety conflict needs direct correction before P02 can proceed. The no-Azure/full-gate conflict is already conservatively resolved in principle; source inspection now supplies a concrete blocker rather than a speculative prerequisite.
* Severity counts: Critical 0; High 1; Medium 0; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned validation paths violate the active file-operation boundary

* Related IDs: C5-C7; acceptance 6; P02-T01; P02-T02; plan Dependencies.
* Evidence: .copilot-tracking/details/2026-10-30/employee-single-case-view-552-phase-details.md, P02-T01, directs PATH=/tmp/mv/bin:$PATH and flock against a /tmp lock. The plan repeats those dependencies and requires fresh external browser output without naming a reviewer-readable permitted location. The active execution constraints prohibit all file operations under /tmp, including reads and execution of files there. Historical .copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md, RV-001, shows that precisely this location restriction already prevented independent raw evidence inspection. tools/rpi-checks.py, heavy_lock, opens its canonical lock in /tmp; its preflight invokes az bicep version and its infrastructure checks invoke az bicep build/lint.
* Concern: the parent cannot execute the planned /tmp interpreter/lock instructions safely. An unspecified external evidence location risks reproducing the original inaccessible-evidence outcome. The complete runner must not be launched merely to discover a conflict already established by source.
* Impact: required checks may remain unperformed, or evidence may again be unavailable to the independent reviewer. Executing these instructions would violate the active safety boundary; replacing the canonical lock or weakening the complete gate would not resolve it.
* Smallest useful change: revise P02-T01 and the dependencies to use only an existing permitted interpreter/tool environment and a concrete permitted, project-relative generated-evidence location readable by both parent and reviewer. Check availability without touching /tmp; install dependencies only after a genuine missing-dependency failure and within the applicable pip policy. Preserve the required shared-lock contract: if it cannot be acquired within the active restrictions, explicitly mark the affected heavy checks blocked rather than run unlocked or invent a substitute lock. In P02-T02, persist the concrete full-gate blockers before the local commit: forbidden canonical lock access and prohibited az invocation. Do not execute or patch the runner, access historical /tmp evidence, relocate it without authority, fabricate a receipt or claim a full pass. Preserve generated-output retention rules and do not stage generated browser assets as implementation.
* Action owner: planning parent, carrying the corrected operational instructions into implementation and reviewer handoff.
* Exact resolving evidence: plan/details name permitted tool and evidence paths or explicit unavailable-tool outcomes; the changes record and reviewer handoff identify the same accessible fresh JSON/PNG directory; commands/outcomes distinguish executed checks from lock/tool-blocked checks; the complete gate is recorded as not executed with the inspected heavy_lock/preflight/infrastructure reasons. If shared-lock acquisition remains impossible, the affected validation stays blocked and acceptance remains qualified.
* Decision route: direct planner correction. No user response is required to obey existing restrictions and report a blocker. A future relaxation of restrictions would be a separate authorization request, not part of this critique or a prerequisite for an honest local-only blocked closeout.

## Strengths and Residual Risk

* Preserving the merged implementation avoids unnecessary production risk and duplicate work.
* The scan helper appends full violations and incomplete results before asserting its severity threshold. The plan correctly adds an all-violations assertion and failure serialization in the owning script; reuse alone would not satisfy that requirement.
* The responsive scroll design uses focus and actual keyboard scrolling, not an imperative scrollTop assignment or a source-string proxy.
* Existing fallback, touch, keyboard, enlarged-text and reduced-motion behavior remains in scope; no regression suppression or new unit methods are planned.
* Current rendered evidence may establish this candidate's local geometry and interactions, but cannot retroactively turn the original Partial Review into a pass.
* Normal verification must fail on missing/unverified axe; optional baseline capture is not equivalent acceptance evidence.
* Full-gate, hosted, human, AT and cross-browser limitations remain explicit. A local commit is persistence, not permission to publish or declare issue-wide acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved significant/divergent user decision was identified.
* P02 execution needs the direct path/lock reconciliation in PC-001. If the required shared lock remains forbidden, preserve the resulting blocked validation rather than requesting or inferring a bypass.
* The complete gate has concrete safety blockers under current direction. No Azure command, alternate gate or permission change is recommended.

## Limitations

* No application, tests, browser, scanner, gate, live sign-in or Azure command was run in this critique.
* No current or historical rendered artifacts were inspected. Their future availability and measured results are validation outcomes, not planning facts.
* Merged-PR/base provenance and the source style/app integration described by C2/C3 are assessed from supplied research and the historical Review, not a new independent history or complete runtime audit.
* No external research or fresh Web Interface Guidelines retrieval was performed; this is a plan critique, not the later required scoped web review.
* Existing untracked parent RPI inputs were left untouched. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly reconcile tool/evidence paths and lock-blocked execution in plan/details, record the known full-gate blockers, and finalize critique dispositions without another critique.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/employee-single-case-view-552-research.md](.copilot-tracking/research/2026-10-30/employee-single-case-view-552-research.md) | Supplied research and no-runtime-rewrite decision |
| [.copilot-tracking/plans/2026-10-30/employee-single-case-view-552-plan.md](.copilot-tracking/plans/2026-10-30/employee-single-case-view-552-plan.md) | Final-candidate plan requiring direct correction |
| [.copilot-tracking/details/2026-10-30/employee-single-case-view-552-phase-details.md](.copilot-tracking/details/2026-10-30/employee-single-case-view-552-phase-details.md) | Phase execution and evidence instructions |
| [.copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md](.copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md) | Preserved historical Partial Review and RV-001 |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-single-case-view-552-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-single-case-view-552-plan-critique.md) | This single critique and original Revise verdict |

## Next Steps

The active planning parent should resolve PC-001 directly, preserve this original
Complete / Revise outcome, finalize the plan and continue the already-authorized
ordered RPI sequence only within safe execution boundaries. Record blocked checks
honestly and return the resulting limitations to the one later independent Review.
No new critique, RPI loop, user response, push or Azure operation is required.
