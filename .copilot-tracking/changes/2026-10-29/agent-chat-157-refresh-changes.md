<!-- markdownlint-disable-file -->
# RPI Changes: agent-chat-157-refresh

## Metadata

* Task ID: pr-503-refresh-2026-10-29
* Related plan: .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md
* Implementation date: 2026-10-29

## Execution Status

Full RPI implementation and independent Review complete. All P01-P03 markers
have execution evidence. Rebased local candidate is validated by focused checks;
complete publication gate was attempted and failed. Hosted CI and publication
remain blocked/separate; no push occurred.

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
At the end of focused validation no full API discovery had run. Focused tests
did not acquire the heavy lock. No live model/private data/Azure operation or
push occurred. The later locked full-gate attempt is recorded below.

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

### Candidate commit and preservation checks

* `git merge-base --is-ancestor <captured-main> HEAD && git diff --check`:
  passed.
* Explicit byte assertions via /tmp/mv/bin/python and git show confirm final
  docs/reference/log.md starts with main's complete original bytes and contains
  the topic's complete appended entry. Both sides preserved.
* `git diff --exit-code 949aafaf HEAD -- <original changes, critique, Review>`:
  empty; original adverse RPI evidence byte-preserved.
* Re-resolved `gh api user --jq '{id,login}'`, staged only this loop's paths,
  then `git commit -m "fix(chat): reconcile main integration and refresh regressions"
  -m "Preserve skill lenses, privacy readiness and completion receipts across the rebase. Record focused validation and retain original acceptance findings."
  -m "Refs #503" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"`:
  success, ca5cb0101040c8176c4f32812be71af02b56670a.
* `git status --short`: clean after candidate commit. All replayed and new
  commits use the authenticated numeric-id noreply author/committer address.

### P03 independent Review

Execution Complete; outcome Conformant for the bounded local refresh at
ca5cb0101040c8176c4f32812be71af02b56670a against captured main.
One independent assessor, no new refresh finding. Original failed acceptance
and RV-001 through RV-005 preserved. Full record:
.copilot-tracking/reviews/logs/2026-10-29/agent-chat-157-refresh-review.md.
Later evidence commits do not imply independent exact-head approval.

* `git fetch origin main && git rev-parse origin/main HEAD`: main remains
  5653547507f3056f09a726a18516237728da5e5b; candidate ca5cb010.
* `flock -n /tmp/ama-rpi-heavy.lock true`: success, exit 0.
  This is the caller's eligibility probe, not a held lock. The full-gate
  runner must acquire/hold its own same shared lock for any discovery.
* Planned after this original Review is committed:
  `PATH=/tmp/mv/bin:$PATH /tmp/mv/bin/python tools/rpi-checks.py --all
  --base 5653547507f3056f09a726a18516237728da5e5b
  --out <session-files>/pr503-full-gate-20261029 --lock-timeout 1`.
  This is not yet a pass or valid receipt. No cloud fallback is authorized.

### Complete local gate: actual execution and blockers

* Committed original Review and reconciled state using
  `git commit -m "docs(chat): preserve independent refresh review and handoff"
  -m "Record the original bounded Review and retained publication boundaries. Refs #503"
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"`:
  success, 3f108aea120126bc6e7209fe0411c364e6692ecc.
  Authenticated account re-resolved before committing.
* Ran the exact planned `PATH=/tmp/mv/bin:$PATH /tmp/mv/bin/python
  tools/rpi-checks.py --all --base
  5653547507f3056f09a726a18516237728da5e5b --out
  <session-files>/pr503-full-gate-20261029 --lock-timeout 1`.
  Exit 1: candidate has ignored inputs. Inspection showed lint/type caches,
  bytecode and editable-install metadata. Nothing pre-existing was deleted,
  stashed, moved or ignored via a bypass.
* Alternative local validation route:
  `git worktree add --detach <session-files>/pr503-gate-candidate
  3f108aea120126bc6e7209fe0411c364e6692ecc`.
  Created only this run's clean exact-commit detached checkout, preserving the
  supplied primary worktree and all its generated/ignored inputs.
* From that clean checkout:
  `flock -n /tmp/ama-rpi-heavy.lock true &&
  PATH=/tmp/mv/bin:$PATH /tmp/mv/bin/python tools/rpi-checks.py --all
  --base 5653547507f3056f09a726a18516237728da5e5b
  --out <session-files>/pr503-full-gate-clean-20261029 --lock-timeout 1`.
  Probe succeeded. Runner acquired the same shared lock at
  2026-10-29T13:15:17.969151+00:00 and held it during execution. Full API
  discovery therefore satisfied the caller's lock condition; no probe-only
  concurrency assumption was used.
* Full attempt completed, exit 1. Receipt sealed 2026-10-29T13:41:37.146632+00:00.
  Required project-api group rejected 317 integration/dependency skips even
  though unittest itself returned OK. Workflow matrix drift was also reported
  for mvp-ci.yml, mvp-validation.yml, src-deploy.yml and infra-plan.yml.
  `git diff --exit-code <captured-main> HEAD -- tools/rpi-checks.py
  .github/workflows` was empty: those gate/workflow contracts are unchanged
  from captured main, not fixed or weakened in this bounded refresh.
* Full discovery results: core 1,486 tests / OK / 191 skips; agents 120 / OK;
  API 1,284 / OK / 317 skips; orchestrator 46 / OK; importer 39 / OK.
  Skips are not executed integration passes. Browser and real-SQL groups
  were not completed by this full gate after its API prerequisite rejection.
  Independently executed focused/browser results above remain their own
  bounded evidence, not substitutes for the missing full-gate groups.
* The full run also completed namespace/static/infra/migration and four local
  image contracts plus the logo-0600 startup stress path. Local Bicep
  build/lint used offline Azure CLI tooling, not Azure resource operations.
  No Azure resource was created or modified.
* Durable external failed receipt:
  <session-files>/pr503-full-gate-clean-20261029/receipt.json.
  SHA-256: dbe5f862f2065aee2ff9a17fbcfc3302dce18b188d9b153d465b529ec0d1dab1.
  Bound HEAD: 3f108aea120126bc6e7209fe0411c364e6692ecc.
  Scope full / status failed. It is not a valid publication receipt. A later
  evidence commit invalidates exact-head reuse; do not resume this receipt
  after a source/evidence/base change.
* `git -C <session-files>/pr503-gate-candidate status --short`: clean.
  `git worktree remove <session-files>/pr503-gate-candidate`: success; removed
  only this run's newly created clean duplicate checkout. Retained all gate
  logs, environments, images and failed receipt; no historical evidence cleanup.

The clean-checkout gate attempt was ordinary local validation judgment, not a
new child workstream or a change to the caller's branch/source/approval scope.
Original independent Review is preserved without a second Review or attempted
remediation of separate main gate-policy problems.

## Pre-Review Reconciliation

P01 and P02 source/test/documentation changes, validation and commit complete.
P03 independent Review Complete / Conformant; no new findings to remediate.
Original 2026-10-27 artifacts and failed acceptance verdict are unchanged.
No new implementation defect established. Complete gate failed on unchanged
gate/workflow contracts; fresh hosted CI remains unavailable until coordinator
publication and cannot be inferred from these local results.

## Blockers

Publication blocked: complete-gate API skip contract and workflow-matrix drift;
fresh exact-head gate/review and hosted checks are still required. Primary
worktree ignored caches remain intact, so future gate execution needs an
authorized clean-candidate strategy. Remote PR still references its old head
because this task explicitly forbids push. No new source defect is established
by the failed gate, and no check/protection/policy was weakened.

## Final Local Handoff

* Final `git fetch origin main && git rev-parse origin/main`:
  fetched main is still 5653547507f3056f09a726a18516237728da5e5b.
* `git merge-base --is-ancestor origin/main HEAD && git diff --check`:
  passed. No unresolved paths, source modifications or untracked inputs;
  final changes consist only of this loop's four evidence/state updates.
* Final protected-snapshot diff against captured main: empty.
* `/tmp/mv/bin/python -m json.tool <state-path> > /dev/null`: valid JSON.
* Re-resolved authenticated GitHub numeric-id/login before final commit.
* Final evidence-only commit uses
  `git commit -m "docs(chat): record complete gate blockers and local handoff"
  -m "Preserve failed gate evidence without changing main gate policy. Leave rebased history local for coordinator publication. Refs #503"
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"`.
  This does not change the reviewed source tree or upgrade its failed
  publication receipt to approval of the later exact head.

## Remaining Work

No remaining source implementation or one-pass RPI execution. No child work
selected or started. Full-gate remediation/publication are distinct follow-up;
no push or hosted success is claimed.

## Follow-Up Items

Ranked current choices:

1. Coordinator gate-contract reconciliation, exact-head gate/review and fresh
   hosted CI: directly unblocks delivery; evidence is the failed external
   receipt and original hosted rubric failure.
2. Original RV-001 denied-turn accounting: bounded engineering work with an
   existing explicit regression objective; original feature acceptance remains
   Not accepted.
3. Original named-human accessibility/activation evidence: browser tests cannot
   replace RV-003/RV-004 human/DPO/Legal decisions.

Stop automatic session and switch to manual mode remain control choices.
No follow-up is started without owner selection.
