<!-- markdownlint-disable-file -->
# RPI Phase Details: hazard-referral-controls-85

Task ID 85, date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md.
Research: .copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; current actor/identity/failure regressions pass | P01-T01 |
| P02 | Complete; final targeted/static and actual SQL evidence recorded | P02-T01 |
| P03 | Review/correction ONE and draft PR #388 publication complete; independent acceptance outstanding | P03-T01/P03-T02/P03-T03 |

<!-- rpi:phase id=P01 -->
## P01: Correct hazard evidence boundary

<!-- rpi:task id=P01-T01 -->
### P01-T01: Current identity and failure scope

Evidence C12 reproduces three defects. Use canonical `_actor` for current
registered staff, including fresh SQL lookup; do not build another authority
registry or alter delegation rules. Hazard-owned context should retain current
actor checks and independent identities, validate again under SQL save writer
transaction and discard failed staged state/audit before recovery reads. Preserve
original exception; log/add explicit uncertainty when recovery fails.
Capture a deep copy of pre-operation pending audit before staging hazard
events. Restore it even if existing SQL save eagerly discards after authority
or conflict refusal. Clear/restore hazard context in finally. Repeat separate
caller and destination subject validation inside writer lock.

Likely targets: new core/hazard.py, workflows.py hazard methods only, minimal
sqlstore.py import/validator hook. Existing stock/finance/provider/change hooks
must remain intact. No source edits outside this worktree.

Retain original raiser and repair-recorder identities with code and OID, so
email changes or aliases cannot establish independence. Missing legacy
identity cannot invent approval: retain conservative existing email/name
fallback. Destination/receiver must not be satisfied by stale code alone.
JSON is not SQL-atomic: save before hazard/emergency audit, restore known
pre-save failure snapshot; if audit fails after replacement, preserve committed
state and annotate/log uncertain audit completeness with original error.

Completion: fail-before actual assertion output; after-fix current/revoked/
alias tests and atomic failure tests. No test removals or >12 semantic additions.

<!-- rpi:phase id=P02 -->
## P02: Persistence and documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Canonical parity, failure evidence and KB

Use existing tiny fixture only, do not modify dataset.py. Canonical JSON/SQLite
hazard suite plus HTTP auth/lifecycle. Add isolated MSSQL adapter to reuse
semantic tests without pretending SQLite-specific transaction traces are SQL
Server proof. Create only own disposable loopback-bound container with random
unlogged secret, no shared DB; clean exact own ID even on failure.

Include transaction-time staff revocation, write/audit failure with durable
reopen and recovery-read uncertainty. Run relevant core/API regressions and
configured lint/format/mypy. Run existing scenario manifest validation with
exact hashes; refresh only if hashed source actually changed.
Within the method budget, use valid unchanged caller with removed/demoted/
same-code substituted destination, before invocation and SQL commit. Test
distinct prior pending audit on both authority/conflict and generic failures,
including recovery-read failure; retain it exactly once, no hazard success
entry, no mutation and no leaked validation scope. Separately test JSON
pre-save refusal and post-save audit failure.

Update core/API READMEs and existing profile-review hazard synthesis, index and
append-only log. Disclose no browser run required because no web edits;
screenshots never count as accessibility acceptance.

Completion: actual commands, test counts, all failed attempts and environment
skips in changes. No claim of actual statutory compliance, verified receipt,
professional approval, operational delegation or live acceptance.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review once and deliver

Fresh independent worker activates rpi-review; exact artifact/source scope.
Assess all four criteria, actor/code/OID independence, transaction validation,
failure quarantine, preserved gates, actual SQL results and scope discipline.
Worker may write only dated review artifact. Preserve all adverse findings.
Caller authorizes concrete fixable finding correction cycle ONE, max TWO, but
not a fabricated independent Pass from parent self-verification.

After review, reconcile state, plan/details/changes and findings. Use fresh
gh api user identity for local noreply author/committer. Commit only owned
source/docs/phase artifacts with Conventional Commit and Copilot trailer.
Normal push and main PR Refs #85; no closing keywords, merge or rewrite.
Record exact final head and PR. No operational human review is ticked.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Authorized RV-001 correction ONE

Original independent Review reproduced committed release followed by _sync
failure; blanket restoration replayed earlier committed audit twice and gave
no persisted-outcome warning. Preserve original Review unchanged. This is
ordinary concrete implementation work explicitly authorized by the caller.

Mark successful COMMIT before SQL post-commit cache/sync work, only in active
hazard context. On later failure, reload without replaying pending baseline,
retain original error and explicitly annotate/log committed outcome. Before
COMMIT, existing quarantine/prior-audit behavior remains required.

Canonical tiny two-store subcases failed before fix: unrelated sibling
write advances sequence, release commits, one-shot/persistent post-commit
sync fault returns original error, reopened release/success audit/prior audit
each exactly once. Reused within the existing canonical SQL failure method and
its actual disposable SQL binding; ten total added semantic methods remain,
with two adapter overrides and three method bindings. No second Review or
independent Pass from self-verification. Post-correction core168/20skips,
API39/no skips and actual SQL16/oneJSON-onlyskip pass; configured gates pass.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Publication after correction evidence

Reconcile completed plan/details/changes/state while retaining Review's
Complete / Not accepted result and independent final-head closure limitation.
Commit owned paths, normal push, main PR Refs #85; no merge or closing action.
