# HVE Artifact Test Report: Repository and AMA Backlog Delivery Coordinator Instructions

* Tested profile(s): Medium (`gpt-5.6-terra`) for `.github/copilot-instructions.md` (`instructions`) and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`agent`)
* Run type: full
* Behavior gate: Executed
* Fidelity: simulation
* Execution status: Complete
* Verdict: Pass
* Sandbox: cleaned up

## Summary

The co-authored instruction set (`.github/copilot-instructions.md` and `.github/agents/ama-backlog-delivery-coordinator.agent.md`) was exercised together at the Medium reasoning profile (`gpt-5.6-terra`) under `simulation` fidelity using black-box scenario `SCEN-TOGETHER-01` (`DESIGN-COORD-01`). The scenario tested multi-issue wave coordination across an active parent epic (`#410`), a stacked child on its 3rd review-correction cycle (`#411` touching `src/api` web UI and `infra/` Python files), an independent sibling child (`#412` touching browser-check tooling), a compliance-blocked issue (`#413`), 16 open PRs, 2 live workers, and 1 merged-PR closure-audit candidate. The simulated run satisfied all five requirement groups (`REQ-01` through `REQ-05`) with zero findings.

## Fidelity and limitations

* **Observed**: Target artifact reads and read-only sandbox containment (pre-run and post-run workspace status showed zero unexpected out-of-sandbox modifications).
* **Simulated**: Contract interpretation, worker launch script construction (`--model gemini-4-carbon`, `--claim-model gemini-4-carbon`, `mkdir -p /mnt/tmp`, `export TMPDIR=/mnt/tmp`, `< /dev/null`), stacked-PR routing (`src-ci.yml` on all PRs vs `rubric-score.lock.yml` on `main`), 5-cycle review-correction budgeting (with at least 3 diagnostic RPI cycles with validation), pre-push local `src-ci.yml` parity commands (`mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, `src/api/tests` on `PYTHONPATH`, `scenario-manifest.json` recipe SHA sync, and `test_accessibility_baseline.py` / `test_content_standard.py` guards), and adaptive 10 to 30 minute delivery scheduling plus hourly cleanup preserving `/mnt/tmp`.
* **Emulated**: Shell execution (`git`, `gh`, `tmux`, `python3`), subagent review dispatches, and `manage_schedule` calls.
* **Tier limitation**: Because the executor ran at the `Medium` profile (`gpt-5.6-terra`), above `Low`, a higher-tier simulator may repair ambiguity a lower-tier run would expose, so conformance evidence from this run does not establish that the artifacts read unambiguously at lower tiers or establish native-runtime tool reliability.

## Reuse eligibility

Not applicable (`full` run).

| Scenario | Requirement | Impact disposition | Evidence source | Grade provenance |
| --- | --- | --- | --- | --- |
| `SCEN-TOGETHER-01` | `REQ-01`..`REQ-05` | affected (`full` run) | fresh execution (`.copilot-tracking/sandbox/2026-11-15-coordinator-instructions-1/test-log.md`) | fresh grade (`.copilot-tracking/sandbox/2026-11-15-coordinator-instructions-1/test-review.md`) |

## Findings

No findings (`0` Critical, `0` High, `0` Medium, `0` Low).

| # | Action | Mapped dimension | Artifact | Profile | Evidence class | Severity | Evidence | Resolving change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| None | None | None | `.github/copilot-instructions.md`, `.github/agents/ama-backlog-delivery-coordinator.agent.md` | Medium (`gpt-5.6-terra`) | simulation | None | `.copilot-tracking/sandbox/2026-11-15-coordinator-instructions-1/test-log.md` | None required |

## Coverage

* **Ran as intended**:
  * `REQ-01`: Native `tmux` launcher script construction with `--model gemini-4-carbon`, `--claim-model gemini-4-carbon`, `mkdir -p /mnt/tmp`, `export TMPDIR=/mnt/tmp`, and `< /dev/null` stdin protection.
  * `REQ-02`: Concurrency management up to 8 live native `rpi-*` `tmux` sessions without a numerical active-issue cap when using coherent parent stacks, and stacked-PR CI economy (`src-ci.yml` vs `rubric-score.lock.yml`).
  * `REQ-03`: Five total review-correction cycles per issue (preserving spent cycles, finite extensions, and at least 3 diagnostic RPI cycles with validation) and isolated human-blocker handling (`#413`).
  * `REQ-04`: Pre-push local `src-ci.yml` parity commands across `src/api`, `infra/`, web UI accessibility/content guards, and `scenario-manifest.json` recipe SHA sync.
  * `REQ-05`: Adaptive 10 to 30 minute delivery recurrence alongside `ama-worker-watch.py` and hourly (`1h`) cleanup preserving `/mnt/tmp`.
* **Untested behavior**: Live GitHub REST/GraphQL and project board mutations, actual `tmux` process creation, and container/SQL execution during full-tier local gates (requires native execution in a live environment).

## Containment

* Pre-run workspace status: `M .github/agents/ama-backlog-delivery-coordinator.agent.md`, `M .github/copilot-instructions.md`, `?? .copilot-tracking/`.
* Post-run workspace status: unchanged outside `.copilot-tracking/`.
* Enforced controls: read-only `hve-core-all:hve-artifact-tester` simulation; zero unexpected out-of-sandbox side effects.

## Satisfied-and-skipped

None (both targets were exercised together in `SCEN-TOGETHER-01`).

## Human review

* [ ] Reviewed and validated by a qualified human reviewer
