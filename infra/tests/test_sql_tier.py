"""SQL tier, backup and recovery contract (issue 145)."""

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = (ROOT / "modules" / "sql.bicep").read_text(encoding="utf-8")
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")
PILOT = (ROOT / "main.pilot.example.bicepparam").read_text(encoding="utf-8")
RUNBOOK = (ROOT / "sql-recovery-runbook.md").read_text(encoding="utf-8")


class SqlTierTests(unittest.TestCase):
    def test_tier_selects_sku_and_serverless_only_settings(self) -> None:
        self.assertIn("serverless ? 'GP_S_Gen5' : 'GP_Gen5'", SQL)
        self.assertIn("autoPauseDelay: serverless ? autoPauseDelayMinutes : null", SQL)
        self.assertIn("minCapacity: serverless ? json('0.5') : null", SQL)
        self.assertEqual(SQL.count("autoPauseDelay:"), 1)

    def test_environment_parameters_reach_the_module(self) -> None:
        for name in (
            "sqlTier",
            "sqlVCores",
            "sqlAutoPauseDelayMinutes",
            "sqlBackupStorageRedundancy",
            "sqlBackupRetentionDays",
        ):
            self.assertRegex(MAIN, rf"param {name} ")
        for arg in (
            "sqlTier: sqlTier",
            "maxVCores: sqlVCores",
            "autoPauseDelayMinutes: sqlAutoPauseDelayMinutes",
            "backupStorageRedundancy: sqlBackupStorageRedundancy",
            "backupRetentionDays: sqlBackupRetentionDays",
        ):
            self.assertIn(arg, MAIN)

    def test_ledger_and_retention_stay_enabled(self) -> None:
        self.assertIn("isLedgerOn: true", SQL)
        self.assertIn("retentionDays: backupRetentionDays", SQL)
        self.assertIn("@maxValue(35)", SQL)

    def test_pilot_example_records_provisioned_tier(self) -> None:
        self.assertIn("param sqlTier = 'provisioned'", PILOT)
        self.assertNotIn("AutoPause", PILOT)

    def test_runbook_records_objectives_and_unperformed_restore(self) -> None:
        for text in (
            "sp_verify_database_ledger",
            "az sql db restore",
            "Undecided",
            "Not performed",
            "NFR-004",
            "#121",
        ):
            self.assertIn(text, RUNBOOK)

    @unittest.skipUnless(shutil.which("bicep"), "bicep CLI not installed")
    def test_provisioned_compiles_without_serverless_properties(self) -> None:
        out = subprocess.run(
            ["bicep", "build", str(ROOT / "modules" / "sql.bicep"), "--stdout"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        params = json.loads(out)["parameters"]
        self.assertEqual(params["sqlTier"]["defaultValue"], "serverless")
        self.assertEqual(params["backupRetentionDays"]["maxValue"], 35)
        self.assertIn("'GP_Gen5'", out)


if __name__ == "__main__":
    unittest.main()
