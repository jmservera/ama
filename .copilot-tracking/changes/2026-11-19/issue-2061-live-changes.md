# Changes: issue 2061 (Refs #2061)

Planned: add docs/adrs/0008-single-external-demo-environment.md (criterion 1). Documentation only; tier FOCUSED.

## Per-criterion status

| # | Criterion | Status | Reason |
| --- | --- | --- | --- |
| 1 | Decision record | Built (proposed, owner approval pending) | ADR 0008 |
| 2 | Bicep one external env, what-if | Unproven | Infra change needs FULL tier and live what-if gate; brief limits FULL to src changes |
| 3 | Delete list, only those removed | Unproven | Requires owner approval of delete list before any removal |
| 4 | Entra URIs and sign-in | Unproven | Graph read denied ("Insufficient privileges"); registration edits are production-shaped and need owner approval |
| 5 | Separate identities, role inventory, negative test | Partly evidenced | Before inventory recorded in research note; split for demo API and negative test not built |
| 6 | End-to-end demo | Unproven | Depends on criteria 2 to 4 redeploy |
| 7 | Production builds, full receipt | Unproven | Full receipt forbidden here (no rpi-checks --all) |
| 8 | Rollback documented | Outlined in ADR only | Needs verified restore steps after redeploy design |

## Files

* docs/adrs/0008-single-external-demo-environment.md (new, Proposed)
* docs/reference/research/issue-2061-live-single-environment-2026-11-19.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

Validation (FOCUSED, docs only): relative links resolved by inspection; no em dashes; no src/infra change so mypy, ruff and rpi-checks do not apply; hosted CI not observed (not pushed).
Witness note: first implement-start was refused (state `changes` pointer was null); fixed the state pointer and retried, second call ok.
