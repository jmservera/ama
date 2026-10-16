---
title: Issue 211 final-candidate plan critique
ms.date: 2026-10-16
---

## Metadata

* Task ID: 211 / issue-211-rule-cards.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md.
* Critique execution status: Complete.
* Assessment count: One independent final-candidate assessment. No implementation,
  delegation, repeat critique, commit or publication was performed.

## Inputs and Criterion Boundary

* Supplied research: .copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md.
* Confirmed direction: complete the ordered RPI loop, then commit, push and open
  a PR to main; reuse rulecards and lawstore; implementation belongs in src/;
  enforce authority on the server; preserve exercise-only labels and do not
  invent real approvals. That publishing direction belongs to the parent, not
  this read-only critique.
* Requirements: all six issue #211 acceptance criteria, the owner's comments
  about remaining identity binding and migrated paths, plan acceptance criteria
  1-5, phases P01-P03, and their tasks. The issue lists dependencies #209, #210,
  #116 and #290. Existing migrated stores and authentication were inspected as
  evidence of reusable foundations, not as proof that every dependency is closed.
* Evidence: src/core/src/zava_forward/core/rulecards.py,
  src/core/src/zava_forward/core/lawstore.py,
  src/core/src/zava_forward/core/mssqlstore.py,
  src/api/src/zava_forward/api/auth.py,
  src/api/src/zava_forward/api/server.py,
  src/core/tests/test_rulecards.py,
  src/api/tests/test_lawstore.py,
  src/api/tests/test_auth.py,
  src/api/tests/test_role_endpoint_inventory.py,
  src/api/tests/test_role_matrix.py, both component pyproject.toml files and
  relevant README sections. ADR 0005's synthetic-demo decision confirms the
  distinction between simulated approvals and real authority. Required project
  entry documents were consulted only for context.
* Boundary: planning credibility for the bounded local engineering slice,
  including source transaction ownership, authenticated identity authority,
  compatibility, exact regression evidence and delivery gates. No legal
  correctness assessment, live Entra assignment, cryptographic ingress
  verification, Azure deployment or UI acceptance is implied.
* Existing topic: feat/src-rule-cards-211; no matching PR was returned by the
  read-only PR lookup. Supplied dated artifacts were already untracked.
  They were neither moved nor modified.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue criteria 1-2: named owner, independent author | Partial | Dedicated claims and server-derived email are sound; fallback binding remains unspecified, PC-002. |
| Issue criterion 3: retained versions, approver and dates | Partial | Existing append-only schema is reused; upgrade and failure evidence needs precision, PC-001 and PC-003. |
| Issue criterion 4: owner hold | Covered in design | Named-owner transition and hold reason are explicit; retain positive, wrong-owner and missing-reason cases. |
| Issue criterion 5: two exercise seeds | Covered in design | Seeds remain unassigned drafts, with no automatic approval. Assignment of a later version is not real approval. |
| Issue criterion 6: source changes preserve cards | Partial | Hook is planned, but transaction ownership and atomicity assertions are underspecified, PC-001. |
| Research C1-C2; P01-T01, P01-T02 | Partial | Whole mutations are intended; shared-connection locking, nested commits and persisted compatibility need explicit contracts. |
| Research C3-C5; P02-T01, P02-T02 | Partial | Existing auth, CSRF and staff law gating are retained; authoritative binding and deny matrix need tightening, PC-002. |
| P03-T01; validation lock | Partial | Correct existing targets and one bounded HTTP harness; missing upgrade and isolation cases, PC-003. The lawstore fixture root resolves correctly. |
| P03-T02; local validation | Partial | Honest platform limits are appropriate; prohibited tool/scratch paths must be replaced, PC-004. |
| P03-T03; full loop and publication | Partial | Commit/push/PR direction is explicit; review findings need a blocking disposition gate, PC-005. |
| Non-goals and authority limits | Covered | No rule engine, UI, Azure deployment or real legal approval is claimed. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 3 Medium, 0 Low.
* Rationale: The reuse and scope decisions are credible. Five direct corrections
  are needed to make the transaction, identity, compatibility and validation
  promises executable and prevent unresolved implementation defects from being
  treated as delivery follow-ups. No significant or divergent user decision is
  needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify one transaction owner across source and rule mutations

* Related IDs: P01-T01, P01-T02, P03-T01; issue criteria 3 and 6.
* Evidence: src/core/src/zava_forward/core/rulecards.py:87-90, 136-145,
  188-207 and 209-235 commit inside helpers and compound operations.
  src/core/src/zava_forward/core/lawstore.py:137-175 shares a SQLite connection
  across threads; :213-243 starts SQL Server transactions only on writes;
  :280-329 reads the source version before the first write and commits source
  ingestion before rebuilding the index. src/api/src/zava_forward/api/server.py
  creates app.law_lock and uses it for current law reads. SQL Server's
  application lock protects database transactions, not independent requests
  concurrently using the same Python connection.
* Concern: The details promise complete-write transactions and source reviews
  "within its transaction", but do not assign ownership of begin/commit/rollback
  when LawStore calls RuleCardStore, or require shared-connection serialization.
  Merely adding transaction wrappers to both stores can nest a begin, let an
  inner review helper commit source rows early, or let another request interfere
  with an in-progress transaction. Version/state reads must occur after lock
  acquisition, not just the inserts.
* Impact: A failed ingestion can leave a committed source without its review;
  a failed activation can partially supersede history; concurrent requests can
  see or affect uncommitted state.
* Smallest useful change: Define the owning public transaction and a joining,
  non-committing internal helper for source review creation. Serialize access
  to each shared connection, including reads, with a consistent lock/reentrancy
  policy; acquire the database write lock before MAX(version) or state checks.
  Keep source versions, provisions and corresponding reviews atomic. State
  separately whether a post-commit index rebuild failure leaves committed
  source/review evidence, and how a retry repairs that derived index. Do not
  promise transactional rollback of immutable snapshot blobs.
* Action owner: Planning parent, then core implementation owner.
* Exact resolving evidence: Revised P01 details and named tests in
  src/core/tests/test_rulecards.py and src/api/tests/test_lawstore.py proving:
  first ingestion creates no change review; a changed source creates its review;
  an unchanged retry creates neither version nor duplicate review; injected
  review/provision failure leaves neither new source version nor review;
  card history remains byte-for-byte equivalent; activation failure after a
  supersession insert leaves both versions' histories unchanged. Add deterministic
  shared-connection and independent-connection writer tests, and a successful
  mutation after rollback to prove locks/transaction flags are released.
  Record the selected index-failure semantics with one failure/retry test.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Distinguish provisioned object binding from email fallback

* Related IDs: P02-T01, P02-T02, P03-T01; issue criteria 1-2; plan acceptance 2.
* Evidence: src/api/src/zava_forward/api/auth.py:125-146 can resolve a staff
  record through ZF_AUTH_EMAIL_FALLBACK after an absent, ambiguous or unmatched
  object-ID lookup. src/api/tests/test_auth.py explicitly preserves fallback
  login for an unknown oid. The current returned user does not record which
  binding succeeded. auth.py also accepts configurable ZF_ROLE_MAP values;
  its module documentation explicitly delegates signature validation to ingress.
* Concern: "Validated, provisioned trusted-proxy identities" does not say whether
  a fallback-only login receives rule capabilities. Preserving existing staff
  login while attaching claims to every resolved staff record would conflate
  an email match with the stronger object binding needed for the named approval
  identity. Configurable role mapping must also not turn a bare rule claim into
  the required workbench role.
* Impact: Approval attribution and self-approval protection could rely on an
  identity resolution path weaker than the plan's claimed provisioned binding.
  Tests using synthetic principal headers cannot prove ingress signatures.
* Smallest useful change: Preserve fallback for existing workbench use, but issue
  rule capabilities only after an unambiguous tenant/object-ID match to a
  provisioned staff identity. Keep canonical staff email as the stored actor,
  as already decided. Derive capabilities afresh from validated principal
  claims, exclude reserved rule claims from staff-role mapping, and require
  staff law access as well as the action capability. Describe local tests as
  parser/server-boundary evidence, not signed-token verification.
* Action owner: Planning parent, then API authentication owner.
* Exact resolving evidence: Add cases to src/api/tests/test_auth.py and the
  single HTTP harness for matched oid with differing claimed email; unknown,
  missing and multiple oids with fallback enabled; duplicate provisioned oid
  ambiguity; rule-only claims, including a custom role-map override; two mapped
  workbench roles; staff-file capability injection; wrong tenant; shared-password
  identity; contractor plus rule claims; and dual-capability self-approval.
  Exercise all six transition routes for wrong capability and wrong named owner,
  assert denied writes leave history unchanged, and test staff-only access to
  collection, history and reviews. Existing fallback workbench tests must still
  pass. README evidence must retain the trusted-ingress deployment limitation.
* Decision route: Direct planner correction; no real tenant role assignment or
  legal delegation is requested.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Test persisted upgrades and isolate the new SQL tables

* Related IDs: P01-T01, P03-T01; retained-history requirement; compatibility NFR.
* Evidence: Existing SQLite rule tables and append-only triggers are initialized
  in src/core/src/zava_forward/core/rulecards.py:29-40 and :75-85.
  src/api/tests/test_lawstore.py:186-203 wipes only reg_* tables before each
  SQL Server case. The plan adds rule tables to the law database, but its
  persistence/reopen coverage does not explicitly require an old-schema fixture
  or expand SQL Server test cleanup.
* Concern: Reopening a database created by the new code does not demonstrate
  compatibility with existing versions, display-name actors and simulated
  approvals. Attaching rule tables to LawStore can also leave cards and reviews
  from previous SQL Server cases behind when only law tables are wiped.
* Impact: Fresh-database tests can pass while upgrades fail, historical evidence
  changes, or existing SQL Server cases become order-dependent.
* Smallest useful change: Add an upgrade fixture built with the current schema
  and representative version/event/review rows. Preserve historical identity
  strings without converting them into new authority; explicitly document the
  new assigned-email-version route for legacy unassigned seeds. Update existing
  SQL Server test cleanup to include rule tables/triggers when initialized,
  keeping it scoped to the existing opt-in test database.
* Action owner: Planning parent, then core/test implementation owner.
* Exact resolving evidence: A named upgrade test in
  src/core/tests/test_rulecards.py opens pre-change persisted data through the
  adapted store, compares full retained history/reviews, repeats initialization,
  confirms append-only rejection, adds a new version and reopens it. A named
  adapter-contract test covers SQL Server table initialization and portable
  query generation locally; extend the existing opt-in SQL Server suite for
  rule-table isolation and lifecycle replay. Record actual SQL Server skips,
  rather than treating contract tests as a live driver run.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Replace prohibited validation paths before execution

* Related IDs: P03-T02; validation lock.
* Evidence: Phase details P03-T02 explicitly select /tmp/zf164 tools, while the
  current execution constraints prohibit file operations in /tmp or other
  temporary directories. Existing selected suites use tempfile.TemporaryDirectory.
* Concern: Following the written commands or default tempfile placement would
  violate the execution boundary. The plan does not identify a permitted
  repository-relative scratch location or control test subprocess placement.
* Impact: Validation cannot be executed as written under the current constraints.
* Smallest useful change: Select permitted repository-local tooling and a
  repository-relative scratch folder; set TMPDIR to its absolute resolved path
  before starting Python/test/package-manager processes. Keep generated fixtures
  and local tooling out of the commit, and clean up only artifacts created by
  this run. Do not inspect or reuse the prohibited tools location.
* Action owner: Planning parent, then validation owner.
* Exact resolving evidence: Revised P03-T02 commands contain no prohibited
  tooling path; the recorded environment and tempfile resolution point inside
  the worktree; loopback fixtures are synthetic; exact-process shutdown and
  final git status demonstrate cleanup without deleting pre-existing work.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Make implementation review findings gate delivery readiness

* Related IDs: P03-T03; full ordered RPI loop; plan acceptance 4-5.
* Evidence: Phase details P03-T03 say to route "any findings as follow-ups"
  before proceeding directly to commit, push and PR creation. There is no
  distinction between accepted residual platform limits and implementation
  defects that invalidate authorization or retained-history acceptance.
* Concern: A single independent review is appropriate and need not be repeated,
  but its substantive findings must be reconciled rather than universally
  deferred. Current wording permits a known bypass or partial-commit defect
  to remain while the implementation is reported as complete.
* Impact: The ordered loop can execute formally without delivering the verified
  outcome requested by the user.
* Smallest useful change: Keep the single review. Require the parent to fix
  implementation-blocking findings in the same loop and rerun affected tests,
  recording resolving evidence. Defer only explicit nonblocking residuals.
  If a blocker cannot be resolved, identify the PR as blocked/draft rather than
  claiming acceptance. Do not require another critique or review pass.
* Action owner: Planning parent and implementation owner.
* Exact resolving evidence: P03-T03 contains the reconciliation gate; the eventual
  changes/review records map every finding to correction/test evidence or an
  explicit nonblocking disposition. The PR distinguishes engineering completion
  from unperformed human approvals and live-platform verification.
* Decision route: Direct planner correction; existing full-loop and publication
  authorization remains in force.

## Strengths and Residual Risk

* Extending the existing stores avoids a second lifecycle implementation and
  keeps immutable history central.
* Dedicated author/owner claims, canonical server-derived actors, rejection of
  caller authority fields, CSRF and existing staff-read gating are appropriate.
* Two unapproved exercise fixtures and simulated events preserve the human/legal
  authority boundary. Owner nomination does not constitute approval.
* No UI, deterministic engine or tenant provisioning is needed for this slice.
  Live ingress, SQL Server/Azure behavior and real approval delegation remain
  explicitly unverified unless corresponding evidence is produced.
* Existing mypy and ruff configuration exempts several migrated targets. Record
  those exclusions when reporting checks; a command's success alone does not
  prove those modules were fully typed or formatted.

## Questions or Blocking Evidence Gaps

* No user question is required. All five findings are bounded planner corrections.
* No missing legal approval should block the labelled synthetic implementation.
  Conversely, its tests must not be presented as legal approval.

## Limitations

* Static critique only: no tests, HTTP app, external platform or driver were run.
  Test names and assertions above are required resolving evidence, not claims
  of observed failures or newly passing tests.
* No prohibited private files were opened. No broader project research or
  delegated assessment was performed. Supplied plan, details and research were
  left unchanged.
* This artifact is the complete actionable finding set for the supplied
  candidate, not the start of serial critique passes.

## Recommended Next Action

* Highest-impact finding: PC-001, source/rule transaction ownership.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T01/P01-T02 to state the owning transaction,
  shared-connection lock and joining review helper, then incorporate PC-002
  through PC-005 in the same finalization.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md | Supplied final-candidate plan |
| .copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md | Supplied implementation and validation details |
| .copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md | Supplied bounded research |
| .copilot-tracking/plans/2026-10-16/issue-211-rule-cards-critique.md | This single complete critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-005 directly,
finalize the plan without another critique, then continue the authorized
implementation, validation, single review, reconciliation and commit/push/PR
loop. No user command or response is required.
