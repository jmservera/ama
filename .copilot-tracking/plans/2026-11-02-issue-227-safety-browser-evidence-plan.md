# Plan: issue #227 browser evidence slice

* [x] Add `src/api/checks/safety_screens_browser_check.py` with a synthetic home of seven hazard states
* [x] Document it in `src/api/README.md`
* [x] Run the check with pinned axe
* [ ] `rpi-checks.py --changed --base origin/main --lock-timeout 600`: BLOCKED on 2026-11-02 ("--out is required and must be a new external directory"); not passed, rerun needed with an external out directory

## Critique (one pass, inline)

Verdict: proceed. Applied: standalone file to avoid conflicts with open slice PRs; axe optional via `ZF_AXE_JS` with hash pin; no production code change; no conformance claim. No finding conflicted with a confirmed decision.
