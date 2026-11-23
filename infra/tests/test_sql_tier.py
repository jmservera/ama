"""SQL tier, backup and recovery contract (issue 145)."""

import os
import re
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

    def test_runbook_parameter_table_matches_bicep_defaults(self) -> None:
        def row(name: str) -> str:
            match = re.search(rf"^\| `{name}` \| ([^|]+) \|", RUNBOOK, re.MULTILINE)
            self.assertIsNotNone(match, name)
            assert match is not None
            return match.group(1).strip()

        module_days = re.search(r"param backupRetentionDays int = (\d+)", SQL)
        main_days = re.search(r"param sqlBackupRetentionDays int = (\d+)", MAIN)
        pilot_days = re.search(r"param sqlBackupRetentionDays = (\d+)", PILOT)
        self.assertTrue(module_days and main_days and pilot_days)
        assert module_days and main_days and pilot_days
        self.assertEqual(module_days.group(1), main_days.group(1))
        self.assertEqual(module_days.group(1), pilot_days.group(1))
        self.assertEqual(row("sqlBackupRetentionDays").split()[0], module_days.group(1))

        self.assertIn("param backupStorageRedundancy string = ''", SQL)
        self.assertIn("(zoneRedundant ? 'Zone' : 'Local')", SQL)
        self.assertIn("param zoneRedundant bool = false", SQL)
        self.assertIn("`Local`", row("sqlBackupStorageRedundancy"))
        self.assertIn("`false`", row("zoneRedundant"))

    def test_runbook_reassessment_keeps_restore_blocked(self) -> None:
        section = RUNBOOK.split("## Reassessment 2026-11-17", 1)[1].split("## Evidence", 1)[0]
        self.assertIn("`Local`", section)
        self.assertIn("blocked", section)
        self.assertIn("#121 is open", section)

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
        defaults = {k: v["defaultValue"] for k, v in params.items() if "defaultValue" in v}

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
        dtu = database_for(sqlTier="dtu", autoPauseDelayMinutes=120, maxVCores=4)
        self.assertEqual(dtu["sku"], {"name": "Standard", "tier": "Standard", "capacity": 10})
        self.assertIsNone(dtu["properties"]["autoPauseDelay"])
        self.assertIsNone(dtu["properties"]["minCapacity"])
        self.assertTrue(dtu["properties"]["isLedgerOn"])


if __name__ == "__main__":
    unittest.main()
