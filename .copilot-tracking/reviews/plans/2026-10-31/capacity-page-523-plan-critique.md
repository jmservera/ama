---
title: Capacity page 523 independent final-candidate plan critique
ms.date: 2026-10-31
---

## Metadata

* Task ID: 523
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md
* Critique execution status: Complete
* Candidate branch: fix/capacity-page-523
* Candidate HEAD and supplied base: 5666bd33e1827670e5c07e3e3063bbbe989b59d3
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction requires Research, Plan, Implement and independent Review,
  verification of merged fixes first, regression-only changes if repaired, and
  exactly one new method in src/api/tests/test_procurement_api.py. Existing
  methods, fixtures, helpers, browser/runtime source and documentation must not
  change; dated original RPI evidence is allowed.
* Supplied canonical research:
  .copilot-tracking/research/2026-10-31/capacity-page-523-research.md,
  including Q1-Q3, C1-C7, W1-W3 and the reported actual SQL/Chromium execution.
* Relevant source inspected: owning procurement fixture and inherited JSON
  suite; resident HTTP reopening prior art; appointment binding; procurement
  reads and authority; SQLite persistence/reload; API authentication;
  src/README.md local gate contract; tools/rpi-checks.py heavy lock.
* Repository context consulted: supplied case-study documents and knowledge-base
  index/memory, plus the linked tracking retention policy. No regulatory,
  private-data or unrelated project assessment was performed.
* Acceptance boundary: AC1-AC6 and P01-T01 through P03-T03, including the exact
  requested API PYTHONPATH, Ruff lint/format, test-only mutation sensitivity,
  original evidence preservation, privacy-safe commit identity/Copilot trailer,
  full post-commit external gate, receipt verification, exact-head assessment,
  topic-only push and main-target PR using Refs #523 only.
* This assesses planning credibility, not implementation acceptance. There is
  no candidate test implementation yet. No tests, browser sessions, installs,
  gate executions, credential operations, remote checks or other-worktree
  actions were performed during this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1-C3, W1-W3; regression-only direction | Covered | Supplied evidence records merged repairs; current binding uses nullable contract metadata. Runtime changes are correctly excluded. |
| AC1, Q2, C4 | Covered within supplied evidence | Actual generated 980-case SQL/Chromium exercise is reported passed, including 601 orders, twelve destinations and recovery scenarios. Not independently rerun here. |
| AC2, P01-T01 | Partial | Persisted missing contract metadata, retained bindings, repeated HTTP reads and invariance are sound; inherited JSON execution is unplanned, PC-001. |
| AC3, P02-T01 | Covered | Scoped strict-lookup mutation can expose the original failure at /api/workorders without production edits. ProcurementMixin inherits AppointmentMixin, so patching the inherited binding is viable. |
| AC4, P02-T01 | Partial | Exact discovery and Ruff commands are specified; planned validation paths and shared-lock execution conflict with current constraints, PC-002. |
| AC5, P03-T01 | Covered | One critique and one original independent implementation Review are retained. Adverse findings must remain visible and publication still requires passing assessment. |
| AC6, P03-T02, P03-T03 | Partial | Commit-before-gate, immutable external receipt, refreshed base, exact-head and no-force topic publication are specified; current gate cannot be executed compatibly as written, PC-002. |
| Live verification, accessibility, approvals | Covered as residual limits | Owner live verification is pending; axe was explicitly NOT RUN; local engineering evidence is not hosted, human or accessibility acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The regression scope and defect sensitivity are credible, but the
  plan omits inherited backend ownership and proposes forbidden validation
  paths. The latter includes a hardcoded gate lock, not merely an output-path
  typo. Both issues must be dispositioned before claiming the candidate is
  executable through publication. Evidence suffices for a complete assessment;
  no additional critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: SQL-specific reopening also runs in the inherited JSON suite

* Related IDs: AC2, AC4, P01-T01, P02-T01.
* Evidence: src/api/tests/test_procurement_api.py:28-35 selects SqlStore or
  Store using self.sql; :617-618 defines JsonProcurementApi(ProcurementApi)
  with sql = False. The proposed new method belongs to ProcurementApi and
  therefore is inherited. Phase details require unconditional SqlStore
  reopening and SQLite cleanup, without an inherited-backend disposition.
* Concern: The full owning suite discovers the method twice. Unconditionally
  constructing SqlStore in the JSON instance switches backend rather than
  reopening that fixture's store. SQLite can seed procurement from the saved
  JSON source, so a pass there would not prove SQLite persisted-reload coverage
  for that instance or continued JSON backend ownership. SQL-only assumptions
  could also fail outside the focused ProcurementApi selector.
* Impact: Focused success can conceal an unintended JSON-to-SQL path in full
  discovery and misrepresent the added regression's execution coverage.
* Smallest useful change: Specify the inherited execution explicitly. Reuse
  the existing self.make_store(self.path) factory to reopen each fixture's
  backend; in the self.sql branch establish that the reopened store is the
  actual SqlStore at the existing SQLite path. Register DB cleanup only for
  the SQL branch, preserving original cleanup and HTTP shutdown. This remains
  exactly one added method and requires no helper or fixture edits.
* Action owner: Planning parent; implementation owner executes the disposition.
* Exact resolving evidence: Revised P01-T01 details distinguish SQL and JSON
  reopening; the one-method diff preserves the factory and cleanup contract;
  focused SQL execution and full owning-suite logs demonstrate both discovered
  instances preserve their original backend and pass. Any alternative explicit
  non-applicability must be disclosed and accepted by the required gate, not
  hidden as execution.
* Decision route: Direct compatible planner correction; no significant or
  divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Validation and publication depend on forbidden file operations

* Related IDs: AC4, AC6, P02-T01, P03-T02, P03-T03; plan Dependencies.
* Evidence: Plan Dependencies points to
  /tmp/ama-523-20261031-c70d35f2-venv; phase details P03-T02 selects
  /tmp/ama-523-20261031-c70d35f2-final. Current execution constraints prohibit
  file operations in /tmp and temporary directories. In relevant supplied
  gate source, tools/rpi-checks.py:2273-2275 hardcodes
  /tmp/ama-rpi-heavy.lock and opens it with creation/write flags. The owning
  fixture also uses tempfile.TemporaryDirectory at
  src/api/tests/test_procurement_api.py:38. Repository gate examples do not
  override the current prohibition.
* Concern: The plan treats these execution prerequisites as available.
  Changing --out alone cannot fix the hardcoded lock. Redirecting temporary
  output must not be assumed to authorize otherwise prohibited directory
  operations. Modifying the gate, removing serialization, bypassing checks
  or weakening receipt verification would violate the authorized test-only
  scope and publication rules.
* Impact: The implementation can be designed correctly while its requested
  checks and mandatory publication gate remain unavailable in this execution
  context. Proceeding as written violates constraints; pushing without the
  full verified gate would misrepresent acceptance.
* Smallest useful change: Replace prospective forbidden-path instructions
  with an explicit validation/publication blocker. Identify a genuinely
  authorized compatible execution context and artifact locations before
  running validation; preserve historical research paths as historical facts,
  not new execution instructions. If none is available, retain evidence and
  stop before gated push/PR. Do not install, change source/tooling, substitute
  a cloud/partial gate or disable the shared lock to clear this finding.
* Action owner: Planning parent, coordinating with the authorized execution
  owner only if compatible validation cannot be arranged under existing rules.
* Exact resolving evidence: Revised P02/P03 dispositions acknowledge the
  hardcoded lock and fixture allocation constraints. Eligible validation
  requires an authorized execution context with no prohibited file operations,
  passing requested API/Ruff logs and a new full post-commit external receipt
  verified against the current origin/main base and exact candidate HEAD.
  Otherwise the resolving disposition is an explicit publication block, not
  a claimed passing gate.
* Decision route: Direct planner correction to execution readiness and blocker
  reporting. No user choice is needed to stop forbidden execution. Any later
  request for different authorization is outside this critique and must not
  be inferred from the current direction.

## Strengths and Residual Risk

* Missing contract_version is isolated while resident bindings remain intact,
  avoiding the existing regression's second missing-metadata cause.
* SqlStore reopening and self.store/app.store reassignment follow actual
  resident HTTP-test prior art. The existing authentication provider retains
  its original store reference, but fixture staff are unchanged and password
  login does not append audit; this alone is not a demonstrated defect.
* Both endpoints twice, stable package/order identity, null/Unknown projection,
  no invented metadata, and procurement/audit invariance protect read-only
  behavior. Persisted source comparisons must observe the SQL document/audit,
  not merely repeat response equality.
* The appointment offer still lacks current contract authority and correctly
  remains 403. Retained resident scope means measures need not themselves be
  Unknown; the Unknown expectation belongs to appointment control.
* The mutation must demonstrate failure on the new test's work-order read
  assertion, not a setup/import error or arbitrary forced exception elsewhere.
* Original adverse critique/Review results remain immutable. Any substantive
  implementation Review finding blocks publication unless the required
  acceptance is met; routing it to later work is not waiver authority.
* Supplied browser evidence is fresh local engineering evidence, not live
  acceptance. Axe NOT RUN and owner live verification remain explicit limits.

## Questions or Blocking Evidence Gaps

* No unresolved product decision.
* Compatible execution of mandatory validation/publication is unresolved,
  PC-002. This does not prevent assessing or correcting the bounded plan.

## Limitations

* Supplied SQL/browser results and merged-history claims were assessed as
  recorded, without reopening external logs or contacting GitHub.
* No implementation, mutation result, full API/Ruff result, final receipt or
  exact-head implementation assessment exists within this critique boundary.
* Intake inspection confirmed the supplied branch and HEAD; untracked supplied
  RPI inputs were present. They were not moved, removed or edited.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: Planning parent.
* Smallest next action: Record the validation/publication blocker and correct
  inherited-backend handling, then finalize dispositions without another
  critique. Proceed only to compatible authorized work.
* User response required: No for these planner corrections.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/capacity-page-523-research.md](.copilot-tracking/research/2026-10-31/capacity-page-523-research.md) | Supplied canonical research and execution claims |
| [.copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md](.copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md](.copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md) | Assessed phase details |
| [.copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md) | Complete independent critique |

## Next Steps

Planning parent resolves PC-001 directly and records PC-002's execution blocker.
No user response or second critique is required. This critique stops here;
implementation and publication are not performed or authorized by this artifact.
