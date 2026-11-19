#!/usr/bin/env python3
"""Bounded, quiet CI deployment operations; never provisions identities or resource groups."""

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any
from uuid import UUID

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ("api", "agents", "orchestrator", "importer")
IMAGE_PARAMETERS = {
    "api": "apiImage",
    "agents": "agentImage",
    "orchestrator": "orchestratorImage",
    "importer": "importImage",
}
RELEASE_MANIFEST_FILE = "release-manifest.json"
PLAN_IMMUTABLE_IMAGE_RE = re.compile(r"^[a-z0-9.-]+/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$")
WORKLOAD_IMAGE_PARAMETERS = {
    "api": "apiImage",
    "agents": "agentImage",
    "orchestrator": "orchestratorImage",
    "auth-renewal": "orchestratorImage",
    "ledger-verify": "orchestratorImage",
    "rank-publish": "orchestratorImage",
    "import": "importImage",
}
HARDENING_CONTRACT: dict[str, Any] = {
    "uid": 10001,
    "gid": 10001,
    "read_only_rootfs_compatible": True,
    "writable_scratch_mounts": ["/tmp", "/state"],
    "capabilities_dropped": ["ALL"],
    "no_new_privileges": True,
    "runtime_enforcement_env": "ZF_CONTAINER_HARDENING=enforced",
}
PARAMETER_FILES = {
    "dev": "main.bicepparam",
    "test": "main.test.bicepparam",
    "pilot": "main.pilot.example.bicepparam",
}
ENVIRONMENT_PARAMETER_FILES = {
    "dev": "parameters/dev.bicepparam",
    "prod": "parameters/prod.bicepparam",
}
OVERRIDES = {
    "location",
    "sqlLocation",
    "aiModelLocation",
    "regionCheckReference",
    "quotaCheckReference",
    "alertEmail",
    "sqlAdminGroupName",
    "sqlAdminGroupObjectId",
    "entraClientId",
    "entraBearerOnly",
}
INJECTED_PARAMETERS = frozenset(
    OVERRIDES
    | {
        "workload",
        "environmentName",
        "allowPublicNetworkAccess",
        "deployApplications",
    }
    | set(IMAGE_PARAMETERS.values())
)


@dataclass(frozen=True)
class FromEmptyStep:
    """Canonical step registration in the reproducible from-empty deployment sequence."""

    step_id: str
    pipeline_hook: str
    rebuild_stages: tuple[str, ...]
    artifacts: tuple[str, ...]
    manual_prerequisite_owner: str | None
    description: str


FROM_EMPTY_STEP_ORDER: tuple[str, ...] = (
    "preflight",
    "what-if",
    "deploy",
    "sql-init",
    "seed",
    "smoke",
)
FROM_EMPTY_STEPS: tuple[FromEmptyStep, ...] = (
    FromEmptyStep(
        step_id="preflight",
        pipeline_hook="verify-environment",
        rebuild_stages=("parameters",),
        artifacts=(
            "infra/scripts/pipeline.py",
            "infra/scripts/tenant-readiness-preflight.py",
            "infra/entra/app-registration.json",
            "infra/secret-inventory.json",
            "infra/defender-decision.json",
        ),
        manual_prerequisite_owner="Juan Manuel Servera (@jmservera)",
        description=(
            "Validate tenant readiness, secret inventory, Defender/policy governance baseline, "
            "and protected GitHub deployment environment rules."
        ),
    ),
    FromEmptyStep(
        step_id="what-if",
        pipeline_hook="plan",
        rebuild_stages=("dependencies",),
        artifacts=(
            "infra/main.bicep",
            "infra/governance.bicep",
            "infra/parameters/dev.bicepparam",
            "infra/parameters/prod.bicepparam",
            "infra/scripts/deploy.py",
            "infra/scripts/pipeline.py",
        ),
        manual_prerequisite_owner=None,
        description=(
            "Compile environment parameters, enforce compile-time isolation guards, "
            "and summarize resource-group ARM what-if changes inside ama."
        ),
    ),
    FromEmptyStep(
        step_id="deploy",
        pipeline_hook="publish,deploy",
        rebuild_stages=(
            "discover",
            "images",
            "credential",
            "applications",
            "authentication",
        ),
        artifacts=(
            "infra/main.bicep",
            "infra/modules/containerapps.bicep",
            "src/api/Dockerfile",
            "src/agents/Dockerfile",
            "src/orchestrator/Dockerfile",
            "src/importer/Dockerfile",
            "infra/scripts/deploy.py",
            "infra/scripts/pipeline.py",
            "infra/scripts/setup-entra.py",
            "infra/scripts/credential_arm.py",
        ),
        manual_prerequisite_owner=None,
        description=(
            "Publish immutable ACR image digests, apply ARM resource-group deployment, "
            "and reconcile Entra application credentials and EasyAuth bindings."
        ),
    ),
    FromEmptyStep(
        step_id="sql-init",
        pipeline_hook="check_sql",
        rebuild_stages=("sql-users",),
        artifacts=(
            "infra/scripts/create-sql-users.py",
            "infra/scripts/create-sql-users.sql",
            "infra/sql/resident-showcase.sql",
            "infra/sql/resident-assistant.sql",
            "infra/staff-initializer-rbac.bicep",
        ),
        manual_prerequisite_owner=None,
        description=(
            "Verify private-only Azure SQL posture and apply idempotent contained Entra "
            "database users, least-privilege role grants, and SQL DDL scripts."
        ),
    ),
    FromEmptyStep(
        step_id="seed",
        pipeline_hook="seed",
        rebuild_stages=("seed", "staff"),
        artifacts=(
            "src/importer/Dockerfile",
            "src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py",
            "infra/scripts/resident_sensor_seed.py",
            "infra/scripts/initialize-workbench-staff.py",
        ),
        manual_prerequisite_owner=None,
        description=(
            "Load deterministic synthetic retrofit and IoT sensor records without reseeding "
            "populated stores, and reconcile synthetic staff roster bindings."
        ),
    ),
    FromEmptyStep(
        step_id="smoke",
        pipeline_hook="smoke",
        rebuild_stages=(
            "health",
            "api-denial",
            "browser-redirect",
            "workload-sql",
            "model-standard",
            "model-capable",
            "restart",
        ),
        artifacts=(
            "infra/scripts/pipeline.py",
            "infra/scripts/private-cutover-proof.py",
            "src/orchestrator/src/zava_forward/orchestrator/rebuild.py",
            "src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py",
        ),
        manual_prerequisite_owner=None,
        description=(
            "Execute post-deployment health, three unauthenticated/forged-header 401 denials, "
            "browser sign-in redirect, private SQL/AI round-trips, and replica restart checks."
        ),
    ),
)
FORBIDDEN_CHECK_PATTERN = re.compile(
    r"(?:placeholder|example\.invalid|n/a"
    r"|(?<![a-z0-9])(?:todo|tbd|assumed|assumption|unverified|pending|unknown|none|na|skip)(?![a-z0-9]))",
    re.IGNORECASE,
)
EMBEDDED_UUID_PATTERN = re.compile(
    r"(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])",
    re.IGNORECASE,
)
FORBIDDEN_REGION_SLUGS = frozenset(
    {
        "placeholder",
        "todo",
        "tbd",
        "assumed",
        "assumption",
        "unverified",
        "pending",
        "unknown",
        "none",
        "na",
        "skip",
    }
)


class PipelineError(RuntimeError):
    """A bounded operation failed; raw command output is deliberately not logged."""


def run(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode:
        raise PipelineError(
            f"{args[0]} operation failed (exit {result.returncode}); output withheld"
        )
    return result.stdout


def az(*args: str) -> Any:
    return json.loads(run("az", *args, "--only-show-errors", "--output", "json"))


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise PipelineError(f"Missing environment variable: {name}")
    return value


def source_sha() -> str:
    value = required("RELEASE_SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise PipelineError("Invalid release SHA")
    return value


def release_tag() -> str:
    run_id, attempt = required("GITHUB_RUN_ID"), required("GITHUB_RUN_ATTEMPT")
    if not run_id.isdecimal() or not attempt.isdecimal():
        raise PipelineError("Invalid workflow run identity")
    return f"sha-{source_sha()}-r{run_id}-a{attempt}"


def changed_images(paths: list[str]) -> list[str]:
    """Per-project path filters include core and the API's agents dependency."""
    selected: set[str] = set()
    for path in paths:
        parts = path.split("/")
        if path.startswith((".github/workflows/", "infra/")):
            selected.update(PROJECTS)
        elif len(parts) >= 2 and parts[0] == "src":
            project = parts[1]
            if project == "core" or project not in PROJECTS:
                selected.update(PROJECTS)
            else:
                selected.add(project)
                if project == "agents":
                    selected.add("api")
    return [project for project in PROJECTS if project in selected]


def parameters(infra: Path, environment: str) -> dict[str, Any]:
    compiled = az(
        "bicep", "build-params", "--file", str(infra / PARAMETER_FILES[environment]), "--stdout"
    )
    compiled = json.loads(compiled["parametersJson"])
    if not isinstance(compiled, dict) or not isinstance(compiled.get("parameters"), dict):
        raise PipelineError("Bicep compiler did not return ARM parameters")
    values = compiled["parameters"]
    overrides = json.loads(required("DEPLOY_PARAMETERS"))
    if not isinstance(overrides, dict) or set(overrides) != OVERRIDES:
        raise PipelineError("DEPLOY_PARAMETERS must contain exactly the documented override keys")
    for key, value in overrides.items():
        if key == "entraBearerOnly":
            if not isinstance(value, bool):
                raise PipelineError("entraBearerOnly must be an explicit boolean")
            values[key] = {"value": value}
            continue
        if not isinstance(value, str) or not value.strip() or "PLACEHOLDER" in value:
            raise PipelineError(f"Missing or invalid parameter: {key}")
        if "example.invalid" in value:
            raise PipelineError(f"Unresolved example parameter: {key}")
        values[key] = {"value": value}
    for key in ("sqlAdminGroupObjectId", "entraClientId"):
        if UUID(overrides[key]).int == 0:
            raise PipelineError(f"Unresolved identity parameter: {key}")
    for key in ("regionCheckReference", "quotaCheckReference"):
        normalized_check = overrides[key].strip()
        if (
            not normalized_check
            or FORBIDDEN_CHECK_PATTERN.search(normalized_check)
            or EMBEDDED_UUID_PATTERN.search(normalized_check)
        ):
            raise PipelineError(f"Unresolved or invalid recorded check parameter: {key}")
    for key in ("location", "sqlLocation", "aiModelLocation"):
        region_slug = overrides[key]
        if (
            not re.fullmatch(r"[a-z][a-z0-9]+", region_slug)
            or region_slug in FORBIDDEN_REGION_SLUGS
            or "placeholder" in region_slug
        ):
            raise PipelineError(f"Invalid region parameter: {key}")
    if overrides["location"] != "uksouth":
        raise PipelineError("Primary location parameter must be uksouth")
    values.update(
        {
            "workload": {"value": "forward"},
            "environmentName": {"value": environment},
            "allowPublicNetworkAccess": {"value": False},
            "deployApplications": {"value": True},
        }
    )
    return compiled


def registry() -> str:
    name = required("AZURE_REGISTRY_NAME")
    if not re.fullmatch(r"[a-zA-Z0-9]{5,50}", name):
        raise PipelineError("Invalid registry name")
    # Name resolution and membership are checked in ama, not subscription-wide.
    record = az("acr", "show", "--resource-group", "ama", "--name", name)
    server = record["loginServer"]
    if not isinstance(server, str) or not re.fullmatch(r"[a-z0-9.-]+", server):
        raise PipelineError("Invalid registry login server")
    run("az", "acr", "login", "--resource-group", "ama", "--name", name, "--only-show-errors")
    return server


def publish(project: str, destination: Path) -> None:
    server = registry()
    image = f"{server}/zava-forward-{project}:{release_tag()}"
    run("docker", "load", "--input", str(destination / f"{project}.tar"))
    run("docker", "tag", f"zava-forward-{project}:release", image)
    run("docker", "push", image)
    digests = json.loads(run("docker", "inspect", "--format", "{{json .RepoDigests}}", image))
    matches = [
        digest
        for digest in digests
        if re.fullmatch(
            re.escape(f"{server}/zava-forward-{project}@sha256:") + r"[0-9a-f]{64}", digest
        )
    ]
    if len(matches) != 1:
        raise PipelineError("Push did not produce exactly one expected immutable digest")
    (destination / f"{project}.json").write_text(
        json.dumps(
            {
                "project": project,
                "image": matches[0],
                "source_sha": source_sha(),
                "tag": release_tag(),
            }
        )
        + "\n"
    )


def build_release_manifest(directory: Path, server: str) -> dict[str, Any]:
    sha = source_sha()
    tag = release_tag()
    project_records: dict[str, dict[str, str]] = {}
    parameter_images: dict[str, str] = {}
    for project in PROJECTS:
        record_path = directory / f"{project}.json"
        if not record_path.is_file():
            raise PipelineError(f"Missing release metadata file for project {project}")
        record = json.loads(record_path.read_text())
        if not isinstance(record, dict):
            raise PipelineError("Release metadata record must be a JSON object")
        image = record.get("image")
        if (
            record.get("project") != project
            or record.get("source_sha") != sha
            or record.get("tag") != tag
            or not isinstance(image, str)
            or "quickstart" in image.lower()
            or not re.fullmatch(
                re.escape(f"{server}/zava-forward-{project}@sha256:") + r"[0-9a-f]{64}", image
            )
        ):
            raise PipelineError("Release metadata does not match this run, project and registry")
        parameter_key = IMAGE_PARAMETERS[project]
        project_records[project] = {
            "dockerfile": f"src/{project}/Dockerfile",
            "image": image,
            "parameter": parameter_key,
            "repository": f"zava-forward-{project}",
        }
        parameter_images[parameter_key] = image
    workloads = {
        workload: {
            "image": parameter_images[param_key],
            "parameter": param_key,
        }
        for workload, param_key in WORKLOAD_IMAGE_PARAMETERS.items()
    }
    return {
        "schema_version": 1,
        "registry": server,
        "source_sha": sha,
        "tag": tag,
        "hardening": dict(HARDENING_CONTRACT),
        "projects": project_records,
        "workloads": workloads,
    }


def verify_release_manifest(manifest: dict[str, Any], server: str) -> dict[str, str]:
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version") != 1
        or manifest.get("registry") != server
        or manifest.get("source_sha") != source_sha()
        or manifest.get("tag") != release_tag()
        or manifest.get("hardening") != HARDENING_CONTRACT
    ):
        raise PipelineError("Release manifest metadata or hardening contract is invalid")
    projects = manifest.get("projects")
    workloads = manifest.get("workloads")
    if not isinstance(projects, dict) or set(projects) != set(PROJECTS):
        raise PipelineError("Release manifest projects do not match canonical workload set")
    if not isinstance(workloads, dict) or set(workloads) != set(WORKLOAD_IMAGE_PARAMETERS):
        raise PipelineError("Release manifest workloads do not cover all hosted apps and jobs")
    images: dict[str, str] = {}
    for project in PROJECTS:
        entry = projects[project]
        if not isinstance(entry, dict):
            raise PipelineError("Release manifest project entry must be an object")
        image = entry.get("image")
        expected_param = IMAGE_PARAMETERS[project]
        if (
            entry.get("parameter") != expected_param
            or entry.get("dockerfile") != f"src/{project}/Dockerfile"
            or entry.get("repository") != f"zava-forward-{project}"
            or not isinstance(image, str)
            or "quickstart" in image.lower()
            or not re.fullmatch(
                re.escape(f"{server}/zava-forward-{project}@sha256:") + r"[0-9a-f]{64}", image
            )
        ):
            raise PipelineError("Release metadata does not match this run, project and registry")
        images[expected_param] = image
    for workload, expected_param in WORKLOAD_IMAGE_PARAMETERS.items():
        binding = workloads[workload]
        if (
            not isinstance(binding, dict)
            or binding.get("parameter") != expected_param
            or binding.get("image") != images[expected_param]
        ):
            raise PipelineError(f"Release manifest workload {workload} image binding mismatch")
    return images


def release_images(directory: Path, server: str) -> dict[str, str]:
    manifest = build_release_manifest(directory, server)
    images = verify_release_manifest(manifest, server)
    (directory / RELEASE_MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    for project in PROJECTS:
        image = images[IMAGE_PARAMETERS[project]]
        # Deploy identity must have AcrPull only, without quarantine bypass.
        run("docker", "pull", image)
    return images


def check_sql() -> None:
    servers = az("sql", "server", "list", "--resource-group", "ama")
    if not isinstance(servers, list) or not servers:
        raise PipelineError("Existing private SQL prerequisite is missing")
    if any(server.get("publicNetworkAccess") != "Disabled" for server in servers):
        raise PipelineError("SQL public access must remain Disabled for every server in ama")


def verify_environment(name: str) -> None:
    if not re.fullmatch(r"(dev|test|pilot)(-plan|-release)?", name):
        raise PipelineError("Invalid GitHub environment")
    repository = required("GITHUB_REPOSITORY")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise PipelineError("Invalid GitHub repository")
    record = json.loads(run("gh", "api", f"repos/{repository}/environments/{name}"))
    reviewers = [
        rule for rule in record["protection_rules"] if rule["type"] == "required_reviewers"
    ]
    if (
        len(reviewers) != 1
        or not reviewers[0].get("reviewers")
        or reviewers[0].get("prevent_self_review") is not True
        or record.get("can_admins_bypass") is not False
        or not isinstance(record.get("deployment_branch_policy"), dict)
        or record["deployment_branch_policy"].get("protected_branches") is not True
    ):
        raise PipelineError(
            "Environment requires reviewers, no self-review/bypass and branch rules"
        )


def verify_federation(identity: str, kind: str, environment: str) -> None:
    """Read-only check that an identity trusts only this repository's exact environment subject."""
    if not re.fullmatch(r"(dev|test|pilot)(-plan|-release)?", environment):
        raise PipelineError("Invalid GitHub environment")
    if kind not in ("managed", "app") or not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", identity):
        raise PipelineError("Invalid federated identity reference")
    repository = required("GITHUB_REPOSITORY")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise PipelineError("Invalid GitHub repository")
    if kind == "managed":
        credentials = az(
            "identity", "federated-credential", "list",
            "--identity-name", identity, "--resource-group", "ama",
        )  # fmt: skip
    else:
        credentials = az("ad", "app", "federated-credential", "list", "--id", identity)
        secrets = az("ad", "app", "show", "--id", identity, "--query", "passwordCredentials")
        if secrets:
            raise PipelineError("Federated identity must not hold client secrets")
    expected = {
        "issuer": "https://token.actions.githubusercontent.com",
        "audiences": ["api://AzureADTokenExchange"],
        "subject": f"repo:{repository}:environment:{environment}",
    }
    if not isinstance(credentials, list) or not credentials:
        raise PipelineError("No federated credential is configured")
    for credential in credentials:
        if any(credential.get(key) != value for key, value in expected.items()):
            raise PipelineError("Federated credential is not scoped to the exact environment")


def summarize_plan(plan: Any, subscription: str, sha: str) -> dict[str, Any]:
    if not isinstance(plan, dict) or plan.get("status") != "Succeeded":
        raise PipelineError("What-if did not succeed")
    changes = plan.get("changes")
    if not isinstance(changes, list):
        raise PipelineError("What-if changes are missing")
    counts: Counter[str] = Counter()
    for change in changes:
        resource = change.get("resourceId", "")
        prefix = f"/subscriptions/{subscription}/resourceGroups/ama/providers/"
        if not isinstance(resource, str) or not resource.lower().startswith(prefix.lower()):
            raise PipelineError("What-if includes a resource outside ama")
        kind = change.get("changeType")
        if kind not in {"Create", "Modify", "NoChange"}:
            raise PipelineError("What-if contains deletion or unresolved/unsupported changes")
        after = change.get("after") or {}
        if str(after.get("type", "")).lower() == "microsoft.sql/servers":
            if after.get("properties", {}).get("publicNetworkAccess") != "Disabled":
                raise PipelineError("What-if SQL public access is not Disabled")
        counts[kind] += 1
    # Never publish resource IDs, names, deltas, parameters or Azure messages.
    return {"source_sha": sha, "status": "Succeeded", "change_counts": dict(counts)}


def publish_step_summary(title: str, lines: list[str]) -> None:
    """Attach a sanitized result to the workflow run summary shown on the PR checks."""
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    with open(target, "a", encoding="utf-8") as handle:
        handle.write("\n".join([f"### {title}", "", *lines, ""]) + "\n")


def what_if_lines(summary: dict[str, Any], environment: str) -> list[str]:
    counts = summary.get("change_counts", {})
    return [
        f"* Environment: {environment}",
        f"* Source revision: {summary['source_sha']}",
        *(f"* {kind}: {counts.get(kind, 0)}" for kind in ("Create", "Modify", "NoChange")),
        "* Deletions, resource names, deltas and parameters are never listed.",
    ]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def smoke(base_url: str, attempts: int = 6, delay: float = 10, browser: bool = False) -> None:
    opener = urllib.request.build_opener(NoRedirect())
    forged = base64.b64encode(
        json.dumps({"auth_typ": "aad", "claims": [{"typ": "oid", "val": "forged"}]}).encode()
    ).decode()
    probes = [
        ("health", "/healthz", {}, 200),
        ("anonymous", "/api/me", {}, 401),
        ("malformed-bearer", "/api/me", {"Authorization": "Bearer invalid"}, 401),
        ("forged-principal", "/api/me", {"X-MS-CLIENT-PRINCIPAL": forged}, 401),
    ]
    if browser:
        probes.append(("browser-sign-in", "/sign-in", {}, 302))
    for name, path, headers, expected in probes:
        for attempt in range(attempts if name == "health" else 1):
            try:
                with opener.open(
                    urllib.request.Request(base_url + path, headers=headers), timeout=20
                ) as response:
                    status = response.status
            except urllib.error.HTTPError as exc:
                status = exc.code
                exc.close()
            except urllib.error.URLError:
                status = 0
            if status == expected:
                break
            if name != "health" or attempt == attempts - 1:
                raise PipelineError(
                    f"Post-deployment {name} check failed; expected HTTP {expected}"
                )
            time.sleep(delay)
    print("Post-deployment health and all three authentication-denial checks passed")


def deployment(infra: Path, environment: str, output: Path, images_directory: Path | None) -> None:
    sha = source_sha()
    output.write_text(json.dumps({"source_sha": sha, "status": "Failed"}) + "\n")
    subscription = str(UUID(required("AZURE_SUBSCRIPTION_ID")))
    compiled = parameters(infra, environment)
    existing = az("containerapp", "list", "--resource-group", "ama")
    if not isinstance(existing, list) or any(not isinstance(item, dict) for item in existing):
        raise PipelineError("Cannot read deployed authentication state; deployment stopped")
    if any((item.get("tags") or {}).get("zava-forward-auth-lock") for item in existing):
        raise PipelineError("Authentication setup holds an advisory lock; wait before deploying")
    if any(
        (item.get("tags") or {}).get("zava-forward-credential-store") == "app" for item in existing
    ):
        raise PipelineError(
            "App-local demo credential detected; this Key Vault pipeline cannot overwrite it. "
            "Use the guarded dependency-only deployment with entraCredentialStore=app "
            "and deployApplications=false"
        )
    if images_directory is not None:
        images = release_images(images_directory, registry())
        compiled["parameters"].update({key: {"value": value} for key, value in images.items()})
    else:
        # Plan the actual deployed images, never replace an existing job by a placeholder.
        jobs = az("containerapp", "job", "list", "--resource-group", "ama")
        targets = {
            "apiImage": f"ca-forward-{environment}-api",
            "agentImage": f"ca-forward-{environment}-agents",
            "orchestratorImage": f"job-forward-{environment}-orchestrator",
            "importImage": f"job-forward-{environment}-import",
        }
        for key, name in targets.items():
            matches = [item for item in [*existing, *jobs] if item.get("name") == name]
            if len(matches) != 1:
                raise PipelineError("PR planning requires all four initialized workload resources")
            image = matches[0]["properties"]["template"]["containers"][0]["image"]
            if (
                not isinstance(image, str)
                or "quickstart" in image.lower()
                or PLAN_IMMUTABLE_IMAGE_RE.fullmatch(image) is None
            ):
                raise PipelineError("PR planning requires existing immutable workload images")
            compiled["parameters"][key] = {"value": image}
        maintenance = [
            item["properties"]["template"]["containers"][0]["image"]
            for item in jobs
            if item.get("name")
            in {
                f"job-forward-{environment}-auth-renewal",
                f"job-forward-{environment}-ledger-verify",
                f"job-forward-{environment}-rank-publish",
            }
        ]
        if any(
            image != compiled["parameters"]["orchestratorImage"]["value"] for image in maintenance
        ):
            raise PipelineError("Existing maintenance jobs have conflicting orchestrator images")
    check_sql()
    with tempfile.TemporaryDirectory(prefix="ama-pipeline-") as temporary:
        parameter_file = Path(temporary) / "parameters.json"
        parameter_file.write_text(json.dumps(compiled))
        parameter_file.chmod(0o600)
        command = (
            "--resource-group",
            "ama",
            "--template-file",
            str(infra / "main.bicep"),
            "--parameters",
            f"@{parameter_file}",
            "--mode",
            "Incremental",
        )
        plan = az("deployment", "group", "what-if", *command, "--no-pretty-print")
        summary = summarize_plan(plan, subscription, sha)
        summary["parameter_sha256"] = hashlib.sha256(parameter_file.read_bytes()).hexdigest()
        if images_directory is not None:
            manifest_path = images_directory / RELEASE_MANIFEST_FILE
            if manifest_path.is_file():
                summary["release_manifest"] = json.loads(manifest_path.read_text())
            summary["deployment_status"] = "Failed"
        output.write_text(json.dumps(summary, indent=2) + "\n")
        publish_step_summary("What-if result", what_if_lines(summary, environment))
        if images_directory is not None:
            result = az(
                "deployment",
                "group",
                "create",
                *command,
                "--name",
                f"release-{environment}-{required('GITHUB_RUN_ID')}",
            )
            if result["properties"]["provisioningState"] != "Succeeded":
                raise PipelineError("Deployment did not succeed")
            check_sql()
            host = result["properties"]["outputs"]["apiInternalFqdn"]["value"]
            if not isinstance(host, str) or not re.fullmatch(
                r"[a-z0-9.-]+\.azurecontainerapps\.io", host
            ):
                raise PipelineError("Deployment did not return a valid private API hostname")
            smoke(f"https://{host}", browser=not compiled["parameters"]["entraBearerOnly"]["value"])
            summary["deployment_status"] = "Succeeded"
            summary["checks"] = [
                "health-200",
                "anonymous-401",
                "malformed-401",
                "forged-401",
                "sql-private",
            ]
            output.write_text(json.dumps(summary, indent=2) + "\n")
            publish_step_summary(
                "Deployment result",
                [f"* Environment: {environment}", "* Status: Succeeded"]
                + [f"* Check passed: {name}" for name in summary["checks"]],
            )


def _load_reproducibility_module() -> ModuleType:
    module_name = "_ama_infra_reproducibility_check"
    cached = sys.modules.get(module_name)
    if isinstance(cached, ModuleType):
        return cached
    module_path = Path(__file__).resolve().with_name("reproducibility_check.py")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise PipelineError(f"Cannot load reproducibility verifier from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def execute_from_empty_dry_run(repo_root: Path = ROOT, environment: str = "dev") -> Any:
    module = _load_reproducibility_module()
    return module.execute_from_empty_dry_run(repo_root=repo_root, environment=environment)


def verify_from_empty_deployment_reproducibility(repo_root: Path = ROOT) -> Any:
    module = _load_reproducibility_module()
    return module.verify_from_empty_deployment_reproducibility(repo_root=repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        choices=(
            "plan",
            "deploy",
            "publish",
            "changed-images",
            "verify-environment",
            "verify-federation",
        ),
    )
    parser.add_argument("--environment", choices=tuple(PARAMETER_FILES), default="dev")
    parser.add_argument("--infra", type=Path, default=ROOT / "infra")
    parser.add_argument("--output", type=Path, default=Path("what-if-summary.json"))
    parser.add_argument("--images", type=Path)
    parser.add_argument("--project", choices=PROJECTS)
    parser.add_argument("--github-environment")
    parser.add_argument("--identity")
    parser.add_argument("--identity-kind", choices=("managed", "app"), default="managed")
    args = parser.parse_args()
    try:
        if args.operation == "verify-environment":
            if not args.github_environment:
                raise PipelineError("A protected GitHub environment is required")
            verify_environment(args.github_environment)
        elif args.operation == "verify-federation":
            if not args.github_environment or not args.identity:
                raise PipelineError("An identity and GitHub environment are required")
            verify_federation(args.identity, args.identity_kind, args.github_environment)
        elif args.operation == "changed-images":
            base = os.environ.get("BASE_SHA", "")
            head = os.environ.get("HEAD_SHA", "")
            if not base or set(base) == {"0"}:
                selected = list(PROJECTS)
            else:
                if not all(re.fullmatch(r"[0-9a-f]{40}", value) for value in (base, head)):
                    raise PipelineError("Invalid path-filter commit")
                selected = changed_images(
                    run("git", "diff", "--name-only", base, head).splitlines()
                )
            print(json.dumps(selected))
        elif args.operation == "publish":
            if args.project is None or args.images is None:
                raise PipelineError("Publish needs project and images")
            publish(args.project, args.images)
        else:
            if args.operation == "plan" and args.images is not None:
                raise PipelineError("Plan does not accept release metadata or apply deployments")
            if args.operation == "deploy" and args.images is None:
                raise PipelineError("Deploy requires release digest metadata")
            deployment(args.infra, args.environment, args.output, args.images)
        return 0
    except PipelineError as exc:
        print(f"Pipeline stopped: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        # Azure output, paths, parameters and exception values may contain identifiers.
        print(
            "Pipeline stopped: validation or external operation failed; raw output withheld",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
