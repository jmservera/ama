"""Discover and initialize Zava Forward Entra authentication without exposing credentials."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, NoReturn
from urllib.parse import urlencode, urlsplit

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
    if (directory and not resolved.is_dir()) or resolved.stat().st_mode & 0o077:
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
            if self.subscription and args[0] in ("containerapp", "afd", "keyvault"):
                args = [*args, "--subscription", self.subscription]
            if body is not None:
                if self.body_directory is None:
                    raise SetupError("Mutation body storage is unavailable in read-only mode.")
                with tempfile.NamedTemporaryFile(mode="w", dir=self.body_directory,
                                                 prefix="request-", suffix=".json", delete=False) as stream:
                    filename = stream.name
                    json.dump(body, stream)
                args = [*args, "--body", f"@{filename}"]
            result = subprocess.run(
                ["az", *args, "--only-show-errors", "-o", "json"], env=self.environment(),
                capture_output=True, text=True, timeout=120, check=False,
            )
            if result.returncode:
                error = result.stderr.lower()
                kind = ("not-found" if any(s in error for s in ("resourcenotfound", "request_resourcenotfound", "status code: 404"))
                        else "permission" if any(s in error for s in ("forbidden", "authorization_requestdenied", "403", "insufficient privileges"))
                        else "login" if any(s in error for s in ("az login", "aadsts", "401"))
                        else "transient" if any(s in error for s in ("429", "503", "504"))
                        else "request")
                raise AzureError(kind)
            return json.loads(result.stdout) if result.stdout.strip() else None
        except (OSError, subprocess.TimeoutExpired):
            raise SetupError("Azure CLI could not run or timed out; check installation/network, then rerun.") from None
        except json.JSONDecodeError:
            raise SetupError("Azure CLI returned invalid JSON; update Azure CLI and rerun.") from None
        finally:
            if filename:
                Path(filename).unlink(missing_ok=True)

    def rest(self, url: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> Any:
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or parsed.netloc not in ("graph.microsoft.com", "management.azure.com")
                or parsed.fragment or parsed.username):
            raise SetupError("Refusing an API request outside the fixed Graph/ARM hosts.")
        for attempt in range(5):
            try:
                value = self.call(["rest", "--method", method, "--url", url], body=body)
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
    args = ["az", "login", "--use-device-code", "--allow-no-subscriptions", "-o", "none", "--only-show-errors"]
    if tenant:
        args += ["--tenant", tenant]
    try:
        process = subprocess.Popen(args, env=cli.environment(), stdout=subprocess.PIPE,
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
    if not readonly and not permissions.intersection(APPLICATION_WRITE):
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
           suffix: str, option: str) -> dict[str, Any]:
    named = [r for r in rows if r.get("name") == explicit] if explicit else []
    tagged = [r for r in rows if r.get("tags", {}).get("zava-forward-role") == role]
    legacy = [r for r in rows if r.get("tags", {}).get("workload") == role]
    candidates = named if explicit else tagged or legacy or [
        r for r in rows if re.fullmatch(suffix, r.get("name", ""))]
    if len(candidates) != 1:
        names = ", ".join(sorted(label(r.get("name", "unnamed")) for r in candidates or rows)) or "(none)"
        raise SetupError(f"Cannot select one {role}. Candidates: {names}. Pass {option} with an exact name.")
    return candidates[0]


def discover(cli: Azure, args: argparse.Namespace, subscription: str) -> tuple[dict[str, Any], list[str]]:
    args.pending_domains = 0
    rows = cli.call(["containerapp", "list", "-g", args.resource_group])
    if not isinstance(rows, list):
        raise SetupError("Container App discovery did not return a list.")
    direct_rows = [r for r in rows if r.get("tags", {}).get("zava-forward-role") == "api"
                   and r.get("tags", {}).get("zava-forward-ingress") == "direct"]
    candidates = rows
    if not args.container_app and direct_rows:
        candidates = direct_rows
    app = choose(candidates, args.container_app, "api", r"ca-.+-api", "--container-app")
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
        data = json.loads(path.read_text())
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
        code, role = row.get("code"), row.get("role")
        fields = [key for key in ("userId", "groupId") if key in row]
        if (not isinstance(code, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", code)
                or code in codes or role not in keys or len(fields) != 1):
            raise SetupError("Roster needs distinct codes, an explicit manifest role and exactly one userId/groupId per row.")
        principal = identifier(row[fields[0]])
        if not principal or principal in principals:
            raise SetupError("Roster principal identifiers must be valid and distinct.")
        codes.add(code)
        principals.add(principal)
        out.append({"code": code, "role": role, "kind": "users" if fields[0] == "userId" else "groups", "id": principal})
    return out


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
    for spec in manifest["appRoles"]:
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


def resolve_roster(graph: Azure, roster: list[dict[str, str]]) -> list[tuple[dict[str, str], set[str]]]:
    resolved = []
    for row in roster:
        select = "id,accountEnabled,userType" if row["kind"] == "users" else "id,securityEnabled"
        principal = graph.rest(GRAPH + f"{row['kind']}/{row['id']}?$select={select}")
        if object_id(principal.get("id")) != row["id"]:
            raise SetupError("Graph returned a different roster principal.")
        groups: set[str] = set()
        if row["kind"] == "users":
            if principal.get("accountEnabled") is not True or principal.get("userType") != "Member":
                raise SetupError("Roster users must be enabled tenant members; guests need separate human approval.")
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
        if actual - {rid}:
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


def secret_reference(cli: Azure, graph: Azure, app: dict[str, Any], registration: dict[str, Any],
                     auth: dict[str, Any], args: argparse.Namespace, readonly: bool) -> tuple[str | None, bool]:
    client = object_id(registration["appId"])
    current = aad_registration(auth)
    secret_name = "entra-" + client.replace("-", "")
    secrets = app["properties"]["configuration"].get("secrets") or []
    existing_ref = current.get("clientSecretSettingName")
    if args.bearer_only:
        return None, False
    if (identifier(current.get("clientId")) == client and existing_ref and existing_ref != secret_name
            and any(s["name"] == existing_ref for s in secrets)):
        return existing_ref, False
    action = (auth.get("globalValidation") or {}).get("unauthenticatedClientAction")
    if action == "Return401" and not args.create_secret and not args.enable_browser:
        return None, False
    stored = any(s["name"] == secret_name for s in secrets)
    credentials = [c for c in registration.get("passwordCredentials", []) if c.get("displayName") == secret_name]
    if stored and credentials:
        expires = datetime.fromisoformat(credentials[-1].get("endDateTime", "").replace("Z", "+00:00"))
        if expires <= datetime.now(timezone.utc):
            raise SetupError("Setup credential is expired; use the documented credential rotation procedure.")
        return secret_name, False
    if stored or credentials:
        print(f"Credential recovery: open {APP_PORTAL} > select the workbench registration > "
              "Certificates & secrets. Review only the credential whose name starts with entra-. "
              "A credential without matching app storage cannot be recovered; an authorized owner "
              "must remove that orphaned setup credential before retrying --create-secret. "
              "Never remove an in-use credential.")
        raise SetupError("Credential/storage handoff is incomplete; auth was not switched. Human recovery required.")
    if not args.create_secret:
        return None, True
    if readonly:
        return secret_name, True
    if args.secret_store == "keyvault":
        vaults = cli.call(["keyvault", "list", "-g", args.resource_group])
        candidates = [v for v in vaults if not args.vault or v["name"] == args.vault]
        if len(candidates) != 1:
            names = ", ".join(label(v["name"]) for v in candidates) or "(none)"
            raise SetupError(f"Select a Key Vault in ama with --vault. Candidates: {names}. "
                             "For private vaults, run inside the approved network or explicitly use --secret-store app.")
        vault = candidates[0]["name"]
        if not args.vault_identity and app.get("identity", {}).get("type") != "SystemAssigned":
            raise SetupError("Pass --vault-identity for the API's Key Vault-enabled managed identity.")
        if args.vault_identity and args.vault_identity not in app.get("identity", {}).get("userAssignedIdentities", {}):
            raise SetupError("Key Vault identity must already be attached to the selected API.")
        print("Checking selected Key Vault endpoint using secret metadata only; no secret values are read.")
        try:
            cli.call(["keyvault", "secret", "list", "--vault-name", vault, "--maxresults", "1"])
        except AzureError:
            raise SetupError("Selected Key Vault endpoint preflight failed; no credential was created. "
                             "Check approved network access and secret-metadata list permission, "
                             "or explicitly use --secret-store app. Vault networking was not changed.") from None
    else:
        vault = None
    app_url = ARM + app["id"] + f"?api-version={API_VERSION}"
    existing = cli.rest(ARM + app["id"] + f"/listSecrets?api-version={API_VERSION}", method="POST")
    preserved = existing.get("value")
    if not isinstance(preserved, list):
        raise SetupError("Cannot preserve existing app secrets; no new credential was created.")
    expiration = (datetime.now(timezone.utc) + timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%SZ")
    password = graph.rest(GRAPH + f"applications/{object_id(registration['id'])}/addPassword",
                          method="POST", body={"passwordCredential": {
                              "displayName": secret_name, "endDateTime": expiration}})
    if not isinstance(password, dict) or not isinstance(password.get("secretText"), str) or not password["secretText"]:
        raise SetupError("Credential creation returned no usable secret; inspect Certificates & secrets before retrying.")
    new_secret: dict[str, Any] = {"name": secret_name}
    if vault:
        filename = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=args.tenant_profile, delete=False) as stream:
                filename = stream.name
                stream.write(password["secretText"])
            result = cli.call(["keyvault", "secret", "set", "--vault-name", vault, "--name", secret_name,
                               "--file", filename, "--expires", expiration])
            new_secret.update(keyVaultUrl=result["id"], identity=args.vault_identity or "system")
        finally:
            if filename:
                Path(filename).unlink(missing_ok=True)
    else:
        new_secret["value"] = password["secretText"]
    configuration = {**app["properties"]["configuration"], "secrets": [*preserved, new_secret]}
    cli.rest(app_url, method="PATCH", body={"properties": {"configuration": configuration}})
    wait_for(lambda: cli.rest(app_url),
             lambda a: any(s["name"] == secret_name for s in a["properties"]["configuration"].get("secrets", [])),
             "App secret reference is not confirmed; auth was not switched. Rerun to reconcile.")
    return secret_name, True


def aad_registration(auth: dict[str, Any]) -> dict[str, Any]:
    providers = auth.get("identityProviders") or {}
    provider = providers.get("azureActiveDirectory") or {}
    return provider.get("registration") or {}


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
    readonly = args.check or args.dry_run
    if args.resource_group != "ama":
        raise SetupError("This exercise only permits resource group ama.")
    unresolved_profile = args.tenant_profile.expanduser()
    if unresolved_profile.is_symlink():
        raise SetupError("Isolated profile must not be a symbolic link.")
    args.tenant_profile = unresolved_profile.resolve()
    operator_profile = Path(os.environ.get("AZURE_CONFIG_DIR", str(Path.home() / ".azure"))).resolve()
    if args.tenant_profile == operator_profile or REPO in args.tenant_profile.parents:
        raise SetupError("Setup profile must be isolated from the operator profile and outside Git.")
    if args.tenant_profile.exists():
        private_path(args.tenant_profile, directory=True)
    print("1/6 Checking Python, Azure CLI and Container Apps extension.")
    operator = Azure(operator_profile, extension_directory=args.tenant_profile / "cliextensions")
    preflight(operator)
    require_extension(operator, "containerapp")
    print("2/6 Checking login, tenant binding, network and Graph access.")
    cli, graph, tenant, subscription = contexts(args, operator)
    manifest = json.loads(MANIFEST.read_text())
    roster = read_roster(args.roster.expanduser(), {r["key"] for r in manifest["appRoles"]})
    if roster and not readonly and not token_permissions(graph).intersection(ASSIGNMENT_WRITE):
        authority_help()
        raise SetupError("Roster assignment permission is missing; no registration changes were made.")
    with run_lock(args.tenant_profile, readonly):
        print("3/6 Discovering the API and its linked public edge in ama.")
        app, urls = discover(cli, args, subscription)
        auth_url = ARM + app["id"] + f"/authConfigs/current?api-version={API_VERSION}"
        try:
            current_auth = cli.rest(auth_url)["properties"]
        except AzureError as error:
            if error.kind != "not-found":
                raise
            current_auth = {}
        action = (current_auth.get("globalValidation") or {}).get("unauthenticatedClientAction")
        if (args.direct_ingress and not args.bearer_only and not args.enable_browser
                and action == "Return401"):
            raise SetupError(
                "Direct API inherited Return401. Review browser activation and rerun with "
                "--enable-browser (plus --create-secret if missing), or explicitly "
                "--bearer-only to preserve service-only access.")
        configured = aad_registration(current_auth).get("clientId")
        resolved_roster = resolve_roster(graph, roster)
        print("4/6 Reconciling application registration, callback URLs and enterprise app.")
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
        print("5/6 Checking private roster assignments and browser credential wiring.")
        remaining = []
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
                runtime = runtime_patch(app, object_id(reg["appId"]), tenant)
                if runtime:
                    drift += 1
                    if not readonly:
                        app_url = ARM + app["id"] + f"?api-version={API_VERSION}"
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
        if sp:
            print(f"Manual assignments, if authority is missing: {SP_PORTAL} > All applications > "
                  f"{label(args.registration_name)} > Users and groups > Add user/group > select principal "
                  "> Select a role > Assign.")
        print("6/6 Summary: " + ("read-only; " if readonly else "") + f"{drift} reconciliation item(s).")
        for item in remaining:
            print("Remaining: " + item)
        print("Separate acceptance: run the private-network SQL staff-binding/restart procedure in infra/README.md "
              "and test an authorized person's browser sign-in. No SQL or network settings were changed.")
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
    result.add_argument("--secret-store", choices=("keyvault", "app"), default="keyvault")
    result.add_argument("--vault", help="Key Vault name in ama")
    result.add_argument("--vault-identity", help="Key Vault-enabled managed identity already attached to the API")
    result.add_argument("--bearer-only", action="store_true", help="Explicit secretless service-test mode, not browser acceptance")
    result.add_argument("--enable-browser", action="store_true",
                        help="Explicitly replace Return401 with credential-backed browser login")
    result.add_argument("--account-photo", action="store_true", help="Merge delegated User.Read and poll human admin consent")
    result.add_argument("--wait-seconds", type=int, default=300, help="Bounded human-consent polling, 0 to report only")
    return result


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
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
        return 1
    except SetupError as error:
        print(f"Blocked: {error}", file=sys.stderr)
        print("Summary: setup incomplete; successful earlier steps are retained. Resolve the blocker and rerun.",
              file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print("Blocked: input or service response was unreadable/malformed; no raw payload was logged. "
              "Check the documented schema, CLI version and permissions, then rerun.", file=sys.stderr)
        print("Summary: setup incomplete; successful earlier steps may persist.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Stopped: interrupted. Earlier changes may persist; rerun to reconcile.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
