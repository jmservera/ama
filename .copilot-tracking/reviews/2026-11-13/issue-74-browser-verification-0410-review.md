<!-- markdownlint-disable-file -->
# Review: #74 home-case browser verification (issue-74-browser-verification-0410)

Date 2026-11-13. One Review, executed as a bounded self-review by the executing agent (not independent). Boundary: the tracking records and the single run evidence in the [changes](../../changes/2026-11-13/issue-74-browser-verification-0410-changes.md).

Outcome: conformant with limits.

## Findings

* Scope kept: one check, one admitted resource window under the lock, no source edit, no SQL, no unit tests, clean worktree.
* The run was preceded by one expected failure (missing playwright in the owned venv), preserved, then a declared-dependency install and a single rerun of the same command; no blind retries.
* Observed 24 PASS (1 server + 23 browser/axe), 0 FAIL, 0 skips, exit 0, axe COMPLETE with the pinned hash. This reproduces the author-reported 24 at head 6f2918011.

## Limits (unchanged adverse and scope items)

* The check opens only `#/case-home/ZF-2` and `#/case-home/ZF-3`. `buildingView` (`#/building/<id>`) is not covered; no building-route, whole criterion 2, assistive-technology, WCAG conformance or human approval claim is made. Automated axe on the `main` element only is not WCAG acceptance.
* CR-001 (home panel hides item applicability) and CR-002 (unknown funding renders as no) and all other original adverse items remain unchanged and unaddressed.
* axe tarball origin is not evidenced beyond hash equality of its `axe.min.js` to the check's pin; the evidence logs and venv are outside the repository and are not committed.
* The plan file was written after the run (disclosed there). Hosted CI and independent exact-head review were not performed; no issue criterion is ticked and no issue is closed.

## Routing

Open items stay with later user-selected work: V2 documentary mapping, G5 and outcome decisions, an existing check for `buildingView` if one is identified, and the separate unit-module verification owned by another worker.
