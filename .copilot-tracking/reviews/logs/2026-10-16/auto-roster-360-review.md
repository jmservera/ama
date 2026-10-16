# Automatic demo roster review

Task auto-roster-360, Refs #360. One post-implementation review.

## Opening Review State

Review boundary: the complete requested offline implementation, not a deployed
tenant or SQL acceptance. Research, plan, details, one critique, changes record
and executable validation are available. Source, docs and test changes are
read-only during this review; only this review record is written.
Implementation tasks P01 and P02-T01/T02 are complete; P02-T03 intentionally
contains this Review and subsequent commit/push/PR delivery.

## Compared Artifacts

* `.copilot-tracking/research/2026-10-16/auto-roster-360-research.md`
* `.copilot-tracking/plans/2026-10-16/auto-roster-360-plan.md`
* `.copilot-tracking/details/2026-10-16/auto-roster-360-phase-details.md`
* `.copilot-tracking/reviews/2026-10-16/auto-roster-360-plan-critique.md`
* `.copilot-tracking/changes/2026-10-16/auto-roster-360-changes.md`
* Changed infra scripts, manifest guidance, Bicep profile tag and three test files.
* `infra/README.md`, cut-over evidence pack, reference index and log.

## Reconciliation and Criterion Assessment

| Boundary | Assessment |
| --- | --- |
| Missing/template selection | Only exact original template can be replaced; populated invalid input retains placeholder/role/ID/duplicate/mode refusal. Symlink and changed-input checks prevent accidental replacement |
| SQL authority | Existing subprocess and SQL query remain; generated codes/roles/supplier scopes come from candidate metadata. Existing bound SQL deliberately blocks regeneration before Entra changes |
| Admin and assignment | One eligible case-insensitive admin prefix is selected, zero/many count and one plain question or explicit UPN; first sorted ProgrammeManager code reserved. Sorted candidate set and seeded shuffle produce distinct, reproducible mappings |
| Human/resource filters | Shared validator retains ConfRm/desk/workspace checks and adds naming/non-user checks. Individual-mailbox Graph purpose is positive evidence; unknown/denied classification fails closed. Persisted generated users rechecked before auth mutation |
| Privacy/persistence | Versioned seed/staff envelope is accepted by both readers; no names/UPNs/IDs/supplier names in generated output. 0700/0600 and atomic replace are tested; readonly preview returns without file/auth/SQL changes |
| Production guard | Development profile plus demo/test/dev environment required. Production/unknown/conflicting evidence, missing default parameter and unrelated deployment cannot authorize generation. Nested module tags bind only via exact output resources. Caller Bicep tags cannot override profile |
| Continued flow | Fresh roster reaches original registration/assignments/credential verification before SQL check, separate confirmation and apply/restart. Final summary explicitly states SQL binding/restart confirmation. Existing lock, read-only and drift tests remain |
| Shortage | Exact post-admin deficit is reported and generation stops. This is the owner's permitted stop alternative; no duplicate-user or reuse bypass |
| Documentation | Current runbook supersedes template instructions while evidence keeps historical observations distinct. Per-criterion audit records actual offline evidence and unmet live boundaries; no issue-body boxes changed |

## Critique and Implementation Decisions

Exactly one critique was executed with original verdict Revise. PC-001 through
PC-006 are explicitly disposed in the plan and supported by implementation:
mailbox-purpose contract, authoritative resource-bound profile checks, shared
envelope decoder, bound-SQL stop, private admin omission from handoff and
terminal admin/shortage cases. No repeat critique or unconfirmed policy change.

Ordinary implementation updates preserve user intent: the permitted shortage
stop rather than reuse, nested deployment tag parameters to match Bicep modules,
and persisted-user mailbox revalidation. No runtime role/capability, network,
approval, private data or legacy source changes. Shared helper extraction avoids
inconsistent parsing/eligibility between setup and SQL. No independent review
agent was necessary for the already-contained evidence boundary.

## Validation Evidence

* Passed: full offline infra suite, 282 tests, zero skips, including compiled
  Bicep and profile-tag override assertions.
* Passed: focused SQL initializer tests, 15 tests.
* Passed: scoped mypy for setup, initializer and shared helper, using
  follow-imports skip and import-untyped exclusion for existing untyped packages;
  shared helper also passed strict mypy.
* Passed: Ruff E/F/I/B/UP for shared helper and Bicep policy tests, and scoped
  existing-file checks with documented pre-existing E501/E402/I001/B007/UP017
  exclusions. New-line length findings: zero. Strict surfaces formatted.
* Passed: 32 local responsive loopback API authentication tests, including
  synthetic app health/role boundaries. No outbound model/Azure setup.
* Passed: git diff whitespace review and added documentation link targets.
* Not run: live setup, tenant/mailbox authority, real-person eligibility,
  browser sign-in, Azure SQL apply/restart, deployments, migration or retirement.
  Explicitly prohibited by this delivery request, not silently skipped.

## Findings and Routing

### RV-001: Medium, residual operational evidence

Evidence: the acceptance pack explicitly labels original live criteria c/d/e
unmet; all current assignment/SQL receipts are mocks. MailboxSettings.Read
availability for every candidate cannot be inferred from existing directory
management scopes, and real tenant access was not tested.

Impact: the operator may receive a fail-closed permission/profile/binding
blocker; no claim that a deployed default run has completed is justified.

Destination: distinct authorized operator follow-up after required owner
migration/cost approval, not a source defect or automatic Azure action here.
Verify real mailbox classification/read authority, restore any already-bound
SQL roster, then obtain browser/SQL/serving-replica acceptance evidence.

## Follow-Up Assessment

The plan's live-person/Exchange/tenant/SQL/browser follow-up is valid and remains
outside active source tasks. Owner/operator action is required; named exercise
Legal/Compliance/DPO ownership does not imply tenant authority or operational
approvals. No new discovery merely to populate follow-ups.

## Outcome

Execution: Complete. Outcome: Residual work, limited to the explicitly separate
live/operator acceptance boundary above. No material implementation defect found
in the reviewed offline boundary. No overall production or issue acceptance.
No source corrections or repeat Review initiated.

## Handoff

Parent completes the already-requested privacy-safe commit, topic push and PR,
leaving merge and issue checkboxes to the owner/coordinator. This one Review is
complete; RV-001 remains a distinct operator work item.
