---
title: Issue 115 digest anchor phase details
description: Failing-first source correction and bounded validation details
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: 115. Slug: issue-115-digest-anchor. Related plan:
.copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md.
Evidence: .copilot-tracking/research/2026-10-18/issue-115-digest-anchor-research.md
C1-C8/W1. No blocking unknowns; operational gates remain separate.

## Phase Index

| Phase | Intent | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Reproduce then correct only recognized-anchor absence | Complete | P01-T01, P01-T02 |
| P02 | Local validation, one Review and authorized publication | Complete, coordinator exact-final-head review remains separate | P02-T01, P02-T02 |
| P03 | Authorized correction ONE after coordinator NOT ACCEPTED | Delivered; SAME coordinator acceptance pending | P03-T01, P03-T02, P03-T03 |

## P03: Qualify Remote Anchor Evidence

User2026-10-18 authorizes correction ONE, max two, same task/PR404; no new Review.
Coordinator Medium: digest-not-a-count.json={} false green even after initial
unrelated-only guard. Original assessments remain frozen and historical.
Essential count/head/chain/algorithm/year/first_prev and publisher filename
invariants are recorded in correction-one receipt; at timestamp and extra
fields do not need a new schema. Fixed diagnostic invalid-anchor problems must
fail report and CLI even with another valid anchor, without exposing content.

P03-T01: add existing fake-based malformed filename and payload matrices,
including syntactically valid names with {}, scalars/collections, incomplete
fields, wrong count/hash/algorithm/chain/year/first_prev, invalid JSON/encoding;
CLI and direct report. Record expected failures before production edit.
P03-T02 depends on failures: qualify before ledger readers, explicit unsuccessful
fixed problem, no broad catches/defaults, no blob mutation. Canonical count name
uses minimum10 digits, allowing larger counts, no new clock-based year cutoff.
P03-T03: same sanitized task TMPDIR/venv focused/coupled/full unittest and configured
Ruff/format/mypy/diff check, original parity and correction hashes. Commit normal
push/PR404 actual-head correction receipt; main unchanged or stop integration.
End with same coordinator follow-up, never a self-issued Pass or second Review.

P03-T01/T02 actual evidence:3 malformed methods failed before source change
(112 assertion failures/30 malformed-data errors); after qualification25 focused/
coupled and44 full orchestrator tests pass, zero skips. Configured Ruff/format/
mypy pass. Frozen original hashes unchanged. Source d0088301ba64cba8c632b6d0b4dcd80474580e41 committed and normally pushed;
P03-T03 publication receipt is complete, stopped for same coordinator.
coordinator NOT ACCEPTED remains authoritative until same-reviewer follow-up.

Single original critique Complete / Revise, PC-001 applied below. No new critique
or user choice needed. Frozen original remains unchanged.

<!-- rpi:phase id=P01 -->
## P01: Establish failing-first regression and minimal correction

Context: list_digests admits all .json; core chain/year checks can pass without
supplied digests, so `if not names` is insufficient. Intent: missing remote
evidence must never become a successful heartbeat. Boundary: no schema/filename
grammar redesign, core ledger changes or operational claims.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add and run bounded regression/control tests before source edit

Use existing FakeImmutableContainer and constructed Store in a task temp dir.
Pre-create `/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp`;
every sanitized test command must pass that absolute path as TMPDIR after
`env -i`. Before first regression, verify `tempfile.gettempdir()` equals that
root in a fresh process. No test fixture source change needed for redirection.
At most eight new methods, none removed, no shared fixture edits. Missing
anchors: unrelated.json bytes only; assert intact false, counts0/0, digests
problem explicitly missing recognized anchors; run CLI asserting exit1/alert
and no OK. Repeat with local digest(s) but no remote anchor to reject local
fallback. Genuine empty ledger has zero audit entries, not a missing fixture:
no blobs or unrelated-only must fail; explicit remote zero-count GENESIS head
succeeds; nonempty remote head/year against empty ledger fails.

Good controls: head-only, and a genuinely completed single 2024 year anchor
for linked 2024/2025 entries. Each verify and CLI passes with/without unrelated
invalid JSON. Assert unrelated bytes are never downloaded. Existing remote
mismatch checks remain intact; add unrelated bytes to a negative control if useful.
Dependency: single critique dispositions. Completion: chosen regression fails
against unchanged source for the expected actual true/exit0 behavior, not an
import/setup error. Preserve output and source hashes.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Correct recognized-anchor absence guard and narrow guide

After expected regression failure, replace all-names absence with no recognized
heads AND no recognized years. Use existing `check="digests"` report shape,
problem text explicitly names missing recognized head/year anchors. No new
exception fallback, signature, marker, transport or publication behavior.
Clarify README that unrelated JSON is not anchor evidence and missing recognized
anchors alert. Do not alter KB, other README sections, policy or authority text.
Dependency: P01-T01. Completion: tests pass and diff is limited to approved targets.

<!-- rpi:phase id=P02 -->
## P02: Validate, reconcile and hand off for one original Review

Context: configured digest migration exclusions limit Ruff/typing assurance;
tests must check actual observable behavior. All commands run in `env -i`
with PATH explicitly set and only public fixture PYTHONPATH (not mvp or source
workarounds), plus the explicit absolute worktree TMPDIR above. Use installed
task-venv Python and tool executables.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run local checks and record exact evidence

From root run focused digest suite plus coupled core `test_recovery` ledger/year
classes after inspecting its existing harness. Run complete orchestrator discovery
from its folder with core/tests fixtures. Run configured `ruff check .`,
`ruff format --check .`, `mypy` from orchestrator and `git diff --check`.
Record actual counts, failures/skips, tools versions and SHA-256 hashes.
All focused/coupled/full discovery invocations retain the same TMPDIR; remove
only task-owned scratch and the empty root when finished, record cleanup.
No SQL/Docker/Azure/browser: unchanged persistence/image/cloud/UI surfaces and
caller offline boundary; report N/A/not run, not successful acceptance.
Dependency: P01. Completion: reconciled plan/details/changes, no silent failures.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Freeze original independent Review and publish delivery

Use a fresh independent worker, activate rpi-review, one original assessment at
candidate commit with exact source/test/README hashes and full evidence pointers.
Allowed write: original .copilot-tracking/reviews/logs/2026-10-18/issue-115-digest-anchor-review.md
only. No nested Review or second original. Freeze critique/Review hashes.
If findings require bounded fixes, at most two source-correction cycles with
separate receipts, never rewrite originals or call them independently accepted.
Resolve gh api user, local noreply author+committer and Conventional Commit with
required Copilot trailer. All task artifacts must be committed. Check remote
main still equals pinned base before publication; if advanced, stop integration
and report, no rebase/force-push. Push exact topic and PR main, Refs #115,
unmet operational gates, source candidate versus final receipt commit distinct.
Record actual publication and checks rather than stale authorization language.
Completion: clean committed worktree, remote head verified, PR URL/head/base,
state waiting for coordinator independent exact-head review.

Actual source candidate d53a7c68245dc708c628bb37853c308d9811fcbe received the
single original independent Review: Complete / Residual work, bounded source
Conformant, no source defects. Zero source-correction cycles; original critique
and Review frozen with hashes in changes. Publication completed on
https://github.com/jmservera/ama/pull/404, initial delivery commit
211458f94c25a705971b0f912b1990f0b8de7aec; source bytes unchanged from candidate.
Final evidence-only receipt reconciles actual publication and stop state.
Source/policy acceptance has not changed. All task markers complete; coordinator
exact-final-head review and RV-002/003/004 remain distinct external follow-ups.
