# Changes: issue 154 live round 3

Added: docs/reference/research/issue-154-live-resident-ux-r3-2026-11-18.md; evidence under .copilot-tracking/evidence/2026-11-18/issue-154-live-r3/. Edited: docs/reference/README.md, docs/reference/log.md. No source change; focused tier (documentation and evidence only).

## Per-criterion table

| Criterion | Proven for demo? |
| --- | --- |
| 1 to 4 (ticked) | Not re-run; carried from round 2 (partly proven live; representative view unproven live) |
| 5a No live resident contact | Proven for the demo (network trace, Azure resource check, DOM, tests) |
| 5b Validated through usability programme | Unproven; cannot be for the demo (SA-010, moderated sessions) |

Validation: unittest tests.test_representative_expiry_api tests.test_resident_demo_api, 53 OK. Azure CLI read-only listing; no resource created, so none to delete.
