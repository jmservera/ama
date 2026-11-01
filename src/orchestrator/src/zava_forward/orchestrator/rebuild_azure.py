"""Azure adapter for the ordered from-empty rebuild and teardown (Refs #148).

The default is a dry run that prints the plan and performs no I/O. Live operation needs an
explicit ``--apply`` and runs only argv lists (never a shell), so no secret appears on a command
line. Stages that have no scripted probe stop with exit status 2 and are never reported as passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .rebuild import (
    BUDGET,
    STAGES,
    Backend,
    Inventory,
    RebuildError,
    Resource,
    Stage,
    canonical,
    dry_run,
    teardown,
)

GROUP = "ama"
BUDGET_API = "2023-05-01"
VAULT_SECRET = "entra-client-secret"
PRIVATE_ENDPOINT = "microsoft.network/privateendpoints"
HEALTH_ATTEMPTS = 6
HEALTH_DELAY = 10.0
SQL_RESOURCE = "https://database.windows.net/"
OPERATOR_GATED = "operator-gated"
VERIFIED = "azure-verified"
GATED_STAGES = ("workload-sql", "model-standard", "model-capable")


class ScriptExit(RebuildError):
    """A command exited non-zero; keeps the status and output for callers that tolerate one."""

    def __init__(self, message: str, code: int, stdout: str):
        super().__init__(message)
        self.code, self.stdout = code, stdout


Runner = Callable[[Sequence[str], Mapping[str, str] | None], str]
Probe = Callable[[str, str], int]

_SECRET_ARG = re.compile(
    r"(?i)(^--?[\w-]*(secret|password|passwd|token|api-?key)[\w-]*$"
    r"|[\w-]*(secret|password|passwd|token|api-?key)[\w-]*\s*[=:]\s*\S"
    r"|eyJ[\w-]{10,}\.[\w-]{10,}"
    r"|[?&]sig=)"
)
_SAFE_ASSIGNMENT = re.compile(
    r"entraClientSecretName=[a-z][a-z0-9-]{0,126}|(enableEntraTokenStore|entraTokenStoreReady)=(true|false)"
)
_SAFE_PARAM_LINE = re.compile(
    r"\s*param\s+(entraClientSecretName|enableEntraTokenStore|entraTokenStoreReady)\b"
)
# Stage-controlled names and secure Bicep parameters that must never come from an override.
RESERVED_PARAMETERS = frozenset({"deployApplications", "deployEnvironmentOnly", "apiImage"})
SECURE_PARAMETERS = frozenset({"teamsWebhookUrl"})
_PUBLIC_REGISTRY = re.compile(
    r"(?s)deploymentProfile\s*[=:]\s*['\"]?development.*allowPublicNetworkAccess\s*[=:]\s*true"
)
_REMAINING_SQL = "Remaining: SQL binding and serving-replica restart are not confirmed."
_EMAIL = re.compile(r"[^\s@\"']+@([^\s@\"']+)")
_SYNTHETIC_DOMAIN = re.compile(r"(?i)(\.test|^example\.(com|org|net))$")
_NAME = re.compile(r"[a-z][a-z0-9-]{1,62}")
_TAG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def assert_no_secret_argv(argv: Sequence[str]) -> None:
    for part in argv:
        if _SAFE_ASSIGNMENT.fullmatch(part):
            continue
        if _SECRET_ARG.search(part):
            raise RebuildError("Refusing a command line that could carry a secret")


def assert_override(override: str) -> None:
    name, separator, _ = override.partition("=")
    if not separator:
        raise RebuildError("Overrides must be NAME=VALUE")
    if name in RESERVED_PARAMETERS:
        raise RebuildError(f"Parameter {name} is controlled by the rebuild stages")
    if name in SECURE_PARAMETERS:
        raise RebuildError(f"Secure parameter {name} must not be passed on a command line")
    assert_no_secret_argv([override])


def assert_synthetic(path: Path) -> None:
    """Reject a seed or roster file that holds a non-synthetic, email-like value."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RebuildError(f"Cannot read synthetic input {path.name}") from exc
    pending: list[Any] = [document]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
        elif isinstance(item, str):
            for match in _EMAIL.finditer(item):
                if not _SYNTHETIC_DOMAIN.search(match.group(1)):
                    raise RebuildError(f"{path.name} holds a non-synthetic address; stopped")


@dataclass(frozen=True)
class AzureConfig:
    subscription: str
    registry: str
    image_tag: str
    parameters: Path
    seed: Path
    roster: Path
    container_app: str
    environment: str = "test"
    workload: str = "forward"
    sql_database: str = "retrofit"
    identity_prefix: str | None = None
    repo_root: Path = field(default_factory=lambda: Path.cwd())
    overrides: tuple[str, ...] = ()
    build_pool: str | None = None

    def validate(self) -> None:
        for value in (self.registry, self.container_app, self.sql_database):
            if not _NAME.fullmatch(value):
                raise RebuildError("Invalid resource name")
        if self.build_pool is not None and not _NAME.fullmatch(self.build_pool):
            raise RebuildError("Invalid build pool name")
        if not _TAG.fullmatch(self.image_tag):
            raise RebuildError("Invalid image tag")
        if self.environment not in ("dev", "test", "pilot"):
            raise RebuildError("Invalid environment")
        for override in self.overrides:
            assert_override(override)
        assert_synthetic(self.seed)
        assert_synthetic(self.roster)

    def registry_is_private(self) -> bool:
        text = self.parameters.read_text(encoding="utf-8") if self.parameters.is_file() else ""
        return not _PUBLIC_REGISTRY.search("\n".join((text, *self.overrides)))

    @property
    def prefix(self) -> str:
        return self.identity_prefix or f"id-{self.workload}-{self.environment}"


def subprocess_runner(argv: Sequence[str], env: Mapping[str, str] | None = None) -> str:
    assert_no_secret_argv(argv)
    merged = {**os.environ, **env} if env else None
    result = subprocess.run(
        list(argv), capture_output=True, text=True, check=False, env=merged, timeout=3600
    )
    if result.returncode:
        raise ScriptExit(
            f"{argv[0]} {' '.join(argv[1:3])} failed ({result.returncode})",
            result.returncode,
            result.stdout,
        )
    return result.stdout


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def http_probe(url: str, mode: str) -> int:
    """Return the status of an unauthenticated GET; redirects are not followed."""
    if not url.startswith("https://"):
        raise RebuildError("Probes need an https URL")
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(url, timeout=30) as response:  # noqa: S310 - https enforced above
            return int(response.status)
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0


SEED_SNIPPET = (
    "import os;from zava_forward.core.factory import open_store;"
    "s=open_store(dict(os.environ));"
    "print(s.db.execute('SELECT COUNT(*) FROM cases').fetchone()[0])"
)


class AzureBackend:
    """Implements the rebuild Backend protocol over the az CLI and the existing helpers."""

    def __init__(
        self,
        config: AzureConfig,
        runner: Runner = subprocess_runner,
        probe: Probe = http_probe,
        sleep: Callable[[float], None] = time.sleep,
    ):
        config.validate()
        self.config, self.run, self.probe, self.sleep = config, runner, probe, sleep
        self.found: dict[str, str] = {}
        self.released: dict[str, frozenset[str]] = {}

    def _az(self, *args: str, env: Mapping[str, str] | None = None) -> str:
        return self.run(["az", *args], env)

    def _json(self, *args: str) -> Any:
        try:
            return json.loads(self._az(*args, "-o", "json"))
        except ValueError as exc:
            raise RebuildError("az returned invalid JSON") from exc

    def check_account(self) -> None:
        active = self._az("account", "show", "--query", "id", "-o", "tsv").strip()
        if active != self.config.subscription:
            raise RebuildError("Active subscription differs from the configured subscription")

    def inventory(self) -> Inventory:
        rows = self._json("resource", "list", "-g", GROUP)
        locks = self._json("lock", "list", "-g", GROUP)
        budgets = self._json(
            "rest",
            "--method",
            "get",
            "--url",
            f"https://management.azure.com/subscriptions/{self.config.subscription}"
            f"/resourceGroups/{GROUP}/providers/Microsoft.Consumption/budgets"
            f"?api-version={BUDGET_API}",
            "--query",
            "value",
        )
        if not all(isinstance(value, list) for value in (rows, locks, budgets)):
            raise RebuildError("Inventory responses were not lists")
        locked = bool(locks)
        resources = tuple(
            Resource(
                str(row["id"]),
                str(row["type"]),
                locked,
                str((row.get("tags") or {}).get("retain", "")).lower() == "true",
            )
            for row in rows
        )
        listed = tuple(Resource(str(row["id"]), BUDGET, locked, False) for row in budgets)
        return Inventory(resources, listed)

    def delete(self, resource: Resource) -> None:
        if resource.kind.lower() == BUDGET:
            self._az(
                "rest",
                "--method",
                "delete",
                "--url",
                f"https://management.azure.com{resource.resource_id}?api-version={BUDGET_API}",
            )
            return
        if resource.kind.lower() == PRIVATE_ENDPOINT:
            nics = self._json(
                "network",
                "private-endpoint",
                "show",
                "--ids",
                resource.resource_id,
                "--query",
                "networkInterfaces[].id",
            )
            if not isinstance(nics, list):
                raise RebuildError("Private endpoint interfaces were not a list")
            self.released[resource.resource_id] = frozenset(str(n) for n in nics)
        self._az("resource", "delete", "--ids", resource.resource_id)
        self._az("resource", "wait", "--deleted", "--ids", resource.resource_id, "--timeout", "900")

    def removed_with(self, resource: Resource) -> frozenset[str]:
        """Resource IDs that Azure removes together with this resource."""
        return self.released.get(resource.resource_id, frozenset())

    def _script(self, name: str, *args: str) -> str:
        script = self.config.repo_root / "infra" / "scripts" / name
        return self.run(["python3", str(script), *args], None)

    def _deploy(self, applications: bool) -> None:
        c = self.config
        args = [
            "--resource-group",
            GROUP,
            "--registry",
            c.registry,
            "--workload",
            c.workload,
            "--environment",
            c.environment,
            "--parameters",
            str(c.parameters),
            "--parameter",
            f"deployApplications={'true' if applications else 'false'}",
        ]
        if applications:
            args += [
                "--parameter",
                f"apiImage={self.found['registry']}/zava-forward-mvp:{c.image_tag}",
            ]
        for override in c.overrides:
            args += ["--parameter", override]
        self._script("deploy.py", *args, "--apply")

    def _sql_env(self, data: Path) -> dict[str, str]:
        token = self._az(
            "account",
            "get-access-token",
            "--resource",
            SQL_RESOURCE,
            "--query",
            "accessToken",
            "-o",
            "tsv",
        ).strip()
        return {
            "ZF_STORE": "mssql",
            "ZF_SQL_AUTH": "token",
            "ZF_SQL_TOKEN": token,
            "ZF_SQL_SERVER": f"{self.found['sql']}.database.windows.net",
            "ZF_SQL_DATABASE": self.config.sql_database,
            "ZF_DATA": str(data),
        }

    def _fqdn(self) -> str:
        fqdn = self._az(
            "containerapp",
            "show",
            "-g",
            GROUP,
            "-n",
            self.config.container_app,
            "--query",
            "properties.configuration.ingress.fqdn",
            "-o",
            "tsv",
        ).strip()
        if not fqdn:
            raise RebuildError("Application has no ingress FQDN")
        return fqdn

    def perform(self, stage: Stage) -> None:
        c, name = self.config, stage.name
        if name == "dependencies":
            self._deploy(False)
        elif name == "discover":
            for key, args in (
                ("registry_name", ("acr", "list")),
                ("sql", ("sql", "server", "list")),
                ("vault", ("keyvault", "list")),
            ):
                names = self._json(*args, "-g", GROUP, "--query", "[].name")
                if not isinstance(names, list) or len(names) != 1:
                    raise RebuildError(f"Expected exactly one {key} in {GROUP}")
                self.found[key] = str(names[0])
            if self.found["registry_name"] != c.registry:
                raise RebuildError("Discovered registry differs from the configured registry")
            self.found["registry"] = self._az(
                "acr", "show", "-n", c.registry, "--query", "loginServer", "-o", "tsv"
            ).strip()
        elif name == "images":
            pool = ["--agent-pool", c.build_pool] if c.build_pool else []
            self._az(
                "acr",
                "build",
                "--registry",
                c.registry,
                *pool,
                "--image",
                f"zava-forward-mvp:{c.image_tag}",
                "-f",
                "src/api/Dockerfile",
                str(c.repo_root / "src"),
            )
        elif name == "sql-users":
            self._script("create-sql-users.py", GROUP, self.found["sql"], c.sql_database, c.prefix)
        elif name == "seed":
            self.found["cases"] = self.run(
                ["python3", "-c", SEED_SNIPPET], self._sql_env(c.seed)
            ).strip()
        elif name == "applications":
            self._deploy(True)
        elif name == "staff":
            self._script(
                "initialize-workbench-staff.py",
                "--resource-group",
                GROUP,
                "--container-app",
                c.container_app,
                "--roster",
                str(c.roster),
                "--apply",
                "--restart",
            )
        elif name == "restart":
            self._az(
                "containerapp",
                "revision",
                "restart",
                "-g",
                GROUP,
                "-n",
                c.container_app,
                "--revision",
                self._az(
                    "containerapp",
                    "show",
                    "-g",
                    GROUP,
                    "-n",
                    c.container_app,
                    "--query",
                    "properties.latestRevisionName",
                    "-o",
                    "tsv",
                ).strip(),
            )

    def _check_authentication(self) -> None:
        """Run the Entra check; only the not-yet-reconciled SQL staff/restart item is tolerated."""
        c = self.config
        args = (
            "-g", GROUP, "-n", c.container_app, "--direct-ingress", "--roster", str(c.roster),
            "--check",
        )  # fmt: skip
        try:
            self._script("setup-entra.py", *args)
        except ScriptExit as exc:
            remaining = [x.strip() for x in exc.stdout.splitlines() if x.startswith("Remaining:")]
            clean = re.search(r"\b0 reconciliation item", exc.stdout) is not None
            if exc.code != 2 or not clean or remaining != [_REMAINING_SQL]:
                raise RebuildError("Entra authentication check reported drift or failed") from exc

    def _await_healthy(self) -> None:
        url = f"https://{self._fqdn()}/healthz"
        for attempt in range(HEALTH_ATTEMPTS):
            status = self.probe(url, "get")
            if status == 200:
                return
            transient = status == 0 or status >= 500
            if not transient or attempt == HEALTH_ATTEMPTS - 1:
                break
            self.sleep(HEALTH_DELAY)
        raise RebuildError(f"healthz returned {status}")

    def _expect(self, status: int, allowed: tuple[int, ...], what: str) -> None:
        if status not in allowed:
            raise RebuildError(f"{what} returned {status}")

    def verify(self, stage: Stage) -> str:
        c, name = self.config, stage.name
        if name == "parameters":
            self.check_account()
            if not c.parameters.is_file():
                raise RebuildError("Parameter file is missing")
            lines = c.parameters.read_text(encoding="utf-8").splitlines()
            if any(_SECRET_ARG.search(x) for x in lines if not _SAFE_PARAM_LINE.match(x)):
                raise RebuildError("Parameter file appears to hold a secret")
            if c.registry_is_private() and not c.build_pool:
                raise RebuildError(
                    "A private registry needs an approved --build-pool; default az acr build "
                    "cannot reach it. Stopped before provisioning"
                )
        elif name == "dependencies":
            if not self._json("resource", "list", "-g", GROUP, "--query", "[].id"):
                raise RebuildError("Dependency deployment produced no resources")
            if self._json("containerapp", "list", "-g", GROUP, "--query", "[].name"):
                raise RebuildError("Applications must not exist before seeding")
        elif name == "discover":
            if not all(self.found.get(k) for k in ("registry", "sql", "vault")):
                raise RebuildError("Discovery incomplete")
        elif name == "images":
            tags = self._json(
                "acr",
                "repository",
                "show-tags",
                "-n",
                c.registry,
                "--repository",
                "zava-forward-mvp",
                "--query",
                "[]",
            )
            if c.image_tag not in tags:
                raise RebuildError("Built image tag not found in the registry")
        elif name == "credential":
            names = self._json(
                "keyvault",
                "secret",
                "list",
                "--vault-name",
                self.found["vault"],
                "--query",
                "[].name",
            )
            if VAULT_SECRET not in names:
                raise RebuildError(f"Operator must provision {VAULT_SECRET} in the vault; stopped")
        elif name == "sql-users":
            pass
        elif name == "seed":
            if not self.found.get("cases", "").isdigit() or int(self.found["cases"]) < 1:
                raise RebuildError("Seeded store holds no cases")
        elif name == "applications":
            states = self._json(
                "containerapp", "list", "-g", GROUP, "--query", "[].properties.provisioningState"
            )
            if not states or any(state != "Succeeded" for state in states):
                raise RebuildError("Applications are not provisioned")
        elif name == "authentication":
            self._check_authentication()
        elif name == "staff":
            self._script(
                "initialize-workbench-staff.py",
                "--resource-group",
                GROUP,
                "--container-app",
                c.container_app,
                "--roster",
                str(c.roster),
                "--check",
            )
        elif name in ("health", "restart"):
            self._await_healthy()
        elif name == "api-denial":
            self._expect(self.probe(f"https://{self._fqdn()}/api/me", "get"), (401,), "API")
        elif name == "browser-redirect":
            self._expect(
                self.probe(f"https://{self._fqdn()}/sign-in", "get"),
                (301, 302, 303, 307),
                "/sign-in",
            )
        elif name in GATED_STAGES:
            return OPERATOR_GATED
        return VERIFIED


def run_rebuild(
    backend: Backend, subscription: str, start: str | None = None
) -> list[dict[str, str]]:
    """Run stages in order, verifying each; return evidence, stopping at a gated stage."""
    names = [stage.name for stage in STAGES]
    if start is not None and start not in names:
        raise RebuildError("Unknown stage")
    if start is None:
        if canonical(backend.inventory(), subscription):
            raise RebuildError("From-empty rebuild requires empty generic and budget inventories")
    evidence: list[dict[str, str]] = []
    if start is not None and names.index(start) > names.index("discover"):
        backend.perform(STAGES[names.index("discover")])
    for stage in STAGES[names.index(start) if start else 0 :]:
        if stage.name not in GATED_STAGES:
            backend.perform(stage)
        classification = backend.verify(stage)
        evidence.append({"stage": stage.name, "evidence": classification})
        if classification == OPERATOR_GATED:
            break
        if classification != VERIFIED:
            raise RebuildError(f"Unverified rebuild checkpoint: {stage.name}")
    return evidence


def plan(config_summary: Mapping[str, str]) -> dict[str, object]:
    report = dry_run()
    report["scope"] = "dry-run plan; no az or network call was made"
    report["operator_gated"] = list(GATED_STAGES)
    report["synthetic_only"] = "seed and roster inputs are scanned for non-synthetic addresses"
    report["config"] = dict(config_summary)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("rebuild", "teardown"))
    parser.add_argument("--apply", action="store_true", help="execute; the default is a dry run")
    parser.add_argument("--subscription", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--image-tag", required=True)
    parser.add_argument("--parameters", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--container-app", required=True)
    parser.add_argument("--environment", default="test")
    parser.add_argument("--workload", default="forward")
    parser.add_argument("--from-stage", choices=[stage.name for stage in STAGES])
    parser.add_argument("--parameter", action="append", default=[], dest="overrides")
    parser.add_argument("--build-pool", help="approved ACR agent pool for a private registry")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return parser


def main(
    argv: Sequence[str] | None = None,
    runner: Runner = subprocess_runner,
    probe: Probe = http_probe,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = AzureConfig(
            subscription=args.subscription,
            registry=args.registry,
            image_tag=args.image_tag,
            parameters=args.parameters,
            seed=args.seed,
            roster=args.roster,
            container_app=args.container_app,
            environment=args.environment,
            workload=args.workload,
            repo_root=args.repo_root,
            overrides=tuple(args.overrides),
            build_pool=args.build_pool,
        )
        config.validate()
        if not args.apply:
            summary = {
                "operation": args.operation,
                "group": GROUP,
                "environment": config.environment,
            }
            print(json.dumps(plan(summary), indent=2))
            return 0
        backend = AzureBackend(config, runner, probe, sleep)
        backend.check_account()
        if args.operation == "teardown":
            deleted = teardown(backend, config.subscription)
            print(json.dumps({"deleted_types": deleted, "inventory": "empty"}, indent=2))
            return 0
        evidence = run_rebuild(backend, config.subscription, args.from_stage)
        print(json.dumps({"stages": evidence}, indent=2))
        return 2 if evidence and evidence[-1]["evidence"] == OPERATOR_GATED else 0
    except RebuildError as exc:
        print(f"REBUILD_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
