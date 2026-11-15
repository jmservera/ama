<!-- markdownlint-disable-file -->
# Review: every list offers a read-only export (issue #80 criterion 2)

* Execution: one Review (code-review agent) over the uncommitted diff, once, after implementation. Not repeated.
* Outcome: no significant issues found. Review was by reading the code; the agent ran no tests. Test evidence is in the changes file.
* Boundary assessed: new CSV routes, link text, concern and proposal row whitelists, importer refusal of exported workbooks.

## Checks

* Role gating: each CSV route reuses its JSON endpoint's role check.
* Privacy: aftercare export omits the resident's statement and history; proposals export uses a fixed field list; conversations and memory are never exported.
* No state change: no write found on any export path.
* Importer: an exported workbook gives a blocking preview, and staging stops.

## Routed follow-ups (not actioned here)

* Owner to tick #80 criterion 2 after human review; this branch does not edit GitHub.
* Law provisions and the aftercare evaluator are exempt, not exported.
* The importer refuses exported workbooks only; a CSV re-import is not detected.
* Process: implementation started before critique (recorded in the critique and changes files).
