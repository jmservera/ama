# Recovery critique: chat-clean-validation-891-0901 (2026-11-13, prospective)

* Executed: one independent read-only rubber-duck pass BEFORE install or test.
* Verdict: approve_with_comments. Applied directly: (1) use `/tmp/v891-0901/bin/python` explicitly for probe and rerun; (2) require resolved `GOLDEN` to exist (not only point into the worktree) before the rerun, else stop.
* Single-rerun boundary and cause-versus-fix distinction judged sound.
