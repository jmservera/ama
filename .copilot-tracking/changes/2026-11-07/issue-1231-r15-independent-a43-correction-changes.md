# Changes: issue 1231 independent correction cycle 1

* ranking_publication.py: stage created 0o600; the primary exception carries stage_retained when the owned stage cannot be removed.
* ranking_publication_runner.py: publish_failed message and next action name the retained hidden file; stage_retained is returned.
* store.py: _log_retained_stage logs a WARNING naming the file on both error paths; the 503 text gains a path-free sentence when a stage remains.
* Tests: umask 0022/0002 mode test (all files 0600, umask restored in finally), exception attribute test, runner and manager-route double-failure tests with a foreign file preserved.
* Checks (source-bound, /tmp/zf79venv, worktree import origin verified, PYTHONDONTWRITEBYTECODE=1): core 66 OK, API wiring 18 OK, Ruff 0.17.1 check and format pass (formatter reflowed two of my new test blocks), mypy 268 files clean, diff check clean.
* Not done: cross-UID access test (would need another user; not fabricated), FULL, push, parent alignment.
