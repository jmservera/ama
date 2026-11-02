# Plan: issue #228 browser evidence slice

* [x] Add `src/api/checks/procurement_screens_browser_check.py` with a real-store synthetic package, capacity and work order
* [x] Document it in `src/api/README.md`
* [x] Run the check with pinned axe; run `rpi-checks.py --changed`

## Critique (one pass, inline)

Verdict: proceed. Applied: standalone file to avoid conflicts with open slice PRs; axe optional via `ZF_AXE_JS` with hash pin; no production code change; no conformance claim; assert that unconfirmed capacity evidence is not shown as met and that no vulnerability, approval or booking wording appears. No finding conflicted with a confirmed decision.
