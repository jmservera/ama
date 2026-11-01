# Issue 521 live SQL window renewal: plan (2026-11-01)

Critique: one pass, self-applied; compatible findings only (guarded UPDATE, rollback on count mismatch).
Validation tier: focused (live ops and documentation only).

* [x] 1. Read-only inspection through the existing job (counts only); back up job config.
* [x] 2. Apply the boundary by running the unchanged `infra/scripts/resident_showcase_sql.py` inside the job
  (token and connect replaced by the job's managed-identity connection; authority end 2027-02-01 set in-process
  from the repository policy value). The script's principal verification ran before the batches.
* [x] 3. Renew rows with one guarded transaction: revoked=0, valid_to equal to the old end and the single
  approved provenance; commit only if exactly 522 rows (matched E3).
* [x] 4. Redeploy with `resident_demo_deploy.py`: what-if (4 resident-owned changes), then apply with
  expiry 2027-01-31T23:59:59Z, image by digest, min 0 max 1. Credential rotation not performed (vault secrets unchanged, not authorised).
* [x] 5. Verify with Playwright and the resident test user; check min 0 and jobs Manual.
* [x] 6. Commit evidence and open a PR with `Refs #521`.
