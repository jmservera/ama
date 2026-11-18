<!-- markdownlint-disable-file -->
# Research: Apply Chronicle Recommendations to Repository and Coordinator Instructions

* **Date**: 2026-11-15
* **Scope**: `.github/copilot-instructions.md` and `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* **Workflow**: `hve-builder` (`improve` mode) + `hve-builder-tester` (`simulation` fidelity)

## Findings

1. **Worker Model and Non-Interactive `tmux` Hardening**:
   * All `tmux` RPI worker dispatches use `--model gemini-4-carbon` and `--claim-model gemini-4-carbon`.
   * Setting `TMPDIR=/mnt/tmp` requires `mkdir -p /mnt/tmp 2>/dev/null || true` and `< /dev/null` stdin redirection so non-interactive `copilot` CLI invocations neither fail when `/mnt/tmp` is recreated nor block on stdin.
2. **Concurrency and Stacked-PR CI Economy**:
   * Concurrency targets up to 8 live native `rpi-*` `tmux` sessions without a numerical active-issue cap when work is organized into coherent parent stacks (`src-ci.yml` runs on all PR branches; `rubric-score.lock.yml` runs only on `main`).
3. **Correction Cycles and Cadence**:
   * Default review-correction allowance is 5 total cycles per issue (preserving spent cycles, finite extensions, and at least 3 diagnostic RPI cycles with validation).
   * Delivery recurrence uses an adaptive 10 to 30 minute interval alongside `ama-worker-watch.py`, while hourly (`1h`) cleanup preserves `/mnt/tmp`.
4. **Local `src-ci.yml` Parity**:
   * Running bare `python3 -m mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, including `src/api/tests` on `PYTHONPATH`, syncing `scenario-manifest.json` recipe SHAs, and running `test_accessibility_baseline.py` / `test_content_standard.py` prevent avoidable hosted CI failures.
