<!-- markdownlint-disable-file -->
# Source assembly record: independent UX lanes without 233 (issue 149, task issue-149-independent-ux-0042, 2026-11-13)

Original record for a separately owned new subset. It is a source freeze, not acceptance, and not a publication candidate yet.

## Status

* Stage: Implement (source-only assembly). Plan: amendment A5 and its correction notes in the [policy amendment](../../plans/2026-11-12/issue-149-parent-plan-2333-policy-amendment.md), with the executed independent critique (Revise, A5C-01 to A5C-03, applied) in the [critique file](../../plans/2026-11-12/issue-149-parent-plan-2333-critique.md), both committed (`e2b452946`, `585021fad`) before any merge.
* The entire 233 feature is EXCLUDED: `aebd381d9` and `837da4fde` are not ancestors of the head, and none of the 233 files (`test_programme_screen.py`, `programme_paging_browser_check.py`, `atlas-screen-trace.md` edits) or `role-screens.js` programme hunks are present (verified by diff against main and symbol search for `screenPageSize`, `programmeCell`, "Open connected view"). 233 is neither admitted nor deferred here; it stays open and human-held with its original candidate. This record claims nothing about 233 status.
* 233 is not a dependency: no real source, test or import dependency of 74, 176, 215, 96, 156 or 134 on 233 was found. The shared `role-screens.js` overlap with 233 is hunk-disjoint and `fundingDraftPanel` (96) is present. One 134 pack row names #233 as an issue pointer for a future executed check; it is preserved verbatim and is not a delivery claim.
* The original d790 candidate, the original adverse Review and the 108 frozen heads are untouched. 1498 is not adopted. 203 is excluded. 108 is not adopted.
* Not run, by instruction: mypy, ruff, unit, browser and hosted-CI lanes, axe, assistive-technology, WCAG, Finance, human or legal acceptance. The new subset needs fresh configured mypy, focused unit and browser checks and an original independent Review before any publication; no earlier Pass is reused as acceptance of this head.
* No new correction pool, no product-code fix, no new test, no amend, rebase or rewrite, no push or publication, no issue, tick or cloud action. Actual source correction history and extensions carry unchanged (82/1490 one combined correction; 134 corrections 1 and 2 plus the preserved adverse amend process note and root fresh assessment; 96 corrections 1 and 2; 233 five spent and held; 74, 176, 215 none recorded); unknown is not zero.

## Merges (normal `git merge --no-ff`, in plan order)

| Step | Input | Pin | Merge commit | Result |
| --- | --- | --- | --- | --- |
| M0 | actual UX parent (includes 82 and the 1490 funding correction) | `318465aae0e484a5523fb37fda434714ca5200ab` | `0bc3d077b` | no conflict |
| M1 | fresh main (includes 1495 `e44de171e`) | `bb9f450fd0ad451a94d65f8cd683bf74f8975b2e` | `c7763486f` | no conflict |
| M2 | 74 | `467a0cf5d108cd6b3f0111661facfc2e85a6ce8a` | `82576c65e` | no conflict |
| M3 | 176 | `da436be3e149f1e445440f16d5460edd590fefc3` | `388fabe84` | no conflict |
| M4 | 215 | `6eacb4953534ab86416a65c337cb9c43bc5cb1f2` | `e765a9f52` | no conflict |
| M5 | 96 combined (backend `94760af7d` carried once) | `423517a71f2acb41baaa292cff08d3be7d32d995` | `2f0dd8485` | no conflict |
| M6 | 156 docs | `d8fe60017407f3f7df4b339dfa0bfaff06dfacbd` | `eadbd8828` | no conflict |
| M7 | 134 main-aligned correction | `ca14b1523495c9304ecc076bd3fef7b4a43d19fa` | `0ea6b004d` | one keep-both conflict, see below |

First-parent chain after the plan commit `585021fad`: `0bc3d077b`, `c7763486f`, `82576c65e`, `388fabe84`, `e765a9f52`, `2f0dd8485`, `eadbd8828`, `0ea6b004d`. Each merge commit has the previous head as first parent and the pin as second parent. The pre-merge read-only sequential `git merge-tree` simulation matched.

## Conflict resolution (M7, only conflict)

`docs/architecture/cutover-evidence-pack.md`: the known keep-both case (134 section against main's later section). The local git rerere cache supplied the earlier resolution; no marker remained and no wording was edited. The resulting blob `5bb0897b370b3a3c82f8f19cdab791bce20cbc29` is byte-identical to the original assembly resolution, the file has zero deleted lines against the pre-merge head and 43 added, and the 134 section, the AI parent integration section and every historical section appear once.

## Source preservation checks (minimum only)

* `git diff --check` against main, a conflict-marker search over tracked files, `node --check` on every tracked JavaScript file and `compileall` of `src` all pass.
* 233 exclusion: neither 233 commit is an ancestor of the head; 233 symbols absent; none of its three non-RPI files differs from main.
* Against fresh main `bb9f450fd`: `src` differs by 22 files, 1256 insertions, 31 deletions; the whole tree by 169 files including `.copilot-tracking`. Changed non-RPI paths: docs (`cutover-evidence-pack.md`, runbook, `docs/reference/README.md`, `log.md`, retrofit README, prototype profile review), `src/api` (README, three checks, `server.py`, `chat.js`, `role-screens.js`, six tests), `src/core` (four source files, six tests). No workflow, manifest, Dockerfile, infra, SQL DDL, migration or gate-tool path is changed; the focused-tier classification is left for the validators and the Review to reassess.

## Pins at the source freeze

* Base lineage: plan commit `585021fad` (from `c807923ec`), actual parent `318465aae`, fresh main `bb9f450fd`.
* Source-frozen head before this record `0ea6b004d022994eb4e493ef77b39af6f4ff3c4a`; `src` tree `1f4ac07f3985a99e7c71af8d24fd84c20dea7028`. This record and the state file touch only `.copilot-tracking/`, so the `src` tree is unchanged at the final head.
* Module trees: `src/api` `db70ee2ce18b`, `src/core` `93de8839f422`, `src/agents` `a35f7e1d7fa9`, `src/orchestrator` `f29cc12760a4`, `src/importer` `887e665146ca`.
* Blobs: `role-screens.js` `3dd3fc729dda`, `server.py` `559dafde45f1`, `store.py` `c4c893e69c02`, `cutover-evidence-pack.md` `5bb0897b370b`, `log.md` `146a82402515`, `docs/reference/README.md` `095c03ab6f96`.

## C3 and current main integration (2026-11-13, task issue-149-c3-integration-0101, source integration only)

Plan: prospective partial plan `3862d97b390a74dac1d103b5c24bfce8bebda871` with its executed independent amendment critique (A55C-01 to A55C-04, all four dispositions preserved, not repeated). Branch `feat/demo-149-c3-integration-0101` from `3862d97b3`, `src` tree `1f4ac07f3985a99e7c71af8d24fd84c20dea7028`. Normal `git merge --no-ff` only; no rebase, retarget, rewrite, amend, push, publication, issue or tick; no application or test source fix and no new test.

| Step | Input | Pin | First parent | Merge commit | Result |
| --- | --- | --- | --- | --- | --- |
| M0 | reviewed C3 (96 impact tests-only candidate, root accepted for integration only) | `ec25487e2b9503b8497a480a6e7e5ab5fed82fe6` (src `bf90280b779378b595a184261a36254f9750357b`) | `3862d97b3` | `d4f0c92fccc2082c08ee99976d3f3144317fc41e` | no conflict |
| M1 | fresh actual `origin/main` after fetch | `c401e5d56446b5752e8d91af6a45f3f06269c4bd` | `d4f0c92fc` | `b705b61f149430517fa753ce9d63da0f809b19a1` | no conflict |

* Main movement: the root-known main `c5bfac6ee` (1498 merge, 00:53:04Z) is an ancestor of the fetched main; the only later commit `c401e5d56` changes `.github/rubric/scores/latest.json` (score record, not a source input). The 1498 merged content (agents `ai_eval.py`, its test and README, 108 offline coverage records) arrives only through this normal main merge; it is merged main, not adoption of an unmerged sibling. No unexpected material main change; no stop.
* C3 hunks (two test files only, 118 insertions and 7 deletions against `9085e85c6`): `src/api/tests/test_role_screens.py` (blob `176ae1d016a2`) and `src/api/tests/test_role_screens_conformance.py` (blob `ff1da56aa9a8`); product `role-screens.js` is unchanged (blob `3dd3fc729dda`). No product, CSS, control, SQL, workflow, manifest, Dockerfile, infra or 233 change and no blanket test deletion.
* 233: `aebd381d9` and `837da4fde` are not ancestors of the head; the entire 233 feature and the original d790 candidate and Review stay excluded and immutable. 233 is neither admitted nor deferred; no complete A2 or epic claim. Eventual Refs-only wording, empty closing references, open #83, the 134 six-partial/four-deferred dispositions and the `ca14b1523` amend qualification are preserved.
* Correction history: 96 has three of five corrections spent and two left; older whole-96 history is unknown and preserved; 233 five spent and held.

### Pins at this source freeze

* Source-frozen head before this record and the state update: `b705b61f149430517fa753ce9d63da0f809b19a1`; `src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`. This record and the state touch only `.copilot-tracking/`, so the `src` tree is unchanged at the final head.
* Module trees: `src/api` `0786923447a54a5bb2ac4e9ac7dd261f61522dca`, `src/core` `93de8839f422d3d502f7f6197bedaf68e45f12a7`, `src/agents` `ce54d120cc1c22177d7fd9f464cc89d39f92c2cb`, `src/orchestrator` `f29cc12760a42a3be2c3d0f854d42b2ce3ada666`, `src/importer` `887e665146ca1720dbb1074e79065bcd48c89810`.
* Blobs: `server.py` `559dafde45f1`, `store.py` `c4c893e69c02`, `ai_eval.py` `63e009089555`, `test_ai_eval.py` `83cbaedb6976`, `cutover-evidence-pack.md` `5bb0897b370b`, `docs/reference/README.md` `095c03ab6f96`, `docs/reference/log.md` `043f5a6644ac` (log differs from the earlier `146a82402515` because main's 108 entries merged).
* Against `3862d97b3`, `src` differs by five files (449 insertions, 22 deletions): the two C3 tests and the main-borne `ai_eval.py`, `test_ai_eval.py` and agents README. Against main `c401e5d56`, `src` differs by 24 files (1374 insertions, 38 deletions), the non-RPI set being the 134/82/74/176/215/96/156 subset already recorded, plus the two C3 tests; the changed non-RPI docs are the same set as before. No workflow, manifest, Dockerfile, infra, SQL DDL, migration or gate-tool path changed relative to main; the focused-tier classification and its actual triggers are preserved for validators and the Review to reassess.

### Checks run (minimum only)

`git diff --check` against main, a conflict-marker search, `node --check` on every tracked `src` JavaScript file and `compileall` of `src` pass. Not run, by instruction: unit, browser, mypy, ruff, axe, full gate; standalone MSSQL, human, assistive-technology, Finance, live and full-gate coverage are unobserved. Old `9085e85c6` results are historical, not a pass for this head; the role/conformance lane is now 21 tests (not 19) and the six-method ApiTests class is not the whole project suite; core 72 reuse needs exact all-archive-input re-proof, with synthetic, form and browser out-of-`src` reads pinned too. Original Review, checkpoint, independent exact-head assessment, hosted checks and human acceptance remain required before publication.

## Affected-integration checkpoint preparation (2026-11-13, task issue-149-checkpoint-0117, metadata only)

Branch `feat/demo-ux-partial-release-0117`, starting at `288b6a37665602718122ed0ab35b9bbdcca963ed` (`src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`, unchanged). Same coherent integration topic, not a sibling pull request. Continues the existing Implement evidence finalization; no new loop, no new plan and no new correction authority.

* Changed: `docs/architecture/cutover-evidence-pack.md` (new dated section "Partial independent UX release affected-integration checkpoint", `ms.date` 2026-11-13; all earlier sections untouched) and this record plus the state file. No source, test, manifest, workflow, infrastructure or gate file changed; no new page.
* Inputs consumed: the C3 integration result, the amendment 0055 result, the C3 root assessment, all eight actual 0104 results (types, forms, home, roles, browser, synthetic, ai, trace) and the actual 216 integrated module result (12 of 12, exit 0, no skips). The trace's stale pending-results statements are reconciled against the completed results. The restricted outer native AI log was not read or copied.
* Original Review `rpi-149-original-review-0104` (Partial; conformant within the bounded partial scope; five Low observations; no Critical, High or Medium) is cited as a provisional actual outcome only: not adopted, not copied, not coordinator-consumed. d790 and Review 0031, early 0045 Partial and the C3 three Low limits are preserved.
* Read-only check: `origin/main` fetched `c401e5d56446b5752e8d91af6a45f3f06269c4bd` (equals expected); no merge or rebase.
* Not run here, by instruction: any test, lint, type, browser or gate; core 72 stays REUSED. A focused diff, ASCII, table and relative-link review of the pack change was applied.
* Not claimed: final Review or Pass, finished RPI, independent exact-head assessment, publication readiness, hosted acceptance, any criterion tick, human or owner approval. 233 held; whole 149, A2, epic, manual acceptance testing, Finance, legal, live and actual SQL Server open.
* Proposal only: bounded CONTINUE under original Review adoption, remaining validation, final metadata equivalence, independent exact-head assessment and actual hosted gates.

## Final evidence assembly (2026-11-13, task issue-149-finalize-evidence-0131, metadata only)

Continues the existing Implement/Review evidence handoff on `feat/demo-ux-partial-release-0117` from `37e2715b5175cce0c5470904817fd69ea5eea5eb` (`src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`, unchanged). No new loop, plan, correction or allowance; no source, test, tool, workflow, infrastructure, manifest or README change.

* Changed: the dated checkpoint section of `docs/architecture/cutover-evidence-pack.md` (216 coexistence wording corrected so it no longer implies a child introduced by this branch, stale "not yet consumed" statements updated, and a final evidence assembly subsection added), this record, the 0042 state, and new dated records under `.copilot-tracking/reviews/2026-11-13/`: the labelled public technical copy of the original Review and its result JSON, the two 0122 provenance complements, the 0125 metadata input proof, the 216 integrated result, the 153 independent records and the adoption record `issue-149-partial-release-evidence-adoption-0131.md`.
* Original Review `rpi-149-original-review-0104`: adopted as an immutable original result, execution Partial and outcome conformant within the bounded partial scope, five Low observations open. The tracked copy is a derivative that omits only private operational handling text, marks each omission and records the SHA256 of the privately retained original. It is not verbatim and not a newly executed Review. The restricted native log was not read or copied.
* Complements, metadata input proof (binds `37e2715b5`, not the final head, three metadata files differ and are not read by any lane) and the 153 input (nine tracked paths read in full, blobs equal at `c358dd675`, `8f8be74e1` and head; independent Pass per input and not an assessment of this head) are recorded with their own Partial status and exact residuals. The 216 content is already on main (PR 1495); the integrated run proves coexistence only.
* Supersession of historical markers: the blockers in the 0048 state (`roles-failures`, `validators-incomplete`, `publication-gates`, `c3-candidate`) and the `validation-pending` blocker and pending Review markers in earlier text of this record are historical. The C3 candidate is integrated, the lanes passed on actual results and the Review has an actual outcome. The current 0042 state is authoritative; original critique and child state history are not rewritten.
* Read-only: `origin/main` fetched equals `c401e5d56446b5752e8d91af6a45f3f06269c4bd`; no merge or rebase.
* Not run: any test, lint, type, browser or gate, by instruction. A focused Markdown, link, table, JSON and diff review was applied.
* Not claimed: RPI fully accepted, fresh validation of the final head, final independent exact-head assessment, publication readiness, hosted acceptance, any criterion tick, human or owner approval. 233 held and neither admitted nor deferred; whole 149, A2, epic, manual acceptance testing, Finance, legal, live and actual SQL Server open.
