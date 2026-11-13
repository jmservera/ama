# Plan: completion-driven coordinator refill (issue 1204)

Task slug: `demo-permanent-refill-1204-0914`. Research: [research](../research/2026-11-13-demo-permanent-refill-1204-0914-research.md).

## Phases

* [x] 1. Add `tools/ama-worker-watch.py`: explicit finite tmux names, all must exist at start (exit 2 otherwise), bounded poll, first completion returns JSON with finished (per-session timestamp) and remaining (exit 0), timeout distinct (exit 3), tmux or tool failure explicit (exit 1). Read-only, argument-array subprocess, no shell.
* [x] 2. Add `tools/test_ama_worker_watch.py`: absent-before-start race, first completion and remaining set, timeout, tmux failure, no-server handling. Mocked, deterministic.
* [x] 3. Edit the coordinator agent: cap is eight useful live sessions not issues; remove default 3 and the slot-until-merge rule; single completion protocol (consume exit/head/evidence, refill before PR prose, re-arm watch), timers kept as fallback and not duplicated; thin-reviewer input preflight; failed bounded recovery gets a concrete handoff; zero workers is fully blocked only with evidenced dispositions.
* [x] 4. Focused checks: helper unit tests, CI ruff profile, diff review; contained behavior scenarios.

## Out of scope

Held 1296 cycle policy paragraphs, workflows, application, infra, live schedules, full gate.
