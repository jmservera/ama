# Plan: issue #227 browser evidence slice

* [x] Add `src/api/checks/safety_screens_browser_check.py` with a synthetic home of seven hazard states
* [x] Document it in `src/api/README.md`
* [x] Run the check with pinned axe
* [x] `rpi-checks.py --changed --base origin/main --lock-timeout 600 --out /tmp/gate227fix`: VERIFIED partial local gate at head 8e2180ca6, base 627aed6fb, 2026-11-02 (external receipt); independent review, hosted CI and human approval still pending

## Critique (one pass, inline)

Verdict: proceed. Applied: standalone file to avoid conflicts with open slice PRs; axe optional via `ZF_AXE_JS` with hash pin; no production code change; no conformance claim. No finding conflicted with a confirmed decision.
