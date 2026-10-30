"""Checked rebuild contracts and disposable SYNTHETIC rehearsal, never Azure execution."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol
from uuid import UUID


class RebuildError(RuntimeError):
    """A checkpoint failed; partial state must be inspected before retry."""


@dataclass(frozen=True)
class Stage:
    name: str
    integration: str
    check: str


STAGES = (
    Stage(
        "parameters", "reviewed environment parameter set", "scope, region, quota and identities"
    ),
    Stage("dependencies", "infra/scripts/deploy.py", "deployApplications=false; no exposed apps"),
    Stage(
        "discover",
        "Bicep deployment outputs",
        "registry, SQL, vault and model IDs; no guessed names",
    ),
    Stage(
        "images",
        "infra/scripts/pipeline.py release",
        "applicable workload images pinned to digests",
    ),
    Stage("credential", "authorized credential provisioning", "private reference only; never argv"),
    Stage("sql-users", "infra/scripts/create-sql-users.py", "least-privilege contained users"),
    Stage(
        "seed", "core SQL store initialization", "synthetic-only provenance; no populated DB reseed"
    ),
    Stage("applications", "infra/scripts/deploy.py", "real images, auth configured, rollout ready"),
    Stage(
        "authentication", "infra/scripts/setup-entra.py", "retained registration and callback check"
    ),
    Stage(
        "staff", "existing Entra/staff reconciliation", "authorized role/roster check; not consent"
    ),
    Stage("health", "pipeline postchecks", "healthz returns 200"),
    Stage("api-denial", "pipeline postchecks", "unauthenticated API returns 401"),
    Stage("browser-redirect", "pipeline postchecks", "browser redirects to intended sign-in"),
    Stage(
        "workload-sql", "API managed identity probe", "SQL write/read and independent audit witness"
    ),
    Stage("model-standard", "API registered task probe", "standard deployment returns source=ai"),
    Stage("model-capable", "API registered task probe", "capable deployment returns source=ai"),
    Stage("restart", "actual serving revision restart", "independent SQL state/audit persistence"),
)

# Only modeled types are admitted. A future adapter must supply full safety evidence.
ORDER = {
    "microsoft.app/containerapps": 0,
    "microsoft.app/jobs": 0,
    "microsoft.network/privateendpoints": 1,
    "microsoft.cognitiveservices/accounts/projects": 1,
    "microsoft.cognitiveservices/accounts/deployments": 1,
    "microsoft.insights/privatelinkscopes/scopedresources": 1,
    "microsoft.insights/metricalerts": 1,
    "microsoft.insights/scheduledqueryrules": 1,
    "microsoft.authorization/roleassignments": 1,
    "microsoft.cdn/profiles": 1,
    "microsoft.network/frontdoorwebapplicationfirewallpolicies": 3,
    "microsoft.insights/privatelinkscopes": 2,
    "microsoft.app/managedenvironments": 2,
    "microsoft.devices/iothubs": 2,
    "microsoft.eventhub/namespaces": 3,
    "microsoft.cognitiveservices/accounts": 3,
    "microsoft.sql/servers/databases": 3,
    "microsoft.sql/servers": 4,
    "microsoft.keyvault/vaults": 4,
    "microsoft.storage/storageaccounts": 4,
    "microsoft.containerregistry/registries": 4,
    "microsoft.insights/components": 4,
    "microsoft.operationalinsights/workspaces": 5,
    "microsoft.insights/actiongroups": 5,
    "microsoft.network/networkinterfaces": 5,
    "microsoft.network/privatednszones/virtualnetworklinks": 5,
    "microsoft.network/privatednszones": 6,
    "microsoft.network/virtualnetworks": 6,
    "microsoft.network/networksecuritygroups": 7,
    "microsoft.managedidentity/userassignedidentities": 8,
    "microsoft.consumption/budgets": 9,
}
BUDGET = "microsoft.consumption/budgets"
LOCAL_SUBSCRIPTION = "11111111-1111-4111-8111-111111111111"


@dataclass(frozen=True)
class Resource:
    resource_id: str
    kind: str
    locked: bool
    retained: bool


@dataclass(frozen=True)
class Inventory:
    resources: tuple[Resource, ...] = ()
    budgets: tuple[Resource, ...] = ()


class Backend(Protocol):
    """Operations must not return until their bounded operation has settled."""

    def inventory(self) -> Inventory: ...
    def perform(self, stage: Stage) -> None: ...
    def verify(self, stage: Stage) -> str: ...
    def delete(self, resource: Resource) -> None: ...


def canonical(inventory: Inventory, subscription: str) -> tuple[Resource, ...]:
    try:
        if str(UUID(subscription)) != subscription or UUID(subscription).int == 0:
            raise ValueError
    except ValueError as exc:
        raise RebuildError("Invalid subscription scope") from exc
    prefix = f"/subscriptions/{subscription}/resourcegroups/ama/providers/"
    records = (*inventory.resources, *inventory.budgets)
    if len(records) > 1000:
        raise RebuildError("Inventory exceeds the 1000-record authoring limit")
    seen: set[str] = set()
    for collection, budget in ((inventory.resources, False), (inventory.budgets, True)):
        for resource in collection:
            rid, kind = resource.resource_id.lower(), resource.kind.lower()
            parts = rid.removeprefix(prefix).split("/")
            if (
                not rid.startswith(prefix)
                or not re.fullmatch(r"[a-z0-9._/-]+", rid)
                or len(parts) < 3
                or len(parts) % 2 != 1
                or any(not part or part in (".", "..") for part in parts)
                or kind != "/".join((parts[0], *parts[1::2]))
                or kind not in ORDER
                or (kind == BUDGET) != budget
                or rid in seen
                or type(resource.locked) is not bool
                or type(resource.retained) is not bool
                or resource.locked
                or resource.retained
            ):
                raise RebuildError("Unapproved scope/type, duplicate, lock or retention evidence")
            seen.add(rid)
    return tuple(sorted(records, key=lambda resource: resource.resource_id.lower()))


def deletion_order(inventory: Inventory, subscription: str) -> tuple[Resource, ...]:
    records = canonical(inventory, subscription)
    return tuple(
        sorted(
            records,
            key=lambda resource: (
                ORDER[resource.kind.lower()],
                -resource.resource_id.count("/"),
                resource.resource_id.lower(),
            ),
        )
    )


def teardown(backend: Backend, subscription: str) -> list[str]:
    initial = backend.inventory()
    expected = canonical(initial, subscription)
    deleted = []
    for resource in deletion_order(initial, subscription):
        if canonical(backend.inventory(), subscription) != expected:
            raise RebuildError(
                "Inventory changed before deletion; stop and review both inventories"
            )
        backend.delete(resource)
        expected = tuple(record for record in expected if record != resource)
        if canonical(backend.inventory(), subscription) != expected:
            raise RebuildError("Deletion not confirmed or inventory changed; no further deletion")
        deleted.append(resource.kind)
    if canonical(backend.inventory(), subscription):
        raise RebuildError("Generic resource or budget inventory is not empty")
    return deleted


def rebuild(backend: Backend, subscription: str) -> list[dict[str, str]]:
    if canonical(backend.inventory(), subscription):
        raise RebuildError("From-empty rebuild requires empty generic and budget inventories")
    evidence = []
    for stage in STAGES:
        backend.perform(stage)
        classification = backend.verify(stage)
        if classification not in ("local-sql-verified", "simulated-not-live"):
            raise RebuildError(f"Unverified rebuild checkpoint: {stage.name}")
        evidence.append({"stage": stage.name, "evidence": classification})
    return evidence


class LocalBackend:
    """A SQLite control-plane simulation; never an Azure or application store adapter."""

    def __init__(self, path: Path):
        self.path = path
        # Exclusive creation prevents accidentally opening a pre-existing dataset.
        with path.open("xb"):
            pass
        with self.connection() as db:
            db.executescript(
                "CREATE TABLE resources (id TEXT PRIMARY KEY, kind TEXT, budget INTEGER);"
                "CREATE TABLE stages (name TEXT PRIMARY KEY);"
                "CREATE TABLE cases (id TEXT PRIMARY KEY, source TEXT);"
                "CREATE TABLE staff (code TEXT PRIMARY KEY, email TEXT UNIQUE);"
                "CREATE TABLE audit (id INTEGER PRIMARY KEY, detail TEXT);"
            )

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path)
        try:
            with db:
                yield db
        finally:
            db.close()

    def inventory(self) -> Inventory:
        with self.connection() as db:
            rows = db.execute("SELECT id, kind, budget FROM resources ORDER BY id").fetchall()
        return Inventory(
            tuple(Resource(rid, kind, False, False) for rid, kind, budget in rows if not budget),
            tuple(Resource(rid, kind, False, False) for rid, kind, budget in rows if budget),
        )

    def add(self, kind: str, name: str) -> None:
        prefix = f"/subscriptions/{LOCAL_SUBSCRIPTION}/resourceGroups/ama/providers/"
        namespace, *types = kind.split("/")
        resource_id = (
            prefix
            + namespace
            + "/"
            + "/".join(part for pair in zip(types, name.split("/"), strict=True) for part in pair)
        )
        with self.connection() as db:
            db.execute(
                "INSERT INTO resources VALUES (?, ?, ?)",
                (resource_id, kind, kind.lower() == BUDGET),
            )

    def perform(self, stage: Stage) -> None:
        index = STAGES.index(stage)
        with self.connection() as db:
            completed = {row[0] for row in db.execute("SELECT name FROM stages")}
            if completed != {item.name for item in STAGES[:index]}:
                raise RebuildError("Reordered, repeated or missing rebuild stage")
            if stage.name == "seed":
                db.execute(
                    "INSERT INTO cases VALUES ('SYN-148', 'SYNTHETIC generated local fixture')"
                )
                db.execute("INSERT INTO audit VALUES (1, 'SYNTHETIC seed witness')")
            elif stage.name == "staff":
                db.execute("INSERT INTO staff VALUES ('SYN-STAFF', 'operator@example.test')")
            db.execute("INSERT INTO stages VALUES (?)", (stage.name,))
        if stage.name == "dependencies":
            for kind, name in (
                ("Microsoft.App/managedEnvironments", "synthetic-env"),
                ("Microsoft.Network/virtualNetworks", "synthetic-net"),
                ("Microsoft.Network/privateEndpoints", "synthetic-pe"),
                ("Microsoft.CognitiveServices/accounts", "synthetic-ai"),
                ("Microsoft.Insights/privateLinkScopes", "synthetic-ampls"),
                ("Microsoft.Insights/components", "synthetic-insights"),
                ("Microsoft.Consumption/budgets", "synthetic-budget"),
            ):
                self.add(kind, name)
            self.add(
                "Microsoft.CognitiveServices/accounts/projects", "synthetic-ai/synthetic-project"
            )
        elif stage.name == "applications":
            self.add("Microsoft.App/containerApps", "synthetic-api")
            self.add("Microsoft.App/jobs", "synthetic-job")

    def verify(self, stage: Stage) -> str:
        with self.connection() as db:
            names = {row[0] for row in db.execute("SELECT name FROM stages")}
            if stage.name not in names:
                raise RebuildError(f"Missing stage witness: {stage.name}")
            if stage.name in ("seed", "staff", "workload-sql", "restart"):
                if db.execute("SELECT * FROM cases").fetchall() != [
                    ("SYN-148", "SYNTHETIC generated local fixture")
                ] or db.execute("SELECT * FROM audit").fetchall() != [
                    (1, "SYNTHETIC seed witness")
                ]:
                    raise RebuildError("Synthetic SQL seed/audit readback failed")
                if stage.name != "seed" and db.execute("SELECT * FROM staff").fetchall() != [
                    ("SYN-STAFF", "operator@example.test")
                ]:
                    raise RebuildError("Synthetic staff readback failed")
                return "local-sql-verified"
            return "simulated-not-live"

    def delete(self, resource: Resource) -> None:
        with self.connection() as db:
            if (
                db.execute("DELETE FROM resources WHERE id = ?", (resource.resource_id,)).rowcount
                != 1
            ):
                raise RebuildError("Synthetic resource deletion failed")


def dry_run() -> dict[str, object]:
    return {
        "scope": "authoring-only; no Azure adapter",
        "stages": [asdict(stage) for stage in STAGES],
        "teardown": {
            "resource_group": "ama (retained; never a deletion target)",
            "inventories": ["resources", "budgets"],
            "order": sorted(ORDER, key=lambda kind: (ORDER[kind], kind)),
            "check": "exact remaining inventory before/after each delete; final both empty",
            "blocked": "unknown types, missing safety evidence, locks, retention or scope drift",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="print contracts without backend I/O")
    mode.add_argument("--synthetic-local", action="store_true", help="disposable SQLite rehearsal")
    args = parser.parse_args(argv)
    try:
        if args.dry_run:
            report = dry_run()
        else:
            with tempfile.TemporaryDirectory(prefix="zf-rebuild-148-") as directory:
                backend = LocalBackend(Path(directory) / "synthetic.sqlite")
                stages = rebuild(backend, LOCAL_SUBSCRIPTION)
                deleted = teardown(backend, LOCAL_SUBSCRIPTION)
                report = {
                    "scope": "SYNTHETIC local SQLite simulation; not Azure/application acceptance",
                    "stages": stages,
                    "deleted_synthetic_types": deleted,
                    "resources_remaining": len(backend.inventory().resources),
                    "budgets_remaining": len(backend.inventory().budgets),
                }
        print(json.dumps(report, indent=2))
        return 0
    except (RebuildError, sqlite3.Error, OSError):
        print(
            "REBUILD_FAILED: local checkpoint failed; no Azure operation was attempted",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
