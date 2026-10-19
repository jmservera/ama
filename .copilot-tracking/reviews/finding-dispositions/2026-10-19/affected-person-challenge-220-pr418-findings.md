---
title: PR 418 bounded five-comment implementation dispositions
description: Evidence-led correction dispositions, not a replacement original Review or independent exact-head acceptance
ms.date: 2026-10-19
---

## Boundary and provenance

Same automatic task 220, branch feat/affected-person-challenge-220, PR #418.
Actual review comments were retrieved through
`gh api repos/jmservera/ama/pulls/418/comments`. Platform COMMENTED is advisory;
all five substantive findings are confirmed and corrected, not dismissed.
The clean worktree was fast-forwarded from published source d3dfd82a to genuine
rubric-only bot commit 63f5b057 before corrections. Workflow 39321399922
successfully records rubric 48, baseline 48. No rescoring or workflow workaround.

This is implementation-owned finding disposition. Coordinator independent
exact-head assessment remains mandatory before any push authorization.
No second original Review or critique, remote write, merge or whole-issue
acceptance is performed. Refs #220; PR remains open with no closing reference.

## Dispositions

| Actual comment | Finding and confirmed cause | Implemented result | Primary proof |
| --- | --- | --- | --- |
| [4318714670](https://github.com/jmservera/ama/pull/418#discussion_r4318714670) | Challenge POST success refreshed an obsolete case through the new route controller | Capture dispatch signal; after success clear the old form's draft but skip refresh on aborted route. No signal on POST, cancellation or retry | `checks.challenge_browser_check --navigation`: two committed writes across ZF-5/list navigation, zero stale-case GETs/retries/page errors. Current/history journeys remain passing |
| [4318714784](https://github.com/jmservera/ama/pull/418#discussion_r4318714784) | Only ZF-1 was marked touched; direct matching-case ownership edits were not durably saved in SQL | Call `_case(case["id"])` for every matching synthetic owner assignment | `TaskReleaseRecord.test_priority_fixture_ownership_survives_reopen_for_every_matching_case`: all JSON/SQLite owner code/name/role values persist; reopened candidate and deterministic sets agree. Existing forged-identity no-write guard passes unchanged |
| [4318714876](https://github.com/jmservera/ama/pull/418#discussion_r4318714876) | Catalog/export evaluated all cases per proposal; writer loaded full case JSON | Once-per-read correction dependency index; current correction-only SQLite JSON/SQL Server OPENJSON writer queries, never reuse a stale read index | 52 proposals/60,000 generated homes: exactly one index build per catalog/export. 60,000 uncorrected generated SQL bodies plus one correction: one returned/decoded target and one query. Native competing correction and cross-case policy tests pass |
| [4318714963](https://github.com/jmservera/ama/pull/418#discussion_r4318714963) | `_rec_view` exposed cross-case correction references without dual entitlement | Pass requesting user on generation/latest/review; recheck current registered identity and both evidence rights; filter references only. Export reuses the same reader boundary | `test_challenge_priority_responses_use_current_dual_entitlement` on JSON/SQLite/native; actual HTTP generation/latest/reject regression. Non-entitled coordinator sees stale flags, no IDs; entitled control sees exact ID. Runtime permission removal/current role downgrade withhold IDs |
| [4318715035](https://github.com/jmservera/ama/pull/418#discussion_r4318715035) | Release-denial audit lived inside failed-disposition audit rollback | Validate current actor/ownership/release first; keep denial-only audit outside rollback, mutation/save/accept-edit audit inside | JSON/SQLite missing-release tests preserve denial and unchanged persisted proposal; actual revoked/changed-model tests preserve denial. JSON/SQLite/native failed-save and native concurrent-correction tests remove failed acceptance/edit state and audit |

Actual HTTP review on a fresh request thread also reproduced uninitialized
`store.local.pending`. Initialize existing SQL `_touched()` before rollback
snapshot, matching resident operation practice. This directly coupled fix does
not change current actor, release, rowversion or dependency guards.

## Validation and retained failures

* Final combined focused run: 148 tests, 146 pass, two existing explicit skips:
  JSON-file rollback-only test on SQLite and opt-in local browser test.
* Final-source native SQL Server: seven tests pass, zero skips, task-owned
  loopback-only disposable server; responsiveness verified and container removed.
* Chromium 156.0.8078.4: navigation, current and history journeys pass.
  Current/history axe 4.10.3: seven scopes, zero violations/incomplete results.
  Reduced motion and 320/390/1280 reflow retain prior bounded behavior.
* Configured Ruff/format/mypy for complete core/API pass (128/62 files); Node
  syntax check for panels.js passes. No tooling/skip/entitlement suppression.
* Generated read/query scan bounds are constructed SQLite/in-memory evidence,
  not a native 60,000-home performance/latency or operational acceptance claim.
* Preserve initial format/type failures, browser synchronization failures,
  observed stale refresh before the intended handler received the guard, and
  the one real HTTP thread-local error. Final success does not relabel them.

Primary fresh raw logs, browser JSON, actual comment payload and SHA256 manifest:
`/home/azureuser/.copilot/session-state/5d61a4a7-dd64-4f31-93c3-14774e9f0718/files/issue220-pr418-findings-evidence/`.
Successful outputs are focused-final-02, static-final-02, native-final and three
browser *-04 JSON files. Original excluded evidence has not been relocated or
reconstructed. Fresh all17 receipt is pending at this committed freeze snapshot
and will be external; the historical source receipt cannot certify this HEAD.

## Changed web scope

Current guideline source was freshly retrieved before implementation and review:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Read panels.js and assessed the changed challenge lifecycle in its form context.
No styling, text, motion, Fluent tokens, semantics or manual-approval change.

### src/api/src/zava_forward/api/web/panels.js

Pass for changed challenge-route lifecycle. Pre-existing out-of-scope observations:

* src/api/src/zava_forward/api/web/panels.js:154 - adjacent unchanged resident form also refreshes after a delayed write without dispatch-route fencing; separate follow-up, not this challenge-handler fix.
* src/api/src/zava_forward/api/web/panels.js:30 - unchanged commitment list is unbounded above 50; separate existing-list performance follow-up.

No fresh full-file guideline conformance, screen-reader or human acceptance
claim. These unrelated observations do not authorize broad UI redesign.

## Original outcomes remain unchanged

Original research, plan critique Revise and original Review Partial / Not accepted
are byte-identical to the fetched source. Review SHA256:
`eec22d64aea801d63ae007c5c8b6e4b69709099d70f4e3a7c9b8f4dc2744fc8e`.
Critique SHA256:
`1a37cbb8f57d8e673eac17d86b81b983ec6244a09eb104d7c157109ac16ffaf0`.
Original failures and acceptance limits remain in changes/history. Whole issue
#220 stays open. Other assistant/form integration and qualified/resident,
human/accessibility, operational/native-load acceptance remain separate work.
