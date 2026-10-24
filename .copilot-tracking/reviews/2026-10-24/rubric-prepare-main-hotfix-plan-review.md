<!-- markdownlint-disable-file -->
---
title: Direct-main preparation hotfix publication blocker
description: Current session state, original Review findings and ordered next work after the local gate preflight blocked
ms.date: 2026-10-24
---

## Authoritative State

All state is managed through the .copilot-tracking folder files. Required
external gate receipts remain external by repository policy; no receipt was
created by the preflight failure below. Do not treat the code validation as
publication approval or the user request as completed.

* Task ID: rubric-prepare-main-hotfix
* User authorized a one-time direct-main fix and push of prepare.py
* Reviewed main base: f1e2d830f17558efd868919de1973ea7244a8841
* Candidate: 5c50b8db, detached at /tmp/ama-prepare-main-hotfix-20261024
* Commit: fix(rubric): honor per-artifact file size limits
* Candidate code: .github/rubric/scripts/prepare.py, two insertions and one deletion
* Additional committed file: dated original RPI evidence, listed below
* Author/committer identity: jmservera, authenticated GitHub no-reply address
* Direct-main push was rejected with GH013; no main update, merge, force-push,
  protection change or scoring dispatch occurred
* The original presentation branch remains docs/capstone-cowork-story
* Original-worktree additions are this Review record and the recovered session
   state listed below; neither changes the isolated candidate

## Session Tracking Artifacts

Percentages describe the named evidence artifact, not completion of the push.

| Full artifact path | Completion | Disposition |
| --- | --- | --- |
| /tmp/ama-prepare-main-hotfix-20261024/.copilot-tracking/changes/2026-10-24/rubric-prepare-main-hotfix-changes.md | 100% | Original pre-gate implementation and Review evidence, committed in candidate |
| /home/jmservera/source/ama/.copilot-tracking/reviews/2026-10-24/rubric-prepare-main-hotfix-plan-review.md | 100% | Current completed Review and ordered Discover handoff, uncommitted in original worktree |
| /home/jmservera/source/ama/.copilot-tracking/rpi-sessions/2026-10-24/rubric-prepare-main-hotfix-state.json | 100% | Current automatic session state and pending post-Review follow-up selection |

Earlier session artifact paths were not recovered by this bounded hotfix task.
Do not invent their paths or completion percentages from the compaction summary.

## Current PR Creation Outcome

PR #445 is open and non-draft: https://github.com/jmservera/ama/pull/445.
Head fix/rubric-artifact-size-limit is
5c50b8dbe3e8abce8b6c4b1ec939e8e53f9ed0da; base main remains
f1e2d830f17558efd868919de1973ea7244a8841. API readback confirms exactly
two files: the two-added/one-removed-line prepare.py correction and the
78-line original dated evidence record. The uncommitted current Review and
session state are not in the PR. No new code commit was made.

Review execution: Complete for the bounded source and PR handoff. Outcome:
Residual work. The owner's request to create a small PR is complete; main
integration, hosted/human acceptance and scorer validation are not complete.
The owner selected Stop automatic session at the post-Review follow-up choice.
Task status is completed, phase Follow-up, automatic session stopped. No child
task, merge or scorer dispatch was started. The ranked follow-ups below are
retained for later explicit selection, not active work.

Last delivery phase: Phase 4, Review, complete. Completed: bounded fix,
three focused regressions, independent conditional assessment, partial full
gate, explicit owner exception, clean gate interruption, rejected normal
direct push, topic-branch publication, PR creation and exact-head/file readback.
In progress: none. Remaining external work: required hosted checks, human
review and owner merge, then owner scorer rerun. No automatic merge or scorer
dispatch occurred; no protections were changed.

### Latest Phase 4: Review Findings

1. The verified correction honors each trusted artifact's size limit with
   global fallback. Registry, root-only wildcard, deck and score files are
   unchanged. The exact reviewed candidate is the PR head.
2. Three focused size-override cases passed. All five project test/lint/type
   groups, namespace/static checks and 12 gate-contract cases passed during
   the broader attempt. Project discovery reported 2392 tests and 468 skips;
   these results are not complete integration acceptance.
3. Full-gate execution was interrupted under the explicit one-time owner
   exception. The external receipt records status failed and Interrupted by
   signal 2. Infrastructure, browser, real SQL, container and scanner gates
   were not completed; no passing receipt is claimed or fabricated.
4. Independent exact-head source assessment found no attributable defect and
   remained conditional on separate validation. No persistent regression test
   was added to this bounded candidate. Human review is not implied.
5. GitHub rejected normal direct-main publication with GH013. The owner then
   authorized the normal small-PR route; PR #445 preserves that protected
   path and explicitly discloses the local-gate exception. No force-push,
   ruleset change, extra score commit or unrelated code was introduced.
6. Small PR creation is complete, not main publication or rubric acceptance.
   Owner review/merge and later real scoring remain. Keep genuine rehearsal,
   delivery, Q&A and thought-leadership evidence gaps visible.

### Latest Phase 5: Discover Follow-Ups

This authoritative order supersedes resolved prerequisite/publication items:

1. Check PR #445 hosted status and support owner review, without merging.
   This is the lowest-effort immediate step toward the trusted-main update;
   required hosted checks and the owner's merge decision remain separate.
2. Plan a change-scoped local publication gate as later selected work. The
   owner identified this engineering improvement after unrelated infra tests
   delayed the rubric fix. Define explicit scope mapping and fail-closed
   coverage; do not generalize this one-time exception or alter policy now.
3. Verify scorer deck recognition after owner merge and a real rerun. Do not
   dispatch scoring without separate authorization. Check deck fingerprint,
   disappearance of the size-skip warning, score and individual floors against
   baseline 55; preserve genuine presentation/delivery evidence limitations.
4. Reconcile stale exact-v2 tests/documentation and durable size-override
   coverage in separately authorized work. Preserve the root wildcard and
   keep unrelated deleted-file fixture repair out of the current small PR.

All task/session state remains under .copilot-tracking. All three listed
artifacts are 100% documented; none of those percentages claims main/scorer
acceptance. The failed receipt remains external as required.

## Earlier Small PR Authorization

The owner requested a small PR after the normal direct-main push was rejected
with GH013, Changes must be made through a pull request. Remote main remains
f1e2d830f17558efd868919de1973ea7244a8841. Use the existing clean candidate
5c50b8dbe3e8abce8b6c4b1ec939e8e53f9ed0da on
fix/rubric-artifact-size-limit, targeting main. The original presentation
branch remains untouched. No duplicate PR or tracked conventional PR template
was found. No new code commit is needed.

The complete gate was stopped with Ctrl+C under the explicit one-time owner
exception. /tmp/ama-prepare-main-hotfix-gate-20261024-3/receipt.json records
status failed and failure Interrupted by signal 2. Eight groups completed:
preflight, five project groups, namespace and static. Infrastructure, browser,
real SQL Server, image and scanner acceptance remain incomplete. The PR must
disclose this rather than claim a complete gate pass.

Current phase: Phase 4, Review, PR publication. Completed: focused tests,
independent conditional source assessment, partial full gate, authorized gate
interruption, rejected direct push, refreshed-base and PR-scope checks. In
progress: publish the topic branch and create the small PR. Remaining: PR
readback and handoff; owner-controlled review/merge and later scorer testing.
No protection change, force-push, merge or scorer dispatch is authorized.

## Owner-Authorized One-Time Publication Exception

On 2026-10-24 the owner explicitly authorized bypassing the complete local
gate for this hotfix only and requested normal publication to main so that
the owner can test the scorer. A change-scoped gate is later work, not part
of this correction. This supersedes the earlier complete-gate prerequisite
for this publication only. It does not authorize changing protections,
force-pushing, dispatching scoring or treating incomplete checks as passed.

The refreshed base remains f1e2d830f17558efd868919de1973ea7244a8841 and
the clean isolated candidate remains
5c50b8dbe3e8abce8b6c4b1ec939e8e53f9ed0da. Next action: interrupt only
the owned gate cleanly, preserve its partial evidence, verify the bounded
diff, push normally to main and verify the remote SHA. Earlier findings
and original evidence remain unchanged; publication is not yet claimed.

## Active Resume After Docker Repair

The latest resume-or-switch request resumes the already recorded automatic
session from Review. It is not used as new manual-to-automatic consent. Mode,
phase and task identity are unchanged. Required human review and exceptional
action confirmations remain binding. After this one Review completes, record
the actual outcome and wait at the ranked follow-up choice; do not start child
work or repeat Review without a later selected task.

The owner's Docker repair is verified: docker version succeeds from a clean
environment with server 29.9.2. Candidate
5c50b8dbe3e8abce8b6c4b1ec939e8e53f9ed0da and freshly fetched main
f1e2d830f17558efd868919de1973ea7244a8841 remain unchanged. Python 3.12.3,
actionlint 1.7.7, Trivy 0.76.0 and Bicep 0.39.26 are available on PATH.

The original adverse Review and the two earlier blocked attempts below are
historical evidence and remain preserved. No passing gate receipt, independent
exact-head acceptance or publication is claimed by this prerequisite check.

* Phase: Phase 4, Review, publication validation resumed
* Completed: Docker repair verified in normal and clean environments; tools,
   clean candidate and unchanged main base confirmed
* In progress: complete exact-head gate, fresh external output directory
   /tmp/ama-prepare-main-hotfix-gate-20261024-3; infrastructure tests have started
* Remaining: independent exact-head assessment, refreshed-base receipt
   verification, authorized normal push and remote SHA readback
* Tracking completion: all artifacts listed above remain 100% documented;
   publication remains incomplete
* Follow-up order: prerequisite restoration complete; exact-candidate gate and
   independent review active; publication conditional on acceptance; hosted
   scoring separately authorized; stale test/documentation work separate

Independent exact-head assessment: Complete, no attributable defects found.
The read-only reviewer verified the full candidate/base diff, unchanged trusted
registry, fallback and override boundaries, trusted-base precedence, unchanged
root-only wildcard and unaffected limits for the other eight active artifacts.
Its isolated source checks and whitespace check passed. It did not execute
extraction, hosted preparation or the full gate. No candidate regression test
was committed; the existing three targeted cases remain separate focused
evidence. This AI-assisted assessment is conditional on the complete gate and
receipt verification, not human engineering sign-off or merge approval.

Gate invocation note: an initial delegated command included an unintended
trailing period and was rejected by argument parsing before creating output.
The corrected invocation started in the same unused external directory.
All preflight checks and the five project test/lint/type groups passed. Do not
treat the expected pre-install namespace-isolation import rejection as a test
failure. Project discovery summaries: core 1243 tests (167 skipped), agents
105 (no skips), API 959 (301 skipped), orchestrator 46 (no skips), importer
39 (no skips); each suite reports OK. Total discovery: 2392 tests, 468 skips.
The 12 gate-contract tests also report OK; their deliberately induced failure
messages are negative-test evidence, not failures of this gate. Namespace
installation/import checks, compilation, JavaScript syntax and workflow lint
also completed. Infrastructure checks are running; required browser, real SQL
Server, image contracts and scanner evidence are not yet established. The
terminal notification contained no input prompt, so no input was sent.

## Earlier Resume State: 2026-10-24

The owner reported Docker started and authorized autonomous continuation.
The isolated candidate and fetched origin/main remain unchanged at
5c50b8dbe3e8abce8b6c4b1ec939e8e53f9ed0da and
f1e2d830f17558efd868919de1973ea7244a8841 respectively. The original
presentation branch was not switched or modified beyond this Review record.
Both Session Tracking Artifacts above remain 100% complete as documentation;
neither percentage represents publication completion. Original committed
evidence and the adverse findings below remain preserved.

Last active delivery phase: Phase 4, Review, Escalate. Phase 5, Discover,
completed for this resumed blocked handoff. No phase step or background
process remains in progress.

* Completed: re-read authoritative tracking and repository gate requirements
* Completed: inspect both worktrees and fetch main; candidate and base unchanged
* Completed: install actionlint 1.7.7 and Trivy 0.76.0 into
  /home/jmservera/.local/bin from official pinned release archives, with each
  SHA-256 checked against its official release checksum file
* Completed: expose /home/jmservera/.azure/bin on the current terminal PATH;
  Bicep 0.39.26 and Python 3.12.3 verified
* Completed: inspect Docker contexts and Docker Desktop WSL mounts; reproduce
  the missing default socket in both normal and sanitized environments
* Completed: attempt the exact-head complete gate with a fresh external output
  path, /tmp/ama-prepare-main-hotfix-gate-20261024-2; blocked on Docker
* In progress: none; Ubuntu WSL Docker engine access requires host correction
* Remaining: verify Docker in the gate environment, complete a new full gate,
  obtain independent exact-head review, refresh main and verify the receipt,
  push normally under the one-time authorization and verify the remote SHA

Pinned tool download/checksum evidence remains external at
/tmp/ama-rubric-tools-20261024-WnUN6F. No shell startup file, Docker context,
project dependency pin, implementation commit or remote ref was changed.

### Latest Phase 4: Review Findings

1. Candidate integrity is preserved. The only behavioral correction remains
   the per-artifact size limit in compute_state. The root-level wildcard,
   artifact registry, deck and score records remain unchanged. Main still
   equals the reviewed base; no reconciliation is currently required.
2. Focused correctness remains the previously recorded three passing cases,
   clean whitespace and script diagnostics. No source changed during this
   continuation, so those checks were not redundantly rerun. They do not
   replace the complete gate or independent exact-head assessment.
3. The second complete-gate attempt used /usr/bin/python3 and the unchanged
   candidate/base, requesting /tmp/ama-prepare-main-hotfix-gate-20261024-2.
   It stopped during Docker identity collection with a nonzero docker version
   result, before any project, browser, SQL, image or scanner suite ran.
   No passing receipt exists; this is blocked validation, not a test failure.
4. Missing user-level tool prerequisites were restored. actionlint 1.7.7
   matches CI; Trivy is exactly 0.76.0. Both official release checksums passed.
   Existing Bicep 0.39.26 is now on the current terminal PATH and Python is
   3.12.3. No elevated install, uv migration or project-pin change occurred.
5. Docker Desktop mounts and the native Docker CLI are present, but Ubuntu
   still has no /var/run/docker.sock. A sanitized invocation also fails to
   connect. Windows desktop-linux uses a named pipe and cannot substitute for
   the gate's Linux default endpoint. Enable or repair Ubuntu WSL integration;
   no manual socket shim, cloud fallback or gate suppression was introduced.
6. Publication remains incomplete. The candidate is unpushed, independent
   review and receipt verification remain pending, and no scoring dispatch,
   merge, protection change or score edit occurred. Preparation correctness
   alone still cannot establish delivery or rubric acceptance.

### Latest Phase 5: Discover Follow-Ups

Authoritative order after this continuation:

1. Restore Docker engine access for Ubuntu under Docker Desktop Settings,
   Resources, WSL Integration, then Apply and restart as required. Verify
   docker version from this distro and the gate's clean environment. Pinned
   actionlint/Trivy installations are complete; retain /usr/bin,
   /home/jmservera/.local/bin and /home/jmservera/.azure/bin on PATH for runs.
2. Resume in /tmp/ama-prepare-main-hotfix-20261024, preserving presentation
   work. Fetch main and seek owner direction if the base moved. Run the full
   exact-head gate with a new external output directory, obtain independent
   exact-head review and verify its receipt against freshly fetched main.
3. Only after every gate succeeds, use the existing one-time authorization
   for a normal direct-main push and remote SHA readback. Stop on protection
   rejection; do not force-push or alter protections.
4. Obtain a new hosted rubric assessment only with separate authorization.
   Check the deck fingerprint and disappearance of the size-skip warning,
   compare score and individual floors against baseline 55, and retain genuine
   rehearsal, delivery, Q&A and thought-leadership gaps.
5. Reconcile stale exact-v2 tests/documentation only as separately authorized
   work. Preserve the root wildcard and keep the unrelated deleted-file
   fixture repair outside this bounded hotfix.

## Prior Blocked Phase and Step Status

Last active delivery phase: Phase 4, Review, Escalate because publication gates
cannot execute. Phase 5, Discover, completed for the blocked handoff.

* Completed: refresh main and inspect the clean original worktree
* Completed: isolate latest main, apply only per-artifact size handling
* Completed: execute all three existing size-override regression cases against
  the exact isolated main module; 3 passed, 52 deselected
* Completed: git diff --check; editor diagnostics show no script errors
* Completed: commit candidate and original dated evidence using privacy-safe identity
* Completed: attempt required complete gate and diagnose preflight blockers
* In progress: none; publication is blocked on host prerequisites
* Remaining: restore gate prerequisites, full exact-head gate, independent review,
  refreshed-base receipt verification, normal direct-main push and remote readback

## Phase 4: Review Findings

1. The bounded script fix directly addresses the verified producer defect:
   compute_state now honors each artifact's configured max_file_bytes. The
   registry and root-level wildcard remain unchanged, so the deck is not
   compressed or renamed to disguise the filtering failure.
2. Focused regression evidence passed: global fallback, inclusive override
   boundary, rejection above the override and unchanged non-deck limits. This
   is narrow evidence only; the complete gate and independent review are not done.
3. Gate command used /usr/bin/python3 (3.12.3), candidate 5c50b8db and base
   f1e2d830f17558efd868919de1973ea7244a8841, with output requested at
   /tmp/ama-prepare-main-hotfix-gate-20261024-1. It stopped before creating
   that directory: BLOCKED: Missing required tool: bicep.
4. A bicep binary exists in /home/jmservera/.azure/bin but is not on PATH.
   actionlint and trivy were also absent from PATH. Trivy 0.76.0 is required.
   No download, elevated install or infrastructure change was attempted.
5. Docker is the controlling host blocker. docker version reported that Docker
   could not be found in this WSL 2 distro and requested Docker Desktop WSL
   integration. This host setting requires owner action; no cloud fallback,
   gate suppression or protection bypass is authorized.
6. The candidate is locally committed but unpushed. The requested publication
   remains incomplete. Deck recognition, a future score or workflow success
   must not be confused with rehearsal, delivery, Q&A or thought-leadership evidence.

## Phase 5: Discover Follow-Ups

Ordered prerequisites and follow-up work:

1. Enable Docker Desktop WSL integration for this distro and verify the local
   engine. Add the existing bicep location to PATH and supply required pinned
   gate tools, including actionlint and Trivy 0.76.0. Do not use a cloud fallback.
2. Resume from the isolated candidate, preserving the presentation branch.
   Fetch main; if the base moved, reconcile with owner direction. Run the full
   exact-head local gate with a new external output directory, obtain independent
   exact-head review and verify the receipt against freshly fetched main.
3. Only after those gates succeed, push the bounded candidate normally to
   main under the explicit one-time authorization and verify the remote SHA.
   Stop on a remote protection rejection; never force or change protections.
4. Obtain a fresh hosted assessment only with owner authorization. Verify the
   deck fingerprint and absence of the size-skip warning, then compare the
   score and criterion floors with baseline 55 without fabricating evidence.
5. Reconcile stale exact-v2 tests/documentation separately if authorized.
   Preserve the wildcard and keep unrelated fixture repairs out of this hotfix.
