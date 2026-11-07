# Issue 1231 r16 plan: align child to parent79 87c027a30

Date: 2026-11-07. Status: prospective, not executed. Research: `.copilot-tracking/research/2026-11-07/issue-1231-r16-87-parent-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-1231-r16-87-parent-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r16-87-parent-critique.md`.

## Objective

Produce a local two-parent merge of parent79 87c027a30 into the child a4ada1e91 that preserves both ancestries, all #1231 fixes (unique stage, concurrent-writer metadata, 0600 permissions, stage_retained diagnostics) and every parent guard (policy hash/registry, future archive date, blocked exit). No new behaviour. Behaviour-preserving integration only.

## Scope and exclusions

* In: preserved backup ref, normal merge, focused checks, dated changes/review/state records.
* Out: push, PR, retarget, FULL gate, SQL, browser, images, scanners, parent/main mutation, ticks, cleanup, edits to parent-owned records, docs/reference/log.md, index or memory.

## Phases

* [ ] Phase 1: Preconditions. Re-verify child HEAD a4ada1e9 and ignored-inclusive clean status, parent 87c027a3 tree f391682d and clean, 357e842d ancestor of both, main 0f420dc9. Stop on any drift. Create ref `backup/issue-1231-a4ada-pre-r16-align` at a4ada1e9 (refuse if it exists).
* [ ] Phase 2: Merge. Run `git merge-tree --write-tree --merge-base=357e842d HEAD 87c027a30`. Require a single tree line (no conflict) matching the researched a00c8d19 unless a source change intervened. Then a normal two-parent merge (`git merge --no-ff` of 87c027a3, or commit-tree with parents a4ada1e9 and 87c027a3 followed by `--ff-only`). On any conflict requiring intent reconciliation, abort, keep the backup ref and report the exact files; never guess.
* [ ] Phase 3: Static integration proof. Confirm by diff that the merged tree equals parent ranking_publication.py, store.py and API wiring test equal to the child's a4ada1e9 blobs (parent did not touch them), and runner/test/README contain both sides' hunks. Confirm no `0o666`, no `mkstemp` regression, no mode weakening in the helper.
* [ ] Phase 4: Focused checks (PYTHONDONTWRITEBYTECODE=1, PYTHONPATH to this worktree src dirs, own external scratch, no pip unless a real missing-dependency failure): core `tests.test_ranking_publication`, `tests.test_ranking_publication_runner`; API `tests.test_ranking_publication_wiring`; Ruff check and format `--no-cache`; mypy for src/core with an external cache; `git diff --check`; print `zava_forward.core.__file__` to prove the worktree origin. Record real commands, exits and skips.
* [ ] Phase 5: Regressions only if a gap is shown. Add a focused test only for an interaction not covered: (a) future-dated winner metadata versus parent future refusal at runner level, (b) double-failure `stage_retained` coexisting with the parent's refusal path. Never edit or relax an existing assertion to obtain a pass.
* [ ] Phase 6: Records. Write dated changes, review (one author Review, honestly labelled non-independent) and state JSON under `.copilot-tracking/`, preserving r15 and earlier files. Commit with the noreply identity and the Copilot trailer. Freeze with ignored-inclusive clean status.

## Acceptance

* Merge commit has parents a4ada1e9 and 87c027a3; both ancestries reachable; backup ref present.
* Focused checks pass, or the first failure is preserved and reported without a fix to hide it.
* No source behaviour change beyond what the two sides already contain, except tests if Phase 5 demonstrates a gap.
* Result is stated as local alignment only; FULL, independent review and hosted checks remain open and old receipts are never called current.

## Follow-Up Items

* New combined-tip FULL gate with `--stack 87c027a3 --stack <tip>` against the then-current fetched main after #86 releases the lane.
* Independent exact-head review of parent and child.
* Cross-UID permission observation and real unsupported-mount behaviour remain unproven.
