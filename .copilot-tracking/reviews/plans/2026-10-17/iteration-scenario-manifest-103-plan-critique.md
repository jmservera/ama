<!-- markdownlint-disable-file -->
# RPI Plan Critique: iteration-scenario-manifest-103

## Metadata

* Task ID: #103
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/iteration-scenario-manifest-103-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/iteration-scenario-manifest-103-phase-details.md
* Critique execution status: Complete
* Critique count: Exactly one final-candidate assessment.

## Inputs and Criterion Boundary

* The two acceptance criteria are exhaustive: a versioned manifest lists every approved profile and workflow as represented, unavailable or deferred; data stays constructed and non-identifying.
* Directly read the plan, phase details and supplied research at .copilot-tracking/research/2026-10-17/iteration-scenario-manifest-103-research.md, including C1-C5 and the recorded Programme Manager review.
* Checked the cited public repository sources: PRD FR-035 and its profile/slice contracts, BRD CON-007, current scenario and IA manifests, existing inventory regression, public fixture recipe, needs inventory, provenance register, chat PERSPECTIVES and existing evaluation registry.
* Read #103 and closed #174 through GitHub on 2026-10-17. #103 has precisely the two stated criteria and no dependencies; #100 is hierarchy only. #174 is registry/scale prior art, not a dependency or authorization to regenerate data.
* Current user direction resolves the scope: all twenty full journeys are unavailable; existing partial IA evidence remains separately identified. No new registry, dataset universe, scale generation, private/support reads, real stock, application changes or fixture-recipe changes.
* The manager review is already executed and recorded in research. It is a role-informed research recommendation, not inventory-owner, legal, resident or operational approval. No second manager review was performed.
* This assessment determines planning credibility, not whether unimplemented validation, privacy guarantees or application journeys have passed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #103 acceptance criterion 1 | Covered | Plan requires exact canonical eleven profile and nine workflow IDs, versioned existing metadata and the permitted status vocabulary. Missing, duplicate and unknown identities are explicit mutation cases. |
| #103 acceptance criterion 2 | Covered | Retains the existing tiny constructed public recipe, synthetic/contains-real-data declarations, explicit source allowlist and digest binding; forbids new resident/home data and default working-data reads. |
| C1: inventory authority | Covered | PRD supplies the profile/workflow meaning; existing manifest IDs and chat PERSPECTIVES provide reusable profile identifiers. The plan cross-checks rather than treating application roles as the approved profile inventory. |
| C2: CON-007 | Covered | CON-007 expressly excludes documentation/unit/CI checks from its accepted-application-build boundary. This offline change cannot claim live AI, SQL, Azure or application acceptance. |
| C3: current manifest | Covered | Existing v0.1.0 has eleven/nine entries with blanket deferred statuses. Plan replaces unsupported full-journey deferrals with unavailable, requires reasons and preserves version history in Git. |
| C4: partial IA evidence | Covered | Existing workbench manifest declares shared IA only, eight listed roles, three case IDs and null default selection. Plan retains those defaults and source recipe, separately from full-journey status and historical EX-HOME defaults. |
| C5: regression and prior art | Covered | Existing inventory test hardcodes every status as deferred. Plan explicitly replaces that obsolete assertion with validator invocation while preserving reciprocal inventory assertions. Existing #174 registry is reused, not replaced. |
| P01-T01: fail-before tests | Covered | Contract tests precede helper behavior; destructive copies cover identities, status authority, unsafe paths, stale source hashes/version, evidence/default omissions and false synthetic declarations. The changes record must retain observed failures and later passes. |
| P01-T02: bounded implementation | Covered | At most one helper module and one new test file; existing metadata and narrowly related inventory fields are updated. No removals, new dataset payload, browser edits, services or runtime behavior changes. |
| P01-T03: validation and documentation | Covered | Targeted core tests include new enforcement and existing inventory coverage, with scoped Ruff/mypy, Markdown/link and diff checks. Existing core discovery supplies the CI route. No browser rerun or human acceptance is claimed. |
| Dependencies and approvals | Covered | No implementation dependency is invented. Pending inventory-owner review remains pending; a deferral needs explicit decision evidence and represented status needs scenario/fixture/check/result provenance. |

## Verdict

* Verdict: Pass
* Rationale: The candidate credibly addresses both exact criteria without expanding them into full FR-035 application delivery. It reuses existing identity, fixture and registry sources; makes unsupported coverage claims unavailable rather than inventing approval; and includes targeted fail-before and mutation enforcement within the explicit file/scope budget.
* Severity summary: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings. No substantive correction or divergent user decision is required by the supplied evidence.

## Strengths and Residual Risk

* The manifest distinguishes coverage of the inventory from execution of a journey. An exhaustive unavailable inventory can satisfy the stated manifest criterion without implying any of the twenty journeys has passed.
* Existing IA statuses and checks are subordinate evidence, not authority to promote a full profile/workflow to represented. Current research supports that conservative classification, not a universal claim that related features do not exist.
* The public recipe in src/api/checks/workbench_browser_check.py constructs three cases from src/core/tests/dataset.py and constructs staff from src/api/checks/workbench-manifest.json. Preserving those sources and binding their versions/hashes avoids creating another fixture population.
* Source hashes establish drift detection against reviewed public sources; declarations and hashes alone are not a universal identifying-data detector. The plan appropriately bounds its claim to constructed public fixtures and makes no private-data privacy attestation.
* Fail-before evidence and subsequent mutation rejection remain implementation obligations. An absent-module import error alone would not demonstrate the claimed behavioral enforcement; the retained evidence must show the contract/mutation behavior and final targeted results. This clarifies the existing test-first obligation, not an added acceptance criterion.
* Full journeys, formal profile mappings, operational ownership and human/application acceptance remain explicitly unproved. The caller has already accepted their exclusion from this iteration.

## Questions or Blocking Evidence Gaps

None for this bounded planning decision. Unverified operational and human acceptance are disclosed non-goals, not blockers to offline manifest enforcement.

## Limitations

* No implementation, tests, linters, browser checks, services or data generation were executed during this critique.
* The manager review was assessed through the supplied research account, not independently rerun or upgraded to an approval.
* No private/support material or working datasets were inspected. No assessment of their contents or privacy is implied.
* This is the single complete final-candidate critique. No concerns are withheld for a further critique.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record Complete/Pass and finalize the candidate for the authorized implementation handoff, preserving its file budget, unchanged fixture recipe and fail-before evidence obligations.
* Planner can directly apply: Yes; disposition/finalization only, with no plan correction required.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/iteration-scenario-manifest-103-plan.md](.copilot-tracking/plans/2026-10-17/iteration-scenario-manifest-103-plan.md) | Assessed final candidate; unchanged |
| [.copilot-tracking/details/2026-10-17/iteration-scenario-manifest-103-phase-details.md](.copilot-tracking/details/2026-10-17/iteration-scenario-manifest-103-phase-details.md) | Assessed phase details; unchanged |
| [.copilot-tracking/research/2026-10-17/iteration-scenario-manifest-103-research.md](.copilot-tracking/research/2026-10-17/iteration-scenario-manifest-103-research.md) | Supplied research and manager-review disposition; unchanged |
| [.copilot-tracking/reviews/plans/2026-10-17/iteration-scenario-manifest-103-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/iteration-scenario-manifest-103-plan-critique.md) | Complete/Pass critique |

## Next Steps

The active planning parent may record this Pass and finalize its handoff directly. No user action, additional manager review or further plan critique is required. This critique performs no implementation.
