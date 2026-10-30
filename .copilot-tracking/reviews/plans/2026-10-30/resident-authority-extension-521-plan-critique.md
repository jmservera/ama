---
title: Resident authority extension final-candidate plan critique
description: Single independent plan assessment for issue 521 continuation
ms.date: 2026-10-30
---

## Metadata

* Task ID: 521, jmservera/ama.
* Task slug: resident-authority-extension-521.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate critique for this continuation.
* Branch: chore/resident-authority-extension-521.
* Inspected HEAD: 92b669335cb8874df227cd2ecd90b45f1e3b0a8d.
* Inspected origin/main: a02984e8d71d312f089ad75713d7a98e59aee420.
* Only this critique artifact was written. No nested agents were used.

## Inputs and Criterion Boundary

* Caller direction: critique, not implementation; ordered full RPI continuation
  after the explicitly requested rebase; resident access through January 31,
  2027 UTC; unchanged min0, synthetic resident-only scope, RBAC/network and
  approval boundaries; credential/SQL rotation plan and unchanged USD700 cap.
* Validation requirements: requested API unittest, Ruff check/format and mypy;
  locked heavy work; complete exact-head gate and independent assessment.
  No tests, installs, Azure actions, sign-in, credentials, source edits or push
  are authorized during this assessment. The execution environment also forbids
  temporary-directory operations, including /tmp.
* Supplied research:
  .copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md,
  C1-C7/W1 and its source pointers. W1 is considered as supplied research;
  the remote issue was not independently retrieved.
* Historical evidence:
  .copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md
  and .copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md.
  Their original adverse outcomes remain historical, not current test results.
* Supporting supplied-source trace: src/README.md; tools/rpi-checks.py;
  infra/README.md, January renewal/rotation/cost sections; owning project
  pyproject.toml files; resident SQL tests; named domain/API/helper tests;
  API SQL opt-in tests. Read-only git inspection confirmed the source boundary.
* Required project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md and
  docs/reference/research/sector/housing-association-primer.md.
  Memory is context, not acceptance evidence.
* Decisions and criteria assessed: AC1-AC4, P01/P02 and all four tasks;
  dependencies, two-method continuation budget, canonical test ownership,
  immutable historical evidence, no live acceptance claim and no publication.
* Boundary: planning credibility and executable validation design. This is
  neither a fresh implementation Review nor evidence that runtime, SQL,
  lint/types, cost headroom or live renewal passed.

Input fingerprints at assessment:

| Input | SHA-256 |
| --- | --- |
| Plan | 33cb7c5fd7a1fe5cf7c34ff7b34ba39bd01774697b760d7ac40233daa254de0c |
| Phase details | 83ba243f1d0f796ceb3e44d644f5868f29126d81aff9802cd1126fd85dd7febb |
| Research | 06cc66964d9f781398a289d2a91ce6ecb61b127e731283b41146c67936df7b8d |

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C4; AC1; January boundary | Covered at planning level | Shared exclusive February 1 UTC cap and unchanged shorter expiries/guards are explicit; execution remains pending. |
| C2/C3; AC1; actual SQL proof | Partial | Authored migration/reapply/rollback tests exist, but the proposed runner does not execute their real-SQL class; PC-002. |
| C5; AC2; cost and USD700 ceiling | Covered | USD46/USD56 and USD15.50/USD25.50 are overlapping, assumption-labelled alternatives; actual liabilities and funding remain unknown. |
| C5; AC3; rotation and rights | Covered | Independent technical Review is assigned; existing-secret Modify refusal, row-specific renewal and separate owner approval remain intact. |
| C6/W1; AC4; live/inference authority | Covered | No live application, inference renewal, extra resources, roles or network change is authorized or claimed. |
| C7; P01-T01; tooling/dependencies | Partial | Missing dependencies justify pip restoration, not inherited environments or unapproved scratch paths; PC-001/PC-003. |
| P01-T01/P02-T02; heavy admission | Partial | Avoiding nested flock is correct; blocking waits contradict the repository's nonqueued admission requirement; PC-004. |
| P01-T01/T02; requested tests and static checks | Partial | API checks are named; changed infra lint/type coverage is not concretely selected and is absent from the runner's default static groups; PC-005. |
| P01-T02; bounded fixes/evidence reconciliation | Covered | Only demonstrated coupled defects may change source; original evidence is preserved. |
| P02-T01; one original independent Review | Covered | Rotation/SQL and guard assessment is assigned to a fresh reviewer, without a repeated original Review. |
| P02-T02; complete exact-head gate | Partial | Storage incompatibility and missing final independent exact-head assessment remain; PC-001/PC-006. |
| Test ownership and continuation budget | Covered | Core owns domain/SQL, API owns HTTP, infra owns helpers; no removals, at most two new methods for demonstrated gaps. Existing October 28 additions are retained. |
| Dependencies and failure handling | Partial | Browser/scanner/SQL failure is honestly blocking, but known runner limitations must be explicit prerequisites rather than assumed coverage; PC-001/PC-002. |

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 3 High, 3 Medium, 0 Low.
* Rationale: scope, cutoff, rotation and cost treatment are credible. Six
  substantive execution-planning corrections are needed before handoff.
  In particular, ordinary discovery plus this full runner cannot establish
  the required resident SQL migration result, and the proposed direct checks
  do not implement their stated isolation boundary.
* Execution status Complete means the supplied planning boundary was assessed.
  It does not mean validation is executable or acceptance is earned.
  The mandatory gate has an identified environment-policy blocker.
* This is the complete actionable finding set for these inputs. The planning
  parent should disposition it directly, not request serial critiques.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned storage and the native runner conflict with the environment prohibition

* Related IDs: P01-T01; P02-T02; local-only execution constraints.
* Evidence: phase details name /tmp/ama-521-validation-20261030,
  /tmp/ama-rpi-heavy.lock and /tmp/ama-521-final-20261030.
  tools/rpi-checks.py:2272-2275 hardcodes creation/opening of the shared lock
  under /tmp. The environment prohibits temporary-directory file operations.
  The candidate plan does not acknowledge this incompatibility.
* Concern: the proposed commands cannot be followed as written. Moving only
  the receipt or venv does not remove the runner's native forbidden lock
  operation; wrapping the runner with a different lock is not a solution.
* Impact: attempting the plan violates an active execution constraint.
  Offline Bicep permission resolves the historical no-az obstacle, not this
  separate storage obstacle.
* Smallest useful change: replace proposed scratch/output locations with
  permitted persistent locations, identified relative to the working
  directory and outside the candidate checkout where required. Explicitly
  mark the unchanged full runner blocked by its native lock path. Do not
  silently edit the runner, substitute a private lock, waive the gate or
  claim that a relocated receipt makes execution compliant.
* Action owner: planning parent; coordinator owns any separately authorized
  tooling/environment prerequisite.
* Exact resolving evidence: revised plan/details contain permitted locations,
  identify the remaining hardcoded-path blocker and its resume condition,
  and preserve the complete-gate requirement. Execution eligibility requires
  evidence of a compliant, approved tooling/environment route preserving
  shared exclusion and exact-head verification before any attempt.
* Decision route: Direct planner correction to acknowledge and obey existing
  constraints. No user response is needed to record the blocker. A future
  proposal to change shared tooling or execution policy is outside this
  candidate and must not be inferred as approved.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The required resident SQL migration class has no executable validation route

* Related IDs: C2/C3; AC1; P01-T01; P02-T02.
* Evidence: src/core/tests/test_resident_showcase_sql.py:216-217 makes
  SqlBoundaryTests opt-in. Its migration/reapply and rollback methods are
  at :608-679. tools/rpi-checks.py:30-39 SQL_SELECTORS does not include that
  module/class. Runner.projects performs ordinary discovery without SQL
  opt-in; Runner.sql runs its fixed API selectors and removes the owned
  container. Extra-test dispatch at :1898-1912 supplies test paths only,
  not SQL credentials/opt-in or an owned live fixture.
* Concern: the details promise real SQL only through the runner-owned
  disposable database, but neither P01's unspecified core selectors nor
  the proposed --all command runs this class against that database.
  Adding core:test_resident_showcase_sql.SqlBoundaryTests as an ordinary
  --extra-test alone would still skip and fail its integration contract.
* Impact: a passing standard full receipt would not prove #521's migration,
  trusted reapply, rollback, row/revocation preservation and narrow rights.
  This recreates historical RV-001 despite apparent complete-gate coverage.
* Smallest useful change: specify the exact SqlBoundaryTests selector and
  its asserted contracts, assign ownership for a supported isolated SQL
  execution route, and establish that route before marking AC1 runnable.
  If the current runner must remain unchanged, record this specific SQL
  criterion blocked rather than claiming --all or extras cover it.
  Do not repurpose another run's container, copy credentials, add a cloud
  fallback or silently expand tooling scope.
* Action owner: planning parent defines the prerequisite and acceptance
  mapping; implementation executor runs only the approved owned-fixture route.
* Exact resolving evidence: revised details identify the fixture lifecycle,
  ownership/loopback checks, driver environment, exact selector, cleanup and
  log destination. Later evidence must show actual execution, zero unexpected
  skips, and passing legacy/reapply/rollback/rights methods on the current
  candidate. A standard full receipt remains separately required.
* Decision route: Direct planner correction. Missing supported execution
  capability is a blocker, not a new resident-authority design decision.
  Any proposed shared-runner enhancement needs separately scoped authority.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Direct focused checks do not enforce the promised credential and data isolation

* Related IDs: P01-T01; no credential/private-data access; AC1.
* Evidence: phase details give a raw python3 API discovery command with
  PYTHONPATH but no environment allowlist. src/api/tests/test_mssqlstore.py:34
  opts in solely on inherited ZF_TEST_MSSQL=1; its module explicitly warns
  that its configured database may be wiped. Resident SQL tests also read
  inherited ZF_SQL_* settings when opted in. By contrast,
  tools/rpi-checks.py:1126-1155 constructs an isolated environment with an
  owned HOME, data path, Azure config, caches and no inherited credentials.
* Concern: saying "never inherited connection strings" does not make the
  direct commands safe. An ambient opt-in can enable destructive SQL tests,
  including a foreign local database, before the final runner is involved.
  Non-editable installs alone also do not relocate test, Python or lint caches.
* Impact: the focused validation route can cross the explicit data/credential
  boundary or dirty the candidate, invalidating later gate admission.
* Smallest useful change: define one explicit allowlisted environment and
  owned persistent workspace for setup and every P01 command. Do not inspect
  or print ambient secret values. Omit ambient SQL/browser/cloud opt-ins and
  connection variables; use isolated HOME/AZURE_CONFIG_DIR, a constructed
  synthetic ZF_DATA location, and permitted bytecode/cache locations.
  Bind python/pip/Ruff/mypy to the intended venv rather than implicit PATH.
  Only the separately proved owned-SQL route may add its ephemeral settings.
* Action owner: planning parent specifies isolation; implementation executor
  applies it before running discovery or installing dependencies.
* Exact resolving evidence: revised details contain a reproducible sanitized
  invocation/environment contract for all P01 commands, with no inherited
  credential sources and explicit opt-in separation. Later command logs
  record safe configuration identities, exits and skips without secret values;
  the candidate remains free of generated/untracked/ignored inputs.
* Decision route: Direct planner correction. Existing prohibitions already
  decide the safe behavior; no broader permission or user response is needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Both validation stages queue despite the repository's nonqueued admission rule

* Related IDs: P01-T01; P02-T02; heavy-lock ownership.
* Evidence: the plan/details prescribe flock -w 600 for focused checks.
  Their full-gate command omits --lock-timeout, whose runner default is
  600 seconds at tools/rpi-checks.py:2298. src/README.md, Stabilization
  validation ladder, requires actual-holder inspection, --lock-timeout 0,
  no waiting/duplicate gates and no polling after busy admission.
* Concern: avoiding double-locking is necessary but insufficient. Both
  proposed routes still wait on a potentially foreign owner; the historical
  intake lslocks observation is not current admission evidence.
* Impact: the executor can queue prohibited heavy work and misrepresent a
  blocked admission as an authorized automatic retry.
* Smallest useful change: specify nonblocking admission for focused work
  using the same approved shared lock, actual-holder inspection immediately
  before admission, and --lock-timeout 0 for the native runner. If busy,
  record blocked checks and resume only at a later explicit coordination
  event. Retain the prohibition on wrapping the native runner in flock.
  Apply only after PC-001's path incompatibility is resolved.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details name the lock owner for
  each stage, nonqueued options, busy-stop/resume behavior and no nested lock.
  Later logs identify admission outcome without foreign-output inspection,
  foreign-process interruption or lock polling.
* Decision route: Direct planner correction; no user decision is required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: The changed infra files are not covered by the cited default lint/type matrix

* Related IDs: P01-T01/T02; requested Ruff/mypy; demonstrated coupled fixes.
* Evidence: phase details say "focused infra lint/types following existing
  runner configuration" without selectors. tools/rpi-checks.py RUFF_GROUPS
  and TYPE_GROUPS do not select infra/scripts/resident_showcase_sql.py,
  infra/tests/test_resident_demo_secrets.py or
  infra/tests/test_resident_demo_deploy.py, all in the supplied source diff.
  Owning-package checks cover src projects, not these infra files.
* Concern: executing the existing runner matrix does not establish static
  validation of all changed Python inputs. The plan leaves selection and
  applicable options to discovery during implementation.
* Impact: the continuation can claim changed-path lint/type coverage while
  the SQL renderer and modified helper tests were never checked.
* Smallest useful change: add explicit targeted Ruff check, Ruff format
  --check and applicable mypy commands for the changed infra files, using the
  repository's existing settings/isolated infra conventions and sanitized
  venv from PC-003. Name any deliberate type exclusion and its rationale;
  do not imply default full-gate coverage. Extend the selector list only
  for demonstrated coupled changes.
* Action owner: planning parent.
* Exact resolving evidence: revised details map every changed Python path
  to its unit/static owner and concrete commands/options. Later evidence
  records each exit and distinguishes focused coverage from the unchanged
  runner matrix. No unrelated lint cleanup, exclusions hiding failures or
  new tests outside the two-method budget are authorized.
* Decision route: Direct planner correction; no user response is required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Final receipt verification is not followed by independent exact-head assessment

* Related IDs: P02-T01/T02; complete exact-head gate; required independent review.
* Evidence: P02-T01 reviews before the evidence commit. P02-T02 commits,
  runs the gate, fetches and verifies a passing receipt, then stops at a
  final report. Neither source assigns an independent assessment of the
  final committed HEAD and verified receipt. src/README.md requires fresh
  main verification immediately before independent exact-head review.
  The gate command pins a02984e8d71d312f089ad75713d7a98e59aee420 while
  the task also requires a current-main fetch, without a drift branch.
* Concern: the original implementation Review cannot assess a future commit
  or receipt, and local receipt verification is not independent assessment.
  A moved origin/main must not silently remain compatible with the pinned base.
* Impact: a local-only final candidate could be reported as fully assessed
  without the required final evidence boundary, or against a stale base.
* Smallest useful change: append a distinct independent exact-head
  assessment after the final commit, complete gate, refetch and verification.
  Keep the original Review immutable; this is final-candidate assessment,
  not a second original Review. Assign a read-only assessor and external
  output so recording it does not create another candidate commit.
  Explicitly stop and invalidate/reconcile under existing authority if main,
  HEAD, tools, images or candidate inputs change; do not silently rebase or
  reuse the old receipt. No push or PR follows.
* Action owner: planning parent assigns the final assessor; coordinator
  preserves receipt/base identity.
* Exact resolving evidence: revised P02-T02 includes the full sequence,
  assessor/output ownership, current-base comparison and drift stop rule.
  Later external evidence binds the assessor's outcome to the exact final
  HEAD, current origin/main SHA and verified receipt. A failed gate leaves
  this assessment blocked, not replaced by the earlier Review.
* Decision route: Direct planner correction implementing an existing
  requirement. No new user response is needed.

## Strengths and Residual Risk

* The source-only continuation avoids another authority implementation.
  AC1 correctly separates configuration equality from exclusive serving
  denial at 2027-02-01T00:00:00Z.
* Cost arithmetic, overlapping baselines, reserve and unchanged USD700 all-in
  ceiling are explicit. Unknown actual headroom remains a live-action stop,
  not an implementation defect or assumed funding.
* Rotation preserves new-secret-only helper refusal, private paths, narrow
  SQL identity rights, individually approved row renewal, rollback limits
  and separate operational approval. The fresh Review is assigned its
  independent technical assessment; no technical approval is claimed here.
* The test ownership and two-new-method ceiling are credible. Missing
  execution capability does not justify duplicate tests, moving tests into
  packages, deleting guard assertions or raising that budget.
* No UI change is planned, so no additional UI-specific acceptance claim
  is appropriate. The full runner's existing browser contracts remain required.
* Offline Bicep tooling is now explicitly permitted. Historical findings
  predicated on prohibiting every az invocation must not be reapplied as
  current restrictions. No cloud API, deployment or sign-in is authorized.
* Live apply, actual January funding, operational credential review and
  paid-inference authority remain separate and unproven. No whole-issue
  closure is justified by any local result.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is required to correct these
  six findings. Current direction already fixes the authority boundary.
* PC-001 identifies a known mandatory-gate execution blocker under the
  current environment. PC-002 identifies missing supported SQL execution.
  Neither is evidence that the resident source implementation is defective.
* The planner must record the compliant resume prerequisites or retain
  blocked validation, not promise that missing tools alone explain all debt.

## Limitations

* No tests, installs, Azure commands, credential reads, live sign-in,
  private-data reads, foreign-output inspection or remote publication occurred.
* Source pointers were used only to assess the supplied plan's credibility.
  Actual runtime/SQL behavior, package/tool availability, lock availability,
  current pricing and funding were not independently executed or established.
* HEAD/base inspection was local. No fetch was performed during this critique;
  main's eventual remote position must be checked at the planned final gate.
* Existing untracked plan/details/research/state artifacts were preserved.
  No historical critique or Review was changed.

## Recommended Next Action

* Highest-impact finding: PC-003, unsafe ambient environment inheritance
  before potentially destructive API SQL discovery.
* Action owner: planning parent.
* Smallest next action: directly revise P01's sanitized invocation contract
  and disposition all six findings in plan/details before implementation.
  Retain explicit blocked gate/SQL status until PC-001/PC-002 are resolved.
* User response required: No for these corrections. No implementation,
  additional critique, gate attempt or expanded tooling authority follows
  from this record.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md](.copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md](.copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md](.copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md) | Supplied evidence synthesis |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md) | This single complete critique |

## Next Steps

Return Complete / Revise to the active planning parent for direct correction
and disposition of PC-001 through PC-006, without another critique. No user
action is required. This assessor stops here; no implementation or publication
is authorized.
