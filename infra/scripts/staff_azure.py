"""Private, bounded Container Apps job transport for SQL staff initialization."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import time
import uuid
from typing import Any

ARM = "https://management.azure.com"
VERSION = "2025-07-01"
MAX_INPUT = 12 * 1024
CHUNK = 200
MAX_CHUNKS = 40
TAG_VERSION = "2021-04-01"


def result_prefix(request: dict[str, Any]) -> str:
    return f"zfstaff-{request['run']}-"


def tags_url(resource_id: str) -> str:
    return resource_url(resource_id + "/providers/Microsoft.Resources/tags/default", TAG_VERSION)


def result_tags(request: dict[str, Any], result: dict[str, Any]) -> dict[str, str]:
    return {
        result_prefix(request) + str(i): frame
        for i, frame in enumerate(encode_result(request, result))
    }


def read_result(cli: Any, relay: str, request: dict[str, Any]) -> dict[str, Any] | None:
    tags = cli.rest(tags_url(relay))["properties"].get("tags") or {}
    frames = [v for k, v in tags.items() if k.startswith(result_prefix(request))]
    if len(frames) > MAX_CHUNKS or any(not isinstance(v, str) or len(v) > 256 for v in frames):
        raise StaffJobError("Azure staff result tags exceed the bounded response size.")
    return decode_result(request, "\n".join(json.dumps({"Log": v}) for v in frames))


def clear_result(cli: Any, relay: str, request: dict[str, Any]) -> None:
    tags = cli.rest(tags_url(relay))["properties"].get("tags") or {}
    owned = {k: v for k, v in tags.items() if k.startswith(result_prefix(request))}
    if owned:
        cli.rest(
            tags_url(relay),
            method="PATCH",
            body={"operation": "Delete", "properties": {"tags": owned}},
        )
    remaining = cli.rest(tags_url(relay))["properties"].get("tags") or {}
    if any(k.startswith(result_prefix(request)) for k in remaining):
        raise StaffJobError("Azure staff result cleanup was not confirmed.")


class StaffJobError(Exception):
    """Sanitized job failure, including uncertain SQL or cleanup outcomes."""


def aad(request: dict[str, Any]) -> bytes:
    return json.dumps(
        [1, request["run"], request["operation"], request["digest"]], separators=(",", ":")
    ).encode()


def encode_result(request: dict[str, Any], result: dict[str, Any]) -> list[str]:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    nonce = os.urandom(12)
    encrypted = AESGCM(base64.b64decode(request["key"], validate=True)).encrypt(
        nonce, json.dumps(result).encode(), aad(request)
    )
    value = base64.b64encode(nonce + encrypted).decode()
    count = (len(value) + CHUNK - 1) // CHUNK
    if count > MAX_CHUNKS:
        raise StaffJobError("Azure staff result is too large; no result was disclosed.")
    return [
        f"ZFSTAFF:{request['run']}:{i}:{count}:{value[i * CHUNK : (i + 1) * CHUNK]}"
        for i in range(count)
    ]


def decode_result(request: dict[str, Any], output: str) -> dict[str, Any] | None:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if len(output) > 512 * 1024:
        raise StaffJobError("Azure staff logs exceeded the bounded response size.")
    chunks: dict[int, str] = {}
    total = None
    for line in output.splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue  # CLI connection/status lines are not worker records.
        message = record.get("Log", "") if isinstance(record, dict) else ""
        if not isinstance(message, str) or not message.startswith("ZFSTAFF:"):
            continue
        parts = message.split(":", 4)
        try:
            if len(parts) != 5 or parts[1] != request["run"]:
                raise ValueError
            index, count = int(parts[2]), int(parts[3])
            if not 0 <= index < count <= MAX_CHUNKS or len(parts[4]) > CHUNK:
                raise ValueError
            if index in chunks or (total is not None and total != count):
                raise ValueError
            total = count
            chunks[index] = parts[4]
        except ValueError:
            raise StaffJobError("Azure staff result framing is invalid.") from None
    if total is None or len(chunks) != total:
        return None
    try:
        encrypted = base64.b64decode("".join(chunks[i] for i in range(total)), validate=True)
        clear = AESGCM(base64.b64decode(request["key"], validate=True)).decrypt(
            encrypted[:12], encrypted[12:], aad(request)
        )
        value = json.loads(clear)
        if (
            not isinstance(value, dict)
            or type(value.get("version")) is not int
            or value["version"] != 1
        ):
            raise ValueError
        if value.get("operation") != request["operation"] or value.get("run") != request["run"]:
            raise ValueError
        return value
    except (ValueError, KeyError, InvalidTag):
        raise StaffJobError("Azure staff result could not be authenticated.") from None


def resource_url(resource_id: str, version: str = VERSION) -> str:
    return f"{ARM}{resource_id}?api-version={version}"


def discover(cli: Any, app: dict[str, Any], source_name: str | None) -> dict[str, Any]:
    """Bind every secret-bearing execution to existing ama API/SQL/admin assets."""
    try:
        app_id = app["id"]
        match = re.fullmatch(
            r"/subscriptions/([0-9a-f-]+)/resourceGroups/ama/providers/"
            r"Microsoft.App/containerApps/(ca-([a-z0-9-]+)-api)",
            app_id,
            re.IGNORECASE,
        )
        if not match or match[1].lower() != cli.subscription.lower():
            raise ValueError
        root = app_id.split("/providers/")[0]
        prefix = match[3]
        expected_source = f"job-{prefix}-init"
        if source_name and source_name != expected_source:
            # Direct-demo environments may deliberately reuse a parent proof initializer.
            if not re.fullmatch(r"job-[a-z0-9-]+-init", source_name):
                raise ValueError
            expected_source = source_name
        source_id = root + "/providers/Microsoft.App/jobs/" + expected_source
        try:
            source = cli.rest(resource_url(source_id))
        except Exception as error:
            if (
                source_name is not None
                or not prefix.endswith("-demo")
                or getattr(error, "kind", None) != "not-found"
            ):
                raise
            expected_source = f"job-{prefix.removesuffix('-demo')}-init"
            source_id = root + "/providers/Microsoft.App/jobs/" + expected_source
            source = cli.rest(resource_url(source_id))
        identity_name = "id-" + expected_source.removeprefix("job-")
        identity_id = (
            root + "/providers/Microsoft.ManagedIdentity/userAssignedIdentities/" + identity_name
        )
        identity = cli.rest(resource_url(identity_id, "2023-01-31"))
        if (
            identity["id"].lower() != identity_id.lower()
            or source["id"].lower() != source_id.lower()
            or source["name"] != expected_source
        ):
            raise ValueError
        environment_id = (
            app["properties"].get("managedEnvironmentId") or app["properties"]["environmentId"]
        )
        if not environment_id.lower().startswith(
            (root + "/providers/Microsoft.App/managedEnvironments/").lower()
        ):
            raise ValueError
        environment = cli.rest(resource_url(environment_id))
        if environment["id"].lower() != environment_id.lower():
            raise ValueError
        subnet = environment["properties"]["vnetConfiguration"]["infrastructureSubnetId"]
        if not re.fullmatch(
            re.escape(root) + r"/providers/Microsoft.Network/virtualNetworks/[^/]+/subnets/[^/]+",
            subnet,
            re.IGNORECASE,
        ):
            raise ValueError
        source_environment_id = source["properties"]["environmentId"]
        if source_environment_id.lower() != environment_id.lower():
            if not source_environment_id.lower().startswith(
                (root + "/providers/Microsoft.App/managedEnvironments/").lower()
            ):
                raise ValueError
            source_environment = cli.rest(resource_url(source_environment_id))
            source_subnet = source_environment["properties"]["vnetConfiguration"][
                "infrastructureSubnetId"
            ]
            if (
                source_environment["id"].lower() != source_environment_id.lower()
                or source_subnet.rsplit("/subnets/", 1)[0].lower()
                != subnet.rsplit("/subnets/", 1)[0].lower()
                or not re.fullmatch(
                    re.escape(root)
                    + r"/providers/Microsoft.Network/virtualNetworks/[^/]+/subnets/[^/]+",
                    source_subnet,
                    re.IGNORECASE,
                )
            ):
                raise ValueError
        relay_tags = cli.rest(tags_url(source_id))["properties"].get("tags") or {}
        if len(relay_tags) > 50 - MAX_CHUNKS:
            raise StaffJobError(
                "Initializer result relay has insufficient tag capacity; inspect owned "
                "stale runs in the serialized operator window before retrying."
            )
        identities = source["identity"]["userAssignedIdentities"]
        if source["identity"]["type"] != "UserAssigned" or {i.lower() for i in identities} != {
            identity_id.lower()
        }:
            raise ValueError
        template = source["properties"]["template"]
        if len(template["containers"]) != 1 or template.get("initContainers"):
            raise ValueError
        image = template["containers"][0]["image"]
        registries = source["properties"]["configuration"]["registries"]
        if (
            len(registries) != 1
            or registries[0].get("identity", "").lower() != identity_id.lower()
            or set(registries[0]) - {"server", "identity", "username", "passwordSecretRef"}
            or registries[0].get("username")
            or registries[0].get("passwordSecretRef")
            or not image.startswith(registries[0]["server"] + "/zava-forward-cutover-proof@sha256:")
            or not re.fullmatch(r"[0-9a-f]{64}", image.rsplit(":", 1)[-1])
        ):
            raise ValueError
        containers = app["properties"]["template"]["containers"]
        api = [c for c in containers if c["name"] == "api"]
        if len(api) != 1:
            raise ValueError
        env = {r["name"]: r.get("value") for r in api[0]["env"]}
        server, database = (
            env.get("ZF_SQL_SERVER") or env.get("SQL_SERVER"),
            (env.get("ZF_SQL_DATABASE") or env.get("SQL_DATABASE")),
        )
        if not isinstance(server, str) or not re.fullmatch(
            r"[a-z0-9-]+\.database\.windows\.net", server
        ):
            raise ValueError
        if not re.fullmatch(r"[A-Za-z0-9_-]+", database or ""):
            raise ValueError
        sql_id = root + "/providers/Microsoft.Sql/servers/" + server.split(".")[0]
        sql = cli.rest(resource_url(sql_id, "2023-08-01"))
        admin = cli.rest(resource_url(sql_id + "/administrators/ActiveDirectory", "2023-08-01"))
        entra_only = cli.rest(
            resource_url(sql_id + "/azureADOnlyAuthentications/Default", "2023-08-01")
        )
        tenant = cli.call(["account", "show"])["tenantId"]
        if (
            sql["properties"]["fullyQualifiedDomainName"] != server
            or sql["properties"]["publicNetworkAccess"] != "Disabled"
            or admin["properties"]["sid"].lower() != identity["properties"]["principalId"].lower()
            or admin["properties"]["tenantId"].lower() != tenant.lower()
            or identity["properties"]["tenantId"].lower() != tenant.lower()
            or admin["properties"].get("principalType", "Application") != "Application"
            or entra_only["properties"]["azureADOnlyAuthentication"] is not True
        ):
            raise ValueError
        database_id = sql_id + "/databases/" + database
        found_database = cli.rest(resource_url(database_id, "2023-08-01"))
        if found_database["id"].lower() != database_id.lower():
            raise ValueError
        return {
            "root": root,
            "relay": source_id,
            "environment": environment_id,
            "identity": identity_id,
            "client": identity["properties"]["clientId"],
            "image": image,
            "registries": [{"server": registries[0]["server"], "identity": identity_id}],
            "server": server,
            "database": database,
            "location": source["location"],
            "app": app_id,
            "tags": source.get("tags", {}),
        }
    except (KeyError, TypeError, ValueError, AttributeError):
        raise StaffJobError(
            "Cannot verify the existing ama initializer image, VNet, SQL-admin identity and "
            "private SQL target. See the in-VNet staff runbook; no network setting was changed."
        ) from None


def execute(
    cli: Any,
    app: dict[str, Any],
    operation: str,
    payload: dict[str, Any],
    *,
    source_name: str | None = None,
    seconds: int = 600,
) -> dict[str, Any]:
    """Run exactly once; remove the owned job/secret before returning any result."""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        raise StaffJobError(
            "Install operator dependencies: python3 -m pip install -r src/api/requirements.txt"
        ) from None
    if operation not in {"candidates", "check", "apply"}:
        raise StaffJobError("Unsupported Azure staff operation.")
    target = discover(cli, app, source_name)
    content = json.dumps(
        {**payload, "target": target["app"], "relay": target["relay"]}, sort_keys=True
    )
    if len(content.encode()) > MAX_INPUT:
        raise StaffJobError("Private roster exceeds the bounded job-secret size.")
    request = {
        "version": 1,
        "run": uuid.uuid4().hex,
        "operation": operation,
        "digest": hashlib.sha256(content.encode()).hexdigest(),
        "key": base64.b64encode(AESGCM.generate_key(bit_length=256)).decode(),
        "payload": json.loads(content),
    }
    name = "job-staff-" + request["run"][:20]
    job_id = target["root"] + "/providers/Microsoft.App/jobs/" + name
    url = resource_url(job_id)
    try:
        cli.rest(url)
    except Exception as error:
        if getattr(error, "kind", None) != "not-found":
            raise
    else:
        raise StaffJobError("Azure staff job name collision; existing resource was not changed.")
    env = {
        "AZURE_CLIENT_ID": target["client"],
        "ZF_SQL_CLIENT_ID": target["client"],
        "ZF_SQL_AUTH": "msi",
        "ZF_SQL_SERVER": target["server"],
        "ZF_SQL_DATABASE": target["database"],
        "ZF_STAFF_TARGET": target["app"],
        "ZF_STAFF_RELAY": target["relay"],
    }
    body = {
        "location": target["location"],
        "tags": {**target["tags"], "zava-forward-staff-run": request["run"]},
        "identity": {"type": "UserAssigned", "userAssignedIdentities": {target["identity"]: {}}},
        "properties": {
            "environmentId": target["environment"],
            "workloadProfileName": "Consumption",
            "configuration": {
                "triggerType": "Manual",
                "replicaTimeout": seconds,
                "replicaRetryLimit": 0,
                "manualTriggerConfig": {"parallelism": 1, "replicaCompletionCount": 1},
                "registries": target["registries"],
                "secrets": [{"name": "request", "value": json.dumps(request)}],
            },
            "template": {
                "containers": [
                    {
                        "name": "staff",
                        "image": target["image"],
                        "command": ["python", "/app/scripts/staff-azure-worker.py"],
                        "args": [],
                        "resources": {"cpu": 0.5, "memory": "1Gi"},
                        "env": [{"name": k, "value": v} for k, v in env.items()]
                        + [{"name": "ZF_STAFF_REQUEST", "secretRef": "request"}],
                    }
                ]
            },
        },
    }
    attempted = False
    provisioned = False
    completed = False
    result_value = None
    deadline = time.monotonic() + seconds
    previous_deadline = cli.deadline
    cli.deadline = deadline
    try:
        attempted = True  # PUT may succeed even if its response is lost.
        cli.rest(url, method="PUT", body=body)
        while time.monotonic() < deadline:
            created = cli.rest(url)
            state = created["properties"].get("provisioningState")
            if state == "Succeeded":
                provisioned = True
                break
            if state in {"Failed", "Canceled"}:
                raise StaffJobError("Azure staff job provisioning failed.")
            time.sleep(2)
        else:
            raise StaffJobError("Azure staff job provisioning timed out.")
        started = cli.call(["containerapp", "job", "start", "-g", "ama", "-n", name])
        execution = started["name"]
        if not re.fullmatch(re.escape(name) + r"-[a-z0-9-]+", execution):
            raise StaffJobError("Azure staff execution target is invalid.")
        while time.monotonic() < deadline:
            status = cli.rest(resource_url(job_id + "/executions/" + execution))["properties"][
                "status"
            ]
            if status in {"Failed", "Stopped", "Canceled", "Degraded"}:
                raise StaffJobError("Azure staff job failed; SQL/restart outcome is unverified.")
            if result_value is None:
                result_value = read_result(cli, target["relay"], request)
            if status == "Succeeded":
                if result_value is None:
                    time.sleep(2)
                    continue  # ARM tag readback may lag terminal execution status.
                completed = True
                break
            time.sleep(2)
        else:
            raise StaffJobError(
                "Azure staff job timed out; SQL may have committed. Do not reapply blindly."
            )
        if result_value.get("ok") is not True:
            raise StaffJobError(
                "Azure staff validation/verification failed; SQL/restart is incomplete."
            )
        return result_value
    except Exception:
        if time.monotonic() >= deadline:
            raise StaffJobError(
                "Azure staff job timed out; SQL may have committed. Do not reapply blindly."
            ) from None
        raise
    finally:
        cli.deadline = time.monotonic() + 90
        if attempted:
            try:
                try:
                    owned = cli.rest(url)
                except Exception as error:
                    if getattr(error, "kind", None) == "not-found":
                        owned = None
                    else:
                        raise
                if owned is None and not provisioned:
                    raise StaffJobError(
                        "Unknown create outcome; early absence is not cleanup proof."
                    )
                if (
                    owned is not None
                    and owned.get("tags", {}).get("zava-forward-staff-run") != request["run"]
                ):
                    raise StaffJobError("Job ownership differs; refusing cleanup.")
                if not completed:
                    try:
                        if owned is not None:
                            cli.call(["containerapp", "job", "stop", "-g", "ama", "-n", name])
                    except Exception:
                        # Deletion is still required if stopping is denied or its response is lost.
                        completed = False
                if owned is not None:
                    cli.rest(url, method="DELETE")
                for _ in range(30):
                    try:
                        cli.rest(url)
                    except Exception as error:
                        if getattr(error, "kind", None) == "not-found":
                            break
                        raise
                    time.sleep(2)
                else:
                    raise StaffJobError("Job deletion was not confirmed.")
                clear_result(cli, target["relay"], request)
            except Exception:
                cli.deadline = previous_deadline
                raise StaffJobError(
                    f"Azure staff cleanup NOT confirmed. Stop/delete only owned job {name} in ama "
                    "(see runbook); its roster secret or encrypted relay tags may remain. "
                    "SQL/restart outcome is unverified."
                ) from None
        cli.deadline = previous_deadline
