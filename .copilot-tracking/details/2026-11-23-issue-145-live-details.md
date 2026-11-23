# Details: issue 145 live

Test `test_runbook_parameter_table_matches_bicep_defaults` in `infra/tests/test_sql_tier.py`: parse the runbook rows for `sqlBackupRetentionDays`, `sqlBackupStorageRedundancy`; assert the number equals the `backupRetentionDays` default in `sql.bicep`, the main.bicep default and the pilot example; assert the empty redundancy default derives `Local` when not zone redundant, matching the runbook text.
