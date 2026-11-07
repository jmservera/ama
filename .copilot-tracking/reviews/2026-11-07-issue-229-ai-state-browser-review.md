# Review: issue #229 AI state browser check

Date 2026-11-07. Execution: executed once, independent read-only code-review agent against the uncommitted diff and new files, after implementation. Assessed boundary: the working-tree change to the checker, its new fixture module, regression test and README note, read against role-screens.js and the core register code. web-design-guidelines source fetched but truncated at 3000 characters (partial); no web file changed, so no web file was reviewed against it.

## Outcome

One medium finding, fixed directly before commit (see changes, Amendment): the model-request assertion could count the landing view's own AI priority read. No other high-confidence findings; selectors, phrases, row wording, workflow-only absence, 503 and empty renderings and the staff override held on reading.

Not established: the new browser section has not run in Chromium (not admitted), no axe scan, no focused-tier `--changed` gate, no independent exact-head assessment, no hosted CI. Result is review of source, not conformance. Whole #229 criterion 4 (WCAG, AT, human) stays unticked.

## Routed follow-ups

* Run the real operator-browser check (with pinned axe, `ZF_AXE_REQUIRED=1`) once admitted, record the final RESULT line.
* Run `python3 tools/rpi-checks.py --changed` once admitted; independent exact-head assessment before any push or PR (target test/ux-evidence-149, Refs #229).
* The "How it failed is Unknown" row is unreachable from the real feeds (reason is always supplied); stays covered only by the existing Node test.
