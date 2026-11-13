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
