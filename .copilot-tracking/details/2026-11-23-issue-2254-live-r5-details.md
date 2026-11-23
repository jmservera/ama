# Details: issue 2254 run 5 (2026-11-23)

Phase 1: seed stored hazard=1 on one open case whose hazards are all released and on one closed case; reopen the store so `_repair_identity_columns` runs; assert the tile equals the body-derived count, the list total equals the tile, and neither id appears in the list.

Phase 2: temporarily drop "hazard" from the repair column tuple; both 2254 tests must fail; restore with git checkout.

Phase 3: evidence files under docs/reference/research/issue-2254-live-2026-11-23/ and the r5 research note.
