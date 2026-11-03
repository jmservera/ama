# Issue 185 details, round 2 (2026-11-03)

Error codes: ROTATION_REFERENCES_MISSING, ROTATION_CHECK_FAILED, ROTATION_STATE_MISMATCH, ROTATION_FAILED_OLD_KEPT, ROTATION_ROLLBACK_INCOMPLETE, ROTATION_REVOKE_FAILED:n, ROTATION_INCOMPLETE.
Precondition: registry run devices equal the manifest, all owned by the run, and store references equal the manifest references.
Live adapters must keep `issue` per-issuance and `run_references` complete after uncertain writes.
