# Plan: issue #229 browser evidence slice

* [x] Add `src/api/checks/data_operator_browser_check.py` with a synthetic home
* [x] Document it in `src/api/README.md`
* [x] Run the check with pinned axe
* [ ] `rpi-checks.py --changed` gate: NOT passed (BLOCKED by heavy-resource lock timeout; rerun required). Corrected 2026-11-02, see the changes note.

## Critique (one pass, inline)

Verdict: proceed. Applied: standalone file to avoid conflicts with open slice PRs; axe optional via `ZF_AXE_JS` with hash pin; no production code change; no conformance claim; assert server-derived exceptions rather than injecting work data the API ignores. No finding conflicted with a confirmed decision.
