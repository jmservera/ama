---
title: Loading and HAX briefing changes
description: Original implementation and validation evidence for issue 531
ms.date: 2026-10-28
---

## Scope and status

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
