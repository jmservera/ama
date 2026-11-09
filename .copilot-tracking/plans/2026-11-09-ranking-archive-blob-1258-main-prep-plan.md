# Issue 1258 main preparation plan (2026-11-09)

Refs #1258. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-main-prep-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-main-prep-details.md`.

## Objective

Advance the parent candidate onto fetched `origin/main` `9f9aacc8b` with a local merge commit that preserves both intents, record that source is byte-equivalent to the approved `52f9b61b` for all executable paths, and record the exact remaining #1292 integration and test plan. No source edit, no sixth cycle.

## Phases

* [ ] Phase 1: commit this prospective research, plan, details and critique alone (no merge, no check yet).
* [ ] Phase 2: `git merge origin/main` locally (merge commit, no rebase, no force). Any conflict or any source path in the merge delta stops the task.
* [ ] Phase 3: source equivalence and bounded validation: tree comparison of `src`, `infra`, `tools`, `.github` against `52f9b61b`; `git diff --check`; Markdown link review of touched tracking records; no code test rerun when equivalence holds.
* [ ] Phase 4: changes record, one original Review, state, local commit, handoff.

## Critique dispositions (one critique, not repeated)

Record: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-main-prep-critique.md`. All five findings are compatible and applied directly.

* PC-MP-1 Blocking: merge the immutable SHA `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` only, after re-fetch confirms `origin/main` still equals it; if it moved, stop and report, do not merge.
* PC-MP-2 Significant: equivalence is claimed only for the tested application trees `src`, `infra`, `tools`, `.github`, not for "all executable paths". The delta also holds docs-side Python/JSON (`docs/capstone/.../anc/test_*.py`, `supplement-integration.json`, `diagram-exports.json`) and tracking JSON; these are unrelated paper tooling, not run, not tested, not claimed. The merge delta must equal the pinned 36 paths and root configuration files (`pyproject`, `requirements*`, `.github`) must be absent from it.
* PC-MP-3 Significant: the future #1292 integration needs new issue-specific authorization before any source resolution or correction; textual forecast does not grant it.
* PC-MP-4 Significant: final records use new unique paths with the `-main-prep` suffix; stop rather than overwrite an existing review or state file.
* PC-MP-5 Minor: merge commit uses the same repo-local identity as author and committer plus the Copilot trailer, verified after the merge.

## Equivalence and tier

Owner DEMO targeted tier. A docs-only advance takes no broad rerun. Equivalence proof: `git rev-parse HEAD^{tree}:src` (and `infra`, `tools`, `.github`) of the merge equals the same objects at `52f9b61b`. If equal, the c5 results (core 137 OK, API wiring 35 OK, ruff and mypy clean) are inherited by tree identity and labelled as inherited, not re-observed. If any differ, the plan stops (unplanned source in the delta) and runs nothing further.

## Remaining #1292 integration plan (not executed here)

When PR 1308 is merged into `main`:

1. Fetch main, record the merge SHA, and plan prospectively again; merge main into this topic (no rebase).
2. Expect textual work in `core/store.py`, `api/server.py` and `core/README.md`. Cycles are spent: any source resolution, ambiguous conflict or correction needs new issue-specific authorization first and is not granted by this plan.
3. Run targeted checks only: core `test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` plus the #1292 `test_priority_order`; API `test_ranking_publication_wiring.py` and `test_case_journey.py`; ruff and mypy on touched files.
4. Verify shared Store/API behavior: Blob selection by `ZF_RANKING_ARCHIVE`, conditional-create publish, status through the listing, with human, cost, manual and path-free guards unchanged.
5. SQL behavior belongs to #1292's own owned disposable SQL evidence and is not inferred here. Azurite or real account, WORM, role grant, Bicep and deployment stay unperformed.

## Stop conditions

Merge conflict; a source path in the delta; an unresolved intent conflict; a failed targeted check. Each is reported without a fix.

## Risks

* The future textual forecast (clean, exit 0) is not semantic proof.
* Inherited equivalence is by tree identity, not new execution.
