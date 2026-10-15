# Issue 115 research: immutable Blob ledger digests

Planning Readiness: Ready. Disposition: executed.

* Evidence: ADR 0002 decisions 1, 2 (daily digests, locked time-based policy, scheduled verification, alert); `mvp/zavaforward_mvp/ledger.py` (local digest files, year digests); `documents.py` (Blob REST client with managed identity); `infra/modules/storage.bicep` (audit-archive immutability pattern); `containerapps.bicep` (scheduled jobs).
* Gap: digests were local files; no immutable container, no scheduled verifier, no alert.
* Decision: reuse the Blob REST client, add `digest_blob.py`, a `ledger-digests` container, a daily job and a log alert.
* Open items: legal retention period (DPO/owner), irreversible lock, deployment and alert-table check. ADR 0005: synthetic fixtures only; Azure deploy only.
