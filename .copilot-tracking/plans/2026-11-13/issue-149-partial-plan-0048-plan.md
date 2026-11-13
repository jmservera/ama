---
title: Issue 149 bounded partial independent UX release plan (0048)
description: Prospective plan-only forward publication conditions for the independent UX subset frozen at 9085e85c6
ms.date: 2026-11-13
---

## Status and honesty record

PLAN ONLY. No source, test or docs-body change, no push, publication, cloud, deploy or spend. This plan adds forward conditions; it does not rewrite A1, A2, A5 or any earlier critique, verdict or pin. Task `issue-149-partial-plan-0048`, parent task `issue-149-independent-ux-0042`, branch `feat/demo-149-partial-plan-0048`.

Identity (verified read-only): head at plan start `9085e85c626745a7133caf59373fe558e94f0a70`, `src` tree `1f4ac07f3985a99e7c71af8d24fd84c20dea7028`, fresh main snapshot `bb9f450fd0ad451a94d65f8cd683bf74f8975b2e`. Module trees: api `db70ee2ce18b`, core `93de8839f422`, agents `a35f7e1d7fa9`, orchestrator `f29cc12760a4`, importer `887e665146ca`.

Research readiness: supplied by the A5 executed critique and source record, the research file `.copilot-tracking/research/2026-11-12/issue-149-parent-plan-2333-research.md` and the original d790 and adverse Review records. No new decision-critical unknown was found, so no new research was run. Planning Readiness: Ready for this bounded plan.

## Coordinator scope decision (recorded, not an approval)

* The release is a separately named BOUNDED PARTIAL INDEPENDENT UX RELEASE: members 74, 176, 215, 96 combined, 156, 134 and the actual UX parent `318465aae0e484a5523fb37fda434714ca5200ab` (includes 82), plus fresh main `bb9f450f`, source-frozen at `9085e85c6`.
* This is the coordinator scope change that original PC-01 and AC-04 and A5C-01 require. It is NOT the complete A2 release and does NOT satisfy the A2 Wave B rule (every member admitted or named in a recorded deferral). The original A2 complete cut line stays UNSATISFIED.
* The ENTIRE 233 feature stays open and human-held (five correction cycles spent; the typing-only extension is unavailable and unavailability is NO APPROVAL). 233 is neither admitted nor deferred. No owner approval, requirement relaxation, 233 deferral, entire-149 completion or epic closure is inferred. No 233 fix elsewhere, no borrowed earlier Pass as new-head acceptance, no acceptance tick, no closing keyword, no new source correction pool.
* The original full candidate `d790b6b45d31131f600414a2728af85ec5b5444f` and its original adverse Review stay held and immutable. The d790 Partial outcome is preserved.
* A5 permitted source assembly only. It is not retroactive publication permission. The conditions below are new and forward only.
* The unmerged sibling 1498 is not adopted. Held and unchanged: affected 233, the full A2 cut line, the epic and all dependent closure.

## Required validators (fresh, on the exact final head or an equivalence-documented identical `src` tree)

Each validator runs from `git archive` of the exact input in an isolated venv with non-editable installs and no source `PYTHONPATH` workaround beyond the documented test-helper path. Results are recorded as actual outcomes; nothing is invented or borrowed from d790.

| Lane | Required check | Status at plan time (honest) |
| --- | --- | --- |
| Types and lint | Configured core and api `ruff check`, `ruff format --check`, `mypy` (core 298 files, api 236 files at 9085) | 0045 lane executed, exit 0 after one archive-only correction (removed pip `build/` copies); result `rpi-149-types-0045-result.json` |
| Forms, 74 historical selectors | `test_finance_grants_screens`, `test_form_held_download_api`, `test_role_endpoint_inventory` and related, 74 tests | NOT passed. The 0045 run had 1 failure (`test_every_role_against_every_endpoint`, 500 on `/api/ai/report`) and the log shows "The law store is not loaded"; the cause is not yet shown to be only the archive environment. No result JSON exists. It must be rerun with a complete input and the failure explained or fixed under the original routes; a failing test is never waived or deleted |
| Home, baseline programme, full API | `HomeCaseApiTests`, `ProgrammeScreen`, `ApiTests` (28 tests) and the full api suite | 0045 home lane: 28 run, OK. The full api suite has no actual result recorded and is still required |
| Four browser journeys | `held_form_download`, `programme_paging` (baseline programme only, no 233 additions), `home_case`, `regulatory_ux_check`; non-queued heavy lock `flock -n /tmp/ama-rpi-heavy.lock`, Playwright 1.64.0, axe-core 4.10.3 (sha256 `880970c0...a68bb`) | 0045 browser lane: all four exit 0 after one environment-only correction (missing tests path); `rpi-149-browser-0045-result.json` |
| Synthetic, 51 historical selectors | `GeneratedDatasetTests`, `NeedsInventoryTests`, `ScenarioManifestTests`, `DeterminismAuditTests` | 0045: 51 run, OK, an actual new result; the d790 51 is not asserted equivalent |
| Core 72 | May be REUSED only when explicitly labelled REUSED and the archive input identity is unchanged: `src/core` tree `93de8839f422d3d502f7f6197bedaf68e45f12a7`, `src/README.md` blob `b6e13012a836b53d1d04ae9ce6c021c331cbfb82`, `README.md` blob `f47c6be00a06ffaa54b561d89fb8bff1fe792434`, all the SAME as d790 | Identity comparison to d790 is a required recorded step; if any differs the 72 are rerun fresh. No new pass is invented |

The forms lane is the only validator with an open failure. No default full gate and no waived applicable check; the focused tier classification of A1 is retained, and the strictest-tier rule applies to any later change in permissions, SQL, deployment, security or dependency manifests.

## Forward publication conditions (all required; none satisfied by this plan)

1. Required validators above all actually recorded green on the final source identity, forms lane included.
2. Original final RPI Review, run once, consumes the actual validator results and the new partial scope, and preserves the d790 Partial outcome; findings route to later work.
3. A final dated affected-surface checkpoint in the existing cut-over pack, with BRD, PRD and ADRs still draft or in review and no human, assistive-technology, Finance, live, full or MSSQL acceptance recorded.
4. A fresh independent exact-final-head assessment on a clean candidate. A metadata-only commit after that needs a documented source and inputs equivalence (same `src` tree and pinned input blobs) and a final-head assessment; an old-head Pass is not blindly reused.
5. Before push: original four RPI areas and the log proof, clean worktree, no dirty, untracked or ignored input.
6. Before merge: actual all-green reported and required checks and MERGEABLE state; no absent, skipped or path-filtered workflow counted as success. Human approval and the merge decision stay with the owner.
7. The unmerged 1498 is not adopted. After the actual merge, evaluate current-main path compatibility explicitly; no gratuitous rebase or retarget.
8. The original adverse and d790 records, A5 pins, the 134 fresh root assessment (`ca14b1523`), the amend-process qualification, six partial and four deferred dispositions and open #83 wording in 134 stay unchanged.

## Closing-message hazard (original RV-002, historical 8307)

A historical commit message carried a closing phrase for #83. Forward rules: no history rewrite; the PR body uses `Refs` only and no closing keyword, even negated; verify `closingIssuesReferences` is empty before and after any body edit; set the squash title and body explicitly, Refs-only, and review the proposed message for any close, fix or resolve keyword before merge; verify #83 is still OPEN after merge. Issue 149 and other unmet issues get `Refs` with the unmet criteria listed; no acceptance box is ticked.

## Unresolved gates carried forward

* Forms 74 rerun and explanation (open failure).
* Full api suite actual result; core 72 reuse identity or fresh run.
* Original Review, checkpoint, fresh exact-head assessment, push preconditions, CI and merge gates.
* 233 scope, deferral and epic or A2 completion decisions, which stay held with the owner and are not decided here.

## Pending genuine independent critique

One independent read-only fresh-context critique runs once on the committed plan. It may disagree; its findings are preserved and only coherent plan-only dispositions are applied.

## Correction notes (after the independent critique, 2026-11-13)

The text above is preserved unedited; these notes supersede it where they differ. PLAN ONLY.

* Role regressions (P48C-01). The 0045 roles lane (`rpi-149-roles-0045-result.json`) records a SOURCE FAILURE: `RoleScreens` plus `RoleScreenConformance` ran 19, 17 passed, 2 failed on `9085e85c6` (`test_host_reads_existing_scoped_endpoints_without_post` and a second test on a single-timer expectation), attributed to the `role-screens.js` additions (+90/-1); `role_screens_browser_check` exit 0 (47 PASS). The statement above that the forms lane is the only open failure is withdrawn. Both failures stay open: they are resolved only through the existing owner route (test and source decision belong to the owner), with no new correction pool, no waiver, no deleted or relaxed test, and no earlier Pass borrowed. Publication is blocked until they are actually resolved and the lane is rerun.
* Inherited core gates (P48C-02). The core funding and queue selectors, the mandatory SQLite regression and invariants and the SQL prerequisite probe named in the A1 and A2 focused-tier checks stay required. Core 72 reuse is allowed only if selector-level proof shows that its recorded selectors include each of them against the identical archive input; otherwise the missing selectors run fresh. An unobserved SQL prerequisite is reported UNOBSERVED, never as a pass.
* Equivalence scope (P48C-03). `src` tree equality alone is not equivalence. Per lane, every archived input that lane reads (for example runbook, generator `.py` files, `docs/reference/research/ux`, `tools`, `.github`) must be identical by blob or tree; otherwise the lane is rerun on the final head. The synthetic 51 is rerun if any such input differs.
* Review blocks publication (P48C-04). The condition "findings route to later work" is replaced: the original final Review runs once, and publication needs a passing outcome with every material finding resolved or explicitly outside the bounded scope with owner-visible routing. Non-material findings route to later work. The 0045 source review (`status partial`, no blocking findings, three medium-low or low copy and guideline observations, tests not run) is input only, not the original Review.
* Ancestry and tier (P48C-05). On the final candidate, re-run `git merge-base --is-ancestor` for `aebd381d9` and `837da4fde` against the candidate and re-search for 233 symbols; stop with proof on any ancestry or dependency. Inspect the actual final diff hunks, and escalate to the full tier for any workflow, gate-tool, Dockerfile, dependency-manifest, permission, secret, deployment, security-control or unresolved-impact change.
* Forms status (P48C-06). The forms result now exists: the initial run failed 1 of 74 (500 on `/api/ai/report`, `FileNotFoundError` because the non-editable archive lacks the `evals/` golden file), then a diagnostic run with `ZF_AI_GOLDEN` pointed at the archived golden file passed 74 of 74, no failures or skips. This is an environment-only diagnosis; it counts as the required forms evidence only if the final run documents that archive and `ZF_AI_GOLDEN` setup against the exact final input, and it is not an unconditional final-head pass.
* ADR wording (P48C-07). The checkpoint preserves each actual document status and its scope as read at the checkpoint (for example ADR 0005 Accepted for synthetic development only; the BRD, PRD and ADR 0003 to 0007 blobs equal main `bb9f450`). The phrase "still draft or in review" is not used as a blanket claim and no further approval is inferred.

## Amendment 0055: caller-scope correction and C3 integration conditions (2026-11-13)

PLAN ONLY, tracking files only. Everything above, including the original A6 plan (source-only `f128...`) and its actual Revise critique with P48C-01..07, is preserved unedited. This amendment supersedes earlier text only where it differs, and only prospectively. It waives no failing check and erases no adverse history.

### A55-01 Root correction of the "full API" requirement

The original caller brief (`ux-partial-plan-0048.txt`) named "home/baselineprogramme/fullApiTests". That meant the FULL LOCAL `test_mvp.ApiTests` CLASS (6 methods) inside the home, baseline programme and ApiTests lane. The earlier table rows "Home, baseline programme, full API" and "ApiTests (28 tests) and the full api suite", and the unresolved-gate bullet "Full api suite actual result", misread this as a new gate over the entire api project suite. That was a caller-scope misinterpretation, not a failing check that is being waived. The whole-api-suite gate is withdrawn before it becomes a publication condition. The home lane is `HomeCaseApiTests`, `ProgrammeScreen` and the full `ApiTests` class (28 tests in the 0045 run, which is the actual count and not changed here). The 0045 home lane result (28 run, OK) is an actual new result on `9085e85c6` and is not final-head acceptance.

The validation tier stays the standing owner focused modified and impact tier. There is no default full gate. A full api suite or any extra selector is required only for a distinct, source-backed impact that is identified explicitly in the final diff review (for example an api route, auth or SQL change); no full campaign is invented.

### A55-02 Required impact-selected validators on the final candidate

All run against exact archived final-input identity, with actual outcomes recorded. Failures and diagnostics are preserved; no test is deleted, relaxed or waived.

* Core 72: all 10 original selector classes with exact input and selector proof. Reuse of the original ROOT result `rpi-149-core-validation-0025-result.json` (10 selectors, 72 tests, 0 skips, SQLite plus mocked portability, NOT actual MSSQL) is allowed only when the archived inputs are identical: `src/core` tree `93de8839f422d3d502f7f6197bedaf68e45f12a7`, `src/README.md` blob `b6e13012a836b53d1d04ae9ce6c021c331cbfb82`, `README.md` blob `f47c6be00a06ffaa54b561d89fb8bff1fe792434`. Root already proved these three identities equal for the archived inputs at `9085e85c6`; the final candidate must be re-compared, and any difference means a fresh run. The SQLite, queue and funding selectors required by P48C-02 are mapped to the enumerated selectors honestly; any selector not actually present runs fresh. Mocked or SQLite results are never reported as MSSQL.
* Forms 74: the four forms classes with the documented archive plus `ZF_AI_GOLDEN` input path per P48C-06, on the final input lineage.
* Home, baseline programme and ApiTests: `HomeCaseApiTests`, `ProgrammeScreen`, full `ApiTests` class.
* Role 19: the local `RoleScreens` and `RoleScreenConformance` classes (19 tests) plus the existing role browser check. The two recorded failures stay actual until a reviewed C3 candidate actually fixes them.
* Finance, design and content impact selectors: required only if the final source differs in those areas.
* Synthetic 51: the four classes `GeneratedDatasetTests`, `NeedsInventoryTests`, `ScenarioManifestTests`, `DeterminismAuditTests`, rerun if any lane input differs (P48C-03).
* Four browser journeys (`held_form_download`, `programme_paging`, `home_case`, `regulatory_ux_check`) plus the existing role browser check.
* Configured lint and types (core and api `ruff check`, `ruff format --check`, `mypy`).

### A55-03 C3 candidate and integration conditions

Facts recorded as of 2026-11-13: native `96-impact-c3-0052` is correcting two role contract failures (the approved read-only freshness POST versus the blanket no-POST expectation, and accessible focus restoration versus the single-timer expectation). It works in a separate `9085e85c6`-based worktree, with one C3 of five cycles using the ORIGINAL 423 UI and backend 2236 states and two spent. The older whole-96 unknown is preserved. No actual fix or Pass exists yet.

* The current `9085e85c6` head is NOT publishable. The A6 plan source-only `f128...` stays immutable.
* Publication needs an actual reviewed clean C3 candidate (reviewed against the original role contract tests, which are not rewritten to fit), normal integration of that candidate into the exclusive parent, a FRESH final source freeze, and the impact-selected validators of A55-02 on the new identity with explicit input-identity mapping.
* A `9085e85c6` Pass or diagnostic is not reused after any source change unless an input-identity proof shows the lane inputs are identical.
* This plan task does not fix, merge or adopt any source. The C3 author is not instructed to adopt main.

### A55-04 Merged 1498 and current main

PR 1498 actually merged 2026-11-13T00:53:04Z; main is `c5bfac6eeca7f6180588a3ffdad124bfb14d0943`. This supersedes P48 condition 7 and the "unmerged sibling 1498 is not adopted" wording prospectively, and makes the earlier `bb9f450f` snapshot historical. The root permits a LATER final integration author to normally merge actual current main after C3 acceptance, with no new parent deferral, retarget or rewrite. This plan task merges no product source. Every input that changed on main (AI harness, README, tests, original RPI records) is compared for final validation compatibility at integration, and the old `bb9f450f` base claims stay historical. The full tier is triggered only by actual new permission, SQL, security, deployment, dependency-manifest or control changes.

### A55-05 Unchanged and retained gates

* The release stays the separately named PARTIAL independent UX release, not the complete A2. 233 is neither admitted nor deferred, the original full candidate and Review are immutable, and the five-spent 233 extension is unavailable, which is no approval.
* No epic, human, resident, assistive-technology, Finance, live, full or MSSQL acceptance is recorded, and no new source pool is created.
* Before the respective publication gates: actual final original RPI Review, a fresh independent exact-head assessment, the checkpoint, hosted checks all green and MERGEABLE, a clean candidate, the four RPI areas and the log proof.
* Standing coordinator guarded merge authority is unchanged. No new human merge approval gate is invented for run-owned PRs; the named human acceptance ACs stay open.
* Final ADR status is read per blob, with no blanket draft claim. PR and squash message are Refs-only with empty `closingIssuesReferences`, and #83 stays OPEN; no history rewrite.
