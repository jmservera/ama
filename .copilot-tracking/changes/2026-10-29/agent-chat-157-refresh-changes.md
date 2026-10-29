<!-- markdownlint-disable-file -->
# RPI Changes: agent-chat-157-refresh

## Metadata

* Task ID: pr-503-refresh-2026-10-29
* Related plan: .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md
* Implementation date: 2026-10-29

## Execution Status

In progress; full-plan scope. P01/P01-T01 complete; P02 active, P03 pending.

## Execution Summary

Rebase the explicitly selected active draft branch, preserve both sides'
runtime/documentation intent, validate locally and leave commits unpushed.

## Commands and Results

### Intake and P01 preflight

* `git status --short && git branch --show-current && git remote -v`:
  clean initial worktree; feat/agent-chat-157; expected origin.
* `gh pr view 503 --json state,isDraft,headRefName,baseRefName,title,body`:
  OPEN draft, main base, correct head; original acceptance Not accepted.
* `git fetch origin`: success.
* `git log --oneline origin/main..HEAD && git diff --stat origin/main...HEAD`:
  four topic commits; 26 changed files.
* `gh pr checks 503`: exit 1; source jobs passed on old head, rubric
  conclusion failed and rubric/score pending.
* `gh run view 40584414999 --job 122472998400 --log-failed`:
  missing tool/data report-as-failure; no fresh CI inferred.
* `/tmp/mv/bin/python --version && /tmp/mv/bin/ruff --version &&
  /tmp/mv/bin/mypy --version`: 3.12.3 / 0.17.1 / 2.4.0.
* Fresh `git status --short`, branch, rebase-directory absence and
  `gh pr view 503 --json state,isDraft,headRefName,baseRefName`: correct
  active branch; only this loop's new evidence untracked; no rebase underway.
* `git fetch origin main && git rev-parse HEAD origin/main`: success.
  Pre-rebase HEAD: 949aafaf7260965671297eabd6335a0311b9b45d.
  Captured main: 5653547507f3056f09a726a18516237728da5e5b.
  All reconciliation/snapshot checks use this immutable captured target.

## Implementation-Time Plan and Detail Updates

One independent critique: Complete / Revise. PC-001 through PC-003 applied.
PC-004's focused-only recommendation applied; its claimed parent prohibition
on external temporary writes rejected as unsupported by parent instructions.
No second critique and no user decision required.

### P01 rebase and semantic integration

* `GIT_EDITOR=true git rebase 5653547507f3056f09a726a18516237728da5e5b`:
  stopped at first topic commit with five conflicts: log, core chat_panel,
  API server, chat.js and API test_chat_panel.
* Inspected main and topic stages and adjacent source. Preserved all main
  log entries then appended topic entry; README auto-merge retained both.
* Kept main's five skill lenses, general workflow sources and audit semantics,
  forwarding skill through the new receipt wrapper and applying identical
  lens transformations before completion-time comparison. Kept typed provider
  usage receipts, admission and bounded history/source serialization.
* Counted selected-skill system text inside the context limit, preserving
  skill/context/audit metadata on limit fallback. Preserved main's explicit
  unexpected-provider error logging.
* Kept both skills and privacy-status endpoints; retained main's version-aware
  clearSubmittedQuestion and topic privacy-ready guard, described warning,
  refusal status and unsaved tracking. Both test groups retained.
* Initial combined apply_patch failed to match a conflict block; no files
  changed in that failed attempt. Corrected coherent patch succeeded.
* `gh api user --jq '{id,login}'`: 8036360 / jmservera.
  `git config --local user.email '8036360+jmservera@users.noreply.github.com'`
  and local user.name set before rebase continuation/commit creation.
* `/tmp/mv/bin/ruff format src/core/src/zava_forward/core/chat_panel.py`:
  one file formatted.
* `git add <five resolved paths> && GIT_EDITOR=true git rebase --continue`:
  all four commits replayed, success. Rebased tip 25a45dce.
* `git merge-base --is-ancestor <captured-main> HEAD`: passed.
  `git diff <captured-main> -- .github/rubric
  docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`:
  empty; exact main copies already retained, no restore/edit needed.
* `git diff --check` and `node --check src/api/src/zava_forward/api/web/chat.js`:
  passed. No unresolved paths.
* Existing 8,000-character redaction regression updated to expect the topic's
  intentional 1,000-character inference-limit fallback while still testing
  redaction/storage bounds. Added two API integration tests: selected-skill
  source revocation/usage and selected-system context-cap/audit preservation.

## Validation Command and Coverage Contract

All commands below use /tmp/mv/bin tools from the stated project directory.
Define root as /home/azureuser/source/ama-wt/chat157. Ordered project-local
paths plus sibling sources/tests prevent stale editable imports.

| Working directory | Exact command | Coverage |
| --- | --- | --- |
| src/core | `PYTHONPATH=src:tests:../agents/src:../agents/tests:../api/src:../api/tests /tmp/mv/bin/python -m unittest test_chat_panel test_chatthreads test_chat_memory test_chat_privacy test_scenario_manifest test_dependency_rule -q` | Source lenses, redaction, privacy, threads, immutable manifest and package ownership |
| src/agents | `PYTHONPATH=src:tests:../core/src:../core/tests:../api/src:../api/tests /tmp/mv/bin/python -m unittest test_chat_model test_chat_eval test_chat_provenance test_chat_fixture test_dependency_rule -q` | Admission/usage, development evaluation, frozen fixture/provenance |
| src/api | `ZF_BROWSER_TESTS=1 PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest test_chat_panel test_chat_isolation test_role_endpoint_inventory test_chat_fixture_roles test_case_journey test_dependency_rule -q` | Skill and legacy routes, receipts, role/current-source rechecks, browser warning/refusal/manual path, version-aware unsaved draft behavior |
| Each core/agents/api | `/tmp/mv/bin/ruff check . && /tmp/mv/bin/ruff format --check . && /tmp/mv/bin/mypy` | Full affected-component static checks |
| src/api | `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests /tmp/mv/bin/python -m checks.employee_chat_browser_check --axe <session-files>/axe-4.10.3.min.js --out <session-files>/employee-chat.json` | Main employee-dialog keyboard, lifecycle and accessibility engineering regressions |
| src/api | Same PYTHONPATH, `/tmp/mv/bin/python -m checks.regulatory_ux_check --axe <session-files>/axe-4.10.3.min.js --out <session-files>/regulatory-chat.json` | Precise disclaimer, privacy warning and synthetic regulatory UI regression |

Confirm module import origins under the same ordered PYTHONPATH before tests.
Resolve named version-aware test module before execution if its actual filename
differs. Browser suites mandatory due to actual overlapping web/check changes.
Full API discovery is not planned or authorized without the shared lock.

## Validation Record

All session-files paths below resolve to
/home/azureuser/.copilot/session-state/d5a96711-8409-4788-96d1-d21413054efe/files.
No new dependency install was necessary.

| Check | Result |
| --- | --- |
| Core exact table command | Passed: 86 tests, no skips; includes test_scenario_manifest |
| Core Ruff / format / mypy | Passed; 106 formatted files, 159 typed source files |
| Agents exact table command | Passed: 47 tests, no skips |
| Agents Ruff / format / mypy | Passed; 20 formatted files, 24 typed source files |
| Initial API selectors excluding case_journey | Failed: 92 tests, one Chromium failure because case chat now lives in main's AI assistance tab; no source defect |
| Initial API static checks | Ruff and mypy passed; format failed on merged spacing/new test wrapping |
| API corrected exact table command | Passed: 118 tests, no skips, including actual Chromium; external api-focused.log |
| Final API Ruff / format / mypy | Passed; 56 formatted files, 107 typed source files |
| Separate final test_case_journey rerun | Passed: 26 tests |
| Workflow isolated browser-module Ruff / format | Passed for design_system_browser_check.py and regulatory_ux_check.py |
| Employee chat browser check | Passed, including actual unavailable-model path, six skills, nine controlled late successes, denied routes, keyboard/focus/reflow/reduced motion and pinned axe |
| Regulatory browser check | Passed: 19 states, pinned axe executed, target sizes, keyboard and reflow |
| Design-system browser check | Passed, including delegated workbench checks and all roles; Chromium 156.0.8078.4 |
| `node --check src/api/src/zava_forward/api/web/chat.js` | Passed |
| `/tmp/mv/bin/python tools/rename-zava-tests.py` | Passed: 25 tests; deliberate broken.pptx rejection logged |
| `git diff --check` | Passed |

Core import-origin probe used the exact table PYTHONPATH and imported
zava_forward.core.chat_panel, zava_forward.agents.chat and
zava_forward.api.server; all __file__ values resolve to this worktree.

Browser dependency command:
`curl --fail --silent --show-error --location --retry 2 --connect-timeout 10
--max-time 30 https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js
--output <session-files>/axe-4.10.3.min.js && sha256sum <session-files>/axe-4.10.3.min.js`.
Passed; hash 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb
matches the existing check's pinned constant. Both browser commands in the
table executed with the actual resolved session-files paths and explicit
PYTHONPATH. JSON results remain external; no generated assets committed.

The existing Node case-journey harness needed an explicit /api/chat/status
fixture response and one event-loop readiness wait to honor the topic's
fail-closed privacy gate; otherwise it would exercise a permanently disabled
form. The existing Chromium test now deep-links ?tab=ai, preserving main's
case-tabs navigation. No assertion weakened. Two integration tests added,
within the locked budget. Static rerun initially caught a 103-column raw-JS
fixture line; split it and reran all API static checks successfully.
`/tmp/mv/bin/ruff format src/api/tests/test_chat_panel.py` fixed formatting.
Final raw-JS fixture split was covered by its separate 26-test rerun.

Synthetic API fixtures explicitly log unavailable law-store rule evaluation;
these expected diagnostics did not fail the focused suites or create approvals.
No full API discovery, no shared-heavy-lock acquisition for focused tests,
no live model/private data/Azure operation and no push occurred.

### Web guideline review

Fetched the complete current rules before edits and refreshed before review:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
retrieved 2026-10-29. Reviewed changed chat.js against all fetched rules in its
existing Fluent/native context. Applicable native labels/name/autocomplete,
described privacy warning, live status, version-aware unsaved preservation,
manual errors and keyboard behavior retained. No added animations, media,
navigation, date formatting or hydration surface.

## src/api/src/zava_forward/api/web/chat.js

Pass for the reconciled web changes; no new finding. Existing submit text does
not add a spinner, and privacy loading intentionally disables submission until
warning readiness. These inherited engineering choices and automated axe
results are not full guideline, human accessibility or WCAG acceptance.

### Related documentation

Clarified src/api/README.md: the 8,000-character masked storage limit differs
from the 1,000-character inference allowance, selected-skill instructions
count toward the combined cap, and completion rechecks use the same lens.

## Pre-Review Reconciliation

P01 complete. P02 source/test/documentation changes and validation complete;
commit pending. P03 independent Review remains the next lifecycle phase.
Original 2026-10-27 artifacts and failed acceptance verdict are unchanged.
No active implementation blocker; fresh hosted CI and publication gate remain
separate and cannot be inferred from these local results.

## Blockers

No current implementation blocker. Publication requires separate local gate,
exact-head review and fresh hosted checks; no publication is authorized here.

## Remaining Work

P02 commit; P03 independent Review and local evidence; complete publication
gate attempt after original Review is persisted, without push.

## Follow-Up Items

Coordinator publication/fresh CI; original RV-001 through RV-005 unchanged.
