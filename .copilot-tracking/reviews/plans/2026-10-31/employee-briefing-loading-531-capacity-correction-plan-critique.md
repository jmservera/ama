---
title: Independent plan critique - Employee briefing validation capacity correction
description: Single final-candidate assessment of bounded assurance recovery and publication
ms.date: 2026-10-31
---

## Metadata

* Task ID: 531 / employee-briefing-loading-531-capacity-correction
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-capacity-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-briefing-loading-531-capacity-correction-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate independent critique.
* Observed HEAD: 18c1531f77730d935aa66a90ceec3594e41cb855
* Observed origin/main: 1330869ea675ff019958846330108b4f45e163ce
* Write boundary: This critique artifact only.

## Inputs and Criterion Boundary

* Current caller permission is authoritative: authorized main merge, 1800-second heavy-lock wait with one capacity-timeout retry, unlocked API/Ruff, local Playwright/axe, full gated publication, pip only, no secrets/cloud Azure actions/force push.
* Read the correction plan, phase details and research; original employee-briefing-loading-531 changes, plan critique and Review; src/README.md local gate contract; src/api/README.md loading/briefing guide; src/api/pyproject.toml; the existing loading runner and its owned-server lifecycle; relevant tools/rpi-checks.py browser bootstrap, environment, locking and verification implementation.
* Read repository context in docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md, and the tracking retention policy. Memory is context, not proof.
* Read-only Git inspection confirms the supplied main SHA is an ancestor of HEAD. The committed task diff contains the existing runner/guide and original task evidence. Gate tool, src-ci workflow and rubric have no difference from the supplied main base.
* Scope is validation correction, not another design or implementation workstream. Preserve every existing scenario, no removals or planned new scenario functions, draft-only authority, separate manager export observation, and permitted case-projection invariance.
* Original RV-001 execution and ancestry blockers are the recovery targets. RV-002 specialist note, RV-003/live AC7 and human/AT/full Fluent acceptance are explicitly outside this correction. PR wording remains Refs #531.
* Assessment evaluates planning credibility, not completed validation or publication. No test, browser, scanner, SQL, live request, receipt verification, commit or nested agent was executed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Current user direction and bounded change budget | Covered | Same active topic; authorized merge; no runtime redesign, scenario replacement or authority change. |
| C1 / original RV-001 / P01-T02 | Covered | Fresh complete API discovery and existing pinned-axe loading runner are required; historical lint or timeouts cannot substitute. |
| C3 / three review outcomes / P01-T02 | Covered | Existing successful_review_check executes real UI/API actions, manager export, same-ID immutable refusal and permitted projection equality. |
| C4 / P01-T01 | Covered | Supplied main is an ancestor; gate tool/workflow/rubric match it. Preservation of both log histories is recorded as merge evidence, not newly reconstructed here. |
| C5 / heavy capacity / P01-T02 and P02-T02 | Covered | Standalone flock exit 75 distinguishes acquisition timeout; full gate uses internal --lock-timeout 1800 and actual timeout diagnostic. One retry only; no nested lock or unlocked heavy fallback. |
| C6 / external outputs and clean candidate / P01-T02 | Partial | Outer bytecode disabling and optional scratch relocation do not cover the actual server-child environment and default scratch lifecycle; PC-001. |
| P01-T03 / original correction Review | Covered | Fresh branch-diff assessment is distinct from the preserved original adverse parent Review and later exact-head assessment. |
| P02-T01 / identity and evidence commit | Covered | Authenticated privacy-safe local identity, matching author/committer, explicit staging, original evidence and requested Copilot trailer. |
| P02-T02 / full publication gate | Covered | Clean committed candidate, full scope, current-main base, internal lock, new external outputs, fail-closed prerequisites and receipt verification precede exact-head assessment. |
| P02-T03 / publication | Covered | Non-force push, main PR, external publication record, Refs #531, hosted checks and owner merge boundary. |
| RV-002 / RV-003 / live AC7 | Covered as exclusions | Explicitly unproved and outside scope; not blocking decisions to reopen in this critique. |

## Verdict

* Verdict: Revise
* Rationale: The validation and publication sequence is credible, but one directly correctable execution detail can recreate the already observed ignored-input preflight failure. Resolve it before assurance execution; no divergent scope decision or further critique is needed.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Complete assessment does not establish passing runtime evidence or publication readiness.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Outer bytecode disabling does not protect the owned server child or default scratch

* Related IDs: C6; non-functional external-output/bytecode requirements; P01-T02; clean-candidate prerequisite for P02-T02.
* Evidence: .copilot-tracking/details/2026-10-31/employee-briefing-loading-531-capacity-correction-phase-details.md, P01-T02, requires PYTHONDONTWRITEBYTECODE=1 but makes the external TemporaryDirectory hook conditional. src/api/checks/loading_briefing_browser_check.py:929 invokes the imported design-system main. src/api/checks/design_system_browser_check.py:233-238 explicitly creates scratch under ROOT/.venv and writes synthetic.json. At lines 244-268 it constructs the child environment from only PATH/HOME/LANG, adds source PYTHONPATH and fixture settings, and launches sys.executable without -B. Consequently, the outer bytecode variable is not forwarded to that server. tools/rpi-checks.py:123-132 demonstrates an existing external TemporaryDirectory bootstrap but that patch alone does not change the child environment. The original changes record documents a real ignored-input gate rejection; tools/rpi-checks.py:168-169 refuses ignored inputs.
* Concern: A literal standalone invocation, even with the named outer variable and external --out, does not guarantee the plan's external-only generated output or disabled bytecode contract. Without the hook, fixture/log storage remains repository-local. With only the hook, the server child can still create source-adjacent __pycache__ files. This is an execution-contract gap, not evidence that a new run has already produced those files.
* Impact: Required browser assurance can contaminate the candidate checkout and make the subsequent full-gate preflight fail again. Repeated capacity waits do not resolve this failure. Silent deletion or changing the shared lock is not an acceptable remedy.
* Smallest useful change: Make the standalone execution bootstrap concrete and mandatory: relocate the actual TemporaryDirectory despite its explicit dir argument, and explicitly disable or externally redirect bytecode for the owned server subprocess as well as the launcher. Prefer a parent-owned external execution wrapper using the existing bootstrap pattern and narrowly scoped owned-subprocess configuration; no new production helper or scenario is required. Inventory candidate ignored inputs after execution and before staging/gating. If relocation is needed, use a finite authorized archive/restore-backed selection rather than automatic cleanup.
* Action owner: Planning parent, then the P01-T02 validation executor.
* Exact resolving evidence: Revised P01-T02 identifies the actual bootstrap/invocation and shows how the owned server receives -B, PYTHONDONTWRITEBYTECODE=1 or an external bytecode destination despite the environment whitelist. Retained execution evidence identifies external fixture/log/output locations, actual browser exit/results and the post-execution ignored-input inventory. Empty ignored-input output before P02-T02 proves the clean-input prerequisite; successful browser execution remains separately required.
* Decision route: Compatible parent direct disposition. Current user permission and the existing bounded correction budget already authorize resolving validation setup. No unresolved divergent user decision, alternate lock, new scenario, source redesign or worker-context storage prohibition is asserted.

## Strengths and Residual Risk

* Main integration fixes the evidenced ancestry preflight blocker without force, rebase or gate-hash weakening. Main's rubric/tool/workflow identities are retained.
* The gate really self-locks; the proposed internal 1800-second wait avoids the original critique's nested-lock risk. API/Ruff remain unlocked under current user direction.
* Same-ID export evidence now matches the existing supported runner rather than the earlier aggregate-report proposal. It proves only the stated retained record and permitted projections, not full raw-store or export continuity acceptance.
* Existing Ruff configuration exempts checks from many rules and default formatting discovery. The explicit changed-runner checks in P01-T02 should retain their actual selection/results without overriding inherited style exemptions or overstating coverage.
* Fetch current main again before the post-gate assessment and immediately before push verification, as required by src/README.md:215-217 and the details' fresh-current-base requirement. If it moves, the authorized merge and invalidated evidence must be reconciled and rerun; an unchanged local remote-tracking ref is not a fresh remote observation.
* Lock availability, required local SQL/browser/scanner prerequisites and hosted approvals remain execution risks, not reasons to fabricate passes or use cloud fallbacks.
* RV-002, live AC7 and human/AT/full Fluent acceptance remain explicitly unproved. A passing correction cannot close whole issue 531.
* Keep original adverse critique/Review outcomes immutable. The correction Review and external exact-head assessment do not retroactively turn the parent's Review into acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved divergent user decision.
* PC-001 requires direct execution-detail correction; no new research or user response is required.
* Runtime results, final clean commit, full receipt, current-base verification, independent exact-head assessment and remote publication are future completion evidence, not supplied successes.

## Limitations

* No fresh UI/accessibility audit or conformance assessment was performed. Relevant runner/source contracts were read for planning only.
* Git inspection establishes the locally recorded exact main ancestry and matching tool/workflow/rubric diff, not a new remote fetch or exhaustive independent reconstruction of both log histories.
* Existing parent-owned authorization is respected. This critique does not revive the previous rejected worker-level prohibition on parent execution paths.
* Only this requested artifact was written. Existing dirty/untracked parent artifacts were left intact.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly disposition the owned-server bytecode and mandatory external-scratch invocation in P01-T02, then finalize without a second critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-capacity-correction-plan.md](.copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-capacity-correction-plan.md) | Assessed correction plan |
| [.copilot-tracking/details/2026-10-31/employee-briefing-loading-531-capacity-correction-phase-details.md](.copilot-tracking/details/2026-10-31/employee-briefing-loading-531-capacity-correction-phase-details.md) | Assessed execution and publication details |
| [.copilot-tracking/research/2026-10-31/employee-briefing-loading-531-capacity-correction-research.md](.copilot-tracking/research/2026-10-31/employee-briefing-loading-531-capacity-correction-research.md) | Supplied recovery research |
| [.copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-changes.md](.copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-changes.md) | Preserved execution and preflight failures |
| [.copilot-tracking/reviews/logs/2026-10-31/employee-briefing-loading-531-review.md](.copilot-tracking/reviews/logs/2026-10-31/employee-briefing-loading-531-review.md) | Preserved original adverse Review |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-plan-critique.md) | Preserved prior critique and disposition context |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-capacity-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-capacity-correction-plan-critique.md) | This complete single critique |

## Next Steps

The active planning parent should directly disposition PC-001 and finalize the correction without another critique. Then continue authorized validation, the original correction Review, commit and full current-base exact-head publication gates. No user command or response is required. This critique stops here.
