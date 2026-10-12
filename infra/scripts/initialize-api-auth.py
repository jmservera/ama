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


def initialize(
    group: str, app: str, *, tenant_profile: Path | None = None,
    login: bool = False, check: bool = False,
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
                  "{enabled:platform.enabled,clientId:identityProviders.azureActiveDirectory.registration.clientId}"],
                 operator)
    if auth.get("enabled") is not True:
        raise ValueError("API ingress authentication is disabled; configure Entra in Bicep first.")
    client_id = str(uuid.UUID(_string(auth, "clientId")))
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
        value = _json(["ad", "app", "show", "--id", client_id,
                       "--query", "{id:id,appId:appId,web:web}"], profile)
        if str(uuid.UUID(_string(value, "appId"))) != client_id:
            raise ValueError("Graph returned a different registration client ID.")
        return value

    current = registration()
    object_id = str(uuid.UUID(_string(current, "id")))
    original = _redirects(current)
    changed = callback not in original
    if changed and check:
        raise RuntimeError(f"Callback is missing: {callback}; run initialization without --check.")
    if changed:
        body = {"web": {"redirectUris": list(dict.fromkeys([*original, callback]))}}
        _azure(["rest", "--method", "PATCH", "--url",
                f"https://graph.microsoft.com/v1.0/applications/{object_id}",
                "--body", json.dumps(body)], profile, output="none")
        for attempt in range(5):
            actual = _redirects(registration())
            if callback in actual and set(original).issubset(actual):
                break
            if attempt == 4:
                raise RuntimeError("Callback update could not be verified with all prior redirects intact.")
            time.sleep(2)
    return {"status": "updated" if changed else "already-initialized",
            "clientId": client_id, "callback": callback}


def main() -> int:
    """Run the callback-only initialization command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-g", "--resource-group", required=True)
    parser.add_argument("-n", "--container-app", required=True)
    parser.add_argument("--tenant-profile", type=Path, help="Graph-authorised Azure CLI profile directory")
    parser.add_argument("--login", action="store_true", help="Explicit isolated device-code login")
    parser.add_argument("--check", action="store_true", help="Verify only; never patch the registration")
    args = parser.parse_args()
    try:
        result = initialize(args.resource_group, args.container_app, tenant_profile=args.tenant_profile,
                            login=args.login, check=args.check)
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        logging.error("%s Use an authorised tenant profile; --login starts an isolated device-code login.", error)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
