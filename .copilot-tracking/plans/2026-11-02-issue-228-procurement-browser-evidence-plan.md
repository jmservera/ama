# Plan: issue #228 browser evidence slice

* [x] Add `src/api/checks/procurement_screens_browser_check.py` with a real-store synthetic package, capacity and work order
* [x] Document it in `src/api/README.md`
* [x] Run the check with pinned axe (both roles, local)
* [ ] Focused gate `rpi-checks.py --changed`: NOT passed. See the correction note.

## Critique (one pass, inline)

Verdict: proceed. Applied: standalone file to avoid conflicts with open slice PRs; axe optional via `ZF_AXE_JS` with hash pin; no production code change; no conformance claim; assert that unconfirmed capacity evidence is not shown as met and that no vulnerability, approval or booking wording appears. No finding conflicted with a confirmed decision.

## Correction note (2026-11-02, after independent review FAIL)

The original gate item claimed a passed focused gate. That is withdrawn. After rebase onto origin/main (already up to date) and the review fixes, `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600 --out /tmp/gate782fix` and a retry (`/tmp/gate782fix2`) both ended `BLOCKED: Global heavy-resource lock timeout` (another process held the lock for 600 s each time). No gate receipt exists for this head. Original artifacts above are preserved unchanged.
