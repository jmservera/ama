# Research: refill correction 2 (issue 1204, 2026-11-13)

Task slug `demo-permanent-refill-1204-0914-c2`. Base: committed `ab5b10c25`. Disposition: executed, focused. Original records are unchanged and the original critique stays retrospective, not prospective.

Root exact-head review of `ab5b10c25` found three coupled defects (agent file lines as of that head):

* Line ~682: exit 2 (absent at start) says "inspect that session's log and exit at once". "Exit" is ambiguous and can read as ending the delivery run, the defect being repaired.
* Lines ~103-105: every retained candidate, failed test or outstanding gate is declared `ready`, so a missing approval would be `ready` merely because a slot is free.
* Line ~599: the launch command uses Bash `${PIPESTATUS[0]}` inside a long string run by tmux's default shell, which may be dash; it is also hard to read and a single per-issue log name.

Planning readiness: Ready. No watcher change unless a test exposes a coupled bug (none found by reading).
