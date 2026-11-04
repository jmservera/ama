# Details: tenure question pack (R3)

* Phase 1: append-only `question_packs` on a tenure report. Fixed template questions owned by data owner, Legal, Finance, home ownership team. Pack records source verification and Legal position versions and is stale when either changes.
* Review: Approved or Returned, named reviewer role containing home ownership, leasehold or data owner, not the drafter or recorder, date not future, note required, one review per pack.
* Phase 2: core tests (draft gates, unsafe input, review rules, stale and redraft); API test (403 for restricted roles, hidden from restricted projections).
* Phase 3: core and API README contract; log.md entry.
