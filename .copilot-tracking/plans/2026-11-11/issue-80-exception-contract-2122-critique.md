<!-- markdownlint-disable-file -->
# Critique: #80 exception-register CSV contract (issue-80-exception-contract-2122)

Executed once on the final candidate plan, details and research, by an independent rubber-duck subagent (read-only, static source verification), 2026-11-11. Not repeated. Verdict: Revise; every finding was compatible with confirmed decisions and applied directly. No significant or divergent issue needs a user decision.

| ID | Finding (summary) | Disposition |
| --- | --- | --- |
| PC-001 | Reference, kind, state and owner role could copy arbitrary strings (for example an email) because the screen only checks that id and kind are strings. | Applied: details section 4 now allowlists `EX-` references and the closed kind, status and owner-role vocabularies; anything else is `Unknown` or fails the list closed. |
| PC-002 | The non-string rule (`Unknown`) conflicted with the parity requirement to `safe_cell` (empty, Yes/No, JSON). | Applied: section 5 and O5 split neutralisation parity for normalised strings from separate non-string expectations. |
| PC-003 | Next-slice browser-download evidence was assigned to an HTTP/Store test file and omitted from the file list; the existing screen "full" fixture contains an unreadable entry, so it cannot show a populated offer. | Applied: section 11 assigns O1, O2 and O7 to a real-browser check, keeps `test_exception_register.py` to O3 data and ledger assertions, requires a new clean populated fixture, and lets that slice state its own file list. |
| PC-004 | A person named with both roles receives both item sets; exclusivity was overstated. | Applied: section 6 and O6 state single-role exclusivity and combined-role behaviour. |
| PC-005 | A 403 from the role projection gate (`server.py:506-507`) happens before the register runs and writes no register denial audit. | Applied: separate case row; no audit line is required or claimed for that denial. |
| PC-006 | Browser initiation does not prove a file was saved. | Applied: status text reads "Download started"; O1 states initiation. |
| PC-007 | The note claimed constructed demonstration data although the register reads the configured store. | Applied: R4a and the note wording state only the absence of operational approval. |

Author verification of the evidence: PC-003 fixture (`test_exception_register_screen.py:43-44`, item `7`) and PC-005 (`server.py:506-507`) were re-read and are correct. No critique advice conflicts with a confirmed decision. The critique is not a substitute for the independent exact-head assessment the coordinator requires.
