<!-- markdownlint-disable-file -->
# Research: integrate final parent cc210fa and revalidate #1419 (closure-first)

* Task slug: issue-1419-handoff-csv-final-parent-1110
* Parent task: issue-1419-handoff-csv-implementation-1110 (clean head 37828a4110977d2b5c9b700267968cde8901cb65, preserved)
* Posture: focused. Output mode: convergence on a tracking/validation-only chain.
* Process note: the first `launch` attempt (seq 1) was refused (no `--brief`); retained as history. Launch seq 2 used the brief. Reading and git inspection below preceded research-open and are not retro-attested.

## Questions and findings

* Q1 What did the ordinary merge change? C1: merge a8acaba5d343408d3d750e25a4b0008db446ae79, tree 0820177872bd42d2f8cba1eb2aad80484f77bdc0, parents 37828a41 and cc210fa4460c28bb6f57b1389a183ae3dc7902cc (parent tree 9d05a507). No conflicts. `git diff 37828a41 HEAD -- src` is only src/api/tests/test_case_journey.py (+2/-1: the `show` stub now filters `nodes.flat().filter(n => n && n.nodeType)`). server.py, app.js, ops.js blobs equal the prior frozen head (0dbf8a74, 734aab48, 4ef77471). No src/core or src/agents change.
* Q2 Was the earlier test_case_journey failure a baseline app defect? Parent C5 evidence (consumed by Root) says the Node fixture stub did not skip null while production `h`/`show` does, so it was a fixture defect. My earlier review item RV-004 called it "pre-existing in parent Capacity code"; that classification was incomplete (pre-existing, but a test-fixture defect, now corrected by the parent). I preserve RV-004 as history and do not rewrite it; this chain supersedes the routing.
* Q3 Is anything in #1419 scope changed? No: CSV route, parser, role gates, projection, 13 fields, UI link and README are byte-identical.
* Q4 Environment: own venv /home/azureuser/.venvs/issue1419 imports server.py and workflows.py from this WT (editable). No pip needed.
* Q5 Browser: app.js and the checker source relevant to the handoff panel are unchanged since the already-tested head, so a minimal real handoff download rerun (own tests, flag, non-blocking heavy lock) suffices; no broad Capacity campaign.

## Decisions

* Tracking/validation-only: no source change planned. A source fix is permitted only for a tightly coupled merge/test defect evidenced by these runs and prospectively planned by plan amendment.
* Validation tier remains the owner demo-policy targeted override (basis: existing permission/store projection reused; no new role, permission or persistence path). Not a waiver, not a full receipt; hosted CI and independent exact-head assessment remain required.

## Planning Readiness

Ready. Research disposition: executed (focused, inline; contrarian check: Q2 shows my prior routing was imprecise, and Q5 shows browser rerun cannot be skipped on hash grounds alone for our own handoff panel, so it is rerun once).
