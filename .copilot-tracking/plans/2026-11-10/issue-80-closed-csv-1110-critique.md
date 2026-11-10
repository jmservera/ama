<!-- markdownlint-disable-file -->
# Critique: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

Executed once, by the author, on the final candidate plan and details. Not an independent review. Verdict: Revise; compatible findings applied directly; no repeat critique.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-1 | A relative link in a hash-routed SPA must be an absolute path, not a hash link, or it navigates the router. | Applied: href `/api/closed-cases.csv?...` plain path (details P3). |
| PC-2 | Omitting limit from the link would export the default 20 even if the displayed page used a different limit. | Applied: page and limit both come from the response. |
| PC-3 | Registering the CSV route in `LIST_EXPORTS` would bypass the progress validation and use `to_csv`, which drops headers for zero rows. | Applied: not in `LIST_EXPORTS`; separate fixed-column encoder. |
| PC-4 | The inventory regex requires every server route string in `GET_ENDPOINTS`; the route string would fail the existing test otherwise. | Applied: P4 inventory entry. |
| PC-5 | A non-primitive value in a summary field must not render as embedded JSON. | Applied: `closed_csv` raises on non-primitives. |
| PC-6 | A blank closed_on could be misread as zero or a date. | Applied: link copy states blank means unknown; no placeholder date. |
| PC-7 | HEAD requests reach `do_GET`; they carry no body anyway. | Accepted, no change. |
| PC-8 | Overlap with #96 server.py. | Checked: separate hunks; merge-tree after commit; stop for stack if it fails. |

No critique advice conflicts with a confirmed decision. No significant or divergent issue needs a user decision.
