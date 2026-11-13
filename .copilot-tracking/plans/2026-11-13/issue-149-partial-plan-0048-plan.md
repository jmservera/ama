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
