<!-- markdownlint-disable-file -->
# Plan: Apply Chronicle Recommendations to Repository and Coordinator Instructions

* **Date**: 2026-11-15
* **Mode**: `hve-builder` (`improve`)

## Phases

1. **Phase 1: Author Target Improvements**
   * Update `.github/copilot-instructions.md` with `src/api/tests` in `PYTHONPATH`, local `src-ci.yml` parity commands (`mypy`, `ruff format`, `scenario-manifest.json` recipe SHA sync, accessibility/content guards), and stacked-PR vs `main` CI trigger rules.
   * Update `.github/agents/ama-backlog-delivery-coordinator.agent.md` with `--model gemini-4-carbon`, `mkdir -p /mnt/tmp` + `TMPDIR=/mnt/tmp` + `< /dev/null`, 8 concurrent `tmux` sessions without a numerical active-issue cap under parent stacks, 5 total review-correction cycles (plus >=3 diagnostic RPI cycles), adaptive 10–30m delivery cadence + 1h `/mnt/tmp`-preserving cleanup, and pre-push `src-ci.yml` parity checks.
2. **Phase 2: Independent Static Review, Behavior Gate (`hve-builder-tester`), and Host Validation**
   * Run independent static review (`coordinator-instructions-static-review-1.md`).
   * Run `hve-builder-tester` full simulation and independent grading (`coordinator-instructions-behavior-report-1.md`).
   * Run mechanical host validation (`coordinator-instructions-validation-1.md`).
