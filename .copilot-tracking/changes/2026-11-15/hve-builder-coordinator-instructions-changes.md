<!-- markdownlint-disable-file -->
# Changes: Apply Chronicle Recommendations to Repository and Coordinator Instructions

* **Date**: 2026-11-15

## Modified Files

* `.github/copilot-instructions.md`: Added `src/api/tests` to the `PYTHONPATH` example, documented pre-push local `src-ci.yml` parity commands (`mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, `scenario-manifest.json` recipe SHA sync, `test_accessibility_baseline.py` / `test_content_standard.py` guards), and documented `src-ci.yml` (all PR branches) vs `rubric-score.lock.yml` (`main` only) triggers for stacked PRs.
* `.github/agents/ama-backlog-delivery-coordinator.agent.md`: Updated default `tmux` RPI worker model to `gemini-4-carbon` (`--model gemini-4-carbon`, `--claim-model gemini-4-carbon`), added `mkdir -p /mnt/tmp` + `export TMPDIR=/mnt/tmp` + `< /dev/null` to the launcher script, updated review-correction budget to 5 total cycles per issue (preserving spent cycles, finite extensions, and >=3 diagnostic RPI cycles with validation), clarified 8 concurrent `tmux` sessions without a numerical issue cap under coherent parent stacks, documented adaptive 10–30m delivery cadence + 1h `/mnt/tmp`-preserving cleanup, and added the pre-push local `src-ci.yml` parity checklist.
* `.copilot-tracking/hve-builder/2026-11-15/*`: Recorded baseline, authoring, static review, behavior report, and host validation logs.
