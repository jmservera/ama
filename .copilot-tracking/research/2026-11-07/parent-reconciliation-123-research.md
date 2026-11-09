<!-- markdownlint-disable-file -->
# Research: discovery parent reconciliation (#123, Refs #440 #128), 2026-11-07

Task slug `parent-reconciliation-123`. Prospective continuation of native session b1e0f493 (earlier task `parent-integration-preparation-123`, 2026-11-05, unchanged). Research disposition: executed (read-only git identity, scope and conflict forecast before any merge). Planning Readiness: Ready.

## Scope and provenance

* Worktree `/home/azureuser/source/ama-wt/integration-123`, branch `feat/discovery-assurance-integration-123`, HEAD `dec700c7af46778140bf5c46d4df932832a31f11`, tree `00c8ace3f07f4bcb54daa2421b6003c2c966ef5b`, ignored-inclusive clean at start.
* Fresh fetch 2026-11-07: `origin/main` `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01` and `origin/feat/discovery-assurance-integration-123` `9bacb87dc04fb51ba747b35ec78061b05af184be` (tree `a28698aff27aa2379a782a8f8f156d3333014e48`). Both equal the coordinator's expected identities, so no intake stop. Open PR #1222 (head `9bacb87d`, base main, `CONFLICTING`) uses Refs only. gh identity id 8036360 login `jmservera`; repository-local email already `8036360+jmservera@users.noreply.github.com`.
* The local HEAD `dec700c7` is the merge base with the remote parent: the remote parent is six commits ahead (`#1225`, `#1227`, `#1230`, `#1232`, `#1234`, `9bacb87d` delivery-evidence integration after reviewed child #1235). Main merge base with local HEAD is `bb3a3b03`.
* Issue and PR snapshots supplied in the task were read as data only.
* Read for this task: repository instructions, the case-study documents and reference index/memory (sizes inspected; memory is context only), the existing issue-123 RPI records and evidence-pack sixth to eighth checkpoints. No private dataset and no model or cloud call.

## Findings

* Remote-parent delta relative to `dec700c7`: 120 files, 6300 additions, 0 deletions. Non-tracking files are only `docs/architecture/cutover-evidence-pack.md` (+1335), `docs/reference/README.md` (+71) and `docs/reference/log.md` (+92); the rest are dated `.copilot-tracking` records. No source, test, schema or tooling file changes. The executable change set of this topic therefore remains the inherited constructed `paired_equity.py` diagnostic, its tests and the core README paragraph.
* Main delta relative to `bb3a3b03`: 437 files (+27591, -134), including API, core (`projection.py`, `quality.py`, `test_list_export.py`), tooling (`tools/rpi-checks.py`, `tools/backlog-sync.py`) and docs. None touches `paired_equity.py`, its tests or modules it imports (`journey_register`, `ranking`, `rai_release`); this must be re-verified after the merge.
* Overlap of changed paths between parent and main: `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md` and `docs/reference/log.md`. `git merge-tree` forecast: README and log auto-merge; the evidence pack conflicts (both sides append; main adds one trailing section "Parent #73 topic checkpoint" and an `ms.date` bump to 2026-11-07). Intent is establishable: both are append-only records, so both sides are retained.
* Absent newer-main content in the parent is not a feature deletion by this topic; after merging main the diff against main must contain no main-side deletions.
* Tier: FOCUSED holds. The parent delta is documentation and RPI evidence; combined with the inherited constructed diagnostic, scope is bounded metric tooling, tests and documentation. No infrastructure, SQL, finance, security, deployment or live policy activation is added. If the post-merge main-relative diff contains any path outside the paired-equity source, test, core README, the three documents and dated RPI records, stop and reclassify.
* Remote-parent evidence (#1225 to #1235 checkpoints) is parent-topic documentation with its own original and adverse records; it is preserved unchanged and is not main acceptance.
* The component guide `src/README.md` (local RPI gate) defines `--changed`, `--lock-timeout 0` non-queued admission and `--required-scope partial` receipt verification against the base.
* No new defect is confirmed by this research.

## Constraints

* Ordinary merges only: first pinned parent `9bacb87d`, then pinned main `b284d0d3`; no rebase, reset, amend, force, main change or push. Preflight pins before each merge.
* Retain both intents on every append-only conflict. Stop if intent cannot be established.
* Heavy lock only for the single focused run `python3 tools/rpi-checks.py --changed --jobs 2 --lock-timeout 0`, non-queued, new owned output on the root filesystem; no SQL, browser, scanner, image or full work; protect #1231 R35 receipt and images, root ranking source and main. Stop if the focused selection needs excluded groups.
* Whole epic, human, legal, accessibility and actual-model criteria stay unproven; `Refs` only.

## Planning Readiness

Ready.
