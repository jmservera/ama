---
title: "RPI Plan Critique: Chromium pathname admission"
description: Independent final-candidate assessment for issue 608
ms.date: 2026-10-31
ms.topic: reference
---

## Metadata

* Task ID: 608
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements authorize early rejection or independently owned short
  scratch. The candidate chooses rejection, which needs no further user decision.
* Supplied research:
  .copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md,
  evidence C1-C6 and W1-W3.
* Inspected implementation context: tools/rpi-checks.py, tools/test_rpi_checks.py
  and src/README.md. Required project specification, knowledge-base index and
  memory were read for context; none supplies additional technical acceptance.
* Assessed all stated requirements, acceptance criteria, P01/P02 and
  P01-T01/P01-T02/P02-T01, dependencies, decisions, test ownership and risks.
* Boundary: Linux filesystem-encoded pathname admission for selections containing
  browser; 107 socket bytes, 45 suffix bytes, 62 TMPDIR bytes and 58 resolved
  output bytes; CLI and Runner admission before writes; preserved ownership,
  privacy, cleanup, receipts and source checks.
* Validation authorization is focused tooling unittest and Ruff only. At most six
  added test methods outside installable packages, with no test removals.
  No heavy full gate, scanner/workflow changes, browser/SQL skips or publication
  is authorized here. Issue criterion 3 remains unproven; use Refs #608.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Functional byte bound; C2, W1-W3; P01-T01 | Covered | The supplied suffix and Linux capacity support 107 - 45 = 62, then 62 - 4 = 58. os.fsencode avoids character-count admission. |
| Selection-aware CLI ordering; C1, C4; P01-T01 | Partial | Normal all/changed selection can precede tool_identity, but resume validation itself probes tools before returning selection. PC-001. |
| Runner before owned writes; C2; P01-T01 | Covered | Constructor establishes selection before folder creation, providing the proposed shared-helper insertion point. |
| Output/source/ownership/privacy/cleanup/receipt preservation; C1-C4 | Covered | Candidate retains resolved new external output checks, owned output/tmp, existing verification and receipt schema. PC-001 requires preserving these while correcting resume ordering. |
| 58/59, approximately 130 bytes, Unicode and symlink acceptance; P01-T02 | Covered | Explicit boundary and no-side-effect cases, including an actual AF_UNIX bind, are planned. |
| No-probe regression coverage; C5; P01-T02 | Partial | Listed CLI assertions do not identify the nested resume-validation probe path. Add resume subcases within the existing six-method budget as part of PC-001. |
| Browser-free long paths; P01-T01/P01-T02 | Covered | Admission is explicitly conditional on browser membership, not blanket output length. |
| Focused validation and unchanged existing tests; P02-T01 | Covered | Existing tooling suite and Ruff check/format are selected; exact commands/counts/exits are required. |
| Independent critique/Review dependencies; P01/P02 | Covered | One critique precedes implementation and independent Review follows focused validation. No approval claim is authorized. |
| Criterion 3 and issue linkage; C6; follow-up/handoff | Covered within boundary | Actual full browser/SQL evidence is explicitly deferred, not inferred from focused results; Refs #608 is required. |

## Verdict

* Verdict: Revise
* Rationale: The bounded rejection design is credible, but the specified resume
  ordering cannot establish the promised rejection before tool probes. Correct
  that one implementation-planning gap before finalization.
* Severity counts: Critical 0; High 1; Medium 0; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resume validation probes tools before the planned admission

* Related IDs: Functional Requirements (trustworthy selection before tool_identity);
  Non-Functional Requirements (no side effects on rejection); acceptance criteria
  (reject before probes/lock/Runner/verify); C1, C4, C5; P01-T01 and P01-T02.
* Evidence: tools/rpi-checks.py:2414-2421 calls validate_receipt for resume before
  assigning selected. tools/rpi-checks.py:2232-2239 recomputes and checks selection
  and source identity, then calls tool_identity. tools/rpi-checks.py:194-205 shows
  that tool_identity invokes docker version; later validation also inspects
  Docker images at tools/rpi-checks.py:2303-2319. The phase details explicitly
  place admission after resume selection resolution while only moving main's
  separate tool_identity call.
* Concern: Moving main's top-level probe after admission does not move the probe
  inside validate_receipt. A resume request with an impossible output can still
  invoke Docker or fail on a missing tool before receiving the actionable
  pathname diagnostic. Mocking validate_receipt to return a selection would hide
  the ordering defect.
* Impact: The early, selection-aware no-probe contract is not met for an explicitly
  supported CLI mode, despite no new output directory being created.
* Smallest useful change: Specify resume admission at the existing validated,
  recomputed selection checkpoint before validate_receipt's first tool probe.
  For example, allow a resume-only admission callback after existing receipt
  integrity/schema/selection/source checks and before tool_identity; main supplies
  the output-path helper. Keep the remainder of receipt validation mandatory
  before mkdir/lock/Runner, and leave standalone receipt verification unchanged.
  Do not admit execution based on unchecked parent JSON or skip validation.
* Action owner: Planning parent, followed by the tooling implementer.
* Exact resolving evidence: Revised P01-T01 details identify the concrete
  pre-tool checkpoint and preserve all existing receipt validation on admitted
  paths. Revised P01-T02 includes resume regression subcases using the real
  validate_receipt path and fixture receipt: overlong browser selection returns
  the pathname error without calling tool_identity, Docker subprocess probes,
  heavy_lock, Runner or final verify, and leaves no new output/receipt; admitted
  resume paths still perform ordinary tool/receipt checks and reject tampering.
  Include these as subcases within at most six added methods, retain all existing
  tests, and record focused unittest/Ruff results after implementation.
* Decision route: Direct planner correction. The caller already requires early
  admission and unchanged receipt semantics; no significant or divergent user
  decision is needed.

## Strengths and Residual Risk

* Rejection is explicitly authorized and avoids a new allocation/cleanup lifecycle
  or environment identity change.
* The byte formula is derived, selection-aware and testable with a real Unix
  socket rather than only self-confirming constants.
* Source/existing-output admission and the Runner backstop are retained rather
  than replacing ownership safeguards with a pathname check.
* Chromium naming/version drift is disclosed in supplied research. The supported
  bound is not a guarantee against every future Chromium implementation.
* Focused tests cannot establish actual browser/SQL execution, issue criterion 3,
  hosted approval or a full receipt. This residual boundary is explicitly accepted.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical missing evidence blocks this assessment.
  PC-001 is a source-backed planning correction.

## Limitations

* This assesses the candidate plan, not implemented correctness or runtime
  acceptance. No unittest, Ruff, browser, SQL or full-gate command was run.
* External Chromium/Linux claims were assessed from supplied W1-W3 research;
  no new external retrieval or independent reproduction was performed.
* No implementation, plan, details, research or state file was modified. Existing
  untracked inputs were left intact. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise resume admission and regression details in P01-T01
  and P01-T02, record disposition and finalize without another critique.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md](.copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md](.copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md) | Supplied technical evidence |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-path-608-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-path-608-plan-critique.md) | Complete independent critique |

## Next Steps

No user action is required. Return Revise to the active planning parent for the
direct PC-001 correction and finalization without another critique. This critic
stops here; it does not implement, update state, execute the full gate or publish.
