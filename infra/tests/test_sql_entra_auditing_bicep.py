"""Azure SQL Entra-only, TLS, auditing and network contract (issue 143)."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = (ROOT / "modules" / "sql.bicep").read_text(encoding="utf-8")
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")


def block(source: str, start: str) -> str:
    """Return the brace-balanced block that follows the first `start` marker."""
    begin = source.index(start)
    open_at = source.index("{", begin)
    depth = 0
    for index in range(open_at, len(source)):
        depth += {"{": 1, "}": -1}.get(source[index], 0)
        if depth == 0:
            return source[begin : index + 1]
    raise AssertionError(f"unbalanced block for {start}")


class SqlEntraAuditingContractTests(unittest.TestCase):
    def test_entra_only_authentication_with_group_admin(self) -> None:
        server = block(SQL, "resource server ")
        administrators = block(server, "administrators:")
        self.assertIn("azureADOnlyAuthentication: true", administrators)
        self.assertIn("administratorType: 'ActiveDirectory'", administrators)
        self.assertIn("sid: entraAdminGroupObjectId", administrators)
        self.assertIn("param entraAdminPrincipalType string = 'Group'", SQL)
        self.assertEqual(SQL.count("azureADOnlyAuthentication"), 1)

    def test_no_sql_password_or_sql_login_literals(self) -> None:
        for source in (SQL, MAIN):
            self.assertNotRegex(source, r"(?i)administratorLogin(Password)?\s*:")
            self.assertNotRegex(source, r"(?i)\bsql[A-Za-z]*password\b")
            self.assertNotRegex(source, r"(?i)azureADOnlyAuthentication:\s*false")
        self.assertNotRegex(SQL, r"(?i)password\s*[:=]\s*'")

    def test_tls_12_minimum_and_no_public_network(self) -> None:
        server = block(SQL, "resource server ")
        self.assertIn("minimalTlsVersion: '1.2'", server)
        self.assertIn("publicNetworkAccess: 'Disabled'", server)
        self.assertIn("restrictOutboundNetworkAccess: 'Disabled'", server)

    def test_least_privilege_firewall_has_no_open_rules(self) -> None:
        self.assertNotIn("firewallRules", SQL)
        self.assertNotIn("virtualNetworkRules", SQL)
        self.assertNotIn("0.0.0.0", SQL)
        self.assertNotIn("255.255.255.255", SQL)
        endpoint = block(SQL, "module endpoint ")
        self.assertIn("groupId: 'sqlServer'", endpoint)
        self.assertIn("targetResourceId: server.id", endpoint)

    def test_server_auditing_enabled_to_azure_monitor(self) -> None:
        audit = block(SQL, "resource serverAudit ")
        self.assertIn("state: 'Enabled'", audit)
        self.assertIn("isAzureMonitorTargetEnabled: true", audit)
        for group in (
            "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP",
            "FAILED_DATABASE_AUTHENTICATION_GROUP",
            "BATCH_COMPLETED_GROUP",
        ):
            self.assertIn(group, audit)
        self.assertIn("state: 'Enabled'", block(SQL, "resource threatProtection "))

    def test_diagnostics_route_audit_and_database_logs(self) -> None:
        server_diag = block(SQL, "resource serverDiagnostics ")
        self.assertIn("scope: masterDb", server_diag)
        self.assertIn("SQLSecurityAuditEvents", server_diag)
        self.assertIn("dependsOn: [serverAudit]", server_diag)
        db_diag = block(SQL, "resource databaseDiagnostics ")
        self.assertIn("scope: database", db_diag)
        self.assertIn("categoryGroup: 'allLogs'", db_diag)
        for diag in (server_diag, db_diag):
            self.assertIn("workspaceId: workspaceId", diag)
            self.assertNotRegex(diag, r"enabled:\s*false")

    def test_main_wires_entra_admin_and_workspace_without_secrets(self) -> None:
        module = block(MAIN, "module sql ")
        for arg in (
            "entraAdminGroupName: sqlAdminGroupName",
            "entraAdminGroupObjectId: sqlAdminGroupObjectId",
            "entraAdminPrincipalType: sqlAdminPrincipalType",
        ):
            self.assertIn(arg, module)
        self.assertRegex(module, r"workspaceId:\s*\S+")
        self.assertIsNone(re.search(r"(?i)password|secret", module))


if __name__ == "__main__":
    unittest.main()
