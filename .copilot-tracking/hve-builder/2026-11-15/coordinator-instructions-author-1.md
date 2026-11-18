# HVE Builder Authoring Log — Coordinator and Repository Instructions

* **Date**: 2026-11-15
* **Stage**: `author`
* **Status**: `Complete`
* **Approved Write Boundary**:
  * `.github/copilot-instructions.md`
  * `.github/agents/ama-backlog-delivery-coordinator.agent.md`
  * `.copilot-tracking/` evidence files in `/home/azureuser/source/ama-demo-wt/docs-hve-builder-coordinator`

## Requirement-to-Edit Mapping

1. **Default `tmux` RPI worker model (`--model gemini-4-carbon`)**:
   * Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` Step 5 (`rpi_phase_witness.py --claim-model gemini-4-carbon`, launcher script `--model gemini-4-carbon`, and prose rule requiring Gemini 4 Carbon on all coordinator-launched RPI issue sessions).
2. **Non-interactive `tmux` launcher hardening (`TMPDIR=/mnt/tmp` and `< /dev/null`)**:
   * Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` Step 5 launcher script to run `mkdir -p /mnt/tmp 2>/dev/null || true`, `export TMPDIR=/mnt/tmp`, and redirect `< /dev/null` into `copilot`.
3. **Concurrency and stacked-PR admission clarity**:
   * Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Liveness and stop decision` and `CI economy and PR backlog cap`) and `.github/copilot-instructions.md` (`Branch and Pull Request Workflow`) to state that eight live native `rpi-*` `tmux` sessions is the concurrency target (with no numerical active-issue cap when organized into coherent parent stacks) and that `src-ci.yml` runs on PRs to any branch while `rubric-score.lock.yml` runs only on `main`.
4. **Five-cycle review-correction allowance and diagnostic RPI cycles**:
   * Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Human blockers` and Step 6) from two cycles to five total review-correction cycles per issue, preserving spent history, finite extensions, and at least three scoped diagnostic RPI cycles with validation before stopping solely on the cycle limit.
5. **Adaptive 10–30 minute delivery cadence and hourly `/mnt/tmp` cleanup**:
   * Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Recurring schedules`) to document the adaptive 10 to 30 minute delivery cadence alongside `ama-worker-watch.py` completion notifications and hourly cleanup maintaining `/mnt/tmp`.
6. **Pre-push local `src-ci.yml` parity checklist**:
   * Updated `.github/copilot-instructions.md` and `.github/agents/ama-backlog-delivery-coordinator.agent.md` to specify bare `python3 -m mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, `src/api/tests` on `PYTHONPATH`, `scenario-manifest.json` recipe SHA sync when browser-check scripts change, and `test_accessibility_baseline.py` / `test_content_standard.py` when web UI files change.

## Non-Tool Capability Surface Check

* `.github/copilot-instructions.md` frontmatter (`description`, `applyTo`) is unchanged.
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` frontmatter (`name`, `description`) is unchanged.
