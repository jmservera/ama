# Issue 107 live review (single pass)

Outcome: Conformant, with limits. Execution: self-review once. Boundary: the diff of the test file, research note, index and log.

* The new test asserts revoked status first, then old-image reactivation refusal, disabled invoke, unchanged allowance row, provider calls and domain records, over all ten variations; it ran on SQLite and actual SQL Server.
* Mssql subclasses follow the existing fixture pattern and refuse non-local hosts.
* Limits: old image is modelled as a fresh worker, not a pulled image; no Azure SQL; criterion 2 unproven; independent review and hosted CI outstanding. No material findings open.
