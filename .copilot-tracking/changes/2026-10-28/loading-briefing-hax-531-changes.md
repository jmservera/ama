---
title: Loading and HAX briefing changes
description: Original implementation and validation evidence for issue 531
ms.date: 2026-10-28
---

## Scope and status

### Round-9 parent integration (2026-10-29, P03-T01)

Current bounded outcome: complete and locally validated; local-only commit.
Original Review and separate publication/human acceptance are unchanged.

The user explicitly authorized rebasing the four pushed child commits from
`27d11262` onto `origin/feat/case-journey-ux-526`, now
`b424ac9fe0b74ebbf4ebcbb384a969c1810db66b`, and committing locally without
push. Starting worktree was clean; PR #537 remains open against parent PR #529.
Rebase completed with conflicts only in app.js and timecapture.js.

The app resolution retains the parent's mutation key/registry and duplicate
409 guard, mutation JSON parse errors, finally-based registry cleanup and
error outcome metadata. One outer loading-feedback lifecycle surrounds it;
the child's explicit expired-session 401 status is retained. The timecapture
resolution takes the parent's shared save helper and surfaced local mutation
feedback unchanged. Native handlers still wrap once through h(), not again
inside save(). Auto-merged panels/assistants retain parent shared draft and
pending form state. Incoming tracking files had no conflicts. Both sides'
documentation additions survive; the rubric score is restored from origin/main.
The existing workbench recipe digest already matches the scenario manifest.

Planned validation uses this worktree's own src with
`/home/azureuser/source/ama-wt/issue-526-journey/.venv/bin/python`, the exact
user-specified PYTHONPATH, synthetic local browser fixtures and verified
axe 4.10.3. All heavy commands must hold the shared lock after nonblocking
admission retries lasting no more than 40 minutes. Validation pending.
Historical critique and Review outcomes are unchanged; publication and
independent exact-head acceptance remain separately owned.

#### Supplemental axe selector correction

The exact design-system entry point has no axe switch. After its native
132 checks and all requested suites passed, an additional existing regulatory
UX/axe run was selected to supplement design coverage. It failed because
`chat.locator("[role=status]")` matched both the new temporary loading status
and the existing application result status during the doubt action.
The preserved failure is
`/tmp/ama-531-round9-20261029/regulatory-ux.log`.
Four result assertions now target the panels' direct paragraph status rather
than every nested live region. Text, inbox/history checks and all other
assertions are unchanged; this corrects loading-helper test integration, not
product behavior. The change is an immediately relevant P03 refinement, not
a new acceptance or repeated Review.

The supplemental rerun passed the corrected result assertion but exposed
focus loss: the helper added native `disabled` to the doubt button after its
own handler deliberately set focus-preserving `aria-disabled`. Preserve this
existing lifecycle by letting the helper own native disabled only when the
handler has not already set `aria-disabled="true"`. WeakMap pending exclusion,
busy/spinner feedback and handler guards remain active. The controlled helper
test now verifies that the action-owned ARIA state persists without native
disable during or after the promise. This is a directly coupled P01/P03
integration correction, not an unrelated focus abstraction.
Second failure: `/tmp/ama-531-round9-20261029/regulatory-ux-after.log`.
Fresh full unit, requested browser and supplemental axe validation pending.

The final-source full API, journey, assistants and supplemental regulatory
axe checks passed. The loading check then exposed an independent harness
race at its law-viewer duplicate assertion: navigation can finish before
the automatic initial sources read, so the subsequent route hold could capture
that initial read as well as the deliberate button read. Wait for the
actual initial "Sources held" heading before installing the held route.
The exact one-request and disabled/error/recovery assertions remain intact.
This is P03 harness synchronization only; no further product change.
Failed run: `/tmp/ama-531-round9-final-20261029/loading-briefing.log`.
The first synchronization attempt demonstrated that this briefing fixture has
no law store: its initial read correctly reports that explicit error instead
of a sources heading. Supply the same explicit empty synthetic sources
response used by the existing recovery step for the initial read, wait for
its rendered heading, remove that route, then install the held action route.
The deliberate 503 and recovery remain separate unchanged checks.
Attempt evidence:
`/tmp/ama-531-round9-final-20261029/loading-briefing-after.log`.

#### Final locked validation and handoff

The final product source passed the exact API discovery command using the
requested journey-worktree interpreter from `src/api` and
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
All commands below use that interpreter and source path. No imported installed
API/core/agents source was substituted. All heavy batches acquired
`/tmp/ama-rpi-heavy.lock` with `flock -n` immediately; no admission exceeded
the 40-minute ceiling and no foreign lock was bypassed.

Final evidence root: `/tmp/ama-531-round9-final-20261029/`.
The 02:04:32Z batch passed focused tests, regulatory UX, full API, journey
and assistants before the law-check harness race described above. Only that
browser harness changed afterward. The 02:16:23Z continuation passed the
synchronized loading check twice and all remaining checks, ending 02:16:52Z.

| Command from src/api | Final evidence/result |
| --- | --- |
| `python -m unittest discover -s tests -q` | `unit.log`: 1217 tests in 437.173s, OK, 316 existing environment-dependent skips |
| `python -m unittest test_loading_feedback test_regulatory_ux_check test_scenario_manifest -q` | `focused.log`: 14 tests passed, including ARIA state ownership |
| `python -m checks.case_journey_browser_check --axe /tmp/ama-520-axe-4.10.3.min.js --out <root>/journey` | `journey.log`: 406 checks; `journey/results.json`: 87 scopes, zero violations, 86 incomplete entries |
| `python -m checks.assistants_browser_check --axe /tmp/ama-520-axe-4.10.3.min.js --out <root>/assistants` | `assistants.log`: 206 checks; `assistants/results.json`: 56 scopes, zero violations, 56 incomplete entries |
| `python -m checks.loading_briefing_browser_check --axe /tmp/ama-520-axe-4.10.3.min.js --out <root>/loading-briefing-settled` | `loading-briefing-settled.log`: pass; four axe scopes, zero violations, three incomplete entries |
| Same loading command with `--out <root>/loading-briefing-repeat` | Independent repeat passed the unchanged law duplicate/error/recovery assertions and all four axe scopes |
| `python -m checks.employee_briefing_browser_check` | `employee-briefing.log`: 74 checks passed |
| `python -m checks.design_system_browser_check` | `design-system.log`: 132 checks passed; native runner has no axe switch |
| `python -m checks.regulatory_ux_check --axe /tmp/ama-520-axe-4.10.3.min.js --out <root>/regulatory-ux.json` | 19 browser states passed, zero violations, nine incomplete entries; actual doubt-button focus and history assertions retained |
| `python -m unittest test_scenario_manifest -q` | `scenario-manifest.log`: eight tests passed |
| Targeted Ruff and mypy on changed Python checks/tests | `ruff.log`, `mypy.log`: both passed |

`<root>` denotes the actual external evidence root above, not a repository
output path. Axe version 4.10.3 is content-verified by the existing harnesses,
SHA256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
There are 166 distinct passing axe scopes, not a WCAG or human acceptance
claim; all incomplete results remain in their reports.
Fresh fetched Web Interface Guidelines were applied to the changed helper
and conflict-resolution scope: no remaining introduced findings. Existing
ASCII/sentence-case repository rules take precedence over generic copy rules.
JavaScript syntax checks for app/async-action/timecapture and `git diff --check`
pass. Panels, assistants and timecapture remain byte-identical to the pinned
round-9 parent; append-only knowledge index/log content is unchanged from the
pre-rebase child. The scenario recipe SHA256 remains
`dea58169392471861486ccb9d5ef4f263a4208d34c920847615bfc1a944fe6f0`.

During validation, another process advanced the shared parent remote-tracking
ref to `35309bf2`, adding only a rubric score bot commit after the pinned
`b424ac9f` rebase base. No product behavior changed in that advance. The
explicitly requested main rubric bytes are retained rather than chasing that
bot output; this is not a claim of latest-remote exact-head publication
acceptance. The complete gate and independent exact-head assessment remain
coordinator-owned. No push, az, Azure change, secrets, private data or live
model access was performed.

### CI wrapper retry continuation (2026-10-29, P03-T01)

User-authorized scope is the failure in PR #537's exact design-system browser
module, on the existing clean `feat/loading-briefing-hax-531` worktree. Initial
HEAD is `124ec768`. Read-only PR inspection confirms OPEN with parent base
`feat/case-journey-ux-526`. First execution boundary is unmodified
`python -m checks.design_system_browser_check` from `src/api`, with
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`
and the existing `/tmp/ama-531-venv/bin/python`.

The approved write boundary is the failing check and scenario-manifest recipe
hash, or directly implicated product code if reproduction shows a product
defect, plus existing RPI evidence. Assertions must not be weakened. Shared
product changes require journey, assistants and briefing browser checks with
pinned axe. All heavy runs use `flock -n` admission on
`/tmp/ama-rpi-heavy.lock` with at most 40 minutes of retries. The first run is
waiting for the existing foreign holder; no bypass or foreign output reuse.
Implementation and local validation are now complete within this bounded
P03 continuation; local commit only, no push, az, secret reads or change to
historical critique/Review outcomes.

#### Reproduction and root cause

The exact unmodified CI module acquired the lock at 2026-10-29T01:38:33Z and
failed with exit 1 at the reported button click after 30 seconds. The
standalone module, using identical source-local imports, independently acquired
the lock at 01:39:14Z and failed at the same click with exit 1.
Logs: `/tmp/ama-531-ci-wrapper-before.log` and
`/tmp/ama-531-standalone-before.log`. Thus no wrapper-specific dataset,
route-order, selector-mode or timing difference is needed to reproduce this
candidate; the claimed standalone pass is not reproducible at current HEAD.

Commit `55241ede` intentionally changed `aiBox.load` to preserve existing
briefing content after a failed refresh or mode change, protecting review edits.
The cancelled/cached briefing scenario has already painted "Current synthetic
briefing" before the workflow-mode 503. Its existing "Refresh briefing" remains
enabled after cleanup; "Try loading briefing again" is rendered only when
content was empty. The check retained that now-stale initial-load selector.
Product preservation behavior is correct and is not changed.

The P03 check now explicitly verifies retained content, the enabled refresh
control, absence of the initial-load control, an exact workflow retry request,
replacement output and cleared error. A separate fresh-page 503 verifies the
initial-load retry control still works and clears its error. No generic
either-button fallback, weakened assertion or timing increase is introduced.

#### Completed CI retry validation

All commands below use the interpreter and source-local PYTHONPATH above.
Heavy checks held the shared lock for their complete command execution, with
nonblocking retries admitted within the user-authorized 40-minute limit.

* From `src/api`, `python -m checks.design_system_browser_check`: exit 0,
  132 passing checks, Chromium 156.0.8078.4. Lock admission:
  2026-10-29T01:40:52Z. Both cached-refresh and initial-load recovery pass
  inside the exact CI entry point, followed by every existing role, queue,
  navigation, safety, reflow and stale-response assertion.
  Log: `/tmp/ama-531-ci-wrapper-after.log`.
* From `src/api`, `python -m checks.workbench_browser_check`: exit 0,
  100 passing checks, same Chromium. Lock admission:
  2026-10-29T01:44:35Z.
  Log: `/tmp/ama-531-standalone-after.log`.
* In the same locked batch, `python -m
  checks.loading_briefing_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out
  /tmp/ama-531-ci-retry-loading-axe`: exit 0. Existing shell, refresh/edit
  preservation, pending/history guards, resident, appointment, map and law
  checks pass. Four axe 4.10.3 scopes have zero violations.
  Log: `/tmp/ama-531-ci-retry-loading-axe.log`; report:
  `/tmp/ama-531-ci-retry-loading-axe/axe-results.json`.
* Recipe `sha256sum`:
  `dea58169392471861486ccb9d5ef4f263a4208d34c920847615bfc1a944fe6f0`.
  The scenario manifest records that exact digest.
  From root, `PYTHONPATH=src/core/src:src/core/tests python -m unittest
  test_scenario_manifest -q`: exit 0, all 8 tests pass.
* Owning-project `ruff check src/api/checks/workbench_browser_check.py`:
  exit 0. From `src/api`, `python -m mypy --follow-imports=silent
  checks/workbench_browser_check.py`: exit 0, no issues.
  `git diff --check`: exit 0.
* An additional isolated strict Ruff probe reports the same three pre-existing
  I001/B023/E501 findings in both HEAD and the changed file, outside the edited
  block. They are covered by existing project exemptions and were not changed.
  No new strict diagnostic was introduced; whole-file formatting was not run.

The API guide now distinguishes the two recovery controls. No shared product
code changed, so the conditional journey/assistants reruns are not applicable.
Briefing/axe was nevertheless rerun as directly related regression evidence.
No new original Review, full publication gate, Azure, paid inference, private
dataset access, push or live acceptance is claimed. The complete publication
gate remains coordinator-owned and blocked here by the no-az instruction.

### Authorized rebased continuation (2026-10-29)

The coordinator explicitly authorized rebasing the single implementation commit
onto `origin/feat/case-journey-ux-526`, then independent review and fixes, unit
and browser/axe validation, and local commits only. The original implementation
and Review below remain historical, including their Not accepted outcome.
Current parent is `27d11262658acdc198277dc3bb38cec230ede971`; rebased
implementation is `3507a75e9c5b874a7afeccfcf21a72612e50838f`.

The rebase retained both knowledge-base index entries and append-only log
history, took the incoming tracking artifacts unchanged, and restored
`.github/rubric/scores/latest.json` from `origin/main`. The app/ops conflicts
retain mutation outcome metadata, history barriers, pending-submission guards,
quality save ownership and field-error cleanup. The shared helper wraps native
handlers once; it does not replace those existing action lifecycles.

A separately requested independent review assessed that rebased head against
the current parent. It confirmed preservation of the parent safeguards and
reproduced RV-001/002/003, including refresh resetting a pending review guard.
This continuation owns those three fixes within P01/P02 and their P03
regressions. Validation will use this worktree's own source paths and the
coordinator-specified interpreter, with heavy checks admitted by nonblocking
flock retries for at most 40 minutes. No push, az, secrets or deployed checks.
Current execution: three source corrections and fresh local validation complete.
Local commit only; publication and final exact-head assessment remain with the
coordinator.

#### Rebased review dispositions and regressions

* P02/RV-001: deep-copy the selected case snapshot while holding the store
  lock. Prompt facts, rules text, source validation and post-generation
  statement fragments now share that snapshot. The JSON/SQLite task-mixin
  regression changes a live case during generation and compares statements,
  citations and the saved review's shown/workflow output.
* P01/RV-002: shared form progress is adjacent to, not inside, its busy form.
  Briefing busy/inert state applies only to content, leaving its primary
  polite status outside. Controlled-clock helper coverage asserts form
  topology and disabled cleanup; held-request browser assertions check both
  actual form and briefing status ancestry.
* P02/RV-003: local review inputs mark unsaved values even outside a case.
  Refresh/mode changes require explicit discard, retain old fields after a
  failed read, and cannot replace pending or history-blocked review controls.
  Loading also prevents concurrent replacement and makes old content inert.
  Native guards, dispatched snapshots, late-edit reconciliation and outcome
  precedence from #529 remain intact. Browser regressions cover cancelled
  refresh/mode, failed and successful refresh, a held review and committed-409/
  uncertain-503 barriers without a second POST.
* API guide documents snapshot/announcement/refresh behavior and source-local
  validation paths. Original critique and both assessed-head review outcomes
  remain unchanged; corrections are implementation evidence, not independent
  acceptance of the changed final head.

#### Preserved validation attempts

All heavy attempts used the specified interpreter and source-local PYTHONPATH,
holding the nonblocking heavy lock with at most 40 minutes of admission retries.

* Attempt 1: focused helper/journey/AI units passed, 91 tests, no skips. Loading
  browser reached four passing axe scopes, then the new history-barrier loop
  reloaded while its one-shot hold route was still installed. Corrected the
  harness to replace that route with its explicit synthetic response.
  External evidence: `/tmp/ama-531-rebased-loading-1`.
* Attempt 2: refresh/mode/history regressions passed; the synthetic navigation
  then correctly triggered the newly retained unsaved briefing warning.
  Explicitly accepted this test-only discard to continue into resident checks.
  External evidence: `/tmp/ama-531-rebased-loading-2`.
* Attempt 3: resident review passed; the appointment error assertion still
  searched inside the form after RV-002 moved feedback beside it. Corrected
  the assertion to the appointment region, retaining its error/duplicate and
  no-busy-ancestor assertions. External evidence:
  `/tmp/ama-531-rebased-loading-3`.
* Focused Ruff100 and explicit E501 checks passed for the new helper/browser
  files; changed AI/store Ruff and JavaScript syntax/whitespace checks passed.
  An optional whole-file format probe reported the browser harness's existing
  compact layout; no unrelated whole-file reformat was applied.

#### Completed rebased validation

Final batch held `/tmp/ama-rpi-heavy.lock` from admission at
2026-10-29T01:16:41Z through completion, exit 0. Interpreter:
`/home/azureuser/source/ama-wt/issue-526-journey/.venv/bin/python`.
All commands ran from `src/api` with
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
Import provenance was checked: API and core modules resolve to this worktree,
not the shared venv's editable source.

* `python -m unittest discover -s tests -q`: 1215 tests in 437.567 seconds,
  OK, 316 environment-dependent skips. This does not establish SQL Server or
  external-provider acceptance.
* `checks.loading_briefing_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-531-rebased-loading-4`:
  passed all shell, feedback, snapshot-facing UI, refresh/mode/history,
  resident, appointment, map and law scenarios. Four axe scopes, zero
  violations; 320/390/1280 reflow and reduced motion.
* `checks.case_journey_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-531-rebased-journey-4`:
  passed current parent journey, immutable dispatch/later edits, cache
  reconciliation, mutation/history barriers, keyboard/zoom/forced-colours
  checks; 42 axe scopes, zero violations, no page errors.
* `checks.assistants_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-531-rebased-assistants-4`:
  173 checks passed, 40 axe scopes, zero violations, no page errors.
* `checks.employee_briefing_browser_check`: passed all supplied employee-role
  scope/assignment, independent-panel loading, mode and reflow checks.
* `checks.workspace_scripts_browser_check`: passed actual companion/Leaflet
  recovery, retry budget and stale/session safeguards.
* Changed-file Ruff100, explicit new-file E501, changed-JavaScript syntax and
  `git diff --check` passed. Parent inspected the final briefing screenshot;
  this is bounded visual QA, not staff or assistive-technology acceptance.

Full transcript:
`/tmp/1793236670159-copilot-tool-output-538748-efe42b54-30e6-4418-bfac-aec118e34770.txt`.
Loading/journey Chromium 156.0.8078.4; assistants Chromium 155.0.8059.39.
All axe reports use pinned 4.10.3. Generated reports remain external.
RV-001/002/003 have implementation corrections and targeted passing
regressions; neither historical Not accepted review is rewritten as final-head
independent acceptance. RV-004 and the prohibited-az complete publication gate
remain separate. No push, az, secrets or live-site verification.

### Original implementation boundary

Full P01-P03 implementation on `feat/loading-briefing-hax-531`, stacked on
`feat/case-journey-ux-526` at `6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c`.
Research complete, plan ready after one independent critique with three
directly accepted corrections. P01-P03 source implementation, documentation and
local validation are complete. The original independent Review executed once:
Complete, outcome Not accepted. Three implementation defects remain routed to
later work; this is not accepted delivery or publication.

## P01: Loading and action feedback

P01-T01: added independent `workspace-shell.js` and shared `async-action.js`,
loaded from the native employee shell before dependent application scripts.
Static startup text is immediate once HTML arrives; four-second slow/retry and
fifteen-second support guidance cover held/failed scripts and API startup.
The startup section is removed when login/session becomes usable. Existing
bounded script/Leaflet recovery code and retry budgets are unchanged.

The shared native event lifecycle wraps click, change and submit, starts text
immediately, decorates with a spinner at 200ms, disables/deduplicates the pending
control, uses polite status and surfaces uncaught errors. Mutation observation
preserves later handler-owned disabled states. Direct account/import/filter
listeners, appointment and quality mutations, map refresh, timecapture redraws
and standalone law actions now return/await their full promises or use explicit
regional feedback. Checklist reads have initial local text. Reduced motion
keeps text and a static icon. No mutation auto-retry or navigation lock.

Completion evidence: actual-helper fake-clock test, delayed real resident and
appointment actions, standalone law failure/recovery, held-map regional status,
and existing script-recovery checks. See validation below.

## P02: Briefing and review interaction

P02-T01: `ai_tasks.finish` retains declared statement references, unresolved
references and timezone-bearing generation time with final publication.
Whole-bullet filtering precedes statement splitting, so a partially valid
dropped bullet cannot reappear in metadata. Quarantine reports only its shown
workflow output, not abandoned AI references. Rules briefing derives the
actual first-three case fragments; zero-case output remains explicit.
Cache reads retain preparation time. Declared source case IDs prevent a label
such as "Stage: ..." becoming a fabricated case link.

`aiBox` distinguishes AI/rules, explains fixed ranking/scope, shows preparation
time and expandable statement references with an explicit trust caveat.
Hide/Show is reversible local dismissal. Assistance mode uses plain wording,
applies to briefing/draft requests and resets at sign-out/session login.
`aiNotes` offers outcome-labelled use/edit/do-not-use choices, reveals only
relevant large fields, requires edit/rejection reasons and retains local text
on cancel. External resident drafts remain the actual reviewed payload.
Immutable submitted snapshots and later read-only copyable edits survive;
unverified acceptance remains disabled. No server approval authority changes.

## P03: Validation

Initial dependency probe: system Python and prior issue venv did not have
`zava_forward` installed. Created owned `/tmp/ama-531-venv`, installed existing
`src/core`, `src/agents`, `src/api[dev]` distributions; exit 0.
No dependency manifests changed. No secrets, .env, private data or Azure read.

All heavy checks use an owned descriptor on `/tmp/ama-rpi-heavy.lock` with
`flock -n`, 15-second admission retries and a 2400-second deadline. No foreign
holder was interrupted and no foreign evidence was reused. Interpreter:
`/tmp/ama-531-venv/bin/python`, installed source distributions. Commands below
run from `src/api` with
`PYTHONPATH=tests:../core/tests:../agents/tests`.

### Preserved failures and corrections

* Initial focused API/helper/UI suites: 88 tests, passed.
* First loading browser run failed because the pre-existing busy-button CSS
  appended "(loading)" to accessible button names. Removed that pseudo-content;
  adjacent progress text now carries feedback without changing the action name.
  Original output: `/tmp/ama-531-loading-first`.
* Second loading browser run passed shell, briefing, draft and appointment
  scenarios, then stopped because unsaved resident text correctly cancelled the
  harness navigation. Explicitly accepted that test-only navigation warning;
  corrected the map scope selector (`#mapArea` is a select, not its panel).
  Original output: `/tmp/ama-531-loading-second`.
* Full API discovery initially ran 1178 tests, with one failure and 316 skips.
  `test_case_journey` still selected the retired input/review-submit shape.
  Migrated the existing semantic test to conditional textarea reveal/submit,
  retaining all duplicate, immutable-dispatch and newer-value assertions and
  adding visibility checks for later copyable edits. Original log:
  `/tmp/1793231327675-copilot-tool-output-396757-117b509d-1c58-4007-94f2-74fee95cbad0.txt`.
* The first widened browser batch passed required briefing, script and journey
  checks, then assistants stopped because hidden startup retained a second DOM
  h1. Startup now removes its completed placeholder, preserving the existing
  one-heading check rather than weakening it. Original batch log:
  `/tmp/ama-531-final-validation.log`.
* The widened design/workbench check then found its remaining retired checkbox
  and alert selectors. Migrated them to the new native mode select and polite
  error status, retaining selected-mode retry and error-clear assertions.
  Original log: `/tmp/ama-531-complete-validation.log`.

### Completed checks

* `python -m unittest test_loading_feedback test_case_journey test_ai_tasks
  test_continuity test_continuity_epoch_export -q`: 167 tests, passed, 36
  existing environment-dependent skips.
* `python -m checks.loading_briefing_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-531-loading-final`: passed;
  four axe scopes with zero violations, 320/390/1280 reflow, reduced motion,
  source-case link, unverified AI and real action delay/error/duplicate checks.
* `python -m checks.employee_briefing_browser_check`: passed all supplied staff
  role/scope and reflow checks, including independent queue/briefing loading.
* `python -m checks.workspace_scripts_browser_check`: passed actual Leaflet and
  companion-script recovery, bounded failure/manual retry and stale/session
  safeguards. No recovery budgets changed.
* `python -m checks.case_journey_browser_check --axe
  /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-531-journey-first`: passed;
  existing retained-draft, delayed immutable review, source/race, keyboard,
  200% browser zoom, forced-colours and axe scenarios retained.
* Changed-file Ruff with line limit 100, explicit E501 for new/focused files,
  focused harness/helper-test mypy, six changed JS syntax checks and
  `git diff --check`: passed. Legacy Python exemptions do not waive the
  100-column limit for added lines.

Post-placeholder-cleanup loading browser passed again at
`/tmp/ama-531-loading-final-shell` (four zero-violation axe scopes).
Assistants passed 58 existing browser checks with axe evidence at
`/tmp/ama-531-assistants-final/results.json`. The migrated design/workbench
check passed its native component, map, role/navigation, cancellation/cache,
selected-mode retry and manual-access assertions. Final full API discovery
passed in the same locked batch: `python -m unittest discover -s tests -q`,
1178 tests in 433.268 seconds, OK with 316 environment-dependent skips, exit 0.
Log: `/tmp/ama-531-design-and-api-final.log`. These skips do not establish
SQL Server, external-provider or Azure acceptance.

Final loading run after fixture/visual QA:
`/tmp/ama-531-loading-reviewed-final`, passed with four zero-violation axe
scopes. The synthetic AI fixture's text/references/reason now agree, and an
empty review error no longer paints a warning glyph. Parent inspected its
1280px screenshot plus the existing journey 320px screenshot; this is bounded
visual QA, not staff usability or assistive-technology acceptance.
Changed-file mypy passed seven API files; applicable Ruff format passed two
test files. All added Python lines fit the requested 100 columns.
Browser is Chromium 156.0.8078.4. Axe-core 4.10.3 SHA256:
`880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
Screenshots/reports remain external, not committed as claimed receipts.

## Amendments and divergences

The requested UX agent returned questions rather than the bounded design note.
Parent recorded an evidence-based HAX design note in the primary research,
explicitly without claimed user research. No replacement worker was launched.
PC-001/002/003 are plan corrections, not new requirements.

The initial source scan found two additional returned-promise gaps in quality
submission and overview filters. Fixed within P01's approved integration
inventory. P03 also migrates the existing case-journey Node test, not only its
browser counterpart, and workbench's retired mode selectors. These are directly
related correctness/test corrections,
not new user decisions or a second critique.

The API guide and existing design-system state inventory document shipped
behavior and limits; the knowledge-base index and append-only log are updated.

## Remaining work and publication

The RPI loop is complete, not accepted. All P01-P03 implementation markers
record performed work and passed supplied checks, not closure of Review
findings or product/publication acceptance. Candidate and original evidence are
retained for local commit and coordinator handoff only.
Human screen-reader, voice-control,
staff usability, live employee cold-start and SQL Server acceptance remain
unperformed, not passed.

Publication is blocked, not waived. `tools/rpi-checks.py:62` includes `az` in
required tools and `:1358-1365` invokes `az bicep version` during preflight.
The explicit no-az instruction prevents the complete publication gate; no
partial/fabricated receipt or cloud fallback is substituted. No push/PR.

Fresh remote inspection: PR #529 remains OPEN, base main. `origin/main` is
`9bfed51863b05a25e9939d82504c576524688e14`. Remote parent is now
`73e365e618d8cf701a12434e4cd0c2f2affb07f1`; it and the original local anchor
`6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c` have diverged (12 commits each,
merge base `1dde6a908c20358dbb3067dcdd674e5ad0bd246d`). No merge, rebase or
history rewrite is authorized/performed. Coordinator must reconcile the parent,
rerun exact-candidate evidence/gate and assess the resulting head before push.

### Coordinator PR text

Base: `feat/case-journey-ux-526`. Dependency: stacked on PR #529; that parent
must land first. Refs #531.

Adds visible static startup/slow/retry feedback, shared native async action
feedback and HAX-informed source-labelled briefing/draft review. Retains
Fluent-derived tokens, manual paths and human/resident approval boundaries.
Local validation is synthetic only. Original Review is Not accepted;
RV-001/002/003 remain open. Full publication gate and deployed/human acceptance
are not satisfied. Resolve routed defects before publication and replace this draft's validation details with the
final exact-head receipt after dependency reconciliation. Do not use a closing
keyword for #531.

## Original Review and later-work routing

Original record:
`.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-hax-531-review.md`.
Execution Complete, outcome Not accepted; 1 High, 2 Medium implementation
findings and 1 Low acknowledged residual. No fixes or second Review were
performed after this assessment.

1. RV-001, High: freeze rules statement metadata with the published snapshot.
   The independent isolated reproduction showed mutable case data changing
   metadata after template text/citations had already been captured. Highest
   priority for output/source integrity; route to later `rpi-implement`.
2. RV-002, Medium: put action-specific announcers outside busy subtrees.
   Existing attribute/axe checks cannot establish announcements when form or
   briefing ancestors are busy. Small shared correction with broad
   accessibility leverage; route to later `rpi-implement`.
3. RV-003, Medium: protect unsaved briefing correction/reason values and
   pending reviews from refresh. Independently reproduced local work loss;
   preserve old-evidence binding or explicitly confirm discard. Route to later
   `rpi-implement` with success/failure refresh regressions.
4. RV-004, Low residual: separately owned human AT, staff usability, deployed
   cold-start and SQL Server acceptance stays unperformed.

These are follow-up-only routing updates, outside this task's completed
implementation and one-pass Review boundary. Original plan critique and Review
verdicts are preserved. No child is started or user choice inferred.

Automatic mode remains running at Follow-up with task status completed and
outcome Not accepted. State holds ranked later work plus full-gate and parent
lineage blockers. Local history, not a self-referential artifact SHA, identifies
the committed candidate. No push, PR, rebase, merge, az or Azure action.
