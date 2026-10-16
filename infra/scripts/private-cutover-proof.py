#!/usr/bin/env python3
"""Run bounded synthetic private cut-over or public direct-ingress probes."""

import argparse
import base64
import ipaddress
import json
import os
import re
import socket
import stat
import sys
import tempfile
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

if TYPE_CHECKING:
    from zava_forward.core.mssqlstore import _Conn

PROOF = "ama-src-private-proof-2026-10-16"
CASE_ID = "CUTOVER-SYNTHETIC-ONLY"
SENTINEL = "cutover_proof"
REPO = Path(__file__).resolve().parents[2]


def emit(check: str, **result: object) -> None:
    print(json.dumps({"check": check, **result}), flush=True)


def private_dns(host: str) -> list[str]:
    addresses = sorted(
        {row[4][0] for row in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}
    )
    network = ipaddress.ip_network("10.40.0.0/16")
    if not addresses or any(ipaddress.ip_address(address) not in network for address in addresses):
        raise ValueError("Endpoint is not in the approved AMA VNet")
    return addresses


def fixture() -> dict:
    return {
        "as_of": "2026-10-16",
        "staff": [],
        "cases": [
            {
                "id": CASE_ID,
                "wave": "Infrastructure proof only",
                "closed": False,
                "stage": "Contacting resident",
                "stage_since": "2026-10-16",
                "days_in_stage": 0,
                "waiting_on": "Unassigned",
                "reason": PROOF,
                "owner_code": "",
                "owner": "",
                "owner_role": "",
                "resident": {"name": "Synthetic Example", "priority_support": False},
                "home": {
                    "address": "1 Fictional Test Road",
                    "postcode": "TE1 1ST",
                    "area": "Synthetic",
                    "lat": 0,
                    "lon": 0,
                },
                "measures": "Infrastructure test, not works",
                "contractor": {"name": ""},
                "decision": {"status": "Waiting", "by": None, "at": None},
                "funding_ok": False,
                "contacts": [],
                "appointments": [],
                "hazards": [],
                "history": [],
                "documents": [],
            }
        ],
    }


def allowed_tables() -> set[str]:
    from zava_forward.core.assistants import MSSQL_DDL
    from zava_forward.core.mssqlstore import TABLES

    names = set(TABLES)
    for ddl in MSSQL_DDL:
        match = re.match(r"CREATE TABLE (\w+) ", ddl)
        if match is None:
            raise ValueError("Unexpected runtime assistant DDL")
        names.add(match.group(1))
    return names


def preflight(db: "_Conn", allowed: set[str]) -> bool:
    tables = {
        row[0]
        for row in db.execute(
            "SELECT name FROM sys.tables WHERE is_ms_shipped=0 "
            "AND ledger_type<>1 AND is_dropped_ledger_table=0"
        ).fetchall()
    }
    if not tables:
        return False
    if SENTINEL not in tables or not tables.issubset(allowed | {SENTINEL}):
        raise RuntimeError("Unrecognized database; no application data read or changed")
    row = db.execute("SELECT proof FROM cutover_proof WHERE id=1").fetchone()
    if row is None or row[0] != PROOF:
        raise RuntimeError("Unrecognized proof ownership")
    return True


def grant(db: "_Conn", name: str, client_id: str, roles: tuple[str, ...]) -> None:
    if not re.fullmatch(r"id-cutover-test-(api|import)", name):
        raise ValueError("Unexpected contained user")
    sid = "0x" + uuid.UUID(client_id).bytes_le.hex()
    db.execute(
        f"IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name=N'{name}') "
        f"CREATE USER [{name}] WITH SID={sid}, TYPE=E"
    )
    actual = db.execute(
        "SELECT CONVERT(varchar(256), sid, 1) FROM sys.database_principals WHERE name=?",
        (name,),
    ).fetchone()
    if actual is None or actual[0].lower() != sid.lower():
        raise RuntimeError("Existing contained user SID mismatch")
    for role in roles:
        if role not in {"db_datareader", "db_datawriter", "db_ddladmin"}:
            raise ValueError("Unexpected SQL role")
        db.execute(f"ALTER ROLE [{role}] ADD MEMBER [{name}]")


def sql_probe(initialize: bool) -> None:
    from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

    server = os.environ["ZF_SQL_SERVER"]
    emit("sql_private_dns", addresses=private_dns(server), status="Passed")
    env = dict(os.environ, ZF_SQL_AUTH="msi")
    if not env.get("ZF_SQL_CLIENT_ID"):
        raise ValueError("Explicit user-assigned identity is required")
    db = _Conn(connection_string(env))
    try:
        recognized = preflight(db, allowed_tables())
        emit("database_preflight", recognized_proof=recognized, status="Passed")
        if not initialize and not recognized:
            raise RuntimeError("Verification cannot initialize an empty database")
        if initialize:
            if not recognized:
                db.execute(
                    "CREATE TABLE cutover_proof (id INT PRIMARY KEY, proof NVARCHAR(100) NOT NULL)"
                )
                db.execute("INSERT INTO cutover_proof (id,proof) VALUES (1,?)", (PROOF,))
            grant(
                db,
                "id-cutover-test-api",
                os.environ["PROOF_API_CLIENT_ID"],
                ("db_datareader", "db_datawriter", "db_ddladmin"),
            )
            grant(
                db,
                "id-cutover-test-import",
                os.environ["PROOF_IMPORT_CLIENT_ID"],
                ("db_datareader", "db_datawriter"),
            )
            emit("contained_users", count=2, status="Passed")
    finally:
        db.close()
    with tempfile.TemporaryDirectory() as directory:
        seed = Path(directory) / "synthetic-proof.json"
        if initialize:
            seed.write_text(json.dumps(fixture()), encoding="utf-8")
        store = MssqlStore(str(seed), env=env, state_dir=directory)
        try:
            if set(store.cases) != {CASE_ID} or store.cases[CASE_ID]["reason"] != PROOF:
                raise RuntimeError("Synthetic application state differs")
            if store.staff:
                raise RuntimeError("Proof must not contain staff bindings")
            emit(
                "application_sql_state",
                status="Passed",
                cases=1,
                staff=0,
                marker=PROOF,
                seed_available=seed.exists(),
                identity="initializer" if initialize else "api",
            )
        finally:
            store.db.close()


class NoRedirect(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise HTTPError(req.full_url, code, msg, headers, fp)

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


def http_result(url: str, headers: dict[str, str] | None = None) -> tuple[int, str]:
    opener = build_opener(NoRedirect())
    try:
        with opener.open(Request(url, headers=headers or {}), timeout=20) as response:
            return response.status, response.headers.get("Location", "")
    except HTTPError as error:
        try:
            return error.code, error.headers.get("Location", "")
        finally:
            error.close()


def http_status(url: str, headers: dict[str, str] | None = None) -> int:
    return http_result(url, headers)[0]


def session_headers(path: Path) -> dict[str, str]:
    resolved = path.expanduser().resolve()
    if path.expanduser().is_symlink() or resolved == REPO or REPO in resolved.parents:
        raise ValueError("Session input must be a private file outside the repository")
    metadata = resolved.stat()
    if (not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600
            or metadata.st_uid != os.getuid() or metadata.st_size > 16384):
        raise ValueError("Session input requires an owner-only regular file with mode 0600")
    data = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) not in ({"cookie"}, {"token"}):
        raise ValueError("Session input must contain exactly cookie or token")
    value = next(iter(data.values()))
    if (not isinstance(value, str) or not value or not value.isascii()
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise ValueError("Session input contains an invalid credential")
    return {"Cookie": value} if "cookie" in data else {"Authorization": "Bearer " + value}


def browser_redirect(base: str, max_hops: int) -> None:
    current = base + "/app"
    headers = {"Accept": "text/html", "User-Agent": "Mozilla/5.0 DirectIngressProbe"}
    for hop in range(max_hops + 1):
        status, location = http_result(current, headers)
        try:
            target = urlsplit(urljoin(current, location))
            safe = (status == 302 and bool(location) and target.scheme == "https"
                    and not target.username and not target.password and not target.fragment)
            login = safe and target.netloc == "login.microsoftonline.com"
            local = (safe and target.netloc == urlsplit(base).netloc
                     and target.path.startswith("/.auth/") and "\\" not in location
                     and "%" not in target.path and "/../" not in target.path)
        except ValueError:
            login = local = False
        if login:
            emit("browser_sign_in", http_status=status, expected=302, status="Passed",
                 same_origin_hops=hop)
            return
        if not local or hop == max_hops:
            emit("browser_sign_in", http_status=status, expected=302, status="Failed",
                 same_origin_hops=hop)
            raise RuntimeError("Browser sign-in redirect failed")
        current = urljoin(current, location)
    raise RuntimeError("Browser sign-in redirect limit exceeded")


def smoke(base: str, *, direct_ingress: bool = False, auth_hops: int = 0,
          wrong_role_session: Path | None = None) -> None:
    parts = urlsplit(base)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or not parts.hostname.endswith(".azurecontainerapps.io")
        or parts.path not in ("", "/")
        or parts.query
        or parts.fragment
        or parts.username
        or parts.port not in (None, 443)
        or parts.password
        or "\\" in base
    ):
        raise ValueError("Expected a Container Apps HTTPS origin")
    if not 0 <= auth_hops <= 5:
        raise ValueError("Auth hops must be between zero and five")
    if not direct_ingress and (auth_hops or wrong_role_session):
        raise ValueError("Browser/session probes require explicit direct-ingress mode")
    if direct_ingress:
        if ".internal." in parts.hostname:
            raise ValueError("Direct mode requires a public Container Apps origin")
    else:
        emit("api_private_dns", addresses=private_dns(parts.hostname), status="Passed")
    credentials = session_headers(wrong_role_session) if wrong_role_session else None
    base = base.rstrip("/")
    principal = base64.b64encode(
        json.dumps(
            {
                "auth_typ": "aad",
                "claims": [{"typ": "roles", "val": "ProgrammeManager"}],
            }
        ).encode()
    ).decode()
    checks = [
        ("health", "/healthz", {}, 200),
        ("anonymous_api_denial", "/api/me", {}, 401),
        ("malformed_bearer_denial", "/api/me", {"Authorization": "Bearer not-a-jwt"}, 401),
        ("forged_principal_denial", "/api/me", {"X-MS-CLIENT-PRINCIPAL": principal}, 401),
    ]
    if direct_ingress:
        checks[1] = (
            "anonymous_api_denial", "/api/me",
            {"Accept": "application/json", "User-Agent": "ZavaForwardDirectProbe/1.0"}, 401)
        checks[1:1] = [
            ("root", "/", {}, 200),
            ("welcome", "/welcome.html", {}, 200),
            ("browser_json_api_denial", "/api/me",
             {"Accept": "application/json", "User-Agent": "Mozilla/5.0 DirectIngressProbe"}, 401),
        ]
    if credentials:
        status = http_status(base + "/api/me", credentials)
        emit("wrong_role_session", http_status=status, expected=200,
             status="Passed" if status == 200 else "Failed")
        if status != 200:
            raise RuntimeError("Role probe requires an authenticated Contractor session")
        checks.append(("wrong_role_denial", "/api/stats", credentials, 403))
    failed = False
    for name, path, headers, expected in checks:
        status = http_status(base + path, headers)
        emit(
            name,
            http_status=status,
            expected=expected,
            status="Passed" if status == expected else "Failed",
        )
        failed |= status != expected
    if direct_ingress:
        if not credentials:
            emit("wrong_role_denial", status="Not run", expected=403,
                 reason="No private wrong-role session supplied; authorization is unverified.")
        try:
            browser_redirect(base, auth_hops)
        except RuntimeError:
            failed = True
    if failed:
        raise RuntimeError("One or more ingress probes failed")


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError("Invalid arguments; use --help")


def main() -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("mode", choices=("initialize", "verify", "smoke"))
    parser.add_argument("--base-url")
    parser.add_argument("--direct-ingress", action="store_true",
                        help="Probe the public API origin without private DNS validation")
    parser.add_argument("--auth-hops", type=int, default=0,
                        help="Allow 0-5 individually validated same-origin /.auth/ redirects")
    parser.add_argument("--wrong-role-session", type=Path,
                        help="Private mode-0600 Contractor session JSON outside Git: cookie/token")
    mode = "arguments"
    try:
        args = parser.parse_args()
        mode = args.mode
        if args.mode != "smoke" and (
                args.direct_ingress or args.auth_hops or args.wrong_role_session or args.base_url):
            parser.error("HTTP options require smoke")
        if args.mode == "smoke":
            if not args.base_url:
                parser.error("smoke requires --base-url")
            smoke(args.base_url, direct_ingress=args.direct_ingress, auth_hops=args.auth_hops,
                  wrong_role_session=args.wrong_role_session)
        else:
            sql_probe(args.mode == "initialize")
    except Exception as error:
        emit(
            mode,
            status="Failed",
            error_type=type(error).__name__,
            message="Probe stopped; inspect private diagnostics without publishing credentials.",
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
