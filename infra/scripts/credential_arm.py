"""Write a browser credential through a bounded secure ARM deployment."""

from __future__ import annotations

import json
import re
import tempfile
import time
import uuid
from datetime import datetime
from typing import Any

ARM = "https://management.azure.com"
VAULT_VERSION = "2023-07-01"
DEPLOYMENT_VERSION = "2022-09-01"


class CredentialError(ValueError):
    """Sanitized credential transport failure; never include service payloads."""


def vault_id(cli: Any, app: dict[str, Any], vault: str) -> str:
    root = app["id"].split("/providers/")[0]
    if not re.fullmatch(
        r"/subscriptions/" + re.escape(cli.subscription or "") + r"/resourceGroups/ama",
        root,
        re.IGNORECASE,
    ) or not re.fullmatch(r"[a-zA-Z0-9-]{3,24}", vault):
        raise CredentialError("Credential deployment must target the selected ama vault.")
    return root + "/providers/Microsoft.KeyVault/vaults/" + vault


def preflight(cli: Any, app: dict[str, Any], vault: str) -> None:
    resource = vault_id(cli, app, vault)
    found = cli.rest(ARM + resource + "?api-version=" + VAULT_VERSION)
    if (
        found["id"].lower() != resource.lower()
        or found["properties"]["publicNetworkAccess"] != "Disabled"
        or found["properties"].get("enableRbacAuthorization") is not True
    ):
        raise CredentialError("Selected vault is not the existing private RBAC vault.")
    # Metadata only; no value read or data-plane connection is required.
    cli.rest(ARM + resource + "/secrets?api-version=" + VAULT_VERSION)


def store(
    cli: Any,
    app: dict[str, Any],
    vault: str,
    name: str,
    value: str,
    expiration: str,
    *,
    seconds: int = 180,
) -> str:
    resource = vault_id(cli, app, vault)
    if not re.fullmatch(r"entra-[a-f0-9]{32}-[a-f0-9]{12}", name) or not value:
        raise CredentialError("Credential handoff name/value is invalid; storage was not changed.")
    expires = int(datetime.fromisoformat(expiration.replace("Z", "+00:00")).timestamp())
    secret_id = resource + "/secrets/" + name
    deployment = (
        resource.split("/providers/")[0]
        + "/providers/Microsoft.Resources/deployments/entra-"
        + uuid.uuid4().hex
    )
    url = ARM + deployment + "?api-version=" + DEPLOYMENT_VERSION
    template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {"credential": {"type": "secureString"}},
        "resources": [
            {
                "type": "Microsoft.KeyVault/vaults/secrets",
                "apiVersion": VAULT_VERSION,
                "name": vault + "/" + name,
                "properties": {
                    "value": "[parameters('credential')]",
                    "attributes": {"enabled": True, "exp": expires},
                },
            }
        ],
    }
    body = {
        "properties": {
            "mode": "Incremental",
            "template": template,
            "parameters": {"credential": {"value": value}},
        }
    }
    previous = cli.deadline
    deadline = time.monotonic() + seconds
    cli.deadline = min(previous, deadline) if previous is not None else deadline
    try:
        if cli.body_directory is None:
            raise CredentialError("Private credential body storage is unavailable.")
        # The CLI follows ARM's async what-if headers; az rest exposes only the
        # initial body, which cannot establish the scope of a 202 response.
        with (
            tempfile.NamedTemporaryFile(mode="w+", dir=cli.body_directory) as source,
            tempfile.NamedTemporaryFile(mode="w+", dir=cli.body_directory) as parameters,
        ):
            json.dump(template, source)
            json.dump(body["properties"]["parameters"], parameters)
            source.flush()
            parameters.flush()
            planned = cli.call(
                [
                    "deployment",
                    "group",
                    "what-if",
                    "-g",
                    "ama",
                    "--name",
                    deployment.rsplit("/", 1)[-1],
                    "--template-file",
                    source.name,
                    "--parameters",
                    "@" + parameters.name,
                    "--no-pretty-print",
                ]
            )
        changes = planned.get("changes", planned.get("properties", {}).get("changes"))
        root = resource.split("/providers/")[0].lower() + "/"
        actionable = (
            [change for change in changes if change.get("changeType") != "Ignore"]
            if isinstance(changes, list)
            else []
        )
        if (
            planned.get("status") != "Succeeded"
            or not isinstance(changes, list)
            or any(not change.get("resourceId", "").lower().startswith(root) for change in changes)
            or len(actionable) != 1
            or actionable[0].get("resourceId", "").lower() != secret_id.lower()
            or actionable[0].get("changeType") != "Create"
        ):
            raise CredentialError(
                "Credential what-if did not prove exactly one new selected-vault secret. "
                "No deployment was applied; reconcile any orphan credential before retrying."
            )
        cli.rest(url, method="PUT", body=body)
        while time.monotonic() < cli.deadline:
            deployed = cli.rest(url)
            state = deployed["properties"]["provisioningState"]
            if state in {"Failed", "Canceled"}:
                raise CredentialError("Credential deployment failed; auth was not switched.")
            if state == "Succeeded":
                metadata = cli.rest(ARM + secret_id + "?api-version=" + VAULT_VERSION)
                properties = metadata["properties"]
                attributes = properties["attributes"]
                expected_uri = f"https://{vault}.vault.azure.net/secrets/{name}"
                if (
                    metadata["id"].lower() == secret_id.lower()
                    and attributes.get("enabled") is True
                    and attributes.get("exp") == expires
                    and properties.get("secretUri") == expected_uri
                ):
                    return expected_uri
                raise CredentialError(
                    "Credential metadata was not verified; auth was not switched."
                )
            time.sleep(2)
        raise CredentialError(
            "Credential deployment timed out; reconcile deployment/credential before retrying."
        )
    finally:
        cli.deadline = previous
