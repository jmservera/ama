# Plan: issue 2190

Critique (executed once, accepted): port the three existing fixes from commit 17461b0291 rather than rewrite; re-verify each (flake 1 tests fail before and pass after; flake 3 test run; flake 2 loaded repeat runs). Risk: flake 2 has no deterministic test, stated as unproven-by-test. Tier FULL (gate-tool edit); no `--all` run here, the coordinator runs it. No check relaxed.
Phases: 1 port src/tools/tests; 2 re-verify; 3 note, index, log.
