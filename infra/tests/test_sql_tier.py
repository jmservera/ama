"""SQL tier, backup and recovery contract (issue 145)."""

import os
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_bicep_policy import compile_bicep, evaluate, resource

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
            "sp_verify_database_ledger_from_digest_storage",
            "last_digest_block_id",
            "are not native digests",
            "az sql db restore",
            "Undecided",
            "Not performed",
            "NFR-004",
            "#121",
        ):
            self.assertIn(text, RUNBOOK)

    @unittest.skipUnless(
        shutil.which("az") or os.environ.get("REQUIRE_AZ_BICEP") == "1",
        "Azure CLI with Bicep is needed to compile the templates",
    )
    def test_compiled_tiers_select_sku_and_serverless_properties(self) -> None:
        template = compile_bicep("modules/sql.bicep")
        params = template["parameters"]
        self.assertEqual(params["sqlTier"]["defaultValue"], "serverless")
        self.assertEqual(params["backupRetentionDays"]["maxValue"], 35)
        database = resource(template, "Microsoft.Sql/servers/databases")
        defaults = {
            k: v["defaultValue"] for k, v in params.items() if "defaultValue" in v
        }

        def database_for(**overrides):
            return evaluate(
                {"sku": database["sku"], "properties": database["properties"]},
                defaults | overrides,
                template["variables"],
                {"json": float},
            )

        serverless = database_for(autoPauseDelayMinutes=120)
        self.assertEqual(serverless["sku"]["name"], "GP_S_Gen5")
        self.assertEqual(serverless["properties"]["autoPauseDelay"], 120)
        self.assertEqual(serverless["properties"]["minCapacity"], 0.5)
        provisioned = database_for(sqlTier="provisioned", autoPauseDelayMinutes=120)
        self.assertEqual(provisioned["sku"]["name"], "GP_Gen5")
        self.assertIsNone(provisioned["properties"]["autoPauseDelay"])
        self.assertIsNone(provisioned["properties"]["minCapacity"])


if __name__ == "__main__":
    unittest.main()
