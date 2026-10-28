---
title: Resident chat safety correction plan critique
description: Original independent final-candidate critique for task 520-safety
ms.date: 2026-10-28
---

## Metadata

* Task ID: 520-safety; issue #520; PR #525.
* Branch: feat/resident-chat-520.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-safety-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-safety-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise. Preserve this original assessment after disposition;
  a planner correction does not retrospectively change it to Pass.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and primary research at
  .copilot-tracking/research/2026-10-28/resident-chat-520-safety-research.md,
  including C1-C7, FR1-FR4, non-functional requirements, AC1-AC6, P01/P02,
  dependencies, test ownership, change budget and publication restrictions.
* Caller requires the exact reports "The carbon monoxide alarm is sounding in my
  home" and "There is smoke coming from a socket in my home" to receive the
  unchanged existing SAFETY response before ordinary routing. Plausible related
  reports must be covered without broad ordinary-query interception.
* Inspected canonical chat.py, the actual _assistant request path,
  test_resident_chat_api.py, and the affected existing browser checker as needed
  to assess feasibility, regression assertions and validation prerequisites.
* Considered supplied repository/project context and the execution prohibition
  on system temporary paths. No new regulatory, customer or external claims.
* This is exactly one independent plan critique, not an implementation review,
  execution of acceptance tests, whole-issue assessment or publication approval.
  Plan, details, research and source remain unchanged.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, FR4; C1, C6 | Covered | chat.py checks existing safety tokens before unknown and ordinary topics. Plan preserves this order and adds bounded whole-word predicates at the same boundary. |
| FR2; AC2, AC3; C6 | Covered | Positive/negative tables cover CO alarms/exposure, smoke, fire, gas, electrical and water/electrics reports, plus ordinary detector, smoking-policy, socket and water questions. Existing fire/gas/damp/mould behavior remains intact. |
| FR3; AC1; C2, C5 | Covered | Existing SAFETY and human source remain unchanged. Request path calls chat.answer for string routes; only Topic enum routes enter optional advisory/model logic. Planned exact HTTP equality and zero advisor/provider-call assertions fit that contract. |
| AC1-AC3; P01-T01, P01-T02 | Covered | Failing baseline, route and HTTP tables, safety precedence over ordinary/untrusted tokens, no own-home details and no appointment action are explicit. |
| P01-T03; C7 | Covered | Both quoted reports extend the existing typed browser journey after consent. Latest-response scoping avoids treating historical own-home answers as fresh hazard-response leakage. README change is directly related. |
| Test ownership and change budget | Covered | No removals; at most three new test methods in the named API file; existing browser harness reused; no new dependencies or production targets. |
| Non-functional requirements; AC4; P02-T01; C3, C7 | Partial | Relevant API discovery, focused tests, Ruff100/format, mypy and actual browser checks are specified, but the explicit lock path and uncontrolled default scratch paths conflict with execution constraints: PC-001. |
| AC5; P02-T02 | Covered | One original independent Review, preservation of adverse outcomes, no internal reimplementation/review loop, and residual follow-up ownership are explicit caller-aligned boundaries. |
| AC6; P02-T03, P02-T04; C4 | Covered | Privacy-safe local commit and original dated evidence are specified. Prohibited az means no full gate invocation, push, remote resolution or publication claim; coordinator handoff retains the exact-head publication gates. |
| Dependencies, decisions and residual risk | Covered | P02 depends on P01; no unresolved routing-authority choice. Finite lexical coverage and inherited human/hosted acceptance limits are disclosed rather than converted to safety guarantees. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.
* Rationale: The bounded routing correction and regression strategy are credible.
  One execution-contract correction is necessary before validation can proceed
  without forbidden file operations. This is a direct planner correction, not
  grounds to expand scope, alter locked acceptance criteria or request another
  critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation paths violate the no-system-temporary-storage constraint

* Related IDs: non-functional requirements; AC4, AC6; P01-T01 baseline execution;
  P02-T01.
* Evidence:
  * .copilot-tracking/details/2026-10-28/resident-chat-520-safety-phase-details.md:61-62
    explicitly requires /tmp/ama-rpi-heavy.lock.
  * src/api/tests/test_resident_chat_api.py:49-51 creates an unspecified-location
    tempfile.TemporaryDirectory for every ChatApiTests fixture.
  * src/api/checks/resident_assistant_browser_check.py:623 defaults browser
    evidence to tempfile.mkdtemp when --out is absent; lines 638-650 also create
    unspecified-location agenda scratch storage and launch Chromium.
  * The supplied execution instructions prohibit /tmp and /var/tmp file
    operations and require newly created scratch files to be project-relative.
    P02-T01 does not establish a compliant scratch environment for these children.
* Concern: Following the written validation procedure necessarily attempts the
  forbidden lock path. Changing that path alone is insufficient: Python
  fixtures and browser runtime scratch remain uncontrolled. Existing evidence
  placement language does not configure tempfile or child-process storage.
* Impact: Required baseline/unit/browser evidence can be blocked or obtained
  through prohibited writes, undermining AC4 and the no-prohibited-operation
  boundary. A private per-worktree replacement lock would also fail to preserve
  shared heavy-check serialization.
* Smallest useful change: Update the validation execution instructions only:
  select a permitted, genuinely shared lock path coordinated with other heavy
  runners; retain flock -n and the single monotonic deadline of at most 2400
  seconds. Do not silently substitute an unshared worktree lock. Establish
  project-relative runtime scratch before the failing baseline or any test,
  export TMPDIR/TMP/TEMP to its absolute permitted location for Python and
  browser children, and pass an explicit compliant --out to the browser checker.
  Confirm the actual runtime honors those paths; if shared locking or browser
  scratch cannot comply, record that specific validation blocker rather than
  using forbidden paths. Preserve existing tests, method budget and all ACs.
* Action owner: Planning parent owns the instruction correction; implementation
  executor owns environment/path verification and evidence recording.
* Exact resolving evidence: Revised plan/details name the permitted shared lock,
  cross-runner coordination and scratch/output setup while retaining flock -n,
  the <=2400-second deadline, and no-system-temporary-writes restriction. The
  changes evidence records the effective scratch environment, a fresh Python
  tempfile.gettempdir() result under the project, browser output/runtime path
  verification, and the real bounded-lock/unit/browser result or explicit
  compliant prerequisite blocker.
* Decision route: Direct planner correction. No significant or divergent user
  decision is required; the path prohibition is already explicit.

## Strengths and Residual Risk

* The plan correctly targets host-owned matching rather than changing advice,
  request schemas, UI, models or operational authority.
* Whole-word bounded report/context combinations and negative regression tables
  address the supplied overmatching concern without making a general hazard
  detection claim. Implementation still needs to demonstrate these assertions.
* Existing fire/gas tokens already route conservatively; the plan preserves them
  rather than silently redefining ordinary behavior outside the correction.
* Actual HTTP and browser checks complement route tables. Provider/advisor
  non-call assertions test the safety authority boundary independently of text.
* The no-az publication blocker is explicitly accepted as a local-only handoff,
  not waived. A local commit is not a gate receipt or permission to push.
* Original Review findings remain visible and are routed to later work as
  directed. No inference of acceptance follows from committing an adverse Review.

## Questions or Blocking Evidence Gaps

* No unresolved user decision. The planning parent must resolve PC-001 before
  executing validation; inability to establish compliant shared/runtime paths
  becomes an explicit validation blocker, not permission to bypass constraints.

## Limitations

* No source modifications, acceptance tests, browser launches, Azure commands or
  remote mutations were performed in this critique.
* Research reproduction, dependency restoration and full-gate blocker statements
  are supplied evidence, not fresh execution results from this critique.
* No live shared-lock configuration or browser scratch compliance was supplied;
  those operational facts must be recorded during the planned execution.
* Assessment is confined to this bounded correction. It does not establish
  complete linguistic coverage, accessibility conformance, regulatory
  currentness, whole-issue acceptance or exact-head publication readiness.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct validation lock/scratch instructions, record a
  direct disposition against PC-001, and continue the caller-authorized
  implementation sequence without a second critique.
* User response required: No.
