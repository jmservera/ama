#!/usr/bin/env python3
"""Resolve the orchestrator image before an infrastructure what-if or deployment."""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER = "mcr.microsoft.com/k8se/quickstart:latest"
INFRA = Path(__file__).resolve().parents[1]
REPOSITORY = "zava-forward-orchestrator"


class DeploymentError(RuntimeError):
    """Discovery failed; deployment must not continue with a guessed image."""


def az_json(*args: str) -> Any:
    result = subprocess.run(
        ["az", *args, "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise DeploymentError(f"az {' '.join(args[:3])} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise DeploymentError(f"az {' '.join(args[:3])} returned invalid JSON") from exc


def resolve_image(group: str, prefix: str, registry: str) -> tuple[str, str]:
    jobs = az_json("containerapp", "job", "list", "--resource-group", group)
    if not isinstance(jobs, list):
        raise DeploymentError("Job discovery did not return a list")
    targets = {
        f"job-{prefix}-{suffix}" for suffix in ("orchestrator", "auth-renewal", "ledger-verify")
    }
    images: set[str] = set()
    for job in jobs:
        if not isinstance(job, dict) or not isinstance(job.get("name"), str):
            raise DeploymentError("Job discovery returned an invalid job")
        if job["name"] not in targets:
            continue
        try:
            containers = job["properties"]["template"]["containers"]
            if not isinstance(containers, list) or len(containers) != 1:
                raise DeploymentError(f"Expected one container in {job['name']}")
            image = containers[0]["image"]
        except (KeyError, TypeError, IndexError) as exc:
            raise DeploymentError(f"Missing container image in {job['name']}") from exc
        if not isinstance(image, str) or not image.strip():
            raise DeploymentError(f"Empty or invalid container image in {job['name']}")
        if image != PLACEHOLDER:
            images.add(image)
    if len(images) > 1:
        raise DeploymentError(
            "Existing jobs have conflicting real images; choose --orchestrator-image explicitly"
        )
    if images:
        return next(iter(images)), "existing job"

    registries = az_json("acr", "list", "--resource-group", group)
    if not isinstance(registries, list) or any(
        not isinstance(r, dict) or not isinstance(r.get("name"), str) for r in registries
    ):
        raise DeploymentError("Registry discovery did not return a list of registries")
    matches = [r for r in registries if r.get("name") == registry]
    if not matches:
        return PLACEHOLDER, "no existing job image or registry"
    if len(matches) != 1 or not isinstance(matches[0].get("loginServer"), str):
        raise DeploymentError("Registry discovery returned an invalid login server")
    server = matches[0]["loginServer"]
    if not server:
        raise DeploymentError("Registry login server is empty")
    repositories = az_json("acr", "repository", "list", "--name", registry)
    if not isinstance(repositories, list) or any(not isinstance(r, str) for r in repositories):
        raise DeploymentError("Repository discovery did not return a list of names")
    if REPOSITORY not in repositories:
        return PLACEHOLDER, "no existing job image or repository"
    tags = az_json(
        "acr",
        "repository",
        "show-tags",
        "--name",
        registry,
        "--repository",
        REPOSITORY,
        "--orderby",
        "time_desc",
        "--top",
        "1",
    )
    if not isinstance(tags, list) or any(not isinstance(t, str) or not t.strip() for t in tags):
        raise DeploymentError("Registry tag discovery did not return a list of tags")
    if not tags:
        return PLACEHOLDER, "no existing job image or repository tags"
    return f"{server}/{REPOSITORY}:{tags[0]}", "newest registry tag (time_desc)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--parameters", required=True, help="Bicep parameter file")
    parser.add_argument("--registry", required=True, help="Registry name in the resource group")
    parser.add_argument("--workload", default="forward")
    parser.add_argument("--environment", choices=("dev", "test", "pilot"), default="dev")
    parser.add_argument("--orchestrator-image", default="")
    parser.add_argument("--parameter", action="append", default=[], metavar="NAME=VALUE")
    parser.add_argument(
        "--apply", action="store_true", help="Deploy instead of the default what-if"
    )
    args = parser.parse_args()
    for value in args.parameter:
        name, separator, _ = value.partition("=")
        if (
            not separator
            or not name
            or name in {"orchestratorImage", "workload", "environmentName"}
        ):
            parser.error("Use named options for image/workload/environment; others need NAME=VALUE")
    try:
        image, source = (
            (args.orchestrator_image, "explicit --orchestrator-image")
            if args.orchestrator_image
            else resolve_image(
                args.resource_group, f"{args.workload}-{args.environment}", args.registry
            )
        )
        print(f"orchestratorImage={image} (source: {source})", flush=True)
        if image == PLACEHOLDER:
            print(
                "WARNING: placeholder image selected; Python maintenance jobs cannot run on it.",
                file=sys.stderr,
                flush=True,
            )
        command = [
            "az",
            "deployment",
            "group",
            "create" if args.apply else "what-if",
            "--resource-group",
            args.resource_group,
            "--template-file",
            str(INFRA / "main.bicep"),
            "--parameters",
            args.parameters,
        ]
        for parameter in [
            *args.parameter,
            f"workload={args.workload}",
            f"environmentName={args.environment}",
            f"orchestratorImage={image}",
        ]:
            command.extend(["--parameters", parameter])
        return subprocess.run(command, check=False).returncode
    except (DeploymentError, OSError) as exc:
        print(f"Deployment stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
