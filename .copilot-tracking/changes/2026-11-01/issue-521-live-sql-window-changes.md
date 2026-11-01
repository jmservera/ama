# Issue 521 live SQL window renewal: changes (2026-11-01)

No source files changed. Live changes (metadata only, no secrets, no case identifiers):

| Time (UTC) | Operation | Result |
|------------|-----------|--------|
| 15:57 | Read-only probe, job execution `job-cutover-test-init-nr6bgyb` | constraint end 2026-11-01; 522 rows revoked=0 valid_to 2026-10-31T23:59:00 |
| 15:59 | Boundary apply, execution `job-cutover-test-init-mu36xsj` | 7 batches applied, rc 0; constraint now `valid_to <= '2027-02-01T00:00:00'` |
| 16:01 | Row renewal, execution `job-cutover-test-init-meixtw2` | updated 522, committed; all rows valid_to 2027-02-01T00:00:00; view rows 522 |
| ~16:07 | `resident_demo_deploy.py` what-if then `--apply` | 4 resident-owned changes; revision `ca-resident-demo--0000005`; expiry 2027-01-31T23:59:59Z; image digest unchanged (9ce989d9c55d); min 0 max 1 |

Job `job-cutover-test-init`: full JSON diff against the pre-change backup (ignoring system data and status)
shows no difference; trigger type Manual. All eight jobs Manual; all four apps min replicas 0.
Not done: AI tariff expiry, credential rotation, image rebuild, any network or RBAC change.
