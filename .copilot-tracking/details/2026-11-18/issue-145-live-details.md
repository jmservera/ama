---
title: Issue 145 live PITR phase details
ms.date: 2026-11-18
---

# Details

* Restore time: UTC now minus 15 minutes, inside the 14 day short-term window (earliest restore date reported by Azure 2026-11-04).
* Cost: S0 DTU database for under a day, deleted after probe (well under the USD 700 cap).
* Ledger verification: native `sp_generate_database_ledger_digest` then `sp_verify_database_ledger` on the restored copy, plus the app hash chain (`ledger.verify_entries`, `verify_years`) over `audit`. The native check using the copy's own digest shows internal consistency only; external digest blobs are the anchor for tamper evidence and are not rewritten here.
* Revocation, suspension, spent allowance and erasure: the demo tables for assistant allowance, releases and dispatch gate hold zero rows, so non-resurrection can only be reported as vacuous; it is stated as unproven where no state exists to resurrect.
* Output hygiene: only counts, statuses and hashes of public audit heads are recorded.
