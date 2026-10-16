"""Synchronize a deployed API's callback without replacing its Entra registration."""
import argparse
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import time
import uuid


def _azure(args: list[str], profile: Path, *, output: str = "json") -> str:
    result = subprocess.run(
        ["az", *args, "--output", output], capture_output=True, text=True,
        env={**os.environ, "AZURE_CONFIG_DIR": str(profile)},
    )
    if result.returncode:
        raise RuntimeError(f"Azure CLI {args[0]} failed: {result.stderr.strip()}")
    return result.stdout


def _json(args: list[str], profile: Path) -> dict[str, object]:
    value = json.loads(_azure(args, profile))
    if not isinstance(value, dict):
        raise ValueError("Expected an Azure CLI JSON object.")
    return value


def _string(value: dict[str, object], key: str) -> str:
    text = value.get(key)
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"Missing or invalid {key}; deploy the protected API first.")
    return text


def _redirects(registration: dict[str, object]) -> list[str]:
    web = registration.get("web")
    if web is None:
        return []
    if not isinstance(web, dict):
        raise ValueError("Registration web settings are not an object.")
    redirects = web.get("redirectUris")
    if redirects is None:
        return []
    if not isinstance(redirects, list) or not all(isinstance(uri, str) for uri in redirects):
        raise ValueError("Registration redirectUris are not a string array.")
    return redirects


GRAPH_ID = "00000003-0000-0000-c000-000000000000"
USER_READ = "e1fe6dd8-ba31-4d61-89e7-88639da4683d"


def photo_permissions(current: object) -> list[dict]:
    """Merge delegated own-user User.Read; preserve every existing resource/grant."""
    if current is None:
        current = []
    if not isinstance(current, list) or not all(
        isinstance(resource, dict) and isinstance(resource.get("resourceAppId"), str)
        and isinstance(resource.get("resourceAccess"), list) for resource in current
    ):
        raise ValueError("Registration requiredResourceAccess is not a valid resource array.")
    resources = json.loads(json.dumps(current))
    graph = next((resource for resource in resources if resource["resourceAppId"] == GRAPH_ID), None)
    if graph is None:
        graph = {"resourceAppId": GRAPH_ID, "resourceAccess": []}
        resources.append(graph)
    if {"id": USER_READ, "type": "Scope"} not in graph["resourceAccess"]:
        graph["resourceAccess"].append({"id": USER_READ, "type": "Scope"})
    return resources


def initialize(
    group: str, app: str, *, tenant_profile: Path | None = None,
    login: bool = False, check: bool = False, account_photo: bool = False,
    public_url: str | None = None,
) -> dict[str, str]:
    """Add/verify the current callback; optional login writes only an isolated CLI profile."""
    operator = Path(os.environ.get("AZURE_CONFIG_DIR", str(Path.home() / ".azure"))).resolve()
    profile = (tenant_profile or operator / "zava-entra-init").resolve()
    tenant = str(uuid.UUID(_string(_json(["account", "show"], operator), "tenantId")))
    container = _json(["containerapp", "show", "-g", group, "-n", app,
                       "--query", "{fqdn:properties.configuration.ingress.fqdn}"], operator)
    fqdn = _string(container, "fqdn")
    if len(fqdn) > 253 or "." not in fqdn or any(
        not re.fullmatch(r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)", label) for label in fqdn.split(".")
    ):
        raise ValueError("The deployed API has an invalid ingress FQDN.")
    auth = _json(["containerapp", "auth", "show", "-g", group, "-n", app, "--query",
                  "{enabled:platform.enabled,clientId:identityProviders.azureActiveDirectory.registration.clientId,proxy:httpSettings.forwardProxy.convention,proxyHost:httpSettings.forwardProxy.customHostHeaderName,proxyProto:httpSettings.forwardProxy.customProtoHeaderName}"],
                 operator)
    if auth.get("enabled") is not True:
        raise ValueError("API ingress authentication is disabled; configure Entra in Bicep first.")
    client_id = str(uuid.UUID(_string(auth, "clientId")))
    if public_url is not None:
        from urllib.parse import urlsplit

        parsed = urlsplit(public_url)
        host = parsed.hostname or ""
        if (
            parsed.scheme != "https" or parsed.netloc != host or parsed.path not in ("", "/")
            or parsed.query or parsed.fragment or len(host) > 253 or "." not in host
            or any(not re.fullmatch(r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)", label)
                   for label in host.split("."))
        ):
            raise ValueError("Public URL must be an HTTPS origin with a valid DNS hostname and no credentials, port, path, query or fragment.")
        if host != fqdn and (
            auth.get("proxy") != "Custom"
            or auth.get("proxyHost") != "X-Forwarded-Host"
            or auth.get("proxyProto") != "X-Forwarded-Proto"
        ):
            raise ValueError("An edge callback requires Custom forwardProxy with Front Door's X-Forwarded-Host and X-Forwarded-Proto headers.")
        fqdn = host
    callback = f"https://{fqdn}/.auth/login/aad/callback"

    if login:
        if profile == operator:
            raise ValueError("Interactive login must not overwrite the deployment operator profile.")
        profile.mkdir(mode=0o700, parents=True, exist_ok=True)
        if profile.stat().st_mode & 0o077:
            raise ValueError("The tenant login profile directory must have mode 0700.")
        subprocess.run(
            ["az", "login", "--tenant", tenant, "--allow-no-subscriptions",
             "--use-device-code", "--output", "none"],
            check=True, env={**os.environ, "AZURE_CONFIG_DIR": str(profile)},
        )
    graph_tenant = str(uuid.UUID(_string(_json(["account", "show"], profile), "tenantId")))
    if graph_tenant != tenant:
        raise ValueError("Tenant profile does not match the deployed API tenant.")

    def registration() -> dict[str, object]:
        query = "{id:id,appId:appId,web:web,requiredResourceAccess:requiredResourceAccess}" if account_photo else "{id:id,appId:appId,web:web}"
        value = _json(["ad", "app", "show", "--id", client_id,
                       "--query", query], profile)
        if str(uuid.UUID(_string(value, "appId"))) != client_id:
            raise ValueError("Graph returned a different registration client ID.")
        return value

    current = registration()
    object_id = str(uuid.UUID(_string(current, "id")))
    original = _redirects(current)
    changed = callback not in original
    permissions = photo_permissions(current.get("requiredResourceAccess")) if account_photo else None
    permission_changed = account_photo and permissions != current.get("requiredResourceAccess", [])
    if changed and check:
        raise RuntimeError(f"Callback is missing: {callback}; run initialization without --check.")
    if permission_changed and check:
        raise RuntimeError("Delegated own-user Graph User.Read is missing; run --account-photo without --check.")
    if changed or permission_changed:
        body: dict[str, object] = {}
        if changed:
            body["web"] = {"redirectUris": list(dict.fromkeys([*original, callback]))}
        if permission_changed:
            body["requiredResourceAccess"] = permissions
        _azure(["rest", "--method", "PATCH", "--url",
                f"https://graph.microsoft.com/v1.0/applications/{object_id}",
                "--body", json.dumps(body)], profile, output="none")
        for attempt in range(5):
            verified = registration()
            actual = _redirects(verified)
            if callback in actual and set(original).issubset(actual) and (
                not account_photo or verified.get("requiredResourceAccess") == permissions
            ):
                break
            if attempt == 4:
                raise RuntimeError("Registration update could not be verified with all prior redirects and permissions intact.")
            time.sleep(2)
    return {"status": "updated" if changed or permission_changed else "already-initialized",
            "clientId": client_id, "callback": callback}


def main() -> int:
    """Run the callback-only initialization command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-g", "--resource-group", required=True)
    parser.add_argument("-n", "--container-app", required=True)
    parser.add_argument("--tenant-profile", type=Path, help="Graph-authorised Azure CLI profile directory")
    parser.add_argument("--login", action="store_true", help="Explicit isolated device-code login")
    parser.add_argument("--check", action="store_true", help="Verify only; never patch the registration")
    parser.add_argument("--account-photo", action="store_true", help="Also merge delegated own-user Graph User.Read; does not grant admin consent")
    parser.add_argument("--public-url", help="Explicit HTTPS edge origin; requires Custom forwarding using Front Door's X-Forwarded-Host/Proto headers")
    args = parser.parse_args()
    try:
        result = initialize(args.resource_group, args.container_app, tenant_profile=args.tenant_profile,
                            login=args.login, check=args.check, account_photo=args.account_photo,
                            public_url=args.public_url)
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        logging.error("%s Use an authorised tenant profile; --login starts an isolated device-code login.", error)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
