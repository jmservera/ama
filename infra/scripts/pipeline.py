#!/usr/bin/env python3
"""Bounded, quiet CI deployment operations; never provisions identities or resource groups."""

import argparse
import base64
import hashlib
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
from pathlib import Path
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
PARAMETER_FILES = {
    "dev": "main.bicepparam",
    "test": "main.test.bicepparam",
    "pilot": "main.pilot.example.bicepparam",
}
OVERRIDES = {
    "location",
    "sqlLocation",
    "regionCheckReference",
    "quotaCheckReference",
    "alertEmail",
    "sqlAdminGroupName",
    "sqlAdminGroupObjectId",
    "entraClientId",
    "entraBearerOnly",
}


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
    for key in ("location", "sqlLocation"):
        if not re.fullmatch(r"[a-z][a-z0-9]+", overrides[key]):
            raise PipelineError(f"Invalid region parameter: {key}")
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


def release_images(directory: Path, server: str) -> dict[str, str]:
    images: dict[str, str] = {}
    for project in PROJECTS:
        record = json.loads((directory / f"{project}.json").read_text())
        image = record["image"]
        if (
            record["project"] != project
            or record["source_sha"] != source_sha()
            or record["tag"] != release_tag()
            or not re.fullmatch(
                re.escape(f"{server}/zava-forward-{project}@sha256:") + r"[0-9a-f]{64}", image
            )
        ):
            raise PipelineError("Release metadata does not match this run, project and registry")
        # Deploy identity must have AcrPull only, without quarantine bypass.
        run("docker", "pull", image)
        images[IMAGE_PARAMETERS[project]] = image
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
            if not isinstance(image, str) or "@sha256:" not in image:
                raise PipelineError("PR planning requires existing immutable workload images")
            compiled["parameters"][key] = {"value": image}
        maintenance = [
            item["properties"]["template"]["containers"][0]["image"]
            for item in jobs
            if item.get("name")
            in {
                f"job-forward-{environment}-auth-renewal",
                f"job-forward-{environment}-ledger-verify",
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
            summary["deployment_status"] = "Failed"
        output.write_text(json.dumps(summary, indent=2) + "\n")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation", choices=("plan", "deploy", "publish", "changed-images", "verify-environment")
    )
    parser.add_argument("--environment", choices=tuple(PARAMETER_FILES), default="dev")
    parser.add_argument("--infra", type=Path, default=ROOT / "infra")
    parser.add_argument("--output", type=Path, default=Path("what-if-summary.json"))
    parser.add_argument("--images", type=Path)
    parser.add_argument("--project", choices=PROJECTS)
    parser.add_argument("--github-environment")
    args = parser.parse_args()
    try:
        if args.operation == "verify-environment":
            if not args.github_environment:
                raise PipelineError("A protected GitHub environment is required")
            verify_environment(args.github_environment)
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
