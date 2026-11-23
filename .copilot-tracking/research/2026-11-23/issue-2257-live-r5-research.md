# Issue 2257 r5 research

Scope: synthetic demo, desktop only. Issue body has no tick-list; criteria are taken from its Expected line and the r3 per-criterion table.

## Findings

* HEAD already contains the retry control (#2300) and the `cause=sql-write-lock-busy` overlay tag (#2307).
* The r3 follow-up, "log the SQLSTATE class when the overlay fails with a non-lock error", is not in HEAD (`grep -i sqlstate` in `mssqlstore.py` and `assistants.py` is empty). It exists only as unmerged commit 40265c9262 on sibling branch `test/map-unavailable-live-20261123T155532Z`.
* It is the first unticked criterion that code and tests can satisfy: "the cause is found" is inferred, not logged, for `cause=other`.
* Other criteria: retry/recovery proven live in r2 (button not deployed); fresh-session failures not disproven (18 of 18 passed); billing, DPO/Legal and assistive-technology testing not needed (owner decision 2026-11-18).
* A new live probe is not useful: the deployed image 0000055 predates the log change, so it cannot show the new field. No Azure change is made.

## Planning Readiness

Ready. Research disposition: executed (local code and prior evidence reused).
