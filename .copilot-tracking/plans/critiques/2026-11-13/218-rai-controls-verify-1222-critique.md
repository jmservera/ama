# Plan critique: 218 RAI controls verification

* Reviewer: rubber-duck subagent (independent), executed once before any install or test run.
* Verdict: Revise.
* Findings applied directly: use per-module unittest discover with -s tests -p; keep installs offline-safe and record failures; guard src/ against writes (no bytecode, check git status); require nonzero Ran count and recorded skips per module for all 11 modules.
* No user decision required.
