<!-- markdownlint-disable-file -->
# Changes: provider-capacity-controls-90

Task #90, 2026-10-17. Scope: full approved plan, ordered execution.
Plan: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md.
Details: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md.

## P01-T01: Baseline and failing-first reproduction

Uninstalled system interpreter failed with ModuleNotFoundError zava_forward. Created task-owned .venv and installed existing component extras only after that failure. Initial duplicate editable-core install resolution failed; corrected the invocation to one core[dev,sql] entry. Baseline existing quality/procurement: 21 tests pass. No private data read.

Executed before production edits: 29 tests, eight failures (four root behaviors reproduced on both JSON and SQLite): imported numeric-only capacity issues, out-of-period booking succeeds, appointment/non-booked/withdraw changes lack versions, and case advance without order succeeds. Original 21 tests still passed in that run.

## P01-T02: Domain controls and transaction progress

Existing procurement document retained. Source-bound accepted capacity and explicit trusted delegation now gate changes; every lifecycle mutation snapshots issuer/authority/state/appointments. Existing reservation progression works at quota; known zero records deficit; withdrawal explicitly releases with new version/reason. Original uploaded bytes and hash are checked, no fake production seed/delegation added. Deterministic SQLite last-slot, advance-versus-withdraw/rescope/loss, authority revocation, source change and audit failure tests pass: 47 focused tests. Coupled fixture prerequisites now explicitly supply fictional source/delegation, retaining existing safety/resident assertions.

## P02: Existing API, screen and preservation

Existing routes forward contract version and structured source evidence;
package reads deny contractors, whose order reads remain supplier-scoped.
Capacity UI adds original-source/date/home fields, native labels/date/number
controls, live refusal/focus, busy handling and a scrollable semantic table.
Common AI notes explicitly remain not an instruction before/after review.
No new service, role grant, send route, framework or unrelated redesign.

HTTP/browser replay caught and corrected a missing controls helper import.
The wider suite exposed an old building HTTP positive that relied on the
advance bypass; added an explicitly fictional authorized booking, retaining
all building/safety assertions. JSON operation-local compensation also covers
advance and save-then-audit failures; it is not cross-file crash atomicity.
No source test was removed. These are compatible implementation details,
not material deviations requiring another critique.

## Exact-Criterion Engineering Acceptance

| #90 criterion | Executed oracle | Result and boundary |
| --- | --- | --- |
| Nothing scheduled/confirmed beyond evidenced committed capacity | Legacy/unknown/wrong source/version/hash/dates/unit/scope/delegation denials; offered 9 / committed 1 admits one order and refuses second; exact-quota existing booking succeeds; advance cannot bypass; deterministic SQL last-slot and dependency races | Passed on JSON/SQLite and actual local SQL Server; real source truth/legal signature and production authority not attested |
| Every work-order change version + issuer | Sequential immutable issue/appointment/non-booked/reissue/completion/correction/withdraw snapshots, named email/time/delegation/capacity version; failed writes preserve chronology/cache/audit | Passed, including HTTP eight-version lifecycle and local SQL Server inherited checks |
| System draft never instruction | Template note, persisted AI instruction_status, review effect and UI label; accept/reject review never mutates procurement | Passed; no model inference or live send |
| Contractor read-only own orders | Two supplier identities, foreign/forged identity refusals, package denial and every mutation route refusal | Passed at domain and HTTP, both contractor browser screens |

## Final Validation

* Exact suite, API cwd: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_quality_procurement test_procurement_api test_role_matrix -q`: 63 passed.
* Combined API-cwd preservation command adds test_resident_decisions, test_hazard_referral, test_buildings, test_sqlstore, test_mvp, test_change_provenance, test_bulk_edits, test_bulk_edit_api, test_form_staging, test_form_staging_api, test_ai_tasks, test_content_standard: 278 run, 277 passed and one existing opt-in skip.
* Distinct core-cwd test_buildings/test_quality_procurement/test_resident_decisions/test_hazard_referral: 114 run, 113 passed and one existing opt-in skip. This avoids mistaking the API module of the same name for the core building suite.
* Standard existing test_mssqlstore.MssqlProcurement and MssqlProcurementApi: 29 passed on a new task-owned loopback SQL Server 2022 container, no mounts/shared/live database. Environment connection credentials never printed or committed.
* Browser: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python checks/procurement_browser_check.py`: passed original-source input, inline refusal/focus, keyboard save, quota booking/version, two own-only contractor screens/write denials, 320/390/1280 reflow and reduced motion, zero page errors. External requests blocked. Teardown can log harmless loopback BrokenPipe for abandoned background fetches; these are not hidden application page errors.
* Existing configured changed-path Ruff passed, new typed test/browser and building fixture format passed; inherited migration exclusions unchanged. Core mypy passed 110 source files; API mypy passed 52 source files. Both changed JS files pass `node --check`; `git diff --check` passed.
* A later explicit-path format check bypassed existing migration exclusions and reported baseline formatting differences. Replayed with `ruff format --force-exclude --check` on the same changed core paths: four eligible files already formatted; excluded legacy modules left unchanged. Configured legacy mypy overrides also remain unchanged; type success does not imply newly strict coverage for those modules.
* Current web guidelines retrieved fully and refreshed on 2026-10-17 from raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md. Changed capacity fields/table/status and common AI note reviewed with existing Fluent 2 tokens/native semantics. No new changed-region substantive finding; existing action inputs/unsaved-navigation behavior is not redesigned. No full-site or WCAG claim.

## Remaining Boundaries and Follow-Ups

Actual contract evidence/delegations and operational approval belong to the
named human contract authority owner before live use. Hosted AI/Azure and
human/screen-reader/WCAG acceptance belong to later deployment/UX validation.
These are explicit distinct out-of-scope follow-ups, not blocked engineering
implementation. JSON is single-process and separate-file snapshot/ledger,
unlike SQL transaction/crash guarantees. No private data, live provider
instruction, award/payment, cloud/paid AI or production permission occurred.

## Phase Execution

| Phase | Execution | Evidence |
| --- | --- | --- |
| Research | Complete; Ready | Exact issue/PRD/BRD/current code, three research waves and bounded independent procurement-manager research instrument |
| Plan | Complete; Ready | Plan/details plus one Revise critique; PC-001..005 applied without divergent decisions |
| Implement | Complete | Failing-first eight failures, implemented controls, final exact/preservation/SQL/browser/quality evidence above |
| Review | Complete; Conformant | One independent read-only comparison, no substantive findings; canonical .copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md |
| Publication | Delivered | Privacy-safe 19431ad with co-author trailer pushed; main PR https://github.com/jmservera/ama/pull/384 opened using Refs #90; no closing/merge/rebase/force push |

## Implementation Status

P01/P02 complete and reconciled with plan/details; the one independent Review
is Complete with Conformant outcome. P03 implementation/evidence publication
is delivered in PR #384. Current-main integration is blocked as recorded
below; no active local engineering defect was found. This evidence does not
claim live company permission, contract approval or full PRD acceptance.

## Publication Preparation

Resolved authenticated GitHub account before staging and configured repository-local
privacy-safe author/committer email; required Copilot co-author trailer retained.
Task-owned loopback SQL container and its mode-0600 ephemeral credential file
were removed after final parity. No shared container/image or database touched.

The final freshness fetch found origin/main had advanced one commit from
reviewed baseline adedf1f to bab4bf3 (#381, initializer infrastructure and shared
KB documentation). No procurement/runtime change was added upstream. Preserved
the explicit no-merge/no-rebase direction; PR targets current main and must
report hosted mergeability/CI rather than invent integrated-main validation.
Shared KB index/log overlap may require later owner integration.

Publication reused the one completed independent Review rather than launching
the PR helper's extra review fan-out. The staged-change MCP tool is unavailable
in this host, so native Git staged diff/hygiene supplied equivalent evidence.
Existing unrelated generic PR notes are preserved; task-specific PR materials
use issue-90 names. No source behavior changed after Review.

## Publication Outcome and Stop

Implementation/evidence commit 19431ad was pushed to the requested topic.
Author and committer both use the resolved GitHub privacy-safe email; the
required Copilot trailer is present. `gh pr create` failed on GraphQL quota;
ordinary `gh api` REST creation succeeded: https://github.com/jmservera/ama/pull/384,
base main, open, Refs #90, no closure.

REST readback reports mergeable=false / mergeable_state=dirty against
bab4bf3. This is a concrete owner/coordinator integration blocker, consistent
with upstream shared-KB overlap. No hosted check runs were registered for
19431ad at read time, so CI/rubric is Pending, not passed. The explicit
no-merge/no-rebase/no-force-push direction is preserved.

Task-specific PR body/reference log and terminal phase/state metadata are
prepared for the final evidence commit/push. No source change followed the
one Review. The automatic session stops after that final push as the user
directed; no child delivery or new review is started. Owner/coordinator
integration/hosted checks, real authority and human acceptance remain
distinct follow-ups, not claimed completed.

## Authorized PR #384 Main Integration (2026-10-17)

The coordinator explicitly authorized rebasing only this run-owned topic,
overriding the earlier no-rebase restriction solely for this integration.
The old publication/stop and conflict observations above remain historical.
No new RPI cycle, independent Review, professional authority or acceptance
claim was created.

* Clean worktree and branch verified before starting:
  feat/provider-capacity-controls-90 at
  6e4dbe18d111673b41049830eb68bf81f89051c8.
* Captured expected remote lease with
  `git ls-remote origin refs/heads/feat/provider-capacity-controls-90`:
  6e4dbe18d111673b41049830eb68bf81f89051c8.
* Ran `git fetch origin main --quiet`; freshly verified final integration
  base is bab4bf3a2ac9ec030d78d27063d1390f800c5c7c.
* Ran `git rebase origin/main`. Only docs/reference/log.md conflicted;
  removed the conflict separators while preserving all upstream bytes first
  and the original complete issue-90 entry afterward. README auto-merged,
  retaining the upstream initializer route and issue-90 capacity route.
* Ran `git add docs/reference/log.md` and
  `GIT_EDITOR=true git rebase --continue`. Integrated topic head before the
  evidence-only commit is db83d4260e4f3d29fa80ce08624155ee4f59ecce
  (implementation 19431ad -> 17d7b3a; evidence 6e4dbe1 -> db83d42).
* `git range-diff adedf1f..6e4dbe1 origin/main..HEAD` shows only shared
  KB context differences for the implementation and an identical evidence
  commit. Exact byte assertions confirm the entire src patch against the
  new base equals the originally reviewed src patch against adedf1f.
  All runtime/tests/browser/component documentation remain byte-identical
  to the reviewed topic. All twelve other upstream changed paths exactly
  match main. No substantive production conflict occurred.
* Exact byte assertion confirms the final KB log equals the complete
  upstream log prefix plus the unchanged issue-90 appended entry.
  All Markdown table rows from both prior index versions are present.
  The original independent Review file is byte-identical; its historical
  Complete/Conformant result is preserved, not promoted into a new
  exact-head external gate. `git diff --check` and main-ancestor check pass.
* No full suite, SQL/browser rerun or dependency installation was warranted:
  conflict resolution changed documentation only and production/test patch
  parity is exact. Earlier executed evidence remains unchanged. No #84/#94
  affected production path required a new combined selection.
* Authenticated account resolved again with `gh api user`; repository-local
  privacy-safe author/committer retained for the integration evidence commit.
  PR body will carry the final publication commit SHA after that commit,
  avoiding a self-referential hash inside its own contents.
* Authorized push command is
  `git push --force-with-lease=refs/heads/feat/provider-capacity-controls-90:6e4dbe18d111673b41049830eb68bf81f89051c8 origin HEAD:refs/heads/feat/provider-capacity-controls-90`.
  No unconditional force, main rewrite, merge or issue closure is authorized.
  External coordinator exact-head PR gate remains forthcoming; Refs #90 only.
