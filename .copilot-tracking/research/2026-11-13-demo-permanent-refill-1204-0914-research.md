# Research: completion-driven coordinator refill (issue 1204, 2026-11-13)

Task slug: `demo-permanent-refill-1204-0914`. Base: `origin/main` 347962dac. Research disposition: executed, focused.

## Evidence

* Owner failure report (request text): sole149 integration finished 08:50:32, no tmux at 08:57:01; root prepared PR prose and a helper missing its diff-state input instead of dispatching; four workers started 09:00:50 and finished in under five minutes, so a ten-minute timer leaves idle gaps.
* Existing agent text (`.github/agents/ama-backlog-delivery-coordinator.agent.md`, Liveness admission rule, step 5 monitoring, Inputs): capped TOTAL active issue assignments at eight, released a slot only after publish and merge, kept "default 3" in Inputs, and monitored only through the recurring timer check.
* External operational helper (`watch-native-completion.py`, session-state files): returns the first completion but treats a session absent before the start as finished (false completion), has no timeout distinction, and returns no per-session timestamps. Not in the repository, so `tools/ama-worker-watch.py` is the approved new read-only helper.
* No suitable repository helper exists (`tools/` listing checked: no tmux watcher).
* Test style: `tools/test_*.py` unittest modules loading hyphenated tools by `importlib`; CI lint profile `ruff --isolated --select E,F,I,B,UP --line-length 100`.

## Planning readiness

Ready. Scope fixed by the owner: agent prose, one helper, one unit test module, RPI evidence. Unknown and not claimed: whether the owner's eight-session cap interacts with the held 1296 correction-policy work (untouched).
