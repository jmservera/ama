<!-- markdownlint-disable-file -->
# RPI Plan Critique: Retire legacy MVP directories

## Metadata

* Task ID: issue-201
* Task slug: mvp-cutover-201
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md
* Research: .copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique.
* Original verdict: Revise. Preserve this verdict and all original findings;
  subsequent planner dispositions belong in the plan, not a rewritten critique.

## Inputs and Criterion Boundary

* Caller authority: ordered RPI followed by authorized topic-branch publication;
  explicit owner SIGNED OFF #201 on 2026-10-27. This critique itself authorizes
  and performs no implementation, commit, tag, push or deployment.
* Supplied boundary: initial HEAD/origin/main
  65a514ed20e97816dbf47e9fb981ab4cfe40597d, BRD 0.21.0, locally absent
  v0.21.0, only mvp/README.md tracked, prototype already absent.
* Decisions: delete only mvp/README.md and its empty directory; no test edits,
  regenerated evidence, workflow/check-name changes, private dataset/secret
  reads, uv, cloud deployment, tag publication or full gate. All five issues
  must use Refs because broader acceptance remains unproved.
* Dependencies and acceptance: one critique disposition before implementation;
  archive readback, live navigation repairs, append-only log, unchanged
  workflows, existing API/rename/parity tests, then one independent Review.
* Evidence considered: supplied research C1-C11/W1-W5; necessary excerpts of
  src/README.md, the BRD, cut-over evidence pack, parity matrix, pointer README,
  existing selected tests and dependency manifests. Required case-study,
  knowledge-base index and owner-memory context were read; memory is not proof.
* Assessment boundary: credibility and safety of the supplied maintenance plan,
  not a new migration audit or hosted/deployment/whole-issue acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C5, C11; P01-T01 | Covered | Migrated source baseline, BRD version and pointer-only archive target agree with supplied evidence. Existing conflicting tags block; no tag movement or push. |
| C6-C10; P01-T02 | Covered | Live prose/link repair, intentional historical/guard strings, additive log repair map and unchanged evidence are distinguished. |
| Owner sign-off; P01/P03 | Covered | Current authority is prospective; historical unsigned/blocked evidence is not turned into new technical acceptance. |
| P02-T01; no private/production access | Partial | Planned discovery lacks an explicit sanitized execution boundary; PC-001. |
| P02-T01; no forbidden scratch locations | Partial | Existing selectors allocate temporary files but no repository-relative scratch routing is specified; PC-001. |
| P02-T01; semantic/regression acceptance | Covered | Existing selectors cover parity destinations and registry; directory, workflow, links and log-prefix checks are planned without regenerated reports. |
| P01-T01/P03-T02; authenticated identity | Partial | Fresh resolution is specified, but phase details prescribe a literal account email; PC-002. |
| W1-W5; P03-T02; Refs-only publication | Partial | Details and requirements retain a conditional closure escape despite current explicit Refs-only direction; PC-003. |
| P03-T01; independent Review | Covered | One original independent Review, truthful outcome and material-findings publication block; no iterative verdict replacement. |
| Scoped validation and retained hosted gates | Covered | src/README.md owner policy supports focused small-maintenance checks; caller forbids the full gate. No full-tier or hosted success is inferred. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 1; Medium 2; Low 0.
* Rationale: the surgical scope, archive handling and evidence policy are
  credible. Before execution, make the test environment explicitly safe,
  remove the literal identity and lock issue references to current authority.
  All three are direct planner corrections, not missing owner decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Bound test execution against inherited integration configuration and forbidden scratch paths

* Related IDs: P02-T01; no secrets/private datasets/production writes; bounded
  existing-test validation.
* Evidence: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md:71-84
  gives bare discovery/selectors and discusses skips, but specifies no
  sanitized environment or scratch root. src/api/tests/test_mssqlstore.py:34-59
  enables SQL tests with ZF_TEST_MSSQL=1; wipe() uses connection_string() and
  drops a trigger and tables. src/api/tests/test_continuity_epoch_export.py:1400,
  src/api/tests/test_coordinator_api.py:396 and
  src/api/tests/test_progress_report_api.py:378 demonstrate additional SQL
  opt-ins. src/agents/tests/test_eval_registry.py:52-53 creates temporary
  directories for the planned selector.
* Concern: an isolated pip environment does not sanitize inherited application,
  credential, database or integration settings. Recording skips afterward does
  not prevent an inherited opt-in from executing destructive SQL first. Default
  tempfile placement can also violate the explicit prohibition on system
  temporary paths. No actual unsafe environment values were inspected or
  assumed.
* Impact: nominally local validation could cross the no-production/no-private
  boundary or perform forbidden filesystem writes before producing evidence.
* Smallest useful change: add one shared, explicit sanitized launch contract
  for all planned tests. Use an allowlisted non-secret environment, disable
  opt-in SQL/browser/cloud suites, do not inherit ZF_DATA, SQL connection or
  credential settings, and route scratch/cache/home/data locations to newly
  owned repository-relative paths. Set TMPDIR/TMP/TEMP before Python starts.
  Do not read existing private locations or print environment values. Preserve
  the selected tests and fixture-only PYTHONPATH; clean only exact newly owned
  scratch outputs, without touching historical tracking evidence.
* Action owner: planning parent; implementation parent executes the contract.
* Exact resolving evidence: revised P02-T01 records the sanitized wrapper and
  safe relative output/scratch paths; the changes record later preserves the
  exact commands, test counts and opt-in skip reasons, with no inherited
  connection/credential values and no full-gate claim.
* Decision route: Direct planner correction. User response not required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Derive identity from the authenticated account instead of prescribing a literal email

* Related IDs: P01-T01; P03-T02; privacy-safe author/committer identity.
* Evidence: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md:102-105
  specifies a literal noreply address after authentication. The supplied
  repository instructions require deriving {id}+{login}@users.noreply.github.com
  from fresh gh api user results, using repository-local configuration.
* Concern: account lookup followed by a fixed address can attribute the tag
  or commit to a different account if the authenticated identity differs.
* Impact: wrong attribution or privacy-protection rejection; tagger identity
  must be correct before the earlier archive step, not only before committing.
* Smallest useful change: replace the literal email with fresh id/login
  derivation, apply it repository-locally before any annotated tag or commit,
  and ensure author/committer overrides do not replace the derived identity.
* Action owner: planning parent.
* Exact resolving evidence: P01-T01/P03-T02 consistently use fresh account
  fields without a fixed user's email; implementation records identity
  readback for the created tag/commit without credentials.
* Decision route: Direct planner correction. User response not required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Remove the conditional issue-closure escape

* Related IDs: W1-W5; P03-T02; all-five-issues Refs-only requirement.
* Evidence: .copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md:37
  allows Closes with complete evidence, while its scope and publication task
  say Refs only. .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md:108-109
  retains "unless complete evidence changes that conclusion." Current caller
  direction explicitly requires Refs for all five issues.
* Concern: publication instructions contain conflicting authority and permit
  automatic issue closure even though the authorized maintenance scope
  excludes obtaining several decision-critical acceptance results.
* Impact: an executor could insert closure keywords and misrepresent broader
  deployment, baseline, rubric or release acceptance.
* Smallest useful change: make Refs #199, Refs #200, Refs #201, Refs #202 and
  Refs #203 unconditional for this PR in requirements and publication details.
  Retain the per-issue remaining-criteria summary. Later closure requires
  separately authorized work, not reinterpretation inside this task.
* Action owner: planning parent.
* Exact resolving evidence: plan/details contain no conditional permission
  for closing these issues; the final PR title/body use only non-closing
  references and truthfully state remaining acceptance.
* Decision route: Direct planner correction implementing existing user
  direction. User response not required.

## Strengths and Residual Risk

* Local archive creation only when absent, exact owner push command
  git push origin refs/tags/v0.21.0:refs/tags/v0.21.0, no moving existing tags
  and explicit --no-follow-tags branch publication protect archive ownership.
* The archive captures the pointer-era baseline, not a false claim that legacy
  executables remain in that tree; earlier content remains in Git history.
* Historical paths, dated evidence and defensive data guards remain intentional.
  Log-prefix comparison and additive repair mapping avoid destructive cleanup.
* Owner sign-off permits the bounded retirement; it does not supply missing
  hosted CI, deployed health, baseline parity, release or rubric evidence.
* Scoped-only validation and no new tests/generated outputs are accepted scope
  constraints, not reasons to demand a forbidden full gate or larger audit.
* Main movement remains a publication checkpoint: record the observed base
  and stop for authorized reconciliation rather than silently rewriting history.

## Questions or Blocking Evidence Gaps

* None requiring user input. Do not reopen the explicit owner sign-off or ask
  for permission to perform prohibited full-gate/deployment work.
* Publication remains contingent on the planned independent Review and retained
  hosted checks; neither is established by this critique.

## Limitations

* No tests, gate, cloud operations, account lookup, tag/commit/push or deployment
  were performed. The critique makes no implementation-success claim.
* External issue findings are assessed from supplied dated W1-W5, not a fresh
  GitHub retrieval. No broad independent source audit was performed.
* Existing untracked RPI inputs were left in place. Only this requested
  critique artifact was written; plan, details and research remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise the test-launch contract, identity
  derivation and Refs-only wording; record PC-001 through PC-003 dispositions
  with exact resolving evidence in the plan, preserving this original verdict.
* User response required: No.
* Do not request or perform a second critique. The parent finalizes after
  disposition and continues the authorized ordered RPI loop.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md](.copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md](.copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md](.copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md) | Supplied evidence boundary |
| [.copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md) | Original complete critique and findings |

## Next Steps

Planning parent: dispose PC-001 through PC-003 directly, finalize the plan
without another critique, then continue the authorized implementation and one
independent Review. No user action is required. This critique stops here.
