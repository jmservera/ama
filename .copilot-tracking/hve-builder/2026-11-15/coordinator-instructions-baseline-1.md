# HVE Builder Baseline Review — Coordinator and Repository Instructions

* **Date**: 2026-11-15
* **Mode**: `improve`
* **Targets**:
  * `.github/copilot-instructions.md` (type: `instructions`, `applyTo: "**"`)
  * `.github/agents/ama-backlog-delivery-coordinator.agent.md` (type: `agent`, `name: AMA Backlog Delivery Coordinator`)
* **Base Revision**: `45cd2bd00` (`origin/main`)

## Baseline Contract & Non-Tool Capability Surface

1. `.github/copilot-instructions.md`:
   * Frontmatter: `description: "Repository guidance for AMA research, executable development and web work"`, `applyTo: "**"`. Preserved unchanged.
   * Baseline gap: The local test example for `src/api` omitted `src/api/tests` from `PYTHONPATH` when invoked from the repository root and did not state the local `.github/workflows/src-ci.yml` parity commands (`mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, `scenario-manifest.json` recipe SHA sync on browser-check edits, and `test_accessibility_baseline.py` / `test_content_standard.py` guards on web UI edits), nor the branch-trigger distinction between `src-ci.yml` (all PR branches) and `rubric-score.lock.yml` (`main` only).
2. `.github/agents/ama-backlog-delivery-coordinator.agent.md`:
   * Frontmatter: `name: AMA Backlog Delivery Coordinator`, `description: "Loops backlog review, parallel RPI delivery in isolated worktrees, PR review, gated automerge and rebase until done, stopping only on human blockers"`. Preserved unchanged.
   * Baseline gaps against owner directives and session lessons:
     * Default `tmux` worker model referenced `claude-sonnet-5.5` instead of `gemini-4-carbon`.
     * Review-correction cycle allowance stated `two correction cycles` instead of `five total review-correction cycles` (preserving spent cycles, finite extensions, and at least three diagnostic RPI cycles with validation).
     * `tmux` launcher did not ensure `/mnt/tmp` exists (`mkdir -p /mnt/tmp`) or redirect `< /dev/null` for `TMPDIR=/mnt/tmp`.
     * Recurring schedules specified a fixed `10 minutes` interval without noting the adaptive `10 to 30 minute` cadence alongside `ama-worker-watch.py` and `/mnt/tmp` maintenance in the hourly cleanup.
     * CI economy section did not explicitly contrast `src-ci.yml` (any PR branch) vs `rubric-score.lock.yml` (`main` only) or list the pre-push local `src-ci.yml` parity checks.
