# Critique: completion-driven coordinator refill (issue 1204)

Executed once by an independent rubber-duck subagent (runtime default model) against the plan plus the first author batch. Ordering caveat: the first batch was authored in one coherent batch before this critique, so it was not strictly prospective.

Verdict: Fail on the first batch. Contained simulation only (no native agent execution).

Findings and dispositions (all compatible, applied directly in the same task):

* Blocking: watcher race with a short worker already gone at start -> agent text now arms an async watch, treats exit 2 as "inspect log and exit at once" and never as completion.
* Blocking: multiple sessions per issue unexecutable -> unique `rpi-{number}-{role}` names, own worktree and log.
* Blocking: launch log recorded `tee` status -> `${PIPESTATUS[0]}` (bash).
* Major: `error connecting` treated as empty -> only no-server or missing-socket is empty; others exit 1.
* Major: unbounded timeout/poll -> finite positive validation, sleep capped to deadline.
* Major: CLI test not isolated -> query resolved at call time so the patch applies.

Scenario results after correction: 1-8 pass by static trace (scenario 6 also observed with the real CLI; first-completion observed with real tmux).
