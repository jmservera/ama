# Changes: completion-driven coordinator refill (issue 1204)

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`: eight-session cap (not issues), no default 3, finished session frees slot, completion/refill/re-arm protocol, thin-reviewer input preflight, bounded-recovery handoff, evidenced zero-worker blocked rule, timers kept as fallback, PIPESTATUS exit capture, unique per-worker names. Frontmatter and 1296 cycle policy untouched.
* `tools/ama-worker-watch.py`: new read-only watcher (exit 0 finished, 1 tool error, 2 absent at start/bad input, 3 timeout).
* `tools/test_ama_worker_watch.py`: six mocked tests.

Focused checks run (exit 0): `python3 -m unittest test_ama_worker_watch` (6 tests, from tools/); `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` on both files; real tmux smoke (first completion plus remaining, exit 0) and absent-session CLI run (exit 2). Not run: full gate, `rpi-checks --changed`, CI, browser, SQL, Docker, native agent execution.
