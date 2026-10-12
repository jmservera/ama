"""Initialize app-scoped Entra roles and the existing SQL workbench roster."""
import argparse
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import subprocess
import time
from typing import Any
from urllib.parse import urlsplit
import uuid

GRAPH = "https://graph.microsoft.com/v1.0/"


def azure(args: list[str], profile: Path | None = None) -> Any:
    """Run Azure CLI without disclosing tokens, directory payloads or stderr."""
    env = dict(os.environ)
    if profile is not None:
        env["AZURE_CONFIG_DIR"] = str(profile)
    result = subprocess.run(["az", *args, "-o", "json"], env=env,
                            capture_output=True, text=True)
    if result.returncode:
        operation = " ".join(args[:2])
        raise RuntimeError(f"Azure CLI {operation} failed (exit {result.returncode}); "
                           "check the selected profile and its management permissions.")
    return json.loads(result.stdout) if result.stdout.strip() else None


class Directory:
    """Fixed-host Graph reads and application-role additions using a CLI profile."""

    def __init__(self, profile: Path):
        self.profile = profile

    def request(self, path: str, *, body: dict | None = None) -> dict:
        """Issue one fixed-host Graph request; never follow an arbitrary next link."""
        url = path if path.startswith("https://") else GRAPH + path
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "graph.microsoft.com" or not parsed.path.startswith("/v1.0/"):
            raise ValueError("Refusing a Graph continuation outside the fixed v1.0 host.")
        args = ["rest", "--method", "POST" if body is not None else "GET", "--url", url]
        if body is not None:
            args += ["--body", json.dumps(body)]
        value = azure(args, self.profile)
        if not isinstance(value, dict):
            raise ValueError("Graph response is not an object.")
        return value

    def pages(self, path: str) -> list[dict]:
        """Read the complete collection or fail; partial membership is not success."""
        items, seen = [], set()
        while path:
            if path in seen:
                raise ValueError("Graph collection has a repeated continuation.")
            seen.add(path)
            value = self.request(path)
            if not isinstance(value.get("value"), list):
                raise ValueError("Graph collection is missing its value array.")
            items.extend(value["value"])
            path = value.get("@odata.nextLink", "")
            if not isinstance(path, str):
                raise ValueError("Graph continuation is not a string.")
        return items


def read_roster(path: Path) -> list[dict]:
    """Read private operator input; personal directory data must stay outside Git."""
    if path.stat().st_mode & 0o077 or path.parent.stat().st_mode & 0o077:
        raise ValueError("Roster must have mode 0600 in a mode-0700 directory.")
    value = json.loads(path.read_text())
    if not isinstance(value, list) or not value:
        raise ValueError("Roster must be a nonempty array of code/userId objects.")
    codes, ids = set(), set()
    for row in value:
        if not isinstance(row, dict) or not isinstance(row.get("code"), str) or not row["code"]:
            raise ValueError("Each roster position needs a staff code.")
        row["userId"] = str(uuid.UUID(row["userId"]))
        if row["code"] in codes or row["userId"] in ids:
            raise ValueError("Roster codes and directory identities must be distinct.")
        codes.add(row["code"])
        ids.add(row["userId"])
    return value


def person(user: dict) -> dict:
    """Validate an enabled human member and normalize only current identity fields."""
    if user.get("accountEnabled") is not True or user.get("userType") != "Member":
        raise ValueError("Selected account is not an enabled member person.")
    name, email = user.get("displayName"), user.get("userPrincipalName")
    if not isinstance(name, str) or not name.strip() or not isinstance(email, str) or not email.strip() or len(email) > 200:
        raise ValueError("Selected account is missing a usable display name or UPN.")
    if "confrm" in name.lower() or email.lower().startswith(("desk-", "desk.", "wksp-")):
        raise ValueError("Room, desk and workspace accounts cannot be staff.")
    return {"oid": str(uuid.UUID(user["id"])), "name": name, "email": email.lower()}


def effective_roles(assignments: list[dict], uid: str, groups: set[str],
                    resource: str, roles: list[dict], role_map: dict[str, str]) -> set[str]:
    """Match runtime's set of mapped internal roles, including inherited grants."""
    definitions = {r["id"]: role_map[r["value"]] for r in roles if r.get("value") in role_map}
    principals = groups | {uid}
    return {definitions[a["appRoleId"]] for a in assignments
            if a.get("resourceId", resource) == resource and a.get("principalId") in principals
            and a.get("appRoleId") in definitions}


def reconcile_roles(directory: Directory, resource: str, roles: list[dict],
                    role_map: dict[str, str], roster: list[dict], *, apply: bool) -> int:
    """Validate every effective role before adding only missing application grants."""
    path = f"servicePrincipals/{resource}/appRoleAssignedTo"
    assignments = directory.pages(path)
    missing = []
    for row in roster:
        uid = row["oid"]
        groups = {g["id"] for g in directory.pages(
            f"users/{uid}/memberOf/microsoft.graph.group?$select=id")}
        actual = effective_roles(assignments, uid, groups, resource, roles, role_map)
        if actual and actual != {row["role"]}:
            raise ValueError(f"Position {row['code']} has conflicting effective application roles.")
        if not actual:
            choices = [r for r in roles if r.get("isEnabled") is True
                       and "User" in r.get("allowedMemberTypes", [])
                       and role_map.get(r.get("value")) == row["role"]]
            if len(choices) != 1:
                raise ValueError(f"Position {row['code']} needs one enabled matching app-role definition.")
            missing.append((row, groups, choices[0]["id"]))
    if not apply:
        return len(missing)
    for row, _, rid in missing:
        directory.request(path, body={"principalId": row["oid"], "resourceId": resource, "appRoleId": rid})
    for attempt in range(5):
        assignments = directory.pages(path)
        verified = []
        for row in roster:
            groups = {g["id"] for g in directory.pages(
                f"users/{row['oid']}/memberOf/microsoft.graph.group?$select=id")}
            verified.append(effective_roles(assignments, row["oid"], groups, resource, roles, role_map) == {row["role"]})
        if all(verified):
            return len(missing)
        if attempt < 4:
            time.sleep(2)
    raise RuntimeError("New application roles are not confirmed; SQL was not changed. Retry initialization.")


def prepare_roster(db: Any, wanted: list[dict], directory: Directory) -> list[dict]:
    """Resolve live people while preserving every existing position and bound identity."""
    current = {json.loads(body)["code"]: json.loads(body) for _, body in
               db.execute("SELECT email, body FROM staff").fetchall()}
    if not set(current).issubset({r["code"] for r in wanted}):
        raise ValueError("Roster must cover every current staff code.")
    suppliers = {r[0] for r in db.execute("SELECT DISTINCT contractor FROM cases").fetchall() if r[0]}
    out, emails = [], set()
    for spec in wanted:
        old = current.get(spec["code"])
        if old is None:
            if spec.get("role") != "Contractor" or spec.get("contractor") not in suppliers:
                raise ValueError("New positions must be Contractors with an existing explicit supplier scope.")
            old = {"code": spec["code"], "role": "Contractor", "contractor": spec["contractor"]}
        identity = person(directory.request(
            f"users/{spec['userId']}?$select=id,displayName,userPrincipalName,accountEnabled,userType"))
        if identity["oid"] != spec["userId"]:
            raise ValueError("Graph returned a different requested person.")
        if old.get("oid") and old["oid"].lower() != identity["oid"]:
            raise ValueError(f"Refusing to replace the existing binding at {spec['code']}.")
        if identity["email"] in emails:
            raise ValueError("Directory UPNs must be distinct.")
        emails.add(identity["email"])
        out.append(dict(old, **identity))
    return out


def install_roster(db: Any, roster: list[dict], *, apply: bool) -> dict[str, int]:
    """Atomically reconcile current identities/owner labels; preserve all historical actors."""
    from zavaforward_mvp import ledger

    db.execute("BEGIN IMMEDIATE")
    try:
        old_rows = db.execute("SELECT email, body FROM staff").fetchall()
        old = {json.loads(body)["code"]: json.loads(body) for _, body in old_rows}
        new = {r["code"]: r for r in roster}
        if len(new) != len(roster) or not set(old).issubset(new):
            raise ValueError("Roster coverage changed before the SQL write.")
        if len({r["oid"] for r in roster}) != len(roster) or len({r["email"] for r in roster}) != len(roster):
            raise ValueError("Roster identities and UPNs must remain distinct.")
        for code, previous in old.items():
            if previous.get("oid") and previous["oid"].lower() != new[code]["oid"].lower():
                raise ValueError(f"Existing binding changed at {code}; refusing the SQL write.")
            protected = {k: v for k, v in previous.items() if k not in ("name", "email", "oid")}
            if any(new[code].get(k) != v for k, v in protected.items()):
                raise ValueError(f"Protected profile fields changed at {code}.")
        changes = []
        for cid, version, body in db.execute("SELECT id, rowversion, body FROM cases").fetchall():
            case = json.loads(body)
            if case.get("owner_code") in new and case.get("owner") != new[case["owner_code"]]["name"]:
                case["owner"] = new[case["owner_code"]]["name"]
                changes.append((cid, version, json.dumps(case)))
        staff_changes = sum(old.get(code) != row for code, row in new.items())
        result = {"staff_changes": staff_changes, "owner_labels": len(changes)}
        if not apply or not (staff_changes or changes):
            db.execute("ROLLBACK")
            return result
        seq = int(db.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0]) + 1
        for email, _ in old_rows:
            if db.execute("DELETE FROM staff WHERE email=?", (email,)).rowcount != 1:
                raise RuntimeError("Staff changed inside the locked transaction.")
        for row in roster:
            db.execute("INSERT INTO staff (email, body) VALUES (?,?)", (row["email"], json.dumps(row)))
        for cid, version, body in changes:
            if db.execute("UPDATE cases SET body=?, rowversion=rowversion+1, seq=? WHERE id=? AND rowversion=?",
                          (body, seq, cid, version)).rowcount != 1:
                raise RuntimeError("Case version changed inside the locked transaction.")
        count, head = db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone()
        detail = json.dumps({"codes": sorted(new), **result, "application_roles_only": True}, sort_keys=True)
        entry = ledger.make_entry("tenant-staff-initializer", "staff-initialized", "", detail, head,
                                  datetime.now(timezone.utc).isoformat(timespec="seconds"))
        db.execute("INSERT INTO audit (at,who,action,case_id,detail,prev,hash) VALUES (?,?,?,?,?,?,?)",
                   (entry["at"], entry["who"], entry["action"], "", detail, head, entry["hash"]))
        db.execute("UPDATE audit_head SET count=?, hash=? WHERE id=1", (count + 1, entry["hash"]))
        db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq),))
        db.execute("COMMIT")
        return result
    except BaseException:
        db.execute("ROLLBACK")
        raise


def restart_api(group: str, app: str) -> None:
    """Converge startup-cached staff on every serving revision, even after SQL no-op."""
    revisions = azure(["containerapp", "revision", "list", "-g", group, "-n", app])
    traffic = azure(["containerapp", "show", "-g", group, "-n", app,
                     "--query", "properties.configuration.ingress.traffic"])
    latest = azure(["containerapp", "show", "-g", group, "-n", app,
                    "--query", "properties.latestReadyRevisionName"])
    serving = {t.get("revisionName") or latest for t in traffic if t.get("weight", 0) > 0}
    if not serving or not serving.issubset({r["name"] for r in revisions}):
        raise RuntimeError("No traffic-serving revision found; initialization runtime remains incomplete.")
    for revision in revisions:
        name = revision["name"]
        if name not in serving:
            continue
        before = {r["name"] for r in azure(["containerapp", "replica", "list", "-g", group, "-n", app, "--revision", name])}
        azure(["containerapp", "revision", "restart", "-g", group, "-n", app, "--revision", name])
        for attempt in range(60):
            replicas = azure(["containerapp", "replica", "list", "-g", group, "-n", app, "--revision", name])
            if replicas and all(r["name"] not in before and all(c.get("ready") is True for c in r["properties"]["containers"])
                                for r in replicas):
                break
            time.sleep(3)
        else:
            raise RuntimeError("SQL committed but fresh API replicas are not ready; retry --apply --restart.")


def main(argv: list[str] | None = None) -> int:
    """Resolve deployed configuration and reconcile only explicitly selected private people."""
    from zavaforward_mvp.auth import DEFAULT_ROLE_MAP
    from zavaforward_mvp.mssqlstore import _Conn, connection_string

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--container-app", required=True)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--tenant-profile", type=Path, default=Path.home() / ".azure" / "zava-entra-init")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--restart", action="store_true")
    args = parser.parse_args(argv)
    if args.restart and not args.apply:
        parser.error("--restart requires --apply; --check is read-only.")
    wanted = read_roster(args.roster)
    operator_tenant = azure(["account", "show", "--query", "tenantId"])
    if azure(["account", "show", "--query", "tenantId"], args.tenant_profile) != operator_tenant:
        raise ValueError("Administrative profile is not in the deployment tenant.")
    container = azure(["containerapp", "show", "-g", args.resource_group, "-n", args.container_app])
    env = {r["name"]: r.get("value") for r in container["properties"]["template"]["containers"][0]["env"]}
    if env.get("ZF_ENTRA_TENANT_ID", "").lower() != operator_tenant.lower() or env.get("ZF_AUTH") != "trusted-proxy":
        raise ValueError("API is not protected by the expected tenant's trusted proxy.")
    auth = azure(["containerapp", "auth", "show", "-g", args.resource_group, "-n", args.container_app])
    if auth["platform"]["enabled"] is not True:
        raise ValueError("Ingress authentication is disabled.")
    client = str(uuid.UUID(auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"]))
    directory = Directory(args.tenant_profile)
    sp = directory.request(f"servicePrincipals(appId='{client}')?$select=id,appRoles")
    role_map = dict(DEFAULT_ROLE_MAP)
    role_map.update(json.loads(env.get("ZF_ROLE_MAP") or "{}"))
    token = azure(["account", "get-access-token", "--resource", "https://database.windows.net/"])["accessToken"]
    sql_env = {**env, "ZF_SQL_AUTH": "token", "ZF_SQL_TOKEN": token}
    db = _Conn(connection_string(sql_env), token)
    try:
        roster = prepare_roster(db, wanted, directory)
        sql = install_roster(db, roster, apply=False)
        grants = reconcile_roles(directory, sp["id"], sp["appRoles"], role_map, roster, apply=args.apply)
        if args.apply:
            sql = install_roster(db, roster, apply=True)
            if args.restart:
                try:
                    restart_api(args.resource_group, args.container_app)
                except RuntimeError as error:
                    raise RuntimeError(
                        f"SQL initialized but runtime convergence was not confirmed: {error} "
                        "Retry the same --apply --restart command."
                    ) from error
        print(json.dumps({"mode": "apply" if args.apply else "check", "positions": len(roster),
                          "roles_missing_or_added": grants, **sql,
                          "restart_required": not (args.apply and args.restart)}))
        if args.apply:
            return 0 if args.restart else 3
        return 0 if not (grants or any(sql.values())) else 2
    finally:
        db.raw.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as error:
        logging.error("%s", error)
        raise SystemExit(1) from None
