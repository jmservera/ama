<!-- markdownlint-disable-file -->
# Critique: final-parent revalidation plan (#1419)

* Executed once by a rubber-duck subagent, read-only, on the plan, research and details. Verdict: Revise (3 blocking, 1 non-blocking). No user decision required.
* PC-001 Blocking: phase P1 checks only a source diffstat; inspect the full first-parent diff and the stub patch and compare with production behavior.
* PC-002 Blocking: tests must use the explicit venv python; record per-module counts, skips and browser execution; zero discovered, skipped required cases and lock contention are incomplete, not passes or waivers.
* PC-003 Blocking: committing records changes HEAD; distinguish the tested merge commit from the final handoff commit, verify source trees match, and name the exact commit for CI and independent assessment.
* PC-004 Non-blocking: carry the RV-004 correction (preserve its history; corrected routing is a pre-existing fixture defect, not an established production defect) into the handoff.
* Dispositions: see the plan section Critique Disposition. All applied directly.
