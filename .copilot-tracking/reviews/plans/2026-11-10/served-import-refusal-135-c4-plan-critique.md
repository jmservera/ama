---
title: Plan critique, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

Single pass, executed 2026-11-10 on the final candidate plan before any source edit. Execution: self-critique by the implementing session (not independent). Verdict: proceed with the dispositions below.

* K1 (risk): `_discard` on ConflictError path runs twice (once inside `save`, once in the override). Disposition: accepted; second run restores identical snapshots and is idempotent.
* K2 (risk): `_discard` clears `touched` for any other pending case edit. Disposition: the register path calls the method with no other edits; the override is only entered from `record_import_refusals`, documented in the docstring.
* K3 (gap): JSON audit failure after durable save. Disposition: explicit `PartiallyRecordedError`; no atomicity claim.
* K4 (gap): `mssql_python.Error` unavailable when the driver is missing. Disposition: import only when `ZF_STORE=mssql`; a missing driver then surfaces in `open_store` as an import failure already outside the contract and is not masked.
* K5 (scope): a broader audit-before-save refactor of other domains is rejected.
* K6 (web): the copy change is one sentence and needs coverage in the existing screen test; no harness or manifest edit expected. If a scenario manifest recipe changes, its integrity test must be run.
* K7 (evidence): MSSQL proof cannot be waived. If the container or driver is unavailable the claim is blocked.
* K8 (process): this critique is self-run and C3 order adverse is unchanged.
