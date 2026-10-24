"""Discover and initialize Zava Forward Entra authentication without exposing credentials."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import random
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, NoReturn
from urllib.parse import quote, urlencode, urlsplit

import credential_arm
import staff_azure
from staff_roster import person, roster_rows

GRAPH = "https://graph.microsoft.com/v1.0/"
ARM = "https://management.azure.com"
API_VERSION = "2025-07-01"
PROFILE = Path.home() / ".azure" / "zava-entra-init"
ROSTER = Path.home() / ".azure" / "zava-forward-staff" / "roster.json"
REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parents[1] / "entra" / "app-registration.json"
ROLE_NAMESPACE = uuid.UUID("6f1d0c5e-6a0e-4c43-9a55-0c8f7a1b2d34")
GRAPH_APP = "00000003-0000-0000-c000-000000000000"
USER_READ = "e1fe6dd8-ba31-4d61-89e7-88639da4683d"
APPLICATION_WRITE = {"Application.ReadWrite.All", "Application.ReadWrite.OwnedBy",
                     "Directory.ReadWrite.All", "Directory.AccessAsUser.All"}
ASSIGNMENT_WRITE = {"AppRoleAssignment.ReadWrite.All", "Directory.ReadWrite.All",
                    "Directory.AccessAsUser.All"}
APP_PORTAL = "https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
SP_PORTAL = "https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview"
LOCK_TAG = "zava-forward-auth-lock"
STORE_TAG = "zava-forward-credential-store"
HANDOFF_TAG = "zava-forward-secret-handoff"
PROFILE_TAG = "zava-forward-deployment-profile"
TEMPLATE = [{"code": "REPLACE_EXISTING_STAFF_CODE", "userId": "REPLACE_PERSON_OBJECT_ID",
             "role": "REPLACE_APPROVED_WORKBENCH_ROLE"}]
EXERCISE_NOTICE = (
    "Demo/synthetic-exercise assignment only, by owner decision (2026-10-16). "
    "This is not evidence of professional competence or delegated authority."
)


class SetupError(Exception):
    """A sanitized, actionable operator error."""


class AzureError(SetupError):
    def __init__(self, kind: str):
        self.kind = kind
        super().__init__(
            f"Azure request failed ({kind}); no raw directory response was logged. "
            "Check network, selected account and permissions, then rerun."
        )


def identifier(value: Any) -> str | None:
    try:
        return str(uuid.UUID(value)) if isinstance(value, str) else None
    except ValueError:
        return None


def object_id(value: Any) -> str:
    result = identifier(value)
    if not result:
        raise SetupError("Directory response has an invalid identifier; no changes are safe.")
    return result


def label(value: str) -> str:
    """Only resource/display labels, never arbitrary Azure or directory output."""
    value = re.sub(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", "[redacted]", value)
    return re.sub(r"[^A-Za-z0-9 ._/\[\]-]", "?", value)[:120]


def origin(value: str) -> str:
    parsed = urlsplit(value)
    host = parsed.hostname or ""
    if (parsed.scheme != "https" or parsed.netloc != host or parsed.path not in ("", "/")
            or parsed.query or parsed.fragment or len(host) > 253 or "." not in host
            or any(not re.fullmatch(r"(?!-)[a-z0-9-]{1,63}(?<!-)", part) for part in host.split("."))):
        raise SetupError("Public URL must be an HTTPS DNS origin without credentials, port or path.")
    return f"https://{host}"


def private_path(path: Path, *, directory: bool = False, create: bool = False) -> Path:
    if path.is_symlink():
        raise SetupError("Private input/profile must not be a symbolic link.")
    resolved = path.resolve()
    if resolved == REPO or REPO in resolved.parents:
        raise SetupError("Keep private input and authentication profiles outside the repository.")
    if create:
        resolved.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not resolved.exists():
        raise SetupError("Private input/profile is missing; see infra/README.md for setup.")
    if ((directory and not resolved.is_dir())
            or stat.S_IMODE(resolved.stat().st_mode) != (0o700 if directory else 0o600)):
        raise SetupError("Private directories need mode 0700; private files need mode 0600.")
    return resolved


class Azure:
    """Capture all CLI output; body files and CLI caches stay outside Git."""

    def __init__(self, profile: Path, *, body_directory: Path | None = None,
                 extension_directory: Path | None = None):
        self.profile = profile
        self.body_directory = body_directory
        self.extension_directory = extension_directory or profile / "cliextensions"
        self.subscription: str | None = None
        self.deadline: float | None = None

    def environment(self) -> dict[str, str]:
        env = {k: v for k, v in os.environ.items() if k not in ("AZURE_CORE_DEBUG", "AZURE_DEBUG")}
        env.update(AZURE_CONFIG_DIR=str(self.profile),
                   AZURE_EXTENSION_DIR=str(self.extension_directory),
                   AZURE_LOGGING_ENABLE_LOG_FILE="false",
                   AZURE_CORE_COLLECT_TELEMETRY="false",
                   AZURE_EXTENSION_USE_DYNAMIC_INSTALL="no",
                   AZURE_CORE_ONLY_SHOW_ERRORS="true")
        return env

    def call(self, args: list[str], *, body: dict[str, Any] | None = None) -> Any:
        filename = None
        try:
            if self.subscription and args[0] in ("containerapp", "afd", "keyvault", "deployment", "identity"):
                args = [*args, "--subscription", self.subscription]
            if body is not None:
                if self.body_directory is None:
                    raise SetupError("Mutation body storage is unavailable in read-only mode.")
                with tempfile.NamedTemporaryFile(mode="w", dir=self.body_directory,
                                                 prefix="request-", suffix=".json", delete=False) as stream:
                    filename = stream.name
                    json.dump(body, stream)
                args = [*args, "--body", f"@{filename}"]
            timeout = 120.0 if self.deadline is None else min(120.0, self.deadline - time.monotonic())
            if timeout <= 0:
                raise AzureError("network")
            result = subprocess.run(
                ["az", *args, "--only-show-errors", "-o", "json"], env=self.environment(),
                capture_output=True, text=True, timeout=timeout, check=False,
            )
            if result.returncode:
                error = result.stderr.lower()
                if args[0] == "afd" and "'afd' is misspelled or not recognized" in error:
                    raise SetupError(
                        "Front Door CLI commands are unavailable. Install the CDN extension in "
                        "the isolated setup extension directory: "
                        "AZURE_CONFIG_DIR=$HOME/.azure/zava-entra-init "
                        "AZURE_EXTENSION_DIR=$HOME/.azure/zava-entra-init/cliextensions "
                        "az extension add --name cdn --upgrade. "
                        "For --tenant-profile, use that private directory instead.")
                kind = ("not-found" if any(s in error for s in ("resourcenotfound", "request_resourcenotfound", "status code: 404"))
                        else "permission" if any(s in error for s in ("forbidden", "authorization_requestdenied", "403", "insufficient privileges"))
                        else "login" if any(s in error for s in ("az login", "aadsts", "401"))
                        else "transient" if any(s in error for s in ("429", "503", "504"))
                        else "request")
                raise AzureError(kind)
            return json.loads(result.stdout) if result.stdout.strip() else None
        except subprocess.TimeoutExpired:
            raise AzureError("network") from None
        except OSError:
            raise SetupError("Azure CLI could not run or timed out; check installation/network, then rerun.") from None
        except json.JSONDecodeError:
            raise SetupError("Azure CLI returned invalid JSON; update Azure CLI and rerun.") from None
        finally:
            if filename:
                Path(filename).unlink(missing_ok=True)

    def rest(self, url: str, *, method: str = "GET", body: dict[str, Any] | None = None,
             etag: str | None = None) -> Any:
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or parsed.netloc not in ("graph.microsoft.com", "management.azure.com")
                or parsed.fragment or parsed.username):
            raise SetupError("Refusing an API request outside the fixed Graph/ARM hosts.")
        for attempt in range(5):
            try:
                headers = ["--headers", f"If-Match={etag}"] if etag else []
                value = self.call(["rest", "--method", method, "--url", url, *headers], body=body)
                if (method == "GET" and not isinstance(value, dict)) or (
                        value is not None and not isinstance(value, dict)):
                    raise SetupError("API response is not an object; refusing malformed service data.")
                return value
            except AzureError as error:
                if method != "GET" or error.kind != "transient" or attempt == 4:
                    raise
                time.sleep(2 * (attempt + 1))
        raise SetupError("API retry limit reached.")

    def pages(self, path: str) -> list[dict[str, Any]]:
        url = path if path.startswith("https://") else GRAPH + path
        out: list[dict[str, Any]] = []
        seen: set[str] = set()
        while url:
            if not url.startswith(GRAPH) or url in seen:
                raise SetupError("Invalid or repeated Graph continuation; refusing a partial result.")
            seen.add(url)
            data = self.rest(url)
            if not isinstance(data, dict) or not isinstance(data.get("value"), list):
                raise SetupError("Graph collection is malformed; refusing a partial result.")
            if not all(isinstance(row, dict) for row in data["value"]):
                raise SetupError("Graph collection contains an invalid item.")
            out.extend(data["value"])
            url = data.get("@odata.nextLink", "")
            if not isinstance(url, str):
                raise SetupError("Graph continuation is malformed.")
        return out


def device_login(cli: Azure, tenant: str | None) -> None:
    print("Sign in as an authorized application owner/admin in the isolated setup profile.")
    args = ["az", "login", "--use-device-code", "--allow-no-subscriptions", "-o", "none"]
    if tenant:
        args += ["--tenant", tenant]
    env = cli.environment()
    # Older Azure CLI versions emit the device-code instructions as a warning.
    env["AZURE_CORE_ONLY_SHOW_ERRORS"] = "false"
    try:
        process = subprocess.Popen(args, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
    except OSError:
        raise SetupError("Cannot start Azure CLI device login; reinstall Azure CLI.") from None

    def prompts() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            code = re.search(r"(?:enter the code|code)\s+([A-Z0-9]{8,12})\b", line)
            if code and "microsoft.com/devicelogin" in line:
                print(f"Open https://microsoft.com/devicelogin and enter code {code.group(1)}.", flush=True)

    reader = threading.Thread(target=prompts, daemon=True)
    reader.start()
    try:
        result = process.wait(timeout=300)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise SetupError("Sign-in timed out after five minutes; rerun when ready.") from None
    finally:
        reader.join(timeout=5)
        if process.stdout:
            process.stdout.close()
    if result:
        raise SetupError("Sign-in did not complete. Check your browser and account authority, then rerun.")


def authority_help() -> None:
    print("Azure resource-group access is not Entra directory authority.")
    print(f"Option A: open {APP_PORTAL}; App registrations > All applications > "
          "select zava-forward-api > Authentication / App roles; ask the authorized owner to apply the changes.")
    print("Option B: an authorized tenant administrator approves the provisioning client's "
          "Application.ReadWrite.All and AppRoleAssignment.ReadWrite.All permissions plus "
          "User.Read.All / GroupMember.Read.All for roster reads, then rerun with --login. "
          "Do not grant directory permissions to runtime managed identities.")
    print(f"For manual role assignments: {SP_PORTAL} > All applications > select the workbench "
          "> Users and groups > Add user/group > select principal > Select a role > Assign.")


def preflight(operator: Azure) -> None:
    if sys.version_info < (3, 10):  # noqa: UP036 - bootstrap diagnostics also run on older Python.
        raise SetupError("Python 3.10+ required. Ubuntu: sudo apt install python3; "
                         "Windows: winget install Python.Python.3.12; macOS: brew install python@3.12")
    if not shutil.which("az"):
        raise SetupError("Install Azure CLI: python3 -m pip install azure-cli; "
                         "Windows: winget install Microsoft.AzureCLI; macOS: brew install azure-cli")
    operator.call(["version"])


def require_extension(operator: Azure, name: str) -> None:
    try:
        operator.call(["extension", "show", "--name", name])
    except AzureError:
        profile = shlex.quote(str(operator.extension_directory.parent))
        extensions = shlex.quote(str(operator.extension_directory))
        raise SetupError(
            f"Install missing {name} extension in the isolated extension directory: "
            f"mkdir -p {profile} {extensions} && chmod 700 {profile} {extensions} && "
            f"AZURE_CONFIG_DIR={profile} AZURE_EXTENSION_DIR={extensions} "
            f"az extension add --name {name} --upgrade. Then rerun setup."
        ) from None


def token_permissions(cli: Azure, tenant: str | None = None) -> set[str]:
    token = cli.call(["account", "get-access-token", "--resource-type", "ms-graph"])
    try:
        payload = token["accessToken"].split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        if not isinstance(claims, dict):
            raise SetupError("Graph access token has malformed permission hints.")
        if tenant and identifier(claims.get("tid")) != tenant:
            raise SetupError("Graph access token belongs to a different tenant; renew isolated login.")
        scopes, roles = claims.get("scp", ""), claims.get("roles", [])
        if not isinstance(scopes, str) or not isinstance(roles, list) or not all(isinstance(r, str) for r in roles):
            raise SetupError("Graph access token has malformed permission hints.")
        return set(scopes.split()) | set(roles)
    except (KeyError, IndexError, TypeError, ValueError):
        raise SetupError("Cannot inspect Graph permission hints; sign in again with --login.") from None


def account(cli: Azure) -> dict[str, Any]:
    value = cli.call(["account", "show"])
    if not isinstance(value, dict) or not identifier(value.get("tenantId")):
        raise SetupError("No usable Azure account. Run setup with --login, then retry.")
    return value


def contexts(args: argparse.Namespace, operator: Azure) -> tuple[Azure, Azure, str, str]:
    readonly = args.check or args.dry_run
    private_path(args.tenant_profile, directory=True, create=not readonly)
    graph = Azure(args.tenant_profile, extension_directory=operator.extension_directory)
    try:
        management_account = account(operator)
    except AzureError as error:
        if readonly or error.kind not in ("login", "request"):
            raise
        private_path(args.tenant_profile, directory=True, create=True)
        device_login(graph, None)
        operator = graph
        management_account = account(operator)
    tenant = object_id(management_account["tenantId"])
    subscription = identifier(management_account.get("id"))
    if not subscription:
        raise SetupError("Select an account with access to resource group ama in the isolated profile, then rerun.")
    if args.login:
        private_path(args.tenant_profile, directory=True, create=True)
        device_login(graph, tenant)
    try:
        graph_account = account(graph)
        if object_id(graph_account["tenantId"]) != tenant:
            raise SetupError("Isolated profile belongs to a different tenant; rerun with --login.")
        permissions = token_permissions(graph, tenant)
    except AzureError as error:
        if readonly or error.kind not in ("login", "request", "permission"):
            raise
        private_path(args.tenant_profile, directory=True, create=True)
        device_login(graph, tenant)
        graph_account = account(graph)
        if object_id(graph_account["tenantId"]) != tenant:
            raise SetupError("Login returned a different tenant; refusing changes.") from None
        permissions = token_permissions(graph, tenant)
    if not (readonly or args.list_staff or args.lookup_upn) and not permissions.intersection(APPLICATION_WRITE):
        if graph_account.get("user", {}).get("type") == "servicePrincipal":
            print("The selected login is a service principal without directory application-write authority.")
        authority_help()
        raise SetupError("Provisioning Graph application-write permission is missing. Use Option A or B above.")
    if not readonly:
        private_path(args.tenant_profile, directory=True, create=True)
        graph.body_directory = args.tenant_profile
        operator.body_directory = args.tenant_profile
    operator.subscription = subscription
    return operator, graph, tenant, subscription


def choose(rows: list[dict[str, Any]], explicit: str | None, role: str,
           suffix: str, option: str, *, interactive: bool = False) -> dict[str, Any]:
    named = [r for r in rows if r.get("name") == explicit] if explicit else []
    tagged = [r for r in rows if r.get("tags", {}).get("zava-forward-role") == role]
    legacy = [r for r in rows if r.get("tags", {}).get("workload") == role]
    candidates = named if explicit else tagged or legacy or [
        r for r in rows if re.fullmatch(suffix, r.get("name", ""))]
    if len(candidates) != 1:
        names = ", ".join(sorted(label(r.get("name", "unnamed")) for r in candidates or rows)) or "(none)"
        if interactive and not explicit and sys.stdin.isatty():
            print(f"Found these {role} resources: {names}.")
            answer = input(f"Which {role} should this run use (or Enter to stop and deploy it first)? ").strip()
            selected = [r for r in candidates if r.get("name") == answer]
            if len(selected) == 1:
                return selected[0]
        raise SetupError(f"Cannot select one {role}. Candidates: {names}. Pass {option} with an exact name.")
    return candidates[0]


def discover(cli: Azure, args: argparse.Namespace, subscription: str) -> tuple[dict[str, Any], list[str]]:
    args.pending_domains = 0
    rows = cli.call(["containerapp", "list", "-g", args.resource_group])
    if not isinstance(rows, list):
        raise SetupError("Container App discovery did not return a list.")
    direct_rows = [
        r for r in rows
        if (r.get("tags", {}).get("zava-forward-role") == "api"
            or ("zava-forward-role" not in r.get("tags", {})
                and r.get("tags", {}).get("workload") == "api"))
        and r.get("tags", {}).get("zava-forward-ingress") == "direct"
    ]
    candidates = rows
    if not args.container_app and direct_rows:
        if len(direct_rows) != 1:
            names = ", ".join(sorted(label(r["name"]) for r in direct_rows))
            raise SetupError(
                f"Cannot select one api. Candidates: {names}. Pass --container-app with an exact name.")
        candidates = direct_rows
    interactive = not (args.check or args.dry_run or args.yes)
    app = choose(candidates, args.container_app, "api", r"ca-.+-api", "--container-app",
                 interactive=interactive)
    args.direct_ingress = (
        args.direct_ingress or app.get("tags", {}).get("zava-forward-ingress") == "direct")
    name = app["name"]
    app = cli.call(["containerapp", "show", "-g", args.resource_group, "-n", name])
    if not isinstance(app, dict):
        raise SetupError("Container App discovery returned malformed service data.")
    expected = f"/subscriptions/{subscription}/resourceGroups/{args.resource_group}/providers/Microsoft.App/containerApps/{name}"
    if app.get("id", "").lower() != expected.lower():
        raise SetupError("Discovered API is outside the selected subscription/resource group.")
    fqdn = app.get("properties", {}).get("configuration", {}).get("ingress", {}).get("fqdn")
    if not isinstance(fqdn, str):
        raise SetupError("API has no ingress hostname; deploy the API first.")
    app_url = origin("https://" + fqdn)
    urls = {app_url}
    if args.direct_ingress:
        if args.edge_profile:
            raise SetupError("--direct-ingress cannot use --edge-profile; select one ingress mode.")
        properties = app.get("properties", {})
        ingress = properties.get("configuration", {}).get("ingress", {})
        environment_id = properties.get("environmentId") or properties.get("managedEnvironmentId")
        prefix = (f"/subscriptions/{subscription}/resourceGroups/{args.resource_group}"
                  "/providers/Microsoft.App/managedEnvironments/")
        if (ingress.get("external") is not True or not isinstance(environment_id, str)
                or not environment_id.lower().startswith(prefix.lower())
                or not re.fullmatch(r"[A-Za-z0-9_-]+", environment_id[len(prefix):])):
            raise SetupError(
                "Direct ingress requires external API ingress in an environment in ama.")
        environment = cli.rest(ARM + environment_id + f"?api-version={API_VERSION}")
        vnet = environment.get("properties", {}).get("vnetConfiguration") or {}
        if vnet.get("internal") is not False:
            raise SetupError(
                "Direct ingress requires a verified external Container Apps environment.")
        if args.public_url and origin(args.public_url) != app_url:
            raise SetupError("Direct public URL must match the selected API ingress FQDN.")
        print(f"Selected direct API: {label(name)}; one API FQDN callback origin.")
        return app, [app_url]
    require_extension(cli, "cdn")
    profiles = cli.call(["afd", "profile", "list", "-g", args.resource_group])
    if not isinstance(profiles, list):
        raise SetupError("Front Door discovery did not return a list.")
    if args.edge_profile and not any(p["name"] == args.edge_profile for p in profiles):
        raise SetupError("Selected edge profile is not in resource group ama.")
    linked_profiles: dict[str, set[str]] = {}
    for profile in profiles:
        pname = profile["name"]
        if args.edge_profile and pname != args.edge_profile:
            continue
        groups = cli.call(["afd", "origin-group", "list", "-g", args.resource_group, "--profile-name", pname])
        linked: set[str] = set()
        for group in groups:
            origins = cli.call(["afd", "origin", "list", "-g", args.resource_group,
                                "--profile-name", pname, "--origin-group-name", group["name"]])
            if any(o.get("hostName") == fqdn and o.get("enabledState", "Enabled") == "Enabled" for o in origins):
                if any(o.get("hostName") != fqdn and o.get("enabledState", "Enabled") == "Enabled" for o in origins):
                    raise SetupError("Edge origin group mixes APIs; select a dedicated API edge before setup.")
                linked.add(group["id"].lower())
        if not linked:
            continue
        profile_urls: set[str] = set()
        linked_profiles[pname] = profile_urls
        endpoints = cli.call(["afd", "endpoint", "list", "-g", args.resource_group, "--profile-name", pname])
        domains = cli.call(["afd", "custom-domain", "list", "-g", args.resource_group, "--profile-name", pname])
        by_id = {d["id"].lower(): d for d in domains}
        for endpoint in endpoints:
            if endpoint.get("enabledState") != "Enabled":
                continue
            routes = cli.call(["afd", "route", "list", "-g", args.resource_group,
                              "--profile-name", pname, "--endpoint-name", endpoint["name"]])
            for route in routes:
                if (route.get("enabledState", "Enabled") != "Enabled"
                        or route.get("originGroup", {}).get("id", "").lower() not in linked):
                    continue
                if "/*" not in route.get("patternsToMatch", []) or "Https" not in route.get("supportedProtocols", []):
                    raise SetupError("Linked edge route must cover HTTPS /*, including the authentication callback.")
                if route.get("linkToDefaultDomain") == "Enabled":
                    profile_urls.add(origin("https://" + endpoint["hostName"]))
                for domain_ref in route.get("customDomains", []):
                    domain = by_id.get(domain_ref["id"].lower())
                    if not domain:
                        raise SetupError("Edge route refers to an undiscovered custom domain.")
                    if domain.get("domainValidationState") != "Approved" or domain.get("deploymentStatus") != "Succeeded":
                        args.pending_domains += 1
                        print("A linked custom domain is pending validation/deployment; its callback is not yet eligible.")
                        continue
                    profile_urls.add(origin("https://" + domain["hostName"]))
    if args.edge_profile and args.edge_profile not in linked_profiles:
        raise SetupError("Selected edge is not linked to the discovered API origin.")
    if linked_profiles:
        linked_rows = [p for p in profiles if p["name"] in linked_profiles]
        selected_edge = choose(linked_rows, args.edge_profile, "api-edge", r"afd-.+", "--edge-profile")
        urls.update(linked_profiles[selected_edge["name"]])
        if urls == {app_url}:
            raise SetupError("Selected edge has no eligible public callback route; review endpoint/domain deployment.")
    if args.public_url:
        explicit_url = origin(args.public_url)
        if explicit_url not in urls:
            raise SetupError("Explicit public URL is not an enabled, linked API/edge URL.")
    print(f"Selected API: {label(name)}; {len(urls)} API/edge callback origin(s).")
    return app, sorted(urls)


def read_roster(path: Path, keys: set[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    private_path(path)
    private_path(path.parent, directory=True)
    try:
        data = roster_rows(json.loads(path.read_text()))
    except (OSError, ValueError):
        raise SetupError("Private roster is unreadable or invalid JSON; see the documented schema.") from None
    if not isinstance(data, list) or not data:
        raise SetupError("Private roster must be a nonempty array.")
    out = []
    codes: set[str] = set()
    principals: set[str] = set()
    for row in data:
        if not isinstance(row, dict):
            raise SetupError("Each roster row must be an object.")
        if any(word in str(value).upper() for value in row.values()
               for word in ("PLACEHOLDER", "REPLACE_", "<", "YOUR_")):
            raise SetupError("Roster still contains template placeholders. Fill real existing staff codes, "
                             "person object IDs and approved roles, then rerun; no cloud writes were made.")
        code, role = row.get("code"), row.get("role")
        role = next((r["key"] for r in json.loads(MANIFEST.read_text())["appRoles"]
                     if r["label"] == role), role)
        fields = [key for key in ("userId", "groupId") if key in row]
        if (not isinstance(code, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", code)
                or code in codes or role not in keys or len(fields) != 1):
            raise SetupError("Roster needs distinct codes, an explicit manifest role and exactly one userId/groupId per row.")
        principal = identifier(row[fields[0]])
        if not principal or principal == str(uuid.UUID(int=0)) or principal in principals:
            raise SetupError("Roster principal identifiers must be valid and distinct.")
        codes.add(code)
        principals.add(principal)
        out.append({"code": code, "role": role, "kind": "users" if fields[0] == "userId" else "groups", "id": principal})
    return out


def roster_input(path: Path) -> tuple[bytes | None, bool]:
    """Only the exact shipped template is replaceable, never partial operator input."""
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise SetupError("Private roster paths must not contain symbolic links.")
    if REPO == path.resolve() or REPO in path.resolve().parents:
        raise SetupError("Keep the private roster outside Git.")
    if not path.exists():
        if path.parent.exists():
            private_path(path.parent, directory=True)
        return None, True
    private_path(path)
    private_path(path.parent, directory=True)
    try:
        data = path.read_bytes()
        return data, json.loads(data) == TEMPLATE
    except (OSError, ValueError):
        raise SetupError("Private roster is unreadable or invalid JSON.") from None


def demo_resource_id(value: Any, resource_type: str) -> tuple[str, str]:
    """Validate a group-scoped app/environment ID before normalizing its binding."""
    match = re.fullmatch(
        r"/subscriptions/([^/]+)/resourceGroups/(ama)/providers/Microsoft[.]App/"
        + re.escape(resource_type) + r"/([A-Za-z0-9_-]+)",
        value if isinstance(value, str) else "", re.IGNORECASE)
    if not match or identifier(match[1]) != match[1].lower():
        raise SetupError("Demo resource identity has an unsupported subscription/group/type scope.")
    return match[1].lower(), value.lower()


def demo_template_contract(template: Any) -> dict[str, Any]:
    """Check the supported ARM envelope, not provider-specific deployment validity."""
    error = ("Demo deployment template contract is malformed or unsupported; "
             "no roster generated. Nested deployments require separate verified evidence.")
    schemas = {
        "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json",
        "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json",
    }
    if not isinstance(template, dict):
        raise SetupError(error)
    supported = {"$schema", "languageVersion", "contentVersion", "parameters", "variables",
                 "outputs", "metadata", "definitions", "functions", "resources"}
    if template.keys() - supported:
        raise SetupError(error)
    schema = template.get("$schema")
    language = template.get("languageVersion", "1.0")
    if (not isinstance(schema, str) or schema.removesuffix("#") not in schemas
            or not isinstance(language, str) or language not in ("1.0", "2.0")
            or not isinstance(template.get("contentVersion"), str)
            or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){3}", template["contentVersion"])):
        raise SetupError(error)
    for key in ("parameters", "variables", "outputs", "metadata", "definitions"):
        if key in template and not isinstance(template[key], dict):
            raise SetupError(error)
    if ("definitions" in template and language != "2.0"
            or "functions" in template and not isinstance(template["functions"], list)):
        raise SetupError(error)
    resources = template.get("resources")
    if language == "2.0":
        if (not isinstance(resources, dict) or any(
                not isinstance(key, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key)
                for key in resources)):
            raise SetupError(error)
        pending = [(resource, False) for resource in resources.values()]
    else:
        if not isinstance(resources, list):
            raise SetupError(error)
        pending = [(resource, False) for resource in resources]
    while pending:
        resource, child = pending.pop()
        if (not isinstance(resource, dict) or any(
                not isinstance(resource.get(key), str) or not resource[key].strip()
                for key in ("name", "type", "apiVersion"))):
            raise SetupError(error)
        kind = resource["type"]
        if (not re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", kind)
                or not child and "/" not in kind
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:-[A-Za-z0-9.-]+)?",
                                    resource["apiVersion"])
                or kind.lower() == "microsoft.resources/deployments"
                or "properties" in resource and not isinstance(resource["properties"], dict)):
            raise SetupError(error)
        if "resources" in resource:
            children = resource["resources"]
            if not isinstance(children, list) or language == "2.0":
                raise SetupError(error)
            pending.extend((nested, True) for nested in children)
    return template.get("parameters", {})


def demo_deployment_parameters(cli: Azure, deployment: dict[str, Any]) -> dict[str, Any]:
    """Resolve only literal demo evidence against this deployment's actual contract."""
    error = ("Demo deployment template/parameters are unknown or malformed; "
             "verify readable deployment history before generating a roster.")
    name = deployment.get("name")
    supplied = deployment["properties"].get("parameters", {})
    if (not isinstance(name, str) or not re.fullmatch(r"[-\w.()]{1,64}", name)
            or name.startswith("-")
            or not isinstance(supplied, dict)):
        raise SetupError(error)
    template = cli.call(["deployment", "group", "export", "-g", "ama", "-n", name])
    declarations = demo_template_contract(template)
    resolved = {}
    for key, expected in (("deploymentProfile", str), ("environmentName", str), ("tags", dict)):
        if key not in declarations:
            if key in supplied:
                raise SetupError(error)
            continue
        declaration = declarations[key]
        kind = "object" if key == "tags" else "string"
        if (not isinstance(declaration, dict) or not isinstance(declaration.get("type"), str)
                or declaration["type"].lower() != kind):
            raise SetupError(error)
        if key in supplied:
            entry = supplied[key]
            if not isinstance(entry, dict) or "value" not in entry or "reference" in entry:
                raise SetupError(error)
            value = entry["value"]
        elif "defaultValue" in declaration:
            value = declaration["defaultValue"]
        else:
            raise SetupError(error)
        if not isinstance(value, expected):
            raise SetupError(error)
        resolved[key] = value
    return resolved


def require_demo(cli: Azure, app: dict[str, Any]) -> None:
    """Require resource-bound development evidence; production always wins."""
    resources = [app]
    subscription, app_id = demo_resource_id(app.get("id"), "containerApps")
    if cli.subscription and subscription != cli.subscription.lower():
        raise SetupError("Demo app identity is outside the selected subscription.")
    properties = app.get("properties", {})
    if not isinstance(properties, dict):
        raise SetupError("Demo app properties are unknown or malformed; no roster generated.")
    environment_id = properties.get("environmentId") or properties.get("managedEnvironmentId")
    if environment_id:
        environment_subscription, normalized_environment = demo_resource_id(
            environment_id, "managedEnvironments")
        if environment_subscription != subscription:
            raise SetupError("Demo environment is not bound to the selected app in ama.")
        environment = cli.rest(ARM + environment_id + f"?api-version={API_VERSION}")
        if (not isinstance(environment, dict)
                or not isinstance(environment.get("id"), str)
                or demo_resource_id(environment["id"], "managedEnvironments")[1]
                != normalized_environment):
            raise SetupError("Demo environment readback does not match the selected app binding.")
        resources.append(environment)
    profiles, environments = [], []
    for resource in resources:
        tags = resource.get("tags", {})
        if not isinstance(tags, dict):
            raise SetupError("Demo resource tags are unknown or malformed; no roster generated.")
        if PROFILE_TAG in tags:
            profiles.append(tags[PROFILE_TAG])
        if "environment" in tags:
            environments.append(tags["environment"])
    ids = {app_id}
    if isinstance(environment_id, str):
        ids.add(environment_id.lower())
    deployments = cli.call(["deployment", "group", "list", "-g", "ama"])
    if not isinstance(deployments, list):
        raise SetupError("Demo deployment history is unknown or malformed; no roster generated.")
    for deployment in deployments:
        if not isinstance(deployment, dict):
            raise SetupError(
                "Demo deployment history is unknown or malformed; no roster generated.")
        deployed = deployment.get("properties")
        if deployed is None:
            continue
        if not isinstance(deployed, dict):
            raise SetupError(
                "Demo deployment history is unknown or malformed; no roster generated.")
        outputs = deployed.get("outputResources")
        if outputs is None:
            outputs = []
        if (not isinstance(outputs, list) or any(
                not isinstance(r, dict) or not isinstance(r.get("id"), str) for r in outputs)):
            raise SetupError("Demo deployment resource binding is malformed; no roster generated.")
        if not any(r["id"].lower() in ids for r in outputs):
            continue
        if deployed.get("provisioningState") != "Succeeded":
            raise SetupError(
                "Demo profile evidence is not a successful deployment; no roster generated.")
        parameters = demo_deployment_parameters(cli, deployment)
        parameter_tags = parameters.get("tags", {})
        if PROFILE_TAG in parameter_tags:
            profiles.append(parameter_tags[PROFILE_TAG])
        if "deploymentProfile" in parameters:
            profiles.append(parameters["deploymentProfile"])
        if "environmentName" in parameters:
            environments.append(parameters["environmentName"])
        if "environment" in parameter_tags:
            environments.append(parameter_tags["environment"])
    if (not profiles or any(p != "development" for p in profiles) or not environments
            or any(e not in ("dev", "test", "demo") for e in environments)):
        raise SetupError(
            "Automatic demo roster refused: a development profile and demo/test/dev environment "
            "must be verified for this app/environment. Production, unknown or conflicting "
            "profile evidence is not allowed; direct ingress or a test name is not proof.")


def candidate_staff(cli: Azure, args: argparse.Namespace,
                    app: dict[str, Any]) -> list[dict[str, str]]:
    command = staff_command(args, app) + ["--list-candidates"]
    environment = {**cli.environment(), "ZF_SETUP_EXPECTED_APP": app["id"]}
    if cli.subscription:
        environment["ZF_SETUP_SUBSCRIPTION"] = cli.subscription
    if args.run_in_azure:
        result = subprocess.CompletedProcess(command, 1, "", "")
    else:
        try:
            result = subprocess.run(command, env=environment, capture_output=True, text=True,
                                    timeout=120, check=False)
        except (OSError, subprocess.TimeoutExpired):
            result = subprocess.CompletedProcess(command, 1, "", "")
    if result.returncode and not args.dry_run:
        try:
            failure = json.loads(result.stdout) if result.stdout.strip() else {}
            if isinstance(failure, dict) and failure.get("error") == "validation":
                raise SetupError("SQL candidate validation failed; Azure fallback was not attempted.")
            value = azure_staff(args, app, "candidates", cli)
            args.run_in_azure = True
            result = subprocess.CompletedProcess(command, 0, json.dumps(value["candidates"]), "")
        except (staff_azure.StaffJobError, AzureError) as error:
            print("Azure staff candidate lookup: blocked. " + str(error))
    if result.returncode:
        handoff = ["python3", "infra/scripts/setup-entra.py", "--container-app", app["name"],
                   "--tenant-profile", str(args.tenant_profile), "--roster", str(args.roster)]
        for flag, enabled in (("--direct-ingress", args.direct_ingress), ("--check", args.check),
                              ("--dry-run", args.dry_run), ("--list-staff", args.list_staff)):
            if enabled:
                handoff.append(flag)
        if args.seed is not None:
            handoff += ["--seed", str(args.seed)]
        print("Private SQL candidate lookup is blocked. No codes were invented or roster written; "
              "SQL binding and replica restart: NOT done.")
        print("On an authorized private-connected host with the same isolated profile, run:")
        print(shlex.join(handoff))
        raise SetupError(
            "Private SQL candidates unavailable. SQL public access must stay Disabled.")
    definitions = json.loads(MANIFEST.read_text())["appRoles"]
    role_keys = {r["key"] for r in definitions}
    aliases = {r["label"]: r["key"] for r in definitions}
    try:
        data = roster_rows(json.loads(result.stdout))
        rows: list[dict[str, str]] = []
        codes: set[str] = set()
        for row in data:
            code, role = row.get("code"), row.get("role")
            role = aliases.get(role, role)
            if (not isinstance(code, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", code)
                    or any(word in code.upper() for word in ("PLACEHOLDER", "REPLACE_", "YOUR_"))
                    or code in codes or not isinstance(role, str) or role not in role_keys
                    or type(row.get("bound")) is not bool):
                raise ValueError
            codes.add(code)
            candidate = {"code": code, "role": role}
            if role == "Contractor":
                supplier = row.get("contractor")
                if (not isinstance(supplier, str) or not supplier.strip()
                        or any(word in supplier.upper()
                               for word in ("PLACEHOLDER", "REPLACE_", "<", "YOUR_"))):
                    raise ValueError
                candidate["contractor"] = supplier
            if row["bound"] and not args.list_staff:
                raise SetupError(
                    "SQL already contains immutable staff bindings. Restore the existing "
                    "private roster; random regeneration is unsafe. No Entra changes made.")
            rows.append(candidate)
        return sorted(rows, key=lambda r: r["code"])
    except (ValueError, TypeError):
        raise SetupError("SQL candidate response is invalid; no roster generated.") from None


def eligible_people(graph: Azure) -> list[dict[str, str]]:
    people = []
    seen: set[str] = set()
    emails: set[str] = set()
    path = "users?$select=id,displayName,userPrincipalName,accountEnabled,userType"
    for user in graph.pages(path):
        try:
            identity = person(user)
        except (ValueError, KeyError, TypeError):
            continue
        if not individual_mailbox(graph, identity["oid"]):
            continue
        if identity["oid"] in seen or identity["email"] in emails:
            raise SetupError("Graph returned duplicate candidate people; no roster generated.")
        seen.add(identity["oid"])
        emails.add(identity["email"])
        people.append(identity)
    return sorted(people, key=lambda p: p["oid"])


def individual_mailbox(graph: Azure, principal: str) -> bool:
    try:
        purpose = graph.rest(GRAPH + f"users/{principal}/mailboxSettings/userPurpose")
    except AzureError as error:
        if error.kind in ("not-found", "request"):
            return False  # no mailbox (for example unlicensed): not an individual staff candidate
        raise SetupError(
            "Cannot verify mailbox eligibility. An authorized provisioning profile needs "
            "MailboxSettings.Read access to candidate user purposes; no permissions were "
            "granted. Unknown mailbox types cannot be assigned automatically.") from None
    return purpose.get("value") == "user"


def generate_roster(graph: Azure, args: argparse.Namespace,
                    candidates: list[dict[str, str]],
                    *, readonly: bool, expected: bytes | None) -> list[dict[str, str]]:
    print(EXERCISE_NOTICE)
    candidates = sorted(candidates, key=lambda r: r["code"])
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**63)
    print(f"Assignment seed: {seed}; reuse with --seed {seed}.")
    managers = [c for c in candidates if c["role"] == "ProgrammeManager"]
    if not managers:
        raise SetupError(
            "SQL has no ProgrammeManager position for the administrator; no codes invented.")
    people = eligible_people(graph)
    admins = [p for p in people if p["email"].startswith("admin@")]
    upn = args.admin_upn
    if upn is None and len(admins) == 1:
        admin = admins[0]
    else:
        if upn is None:
            print(f"Found {len(admins)} eligible tenant members whose UPN starts with admin@.")
            if readonly or not sys.stdin.isatty():
                raise SetupError(
                    "Supply --admin-upn for the intended enabled member administrator; "
                    "no roster written.")
            upn = input("Which tenant administrator UPN should this demo use? ").strip()
        selected = [p for p in people if p["email"] == upn.strip().lower()]
        if len(selected) != 1:
            raise SetupError(
                "Administrator input did not match one eligible member; no roster written.")
        admin = selected[0]
    remaining = [p for p in people if p["oid"] != admin["oid"]]
    missing = len(candidates) - 1 - len(remaining)
    if missing > 0:
        raise SetupError(f"Need {len(candidates) - 1} distinct non-admin users; "
                         f"{len(remaining)} eligible. Missing exactly {missing} user(s). "
                         "Stopped: initializer requires a distinct person per code; "
                         "no roster written.")
    random.Random(seed).shuffle(remaining)
    admin_code = managers[0]["code"]
    rows = []
    for candidate in candidates:
        identity = admin if candidate["code"] == admin_code else remaining.pop()
        rows.append({**candidate, "userId": identity["oid"]})
    print(f"Roster plan: {len(rows)} staff codes, {len(rows)} distinct people "
          f"from {len(people)} eligible members.")
    if args.run_in_azure:
        print("Administrator: ProgrammeManager position selected; staff codes remain private.")
    else:
        print("Administrator: Retrofit Programme Manager (ProgrammeManager), "
              f"code {admin_code}.")
        print("Codes covered: " + ", ".join(r["code"] for r in rows))
    for role in sorted({r["role"] for r in rows}):
        print(f"  {role}: {sum(r['role'] == role for r in rows)}")
    if readonly:
        print("Read-only roster preview; no private files, Entra assignments "
              "or SQL bindings written.")
        return []
    if not args.yes and (not sys.stdin.isatty()
                         or input("Write this private demo roster? [y/N] ").strip().lower() != "y"):
        raise SetupError(
            "Roster not written; review the plan and rerun with --yes to accept.")
    parent = private_path(args.roster.parent, directory=True, create=True)
    current, replaceable = roster_input(args.roster)
    if current != expected or not replaceable:
        raise SetupError("Roster changed while planning; rerun without overwriting it.")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", dir=parent, prefix=".roster-", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump({"version": 1, "seed": seed, "staff": rows}, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, args.roster)
    except OSError:
        raise SetupError(
            "Private roster could not be saved; no Entra or SQL changes made.") from None
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
    print("Private roster saved; subsequent runs reuse it without reshuffling.")
    roles = {r["key"] for r in json.loads(MANIFEST.read_text())["appRoles"]}
    return read_roster(args.roster, roles)


def app_url(app: dict[str, Any]) -> str:
    return ARM + app["id"] + f"?api-version={API_VERSION}"


def coordination_status(cli: Azure, app: dict[str, Any]) -> None:
    if app.get("tags", {}).get(LOCK_TAG):
        raise SetupError("Another authentication session holds the app advisory lock. "
                         "Wait; if interrupted, an authorized operator must verify it stopped "
                         "before removing only the zava-forward-auth-lock tag.")
    properties = app.get("properties", {})
    if properties.get("provisioningState") != "Succeeded":
        raise SetupError("API provisioning/revision update is in progress or failed; wait for Succeeded.")
    environment_id = properties.get("environmentId") or properties.get("managedEnvironmentId")
    if environment_id:
        environment = cli.rest(ARM + environment_id + f"?api-version={API_VERSION}")
        state = environment.get("properties", {}).get("provisioningState")
        if state and state != "Succeeded":
            raise SetupError("Container Apps environment provisioning is in progress or failed; wait.")
    revisions = cli.call(["containerapp", "revision", "list", "-g", "ama", "-n", app["name"]])
    if any(r.get("properties", {}).get("provisioningState") in ("Provisioning", "Updating")
           or r.get("properties", {}).get("runningState") in ("Processing", "Activating")
           for r in revisions):
        raise SetupError("An API revision update is in progress; wait before changing authentication.")
    deployments = cli.call(["deployment", "group", "list", "-g", "ama"])
    if any((d.get("properties") or {}).get("provisioningState") in
           ("Accepted", "Running", "Creating", "Updating") for d in deployments):
        raise SetupError("A resource-group deployment is running; authentication setup must wait.")


@contextmanager
def authentication_lock(cli: Azure, app: dict[str, Any], readonly: bool) -> Iterator[None]:
    current = cli.rest(app_url(app))
    coordination_status(cli, current)
    if readonly:
        yield
        return
    etag = current.get("etag")
    if not isinstance(etag, str):
        etag = None
    token = uuid.uuid4().hex
    tags = {**current.get("tags", {}), LOCK_TAG: token}
    cli.rest(app_url(app), method="PATCH", body={"tags": tags}, etag=etag)
    locked = cli.rest(app_url(app))
    if locked.get("tags", {}).get(LOCK_TAG) != token:
        raise SetupError("Another session acquired the authentication lock; no auth changes were made.")
    try:
        yield
    finally:
        latest = cli.rest(app_url(app))
        if latest.get("tags", {}).get(LOCK_TAG) == token:
            remaining = {k: v for k, v in latest.get("tags", {}).items() if k != LOCK_TAG}
            cli.rest(app_url(app), method="PATCH", body={"tags": remaining},
                     etag=latest.get("etag"))


def discover_credential_target(cli: Azure, app: dict[str, Any],
                               args: argparse.Namespace) -> tuple[str, str]:
    secrets = app.get("properties", {}).get("configuration", {}).get("secrets") or []
    attached = app.get("identity", {}).get("userAssignedIdentities") or {}
    references = [s for s in secrets if s.get("keyVaultUrl")]
    referenced_vaults = {urlsplit(s["keyVaultUrl"]).hostname.split(".")[0]
                         for s in references if urlsplit(s["keyVaultUrl"]).hostname}
    containers = app.get("properties", {}).get("template", {}).get("containers") or []
    configured_vaults = {urlsplit(e.get("value", "")).hostname.split(".")[0]
                         for c in containers for e in c.get("env", [])
                         if e.get("name") == "KEY_VAULT_URI"
                         and urlsplit(e.get("value", "")).hostname}
    vaults = cli.call(["keyvault", "list", "-g", args.resource_group])
    if args.vault:
        candidates = [v for v in vaults if v["name"] == args.vault]
    else:
        candidates = [v for v in vaults if v["name"] in referenced_vaults]
        if not candidates:
            candidates = [v for v in vaults if v["name"] in configured_vaults]
        if not candidates:
            tags = app.get("tags", {})
            candidates = [v for v in vaults if all(v.get("tags", {}).get(k) == tags[k]
                          for k in ("environment", "purpose", "owner") if k in tags)
                          and "environment" in tags]
        if not candidates:
            deployments = cli.call(["deployment", "group", "list", "-g", args.resource_group])
            names = {((d.get("properties") or {}).get("outputs") or {}).get(
                "keyVaultName", {}).get("value") for d in deployments}
            candidates = [v for v in vaults if v["name"] in names] or vaults
    vault = choose(candidates, args.vault, "Key Vault", r".*", "--vault",
                   interactive=not (args.yes or args.check or args.dry_run))["name"]
    refs = {s.get("identity") for s in references
            if urlsplit(s["keyVaultUrl"]).hostname == f"{vault}.vault.azure.net"
            and s.get("identity") in attached}
    if args.vault_identity:
        identity = args.vault_identity
    elif len(refs) == 1:
        identity = next(iter(refs))
    elif len(attached) == 1:
        identity = next(iter(attached))
    elif not attached and "SystemAssigned" in app.get("identity", {}).get("type", ""):
        identity = "system"
    else:
        identities = cli.call(["identity", "list", "-g", args.resource_group])
        tagged = {r["id"] for r in identities if r.get("id") in attached
                  and (r.get("tags", {}).get("zava-forward-role") == "api"
                       or r.get("name", "").endswith("-api"))}
        if len(tagged) != 1:
            deployments = cli.call(["deployment", "group", "list", "-g", args.resource_group])
            principal_ids = {((d.get("properties") or {}).get("outputs") or {}).get(
                "identityPrincipalIds", {}).get("value", {}).get("api") for d in deployments}
            tagged = {key for key, value in attached.items()
                      if value.get("principalId") and value["principalId"] in principal_ids}
        rows = [{"name": key.rsplit("/", 1)[-1], "resource": key} for key in tagged or attached]
        selected = choose(rows, None, "attached API identity", r".*", "--vault-identity",
                          interactive=not (args.yes or args.check or args.dry_run))
        identity = selected["resource"]
    if identity != "system" and identity not in attached:
        raise SetupError("Key Vault identity must already be attached to the selected API.")
    if identity == "system" and "SystemAssigned" not in app.get("identity", {}).get("type", ""):
        raise SetupError("The API has no attached system-assigned identity; use its existing API identity.")
    return vault, identity


def staff_command(args: argparse.Namespace, app: dict[str, Any], *, apply: bool = False) -> list[str]:
    command = [sys.executable, str(Path(__file__).with_name("initialize-workbench-staff.py")),
               "--resource-group", "ama", "--container-app", app["name"],
               "--roster", str(args.roster.expanduser()), "--tenant-profile", str(args.tenant_profile),
               "--apply" if apply else "--check"]
    return [*command, "--restart"] if apply else command


def azure_staff(args: argparse.Namespace, app: dict[str, Any], operation: str,
                cli: Azure) -> dict[str, Any]:
    if args.check or args.dry_run or args.list_staff:
        mode = "--check" if args.check else "--dry-run" if args.dry_run else "--list-staff"
        raise staff_azure.StaffJobError(
            f"{mode} never creates Azure jobs or secrets. Run the same read-only command "
            "without --run-in-azure on an authorized private-connected host; "
            "SQL binding/restart remains unverified.")
    payload: dict[str, Any] = {}
    if operation != "candidates":
        roles = {r["key"] for r in json.loads(MANIFEST.read_text())["appRoles"]}
        roster = read_roster(args.roster, roles)
        wanted = roster_rows(json.loads(args.roster.read_text()))
        if any(row["kind"] != "users" for row in roster):
            raise SetupError("Azure SQL staff binding requires individual people.")
        graph = Azure(args.tenant_profile, extension_directory=cli.extension_directory)
        payload = {
            "wanted": wanted,
            "people": {row["id"]: graph.rest(
                GRAPH + f"users/{row['id']}?$select=id,displayName,userPrincipalName,accountEnabled,userType")
                for row in roster},
        }
        for uid, principal in payload["people"].items():
            if person(principal)["oid"] != uid:
                raise SetupError("Graph returned a different roster person; SQL was not changed.")
    transport = Azure(cli.profile, body_directory=private_path(args.tenant_profile, directory=True),
                      extension_directory=cli.extension_directory)
    transport.subscription = cli.subscription
    print("SQL in Azure: temporary ama job/secret; "
          + ("read-only SQL." if operation != "apply" else "bind, verify and restart."))
    value = staff_azure.execute(transport, app, operation, payload, source_name=args.azure_init_job)
    if operation != "candidates" and value.get("positions") != len(payload["wanted"]):
        raise staff_azure.StaffJobError("Azure staff result does not cover the requested roster.")
    return value


def sql_staff_step(args: argparse.Namespace, app: dict[str, Any], *, readonly: bool,
                   cli: Azure | None = None) -> bool:
    cli = cli or Azure(Path(os.environ.get("AZURE_CONFIG_DIR", str(Path.home() / ".azure"))),
                       body_directory=args.tenant_profile,
                       extension_directory=args.tenant_profile / "cliextensions")
    environment = {**cli.environment(), "ZF_SETUP_EXPECTED_APP": app["id"]}
    if cli.subscription:
        environment["ZF_SETUP_SUBSCRIPTION"] = cli.subscription

    def run(apply: bool) -> tuple[int, dict[str, Any]]:
        def remote() -> tuple[int, dict[str, Any]]:
            try:
                value = azure_staff(args, app, "apply" if apply else "check", cli)
            except (staff_azure.StaffJobError, AzureError) as error:
                print("Azure SQL staff step blocked: " + str(error))
                return 1, {}
            if not all(type(value.get(k)) is int and value[k] >= 0
                       for k in ("staff_changes", "owner_labels", "positions")):
                raise SetupError("Azure staff result has invalid counts; SQL/restart is unverified.")
            if type(value.get("restart_required")) is not bool or type(value.get("sql_verified")) is not bool:
                raise SetupError("Azure staff result has invalid verification status.")
            return (0 if value["sql_verified"] else 2), value

        if args.run_in_azure:
            code, value = remote()
            if code in (0, 2):
                return code, value
            result = subprocess.CompletedProcess([], 1, "", "")
        else:
            try:
                result = subprocess.run(staff_command(args, app, apply=apply),
                                        env=environment, capture_output=True, text=True,
                                        timeout=600, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess([], 1, "", "")
        if result.returncode not in (0, 2):
            try:
                failure = json.loads(result.stdout) if result.stdout.strip() else {}
            except ValueError:
                failure = {}
            if isinstance(failure, dict) and failure.get("error") == "validation":
                print("SQL preflight rejected the private roster or deployed auth/SQL controls. "
                      "Review existing staff codes, approved roles, complete coverage and immutable "
                      "bindings with --list-staff; SQL binding/restart: NOT confirmed.")
                return result.returncode, {}
            if not apply and not args.run_in_azure and not args.dry_run:
                args.run_in_azure = True
                code, value = remote()
                if code in (0, 2):
                    return code, value
            print("SQL binding: blocked (private SQL connectivity, installed drivers/packages or "
                  "initializer authority unavailable); SQL binding/restart: NOT confirmed.")
            print("From an authorized host with private SQL connectivity and the same private roster, run:")
            command = ["python3", "infra/scripts/initialize-workbench-staff.py",
                       *staff_command(args, app, apply=True)[2:]]
            print(shlex.join(command))
            print("Install first: python3 -m pip install -e src/core -e src/agents -e src/api pyodbc; "
                  "install Microsoft ODBC Driver 18 for SQL Server. SQL public access must stay Disabled.")
            return result.returncode, {}
        try:
            value = json.loads(result.stdout)
        except ValueError:
            raise SetupError("SQL initializer returned an invalid summary; binding/restart are unverified.") from None
        if not isinstance(value, dict) or not all(isinstance(value.get(k), int)
                                                  for k in ("staff_changes", "owner_labels")):
            raise SetupError("SQL initializer summary is incomplete; binding/restart are unverified.")
        return result.returncode, value

    code, summary = run(False)
    if code not in (0, 2):
        return False
    print(f"SQL plan: {summary['staff_changes']} staff binding(s), "
          f"{summary['owner_labels']} owner label(s); checking serving-replica restart evidence.")
    marker = hashlib.sha256(args.roster.read_bytes() + str(
        app.get("properties", {}).get("latestReadyRevisionName", "")).encode()).hexdigest()
    if code == 0 and app.get("tags", {}).get("zava-forward-staff-state") == marker:
        print("SQL binding: current; replica restart: previously verified for this roster/revision.")
        return True
    if readonly:
        print("SQL binding/restart: read-only, no changes or restart performed.")
        return code == 0 and summary.get("restart_required") is False
    if not args.yes and (
        not sys.stdin.isatty()
        or input("Apply these SQL bindings and restart the API replicas? [y/N] ").lower() != "y"
    ):
        print("SQL binding and replica restart: NOT done. Rerun with --yes after reviewing the plan.")
        return False
    code, summary = run(True)
    done = code == 0 and summary.get("restart_required") is False
    if done:
        latest = cli.rest(app_url(app))
        cli.rest(app_url(app), method="PATCH", body={
            "tags": {**latest.get("tags", {}), "zava-forward-staff-state": marker}})
    print("SQL binding: " + ("done; replica restart: verified." if done else "incomplete; replica restart: NOT verified."))
    return done


def lookup_person(graph: Azure, args: argparse.Namespace, roles: set[str]) -> None:
    if args.check or args.dry_run:
        raise SetupError("--lookup-upn writes only private output; do not combine it with read-only modes.")
    definitions = json.loads(MANIFEST.read_text())["appRoles"]
    args.staff_role = next((r["key"] for r in definitions if r["label"] == args.staff_role),
                           args.staff_role)
    if (args.staff_role not in roles or not args.staff_code
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", args.staff_code)):
        raise SetupError("Supply an existing --staff-code and its approved --staff-role; use --list-staff.")
    user = graph.rest(GRAPH + "users/" + quote(args.lookup_upn, safe="") +
                      "?$select=id,accountEnabled,userType")
    if user.get("accountEnabled") is not True or user.get("userType") != "Member":
        raise SetupError("UPN did not identify an enabled member person; no private output was written.")
    row = {"code": args.staff_code, "role": args.staff_role, "userId": object_id(user["id"])}
    parent = private_path(args.roster.parent, directory=True, create=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=parent, prefix="person-", suffix=".json",
                                     delete=False) as stream:
        json.dump([row], stream, indent=2)
    print("Person mapping saved privately at " + stream.name +
          ". Review the code/role against --list-staff, then merge into roster.json; IDs were not printed.")


def collection_filter(expression: str) -> str:
    return "?" + urlencode({"$filter": expression})


def registration(graph: Azure, client: Any, name: str) -> dict[str, Any] | None:
    if identifier(client):
        try:
            value = graph.rest(GRAPH + f"applications(appId='{object_id(client)}')")
            if object_id(value.get("appId")) != object_id(client):
                raise SetupError("Graph returned a different application; refusing to change it.")
            return value
        except AzureError as error:
            if error.kind != "not-found":
                raise
            raise SetupError("Configured client is not an application in this tenant; review it before selecting another.") from None
    # The managed-identity sentinel is deliberately not interpreted as an app UUID.
    escaped = name.replace("'", "''")
    rows = graph.pages("applications" + collection_filter(f"displayName eq '{escaped}'"))
    tagged = [] if rows else [
        r for r in graph.pages("applications?$select=id,appId,displayName,tags")
        if "zava-forward-role=api" in r.get("tags", [])]
    candidates = {object_id(r["id"]): r for r in rows or tagged}
    if len(candidates) > 1:
        names = ", ".join(label(r.get("displayName", "unnamed")) for r in candidates.values())
        raise SetupError(f"Multiple Entra registration candidates: {names}. Select one with --registration-name or --client-id.")
    selected = next(iter(candidates.values()), None)
    return graph.rest(GRAPH + f"applications/{object_id(selected['id'])}") if selected else None


def desired_registration(current: dict[str, Any], urls: list[str], manifest: dict[str, Any],
                         account_photo: bool) -> dict[str, Any]:
    if current.get("signInAudience") != "AzureADMyOrg":
        raise SetupError("Registration is not single-tenant; review ownership/audience before changing it.")
    roles = list(current.get("appRoles", []))
    for spec in [*manifest["appRoles"], *manifest["capabilityRoles"]]:
        value = f"ZavaForward.{spec['key']}"
        existing = [r for r in roles if r.get("value") == value]
        if existing:
            if (len(existing) != 1 or existing[0].get("isEnabled") is not True
                    or "User" not in existing[0].get("allowedMemberTypes", [])):
                raise SetupError("An existing workbench role is disabled/incompatible; review App roles in Entra.")
        else:
            roles.append({"id": str(uuid.uuid5(ROLE_NAMESPACE, spec["key"])),
                          "value": value, "displayName": spec["label"],
                          "description": f"Zava Forward workbench: {spec['label']}",
                          "isEnabled": True, "allowedMemberTypes": ["User"]})
    web = dict(current.get("web") or {})
    web["redirectUris"] = list(dict.fromkeys([
        *web.get("redirectUris", []), *(u + manifest["callbackPath"] for u in urls)]))
    web["implicitGrantSettings"] = {**web.get("implicitGrantSettings", {}), "enableIdTokenIssuance": True}
    desired = {"appRoles": roles, "web": web,
               "identifierUris": list(dict.fromkeys([*current.get("identifierUris", []), f"api://{object_id(current['appId'])}"])),
               "api": {**(current.get("api") or {}), "requestedAccessTokenVersion": 2}}
    if account_photo:
        resources = json.loads(json.dumps(current.get("requiredResourceAccess", [])))
        graph_resource = next((r for r in resources if r["resourceAppId"] == GRAPH_APP), None)
        if graph_resource is None:
            graph_resource = {"resourceAppId": GRAPH_APP, "resourceAccess": []}
            resources.append(graph_resource)
        scope = {"id": USER_READ, "type": "Scope"}
        if scope not in graph_resource["resourceAccess"]:
            graph_resource["resourceAccess"].append(scope)
        desired["requiredResourceAccess"] = resources
    return {key: value for key, value in desired.items() if current.get(key) != value}


def wait_for(read: Any, ready: Any, message: str, seconds: int = 30) -> Any:
    for attempt in range(max(1, seconds // 2 + 1)):
        value = read()
        if ready(value):
            return value
        if attempt < seconds // 2:
            time.sleep(2)
    raise SetupError(message)


def service_principal(graph: Azure, client: str) -> dict[str, Any] | None:
    rows = graph.pages("servicePrincipals" + collection_filter(f"appId eq '{client}'"))
    if len(rows) > 1:
        raise SetupError("Multiple enterprise applications match this registration; review Entra.")
    if rows and object_id(rows[0].get("appId")) != client:
        raise SetupError("Graph returned a different enterprise application; refusing to change it.")
    return rows[0] if rows else None


def resolve_roster(
    graph: Azure, roster: list[dict[str, str]], *, verify_people: bool = False,
) -> list[tuple[dict[str, str], set[str]]]:
    resolved = []
    for row in roster:
        select = "id,accountEnabled,userType" if row["kind"] == "users" else "id,securityEnabled"
        if verify_people and row["kind"] == "users":
            select += ",displayName,userPrincipalName"
        principal = graph.rest(GRAPH + f"{row['kind']}/{row['id']}?$select={select}")
        if object_id(principal.get("id")) != row["id"]:
            raise SetupError("Graph returned a different roster principal.")
        groups: set[str] = set()
        if row["kind"] == "users":
            if principal.get("accountEnabled") is not True or principal.get("userType") != "Member":
                raise SetupError("Roster users must be enabled tenant members; guests need separate human approval.")
            if verify_people:
                try:
                    person(principal)
                except (ValueError, KeyError, TypeError):
                    raise SetupError(
                        "A persisted demo roster user is no longer an eligible person.") from None
                if not individual_mailbox(graph, row["id"]):
                    raise SetupError("A demo roster user does not have an individual-user mailbox; "
                                     "no automatic assignments are safe.")
            groups = {object_id(g["id"]) for g in graph.pages(
                f"users/{row['id']}/memberOf/microsoft.graph.group?$select=id")}
        elif principal.get("securityEnabled") is not True:
            raise SetupError("Roster groups must be security-enabled groups.")
        resolved.append((row, groups | {row["id"]}))
    for row, principals in resolved:
        if any(other["id"] in principals and other["role"] != row["role"]
               for other, _ in resolved):
            raise SetupError("Planned group and user assignments conflict; correct the private roster before retrying.")
    return resolved


def assign_roster(graph: Azure, sp: dict[str, Any], resolved: list[tuple[dict[str, str], set[str]]],
                  readonly: bool) -> int:
    resource = object_id(sp["id"])
    path = f"servicePrincipals/{resource}/appRoleAssignedTo"
    assignments = graph.pages(path)
    roles = {r["value"]: r for r in sp.get("appRoles", []) if r.get("isEnabled") is True
             and "User" in r.get("allowedMemberTypes", [])}
    manifest = json.loads(MANIFEST.read_text())
    supplemental = {
        object_id(roles[value]["id"])
        for spec in manifest["capabilityRoles"]
        if (value := "ZavaForward." + spec["key"]) in roles
    }
    pending = []
    unresolved = 0
    for row, principals in resolved:
        wanted = roles.get("ZavaForward." + row["role"])
        if not wanted:
            if readonly:
                unresolved += 1
                continue
            raise SetupError("Enterprise-app role has not propagated or is incompatible; rerun shortly.")
        rid = object_id(wanted["id"])
        actual = {a["appRoleId"] for a in assignments if a.get("principalId") in principals
                  and a.get("appRoleId") != "00000000-0000-0000-0000-000000000000"}
        if actual - {rid} - supplemental:
            raise SetupError("A roster principal has conflicting effective app roles; review Users and groups in Entra.")
        if rid not in actual:
            pending.append({"principalId": row["id"], "resourceId": resource, "appRoleId": rid})
    if pending and not readonly:
        permissions = token_permissions(graph)
        if not permissions.intersection(ASSIGNMENT_WRITE):
            authority_help()
            raise SetupError("Roster assignment-write permission is missing; no assignments were added.")
        for body in pending:
            graph.rest(GRAPH + path, method="POST", body=body)
        wait_for(lambda: graph.pages(path),
                 lambda rows: all(any(all(a.get(k) == v for k, v in b.items()) for a in rows) for b in pending),
                 "New app-role assignments are not yet verified; rerun before relying on them.")
    return len(pending) + unresolved


def secret_inventory(rows: Any) -> dict[str, dict[str, Any]]:
    message = "Cannot preserve existing app secrets; inventory is incomplete or malformed."
    if not isinstance(rows, list):
        raise SetupError(message)
    inventory: dict[str, dict[str, Any]] = {}
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get("name"), str)
                or not row["name"] or row["name"] in inventory):
            raise SetupError(message)
        inventory[row["name"]] = row
    return inventory


def preserve_app_secrets(configured: Any, response: Any) -> list[dict[str, Any]]:
    known = secret_inventory(configured)
    listed = secret_inventory(response.get("value") if isinstance(response, dict) else None)
    preserved = []
    for name in dict.fromkeys([*known, *listed]):
        reference: dict[str, Any] = {"name": name}
        for field in ("keyVaultUrl", "identity"):
            current, returned = known.get(name, {}).get(field), listed.get(name, {}).get(field)
            if current is not None and returned is not None and current != returned:
                raise SetupError("Cannot preserve existing app secrets; reference metadata conflicts. No new credential was created.")
            value = current if current is not None else returned
            if value is not None:
                reference[field] = value
        if len(reference) > 1:
            if not all(isinstance(reference.get(k), str) and reference[k] for k in ("keyVaultUrl", "identity")):
                raise SetupError("Cannot preserve existing app secrets; Key Vault reference is incomplete. No new credential was created.")
        else:
            value = listed.get(name, {}).get("value")
            if not isinstance(value, str):
                raise SetupError("Cannot preserve existing app secrets; an app value is unavailable. No new credential was created.")
            reference["value"] = value
        preserved.append(reference)
    return preserved


def secret_reference_digest(rows: Any) -> str:
    inventory = secret_inventory(rows)
    references = [{k: inventory[name][k] for k in ("name", "keyVaultUrl", "identity")
                   if inventory[name].get(k) is not None} for name in sorted(inventory)]
    return hashlib.sha256(json.dumps(references, sort_keys=True).encode()).hexdigest()


def verify_secret_handoff(cli: Azure, app: dict[str, Any], readonly: bool) -> None:
    expected = app.get("tags", {}).get(HANDOFF_TAG)
    if expected is None:
        return
    message = ("App secret preservation is not confirmed; auth was not switched. "
               "Restore the expected secret references with an authorized operator before retrying; "
               "do not remove the handoff tag to bypass verification.")
    verified = wait_for(
        lambda: cli.rest(app_url(app)),
        lambda actual: secret_reference_digest(actual["properties"]["configuration"].get("secrets") or []) == expected,
        message)
    if not readonly:
        tags = dict(verified.get("tags", {}))
        tags.pop(HANDOFF_TAG, None)
        cli.rest(app_url(app), method="PATCH", body={"tags": tags})


def azure_credential_guard(app: dict[str, Any], auth: dict[str, Any],
                           args: argparse.Namespace, selected: dict[str, Any] | None = None) -> None:
    if not args.run_in_azure or args.bearer_only:
        return
    tagged_store = app.get("tags", {}).get(STORE_TAG)
    recorded_name = app.get("tags", {}).get("zava-forward-credential-name")
    secrets = app.get("properties", {}).get("configuration", {}).get("secrets") or []
    current_name = aad_registration(auth).get("clientSecretSettingName")
    if (args.secret_store == "app" or tagged_store == "app"
            or (selected is not None and not selected.get("keyVaultUrl"))
            or any(s.get("name") in (recorded_name, current_name) and not s.get("keyVaultUrl")
                   for s in secrets)):
        raise SetupError(
            "Azure setup requires Key Vault storage. Existing/selected app-backed "
            "credentials need a separately approved migration; no credential conversion made.")
    args.secret_store = "keyvault"


def secret_reference(cli: Azure, graph: Azure, app: dict[str, Any], registration: dict[str, Any],
                     auth: dict[str, Any], args: argparse.Namespace, readonly: bool, *,
                     reuse_only: bool = False) -> tuple[str | None, bool]:
    if reuse_only and not readonly:
        raise SetupError("Credential reuse preflight must be read-only.")
    azure_credential_guard(app, auth, args)
    client = object_id(registration["appId"])
    current = aad_registration(auth)
    secret_name = "entra-" + client.replace("-", "")
    secrets = app["properties"]["configuration"].get("secrets") or []
    existing_ref = current.get("clientSecretSettingName")
    verify_secret_handoff(cli, app, readonly)
    if args.bearer_only:
        return None, False
    now = datetime.now(timezone.utc)
    valid = [c for c in registration.get("passwordCredentials", [])
             if c.get("endDateTime") and
             datetime.fromisoformat(c["endDateTime"].replace("Z", "+00:00")) > now]
    matching = [s for s in secrets if any(c.get("displayName") == s["name"] for c in valid)
                and s["name"].startswith(secret_name)]
    if matching:
        selected = next((s for s in matching if s["name"] == existing_ref), matching[-1])
        azure_credential_guard(app, auth, args, selected)
        return selected["name"], record_credential_store(cli, app, selected, readonly)
    if (identifier(current.get("clientId")) == client and existing_ref
            and not existing_ref.startswith(secret_name)
            and any(c.get("displayName") == existing_ref for c in valid)
            and any(s["name"] == existing_ref for s in secrets)):
        selected = next(s for s in secrets if s["name"] == existing_ref)
        azure_credential_guard(app, auth, args, selected)
        return existing_ref, record_credential_store(cli, app, selected, readonly)
    if reuse_only:
        return None, False
    action = (auth.get("globalValidation") or {}).get("unauthenticatedClientAction")
    if action == "Return401" and not args.create_secret and not args.enable_browser:
        return None, False
    if not args.create_secret:
        return None, True
    recorded_store = app.get("tags", {}).get(STORE_TAG)
    if recorded_store not in (None, "keyvault", "app"):
        raise SetupError("Recorded credential store is invalid; review the app store tag before retrying.")
    store = args.secret_store or recorded_store or "keyvault"
    vault = None
    if store == "keyvault":
        try:
            vault, identity = discover_credential_target(cli, app, args)
        except SetupError as error:
            if not readonly:
                raise
            print("Browser credential missing/expired; storage discovery blocked: " + str(error))
            return secret_name, True
        print("Checking selected Key Vault using secret metadata only; no secret values are read.")
        try:
            if args.run_in_azure:
                credential_arm.preflight(cli, app, vault)
            else:
                cli.call(["keyvault", "secret", "list", "--vault-name", vault, "--maxresults", "1"])
        except AzureError as error:
            if not args.run_in_azure and args.direct_ingress and args.secret_store is None and error.kind in (
                    "permission", "request", "transient", "network"):
                action = "would use" if readonly else "using"
                print(f"Private Key Vault unavailable here; {action} the Container App secret store for this demo; vault networking stays private.")
                vault, store = None, "app"
            elif readonly:
                print("Browser credential missing/expired; private Key Vault access is blocked here. "
                      "Run setup from the approved private network; no changes made.")
                return secret_name, True
            else:
                raise SetupError("Private Key Vault preflight failed; run from the approved network "
                                 "with secret permissions. Vault networking was not changed.") from None
    if readonly:
        print("Browser credential missing/expired; would create it in " +
              ("Key Vault with the attached API identity." if vault else "the Container App secret store."))
        return secret_name, True
    app_url = ARM + app["id"] + f"?api-version={API_VERSION}"
    existing = cli.rest(ARM + app["id"] + f"/listSecrets?api-version={API_VERSION}", method="POST")
    preserved = preserve_app_secrets(secrets, existing)
    # A unique handoff name lets an interrupted run reuse only a matched credential
    # and storage pair, never an orphan's unrecoverable value.
    secret_name += "-" + uuid.uuid4().hex[:12]
    expiration = (datetime.now(timezone.utc) + timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%SZ")
    password = graph.rest(GRAPH + f"applications/{object_id(registration['id'])}/addPassword",
                          method="POST", body={"passwordCredential": {
                              "displayName": secret_name, "endDateTime": expiration}})
    if not isinstance(password, dict) or not isinstance(password.get("secretText"), str) or not password["secretText"]:
        raise SetupError("Credential creation returned no usable secret; inspect Certificates & secrets before retrying.")
    new_secret: dict[str, Any] = {"name": secret_name}
    if vault and args.run_in_azure:
        new_secret.update(
            keyVaultUrl=credential_arm.store(
                cli, app, vault, secret_name, password["secretText"], expiration),
            identity=identity)
    elif vault:
        filename = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=args.tenant_profile, delete=False) as stream:
                filename = stream.name
                stream.write(password["secretText"])
            try:
                result = cli.call(["keyvault", "secret", "set", "--vault-name", vault, "--name", secret_name,
                                   "--file", filename, "--expires", expiration])
                new_secret.update(keyVaultUrl=result["id"], identity=identity)
            except AzureError:
                if not args.direct_ingress or args.secret_store is not None:
                    raise
                print("Private Key Vault write unavailable; using the Container App secret store for this demo; vault networking stays private.")
                store = "app"
                new_secret["value"] = password["secretText"]
        finally:
            if filename:
                Path(filename).unlink(missing_ok=True)
    else:
        new_secret["value"] = password["secretText"]
    configuration = {**app["properties"]["configuration"], "secrets": [*preserved, new_secret]}
    expected = secret_reference_digest(configuration["secrets"])
    latest = cli.rest(app_url)
    cli.rest(app_url, method="PATCH", body={
        "tags": {**latest.get("tags", {}), STORE_TAG: store,
                 "zava-forward-credential-name": secret_name, HANDOFF_TAG: expected},
        "properties": {"configuration": configuration}})
    verify_secret_handoff(cli, {**app, "tags": {HANDOFF_TAG: expected}}, False)
    return secret_name, True


def aad_registration(auth: dict[str, Any]) -> dict[str, Any]:
    providers = auth.get("identityProviders") or {}
    provider = providers.get("azureActiveDirectory") or {}
    return provider.get("registration") or {}


def record_credential_store(cli: Azure, app: dict[str, Any], secret: dict[str, Any],
                            readonly: bool) -> bool:
    store = "keyvault" if secret.get("keyVaultUrl") else "app"
    wanted = {STORE_TAG: store, "zava-forward-credential-name": secret["name"]}
    changed = not all(app.get("tags", {}).get(k) == v for k, v in wanted.items())
    if readonly or not changed:
        return changed
    latest = cli.rest(app_url(app))
    cli.rest(app_url(app), method="PATCH", body={"tags": {**latest.get("tags", {}), **wanted}})
    return changed


def auth_patch(current: dict[str, Any], client: str, tenant: str, urls: list[str],
               secret: str | None, bearer: bool, *, direct: bool = False,
               enable_browser: bool = False) -> dict[str, Any]:
    desired = json.loads(json.dumps(current))
    desired["platform"] = {**(desired.get("platform") or {}), "enabled": True}
    http = dict(desired.get("httpSettings") or {})
    http["requireHttps"] = True
    if direct:
        http["forwardProxy"] = {"convention": "NoProxy"}
    elif ((any(".azurefd.net" in url for url in urls) or len(urls) > 1)
            and (http.get("forwardProxy") or {}).get("convention") != "Custom"):
        http["forwardProxy"] = {"convention": "Standard"}
    desired["httpSettings"] = http
    providers = dict(desired.get("identityProviders") or {})
    aad = dict(providers.get("azureActiveDirectory") or {})
    aad["enabled"] = True
    aad["registration"] = {**(aad.get("registration") or {}), "clientId": client,
                           "openIdIssuer": f"https://login.microsoftonline.com/{tenant}/v2.0"}
    if secret:
        aad["registration"]["clientSecretSettingName"] = secret
        aad["registration"].pop("clientSecretCertificateThumbprint", None)
    elif bearer:
        aad["registration"].pop("clientSecretSettingName", None)
    aad["validation"] = {**(aad.get("validation") or {}), "allowedAudiences": [client, f"api://{client}"]}
    providers["azureActiveDirectory"] = aad
    desired["identityProviders"] = providers
    validation = dict(desired.get("globalValidation") or {})
    if not current.get("globalValidation"):
        validation["excludedPaths"] = ["/healthz", "/readyz", "/", "/welcome.html", "/style.css", "/zava-logo.png", "/sign-in"]
    if (bearer or enable_browser
            or validation.get("unauthenticatedClientAction") in (None, "AllowAnonymous")):
        validation.update(unauthenticatedClientAction="Return401" if bearer else "RedirectToLoginPage",
                          redirectToProvider="azureactivedirectory")
    desired["globalValidation"] = validation
    return desired


def runtime_patch(app: dict[str, Any], client: str, tenant: str) -> dict[str, Any] | None:
    containers = json.loads(json.dumps(app["properties"]["template"].get("containers", [])))
    choices = [c for c in containers if c.get("name") == "api"]
    if not choices and len(containers) == 1:
        choices = containers
    if len(choices) != 1:
        raise SetupError("Cannot identify one API container for trusted-proxy settings; review the deployed template.")
    container = choices[0]
    env = container.get("env") or []
    wanted = {"ZF_AUTH": "trusted-proxy", "ZF_TRUSTED_PROXY": "1", "ZF_ENV": "production",
              "ZF_ENTRA_TENANT_ID": tenant, "ENTRA_TENANT_ID": tenant, "ENTRA_CLIENT_ID": client}
    revised = [row for row in env if row.get("name") not in wanted]
    revised.extend({"name": key, "value": value} for key, value in wanted.items())
    if all(any(row == {"name": key, "value": value} for row in env) for key, value in wanted.items()):
        return None
    container["env"] = revised
    return {"properties": {"template": {**app["properties"]["template"], "containers": containers}}}


@contextmanager
def run_lock(profile: Path, readonly: bool) -> Iterator[None]:
    if readonly:
        yield
        return
    path = profile / "setup-entra.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SetupError("Another setup may be running. After confirming it stopped, remove setup-entra.lock in the isolated profile.") from None
    try:
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def setup(args: argparse.Namespace) -> int:
    readonly = args.check or args.dry_run or args.list_staff or bool(args.lookup_upn)
    if args.resource_group != "ama":
        raise SetupError("This exercise only permits resource group ama.")
    args.roster = args.roster.expanduser()
    manifest = json.loads(MANIFEST.read_text())
    roles = {r["key"] for r in manifest["appRoles"]}
    expected, generate = (None, False)
    if not args.list_staff and not args.lookup_upn:
        expected, generate = roster_input(args.roster)
    persisted = json.loads(expected) if expected is not None and not generate else None
    generated = isinstance(persisted, dict)
    roster = ([] if args.lookup_upn or args.list_staff or generate
              else read_roster(args.roster, roles))
    if any(r["kind"] != "users" for r in roster):
        raise SetupError("SQL staff binding needs individual userId entries, not groupId mappings.")
    unresolved_profile = args.tenant_profile.expanduser()
    if unresolved_profile.is_symlink():
        raise SetupError("Isolated profile must not be a symbolic link.")
    args.tenant_profile = unresolved_profile.resolve()
    operator_profile = Path(os.environ.get("AZURE_CONFIG_DIR", str(Path.home() / ".azure"))).resolve()
    if args.tenant_profile == operator_profile or REPO in args.tenant_profile.parents:
        raise SetupError("Setup profile must be isolated from the operator profile and outside Git.")
    if args.tenant_profile.exists():
        private_path(args.tenant_profile, directory=True)
    print("1/7 Checking Python, Azure CLI and Container Apps extension.")
    operator = Azure(operator_profile, extension_directory=args.tenant_profile / "cliextensions")
    preflight(operator)
    require_extension(operator, "containerapp")
    print("2/7 Checking login, tenant binding, network and Graph access.")
    cli, graph, tenant, subscription = contexts(args, operator)
    if ((roster or generate) and not readonly
            and not token_permissions(graph).intersection(ASSIGNMENT_WRITE)):
        authority_help()
        raise SetupError("Roster assignment permission is missing; no registration changes were made.")
    with run_lock(args.tenant_profile, readonly), ExitStack() as stack:
        print("3/7 Discovering the API and its configured dependencies in ama.")
        app, urls = discover(cli, args, subscription)
        if args.lookup_upn:
            lookup_person(graph, args, roles)
            return 0
        if args.list_staff:
            candidates = candidate_staff(cli, args, app)
            if args.run_in_azure:
                print(f"Existing workbench positions: {len(candidates)}; "
                      "codes and roles retrieved privately, no SQL changes.")
            else:
                print("Existing workbench positions (code / approved role):")
                for row in candidates:
                    print(label(row["code"]) + " / " + label(row["role"]))
            return 0
        if generate or generated:
            require_demo(cli, app)
        if generate:
            coordination_status(cli, app)
            roster = generate_roster(graph, args, candidate_staff(cli, args, app),
                                     readonly=readonly, expected=expected)
            if readonly:
                return 2
        elif generated:
            assert isinstance(persisted, dict)
            print(EXERCISE_NOTICE)
            print(f"Reusing persisted roster: {len(roster)} codes; seed {persisted['seed']}; "
                  "no reshuffle.")
        if args.run_in_azure and not args.bearer_only:
            try:
                auth = cli.rest(
                    ARM + app["id"] + f"/authConfigs/current?api-version={API_VERSION}")["properties"]
            except AzureError as error:
                if error.kind != "not-found":
                    raise
                auth = {}
            azure_credential_guard(app, auth, args)
            candidate_registration = registration(
                graph, args.client_id or aad_registration(auth).get("clientId"),
                args.registration_name)
            if candidate_registration:
                secret_reference(
                    cli, graph, app, candidate_registration, auth, args, True, reuse_only=True)
        resolved_roster = resolve_roster(graph, roster, verify_people=generate or generated)
        coordination_problem = None
        try:
            stack.enter_context(authentication_lock(cli, app, readonly))
        except SetupError as error:
            if not readonly:
                raise
            coordination_problem = str(error)
            print("Coordination: blocked; " + str(error))
        if args.direct_ingress and not args.bearer_only:
            args.enable_browser = True
        auth_url = ARM + app["id"] + f"/authConfigs/current?api-version={API_VERSION}"
        try:
            current_auth = cli.rest(auth_url)["properties"]
        except AzureError as error:
            if error.kind != "not-found":
                raise
            current_auth = {}
        action = (current_auth.get("globalValidation") or {}).get("unauthenticatedClientAction")
        args.create_secret = args.create_secret or (
            not args.bearer_only and (args.direct_ingress or action != "Return401"))
        configured = aad_registration(current_auth).get("clientId")
        print("4/7 Reconciling application registration, callback URLs and enterprise app.")
        reg = registration(graph, args.client_id or configured, args.registration_name)
        drift = 0
        if reg is None:
            drift += 1
            print("Application registration is missing." + (" Would create it." if readonly else " Creating it."))
            if not readonly:
                reg = graph.rest(GRAPH + "applications", method="POST", body={
                    "displayName": args.registration_name, "signInAudience": "AzureADMyOrg",
                    "tags": ["zava-forward-role=api"]})
        sp = None
        if reg:
            client = object_id(reg["appId"])
            patch = desired_registration(reg, urls, manifest, args.account_photo)
            if patch:
                drift += 1
                print("Registration callbacks/roles/settings need reconciliation.")
                if not readonly:
                    graph.rest(GRAPH + f"applications/{object_id(reg['id'])}", method="PATCH", body=patch)
                    reg = wait_for(lambda: graph.rest(GRAPH + f"applications/{object_id(reg['id'])}"),
                                   lambda r: not desired_registration(r, urls, manifest, args.account_photo),
                                   "Registration changes are not verified; rerun after propagation.")
            sp = service_principal(graph, client)
            if sp is None:
                drift += 1
                if not readonly:
                    graph.rest(GRAPH + "servicePrincipals", method="POST", body={"appId": client})
                    sp = wait_for(lambda: service_principal(graph, client), lambda s: s is not None,
                                  "Enterprise app creation is not yet visible; rerun.")
            if sp:
                resource = object_id(sp["id"])
                if sp.get("appRoleAssignmentRequired") is not True:
                    drift += 1
                    if not readonly:
                        graph.rest(GRAPH + f"servicePrincipals/{resource}", method="PATCH",
                                   body={"appRoleAssignmentRequired": True})
                        wait_for(lambda: graph.rest(GRAPH + f"servicePrincipals/{resource}"),
                                 lambda s: s.get("appRoleAssignmentRequired") is True,
                                 "Assignment-required setting was not verified.")
                if not readonly:
                    manifest_values = {"ZavaForward." + r["key"] for r in manifest["appRoles"]}
                    wanted = {r["value"]: r["id"] for r in reg["appRoles"] if r.get("value") in manifest_values}
                    sp = wait_for(lambda: graph.rest(GRAPH + f"servicePrincipals/{resource}"),
                                  lambda s: all(any(r.get("value") == v and r.get("id") == rid
                                                   and r.get("isEnabled") is True
                                                   for r in s.get("appRoles", [])) for v, rid in wanted.items()
                                                if v.startswith("ZavaForward.")),
                                  "Enterprise-app roles have not propagated; rerun shortly.")
        print("5/7 Checking private roster assignments and browser credential wiring.")
        remaining = []
        if coordination_problem:
            remaining.append(coordination_problem)
        if args.pending_domains:
            remaining.append("Linked custom domain validation/deployment pending; rerun to add its callback after approval.")
        if not roster:
            remaining.append("Private roster missing: create the documented private role mappings and rerun.")
        elif sp:
            grants = assign_roster(graph, sp, resolved_roster, readonly)
            drift += grants
            print(f"Roster: {len(roster)} principal(s); {grants} missing assignment(s)"
                  + (" planned." if readonly else " reconciled."))
        else:
            remaining.append("Roster assignment waits for the missing enterprise application.")
        if reg:
            secret, changed = secret_reference(cli, graph, app, reg, current_auth, args, readonly)
            drift += int(changed)
            service_mode = args.bearer_only or (
                (current_auth.get("globalValidation") or {}).get("unauthenticatedClientAction") == "Return401"
                and not args.create_secret and not args.enable_browser)
            if secret is None and not service_mode:
                remaining.append("Browser credential missing: rerun with --create-secret "
                                 "(Key Vault default), or explicitly --create-secret --secret-store app.")
            else:
                desired = auth_patch(
                    current_auth, object_id(reg["appId"]), tenant, urls, secret, service_mode,
                    direct=args.direct_ingress, enable_browser=args.enable_browser)
                if desired.get("globalValidation", {}).get("unauthenticatedClientAction") == "Return401":
                    remaining.append("Bearer-only service action retained; browser sign-in still needs "
                                     "a valid credential and human-reviewed browser configuration.")
                if desired != current_auth:
                    drift += 1
                    if not readonly:
                        cli.rest(auth_url, method="PUT", body={"properties": desired})
                        wait_for(lambda: cli.rest(auth_url)["properties"],
                                 lambda actual: all(actual.get(k) == v for k, v in desired.items()),
                                 "Auth configuration update is not verified; rerun before sign-in.")
                app_url = ARM + app["id"] + f"?api-version={API_VERSION}"
                # The ARM representation, not the CLI one, which carries read-only fields ARM rejects.
                runtime = runtime_patch(cli.rest(app_url), object_id(reg["appId"]), tenant)
                if runtime:
                    drift += 1
                    if not readonly:
                        cli.rest(app_url, method="PATCH", body=runtime)
                        wait_for(lambda: cli.rest(app_url),
                                 lambda a: runtime_patch(a, object_id(reg["appId"]), tenant) is None
                                 and a["properties"].get("provisioningState") == "Succeeded",
                                 "API runtime authentication settings are not verified; rerun.")
        if args.account_photo and sp:
            resource = object_id(sp["id"])
            graph_service = service_principal(graph, GRAPH_APP)
            if not graph_service:
                raise SetupError("Microsoft Graph enterprise application could not be found for consent verification.")
            graph_resource = object_id(graph_service["id"])
            def consented() -> bool:
                return any("User.Read" in g.get("scope", "").split() and g.get("consentType") == "AllPrincipals"
                           and g.get("resourceId") == graph_resource
                           for g in graph.pages("oauth2PermissionGrants" + collection_filter(f"clientId eq '{resource}'")))
            if not consented():
                print(f"Human consent: open {APP_PORTAL} > All applications > select "
                      f"{label(args.registration_name)} > API permissions > Grant admin consent > Yes. "
                      "Only an authorized tenant admin may approve; this script grants no broad management consent.")
                if not readonly and args.wait_seconds:
                    wait_for(consented, bool, "Admin consent is still pending; rerun after an authorized admin approves.",
                             args.wait_seconds)
                else:
                    remaining.append("Graph User.Read admin consent pending (individual users may consent at sign-in).")
        latest_app = cli.rest(ARM + app["id"] + f"?api-version={API_VERSION}")
        if latest_app["properties"].get("provisioningState") != "Succeeded":
            remaining.append("API provisioning is not Succeeded; inspect the Container App rollout "
                             "and rerun after it succeeds. Matching runtime values alone are incomplete.")
        if not readonly and sp and reg:
            verified_sp = graph.rest(GRAPH + f"servicePrincipals/{object_id(sp['id'])}")
            outstanding = assign_roster(graph, verified_sp, resolved_roster, True)
            latest_auth = cli.rest(auth_url)["properties"]
            latest_reg = graph.rest(GRAPH + f"applications/{object_id(reg['id'])}")
            verified_secret, credential_drift = secret_reference(
                cli, graph, latest_app, latest_reg, latest_auth, args, True)
            if (outstanding or desired_registration(latest_reg, urls, manifest, args.account_photo)
                    or latest_auth != desired or credential_drift
                    or verified_secret != secret or verified_sp.get("appRoleAssignmentRequired") is not True
                    or runtime_patch(latest_app, object_id(reg["appId"]), tenant)):
                remaining.append("Final Entra verification found drift; SQL was not applied.")
        print("6/7 Checking SQL staff binding and serving-replica restart.")
        sql_done = False
        if roster and sp and not remaining:
            sql_done = sql_staff_step(args, latest_app, readonly=readonly, cli=cli)
        elif readonly and roster:
            sql_done = sql_staff_step(args, latest_app, readonly=True, cli=cli)
        else:
            print("SQL binding: NOT done; replica restart: NOT done (earlier prerequisite incomplete).")
        if not sql_done:
            remaining.append("SQL binding and serving-replica restart are not confirmed.")
        print("7/7 Summary: " + ("read-only; " if readonly else "") + f"{drift} reconciliation item(s).")
        print("SQL binding: " + ("confirmed; replica restart: confirmed." if sql_done
                                 else "NOT confirmed; replica restart: NOT confirmed."))
        for item in remaining:
            print("Remaining: " + item)
        print("Separate acceptance: test an authorized person's real browser sign-in. "
              "No network settings were changed.")
        return 2 if remaining or (readonly and drift) else 0


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise SetupError("Invalid command arguments; use --help for supported options. Input values were not logged.")


def parser() -> argparse.ArgumentParser:
    result = SafeParser(description=__doc__)
    result.add_argument("-g", "--resource-group", default="ama")
    result.add_argument("-n", "--container-app")
    result.add_argument("--edge-profile")
    result.add_argument("--direct-ingress", action="store_true",
                        help="Use only the verified external API FQDN; never discover Front Door")
    result.add_argument("--run-in-azure", action="store_true",
                        help="Run SQL staff work in a temporary private Container Apps job, not locally")
    result.add_argument("--azure-init-job",
                        help="Existing job-<prefix>-init in the API environment; defaults to API prefix")
    result.add_argument("--public-url", help="Verify this HTTPS origin is linked to the selected API")
    result.add_argument("--registration-name", default="zava-forward-api")
    result.add_argument("--client-id", type=object_id, help="Explicit intended registration; never printed")
    result.add_argument("--tenant-profile", type=Path, default=PROFILE)
    result.add_argument("--roster", type=Path, default=ROSTER)
    result.add_argument("--login", action="store_true", help="Renew isolated device-code login")
    mode = result.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Read-only verification; exit 2 for drift/incomplete")
    mode.add_argument("--dry-run", action="store_true", help="Read-only discovery and plan; never login or mutate")
    result.add_argument("--create-secret", action="store_true", help="Create only a missing app-bound browser credential")
    result.add_argument("--secret-store", choices=("keyvault", "app"),
                        help="Optional override; otherwise discover, prefer private Key Vault")
    result.add_argument("--vault", help="Key Vault name in ama")
    result.add_argument("--vault-identity", help="Key Vault-enabled managed identity already attached to the API")
    result.add_argument("--yes", action="store_true",
                        help="Accept the displayed private roster and SQL/restart plans")
    result.add_argument("--seed", type=int, help="Nonnegative reproducible demo assignment seed")
    result.add_argument("--admin-upn", help="Explicit demo administrator UPN; never printed")
    result.add_argument("--list-staff", action="store_true", help="List only existing SQL staff codes/roles")
    result.add_argument("--lookup-upn", help="Look up a person's object ID into the private roster, never stdout")
    result.add_argument("--staff-code", help="Existing workbench position for --lookup-upn")
    result.add_argument("--staff-role", help="Approved role for --lookup-upn")
    result.add_argument("--bearer-only", action="store_true", help="Explicit secretless service-test mode, not browser acceptance")
    result.add_argument("--enable-browser", action="store_true",
                        help="Explicitly replace Return401 with credential-backed browser login")
    result.add_argument("--account-photo", action="store_true", help="Merge delegated User.Read and poll human admin consent")
    result.add_argument("--wait-seconds", type=int, default=300, help="Bounded human-consent polling, 0 to report only")
    return result


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if args.seed is not None and args.seed < 0:
            raise SetupError("--seed must be a nonnegative integer.")
        if args.wait_seconds < 0 or args.wait_seconds > 1800:
            raise SetupError("--wait-seconds must be between 0 and 1800.")
        if args.login and (args.check or args.dry_run):
            raise SetupError("--check/--dry-run never log in; run --login separately.")
        if args.create_secret and args.bearer_only:
            raise SetupError("--create-secret and --bearer-only select different modes; use one.")
        if args.enable_browser and args.bearer_only:
            raise SetupError("--enable-browser and --bearer-only select different modes; use one.")
        return setup(args)
    except AzureError as error:
        if error.kind in ("permission", "login"):
            authority_help()
        print(f"Blocked: {error}", file=sys.stderr)
        print("Summary: setup incomplete; successful earlier steps are retained. "
              "For an interrupted write, rerun discovery before retrying a mutation.", file=sys.stderr)
        print("SQL binding and replica restart: NOT confirmed.", file=sys.stderr)
        return 1
    except (SetupError, credential_arm.CredentialError) as error:
        print(f"Blocked: {error}", file=sys.stderr)
        print("Summary: setup incomplete; successful earlier steps are retained. Resolve the blocker and rerun.",
              file=sys.stderr)
        print("SQL binding and replica restart: NOT confirmed.", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print("Blocked: input or service response was unreadable/malformed; no raw payload was logged. "
              "Check the documented schema, CLI version and permissions, then rerun.", file=sys.stderr)
        print("Summary: setup incomplete; successful earlier steps may persist.", file=sys.stderr)
        print("SQL binding and replica restart: NOT confirmed.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Stopped: interrupted. Earlier changes may persist; rerun to reconcile.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
