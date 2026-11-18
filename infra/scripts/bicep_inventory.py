"""Offline architecture-to-Bicep resource inventory, module matrix, and rebuild verifier (#136).

Parses repository Bicep entrypoints and modules, ADRs 0001-0003, deployment scripts, rebuild stages,
and the structured Markdown tables in infra/README.md without Azure CLI or network calls.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ARCH_HEADING = "### Proposed architecture resource inventory (ADRs 0001, 0002, 0003)"
MODULE_HEADING = "### Bicep module delivery matrix"
SEQUENCE_HEADING = "### Reproducible from-empty deployment sequence"

ARCH_COLUMNS = (
    "Component ID",
    "Proposed architecture resource",
    "ADR source",
    "Disposition",
    "Bicep template or artifact",
    "ARM resource types or external plane",
    "Named owner",
    "Status and notes",
)
MODULE_COLUMNS = (
    "Module path",
    "Wired in entrypoint(s)",
    "Provisioned ARM resource types",
    "Delivery status",
    "Notes and remaining gates",
)
SEQUENCE_COLUMNS = (
    "Step",
    "Rebuild stage(s)",
    "Action",
    "Repository template or script",
    "Verification check",
)

VALID_DISPOSITIONS = frozenset({"bicep", "bicep-conditional", "manual", "deferred"})
VALID_MODULE_STATUSES = frozenset(
    {"delivered", "delivered-conditional", "delivered-placeholder-workers", "delivered-guard"}
)
PLACEHOLDER_VALUES = frozenset(
    {"", "-", "none", "n/a", "na", "tbd", "todo", "unknown", "unassigned", "undocumented"}
)
PLACEHOLDER_WORKER_IMAGE = "mcr.microsoft.com/k8se/quickstart:latest"

ADR_PATHS: dict[str, str] = {
    "ADR 0001": "docs/adrs/0001-azure-architecture.md",
    "ADR 0002": "docs/adrs/0002-pilot-readiness-architecture.md",
    "ADR 0003": "docs/adrs/0003-journey-derived-capabilities-runtime-fit.md",
}

_SCOPE_RE = re.compile(r"(?m)^\s*targetScope\s*=\s*'([^']+)'")
_RESOURCE_RE = re.compile(r"(?m)^\s*resource\s+(\w+)\s+'([^'@]+)@[^']+'(?:(\s+existing)\b)?")
_MODULE_RE = re.compile(r"(?m)^\s*module\s+\w+\s+'([^']+)'")
_CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_REPO_PATH_PREFIXES = ("infra/", "src/", "docs/", ".github/")


@dataclass(frozen=True)
class ArchitectureRequirement:
    component_id: str
    adr_anchors: tuple[tuple[str, str], ...]


REQUIRED_ARCHITECTURE_COMPONENTS: tuple[ArchitectureRequirement, ...] = (
    ArchitectureRequirement("azure-subscription-and-rg", (("ADR 0001", "azure sql"),)),
    ArchitectureRequirement("parameter-scope-guard", (("ADR 0001", "container apps"),)),
    ArchitectureRequirement("managed-identities-and-rbac", (("ADR 0001", "managed identit"),)),
    ArchitectureRequirement("network-vnet-nsg-dns-pe", (("ADR 0001", "private endpoint"),)),
    ArchitectureRequirement("monitoring-logs-ampls-alerts", (("ADR 0001", "log analytics"),)),
    ArchitectureRequirement(
        "consumption-budgets", (("ADR 0001", "container apps"), ("ADR 0003", "iot hub"))
    ),
    ArchitectureRequirement("key-vault-resource", (("ADR 0001", "key vault"),)),
    ArchitectureRequirement("key-vault-secret-values", (("ADR 0001", "key vault"),)),
    ArchitectureRequirement(
        "storage-blobs-worm-queues", (("ADR 0001", "blob"), ("ADR 0003", "queue"))
    ),
    ArchitectureRequirement(
        "ranking-archive-blob", (("ADR 0001", "ranking"), ("ADR 0003", "ranking"))
    ),
    ArchitectureRequirement(
        "worm-policy-irreversible-lock", (("ADR 0001", "ledger"), ("ADR 0002", "ledger"))
    ),
    ArchitectureRequirement("entra-token-store", (("ADR 0001", "entra"),)),
    ArchitectureRequirement("container-registry", (("ADR 0001", "container registry"),)),
    ArchitectureRequirement(
        "azure-sql-and-ledger", (("ADR 0001", "azure sql"), ("ADR 0003", "azure sql"))
    ),
    ArchitectureRequirement("sql-contained-users-and-roster", (("ADR 0001", "azure sql"),)),
    ArchitectureRequirement(
        "ledger-digest-verification", (("ADR 0001", "ledger"), ("ADR 0002", "ledger"))
    ),
    ArchitectureRequirement("microsoft-foundry-models", (("ADR 0001", "foundry"),)),
    ArchitectureRequirement(
        "container-apps-hosting-and-jobs",
        (("ADR 0001", "container apps"), ("ADR 0003", "queue")),
    ),
    ArchitectureRequirement(
        "iot-hub-and-eventhub-adapter",
        (("ADR 0002", "iot hub"), ("ADR 0003", "event hub")),
    ),
    ArchitectureRequirement("iot-device-identities-and-certs", (("ADR 0003", "iot hub"),)),
    ArchitectureRequirement("public-edge-frontdoor-waf", (("ADR 0002", "front door"),)),
    ArchitectureRequirement("custom-domain-dns-records", (("ADR 0002", "front door"),)),
    ArchitectureRequirement("gis-map-tile-provider", (("ADR 0002", "tile"), ("ADR 0003", "tile"))),
    ArchitectureRequirement("subscription-policy-and-defender", (("ADR 0002", "defender"),)),
    ArchitectureRequirement("entra-app-registration-and-roles", (("ADR 0001", "entra"),)),
    ArchitectureRequirement("contractor-entra-b2b-policy", (("ADR 0002", "b2b"),)),
    ArchitectureRequirement("m365-teams-and-sharepoint-consent", (("ADR 0001", "sharepoint"),)),
    ArchitectureRequirement("github-environments-and-oidc", (("ADR 0001", "entra"),)),
    ArchitectureRequirement("deferred-egress-and-phase2-services", (("ADR 0001", "ai search"),)),
)


@dataclass(frozen=True)
class BicepFileSummary:
    path: str
    target_scope: str
    provisioned_types: frozenset[str]
    existing_types: frozenset[str]
    module_targets: tuple[str, ...]
    uncommented_source: str


@dataclass(frozen=True)
class BicepTree:
    files: dict[str, BicepFileSummary]
    callers: dict[str, tuple[str, ...]]
    placeholder_workers: bool


@dataclass(frozen=True)
class VerificationReport:
    ok: bool
    errors: tuple[str, ...]
    architecture_rows: int
    module_rows: int
    sequence_steps: int
    rebuild_stages: tuple[str, ...]
    pipeline_operations: tuple[str, ...]


def strip_bicep_comments(source: str) -> str:
    """Remove // and /* ... */ comments outside single-quoted Bicep string literals."""
    out: list[str] = []
    index = 0
    length = len(source)
    in_string = False
    while index < length:
        char = source[index]
        if in_string:
            out.append(char)
            if char == "'":
                if index + 1 < length and source[index + 1] == "'":
                    out.append("'")
                    index += 2
                    continue
                in_string = False
            index += 1
            continue
        if char == "'":
            in_string = True
            out.append(char)
            index += 1
        elif source[index : index + 2] == "//":
            while index < length and source[index] != "\n":
                index += 1
        elif source[index : index + 2] == "/*":
            index += 2
            while index < length and source[index : index + 2] != "*/":
                if source[index] == "\n":
                    out.append("\n")
                index += 1
            index += 2
        else:
            out.append(char)
            index += 1
    return "".join(out)


def parse_bicep_file(path: Path, repo_root: Path) -> BicepFileSummary:
    rel_path = path.resolve().relative_to(repo_root.resolve()).as_posix()
    clean = strip_bicep_comments(path.read_text(encoding="utf-8"))
    scope_match = _SCOPE_RE.search(clean)
    target_scope = scope_match.group(1) if scope_match else "resourceGroup"
    provisioned: set[str] = set()
    existing: set[str] = set()
    for match in _RESOURCE_RE.finditer(clean):
        resource_type = match.group(2).strip().lower()
        if match.group(3):
            existing.add(resource_type)
        else:
            provisioned.add(resource_type)
    targets: list[str] = []
    for mod_match in _MODULE_RE.finditer(clean):
        resolved = (path.parent / mod_match.group(1)).resolve()
        targets.append(resolved.relative_to(repo_root.resolve()).as_posix())
    return BicepFileSummary(
        path=rel_path,
        target_scope=target_scope,
        provisioned_types=frozenset(provisioned),
        existing_types=frozenset(existing),
        module_targets=tuple(targets),
        uncommented_source=clean,
    )


def _resource_block_has_command(uncommented: str, symbolic_name: str) -> bool:
    pattern = re.compile(rf"(?m)^\s*resource\s+{re.escape(symbolic_name)}\s+'[^']+'\s*=")
    match = pattern.search(uncommented)
    if match is None:
        return False
    depth = 0
    started = False
    end = len(uncommented)
    for pos in range(match.end(), len(uncommented)):
        ch = uncommented[pos]
        if ch == "{":
            depth += 1
            started = True
        elif ch == "}":
            depth -= 1
            if started and depth == 0:
                end = pos + 1
                break
    block = uncommented[match.start() : end]
    return re.search(r"(?m)^\s*command\s*:", block) is not None


def scan_bicep_tree(repo_root: Path) -> BicepTree:
    root = repo_root.resolve()
    candidates = sorted([*root.glob("infra/*.bicep"), *root.glob("infra/modules/*.bicep")])
    files: dict[str, BicepFileSummary] = {}
    caller_sets: dict[str, set[str]] = {}
    for candidate in candidates:
        summary = parse_bicep_file(candidate, root)
        files[summary.path] = summary
        for target in summary.module_targets:
            caller_sets.setdefault(target, set()).add(summary.path)
    callers = {target: tuple(sorted(sources)) for target, sources in sorted(caller_sets.items())}
    main_summary = files.get("infra/main.bicep")
    apps_summary = files.get("infra/modules/containerapps.bicep")
    main_has_placeholder = (
        main_summary is not None and PLACEHOLDER_WORKER_IMAGE in main_summary.uncommented_source
    )
    apps_missing_worker_cmd = apps_summary is not None and (
        not _resource_block_has_command(apps_summary.uncommented_source, "orchestrator")
        or not _resource_block_has_command(apps_summary.uncommented_source, "importJob")
    )
    return BicepTree(
        files=files,
        callers=callers,
        placeholder_workers=main_has_placeholder or apps_missing_worker_cmd,
    )


def _split_markdown_row(line: str) -> list[str]:
    stripped = line.strip().removeprefix("|").removesuffix("|")
    parts = re.split(r"(?<!\\)\|", stripped)
    return [part.replace(r"\|", "|").strip() for part in parts]


def parse_markdown_section_table(
    markdown: str, heading: str, expected_columns: Sequence[str]
) -> tuple[tuple[dict[str, str], ...], list[str]]:
    errors: list[str] = []
    lines = markdown.splitlines()
    start_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            start_idx = idx + 1
            break
    if start_idx is None:
        return (), [f"Missing required infra/README.md section heading: {heading}"]

    section_lines: list[str] = []
    for line in lines[start_idx:]:
        if line.startswith(("## ", "### ")):
            break
        section_lines.append(line)

    table_lines = [line for line in section_lines if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return (), [f"Section '{heading}' does not contain a populated Markdown table"]

    headers = _split_markdown_row(table_lines[0])
    if tuple(headers) != tuple(expected_columns):
        msg = (
            f"Section '{heading}' columns {headers!r} do not match expected "
            f"{list(expected_columns)!r}"
        )
        return (), [msg]

    separator = _split_markdown_row(table_lines[1])
    if len(separator) != len(headers) or not all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in separator
    ):
        return (), [f"Section '{heading}' has an invalid Markdown table separator row"]

    rows: list[dict[str, str]] = []
    for row_number, raw_line in enumerate(table_lines[2:], start=1):
        cells = _split_markdown_row(raw_line)
        if len(cells) != len(headers):
            errors.append(
                f"Section '{heading}' row {row_number} has {len(cells)} cells; "
                f"expected {len(headers)}"
            )
            continue
        rows.append(dict(zip(headers, cells, strict=True)))
    return tuple(rows), errors


def _code_spans(cell: str) -> list[str]:
    return [match.group(1).strip() for match in _CODE_SPAN_RE.finditer(cell) if match.group(1)]


def _repo_paths_from_cell(cell: str) -> list[str]:
    spans = _code_spans(cell)
    candidates = spans if spans else [token.strip(" ,;()") for token in cell.split()]
    return [
        token.split()[0]
        for token in candidates
        if token.startswith(_REPO_PATH_PREFIXES) and "." in Path(token.split()[0]).name
    ]


def _arm_types_from_cell(cell: str) -> set[str]:
    return {
        span.lower()
        for span in _code_spans(cell)
        if "/" in span and span.lower().startswith("microsoft.")
    }


def _is_meaningful_owner(owner: str) -> bool:
    normalized = owner.strip().strip("`")
    return normalized.lower() not in PLACEHOLDER_VALUES and len(normalized) >= 3


def verify_architecture_inventory(
    repo_root: Path,
    bicep_tree: BicepTree,
    rows: Sequence[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    adr_texts: dict[str, str] = {}
    for adr_label, rel_path in ADR_PATHS.items():
        adr_file = repo_root / rel_path
        if not adr_file.is_file():
            errors.append(f"Missing required ADR file: {rel_path}")
        else:
            adr_texts[adr_label] = adr_file.read_text(encoding="utf-8").lower()

    by_id: dict[str, dict[str, str]] = {}
    for row in rows:
        raw_id = row["Component ID"].strip().strip("`")
        if not raw_id:
            errors.append("Architecture inventory row has an empty Component ID")
            continue
        if raw_id in by_id:
            errors.append(f"Duplicate Component ID in architecture inventory: {raw_id}")
            continue
        by_id[raw_id] = row

    for req in REQUIRED_ARCHITECTURE_COMPONENTS:
        for adr_label, anchor in req.adr_anchors:
            adr_body = adr_texts.get(adr_label, "")
            if adr_body and anchor.lower() not in adr_body:
                errors.append(
                    f"ADR anchor '{anchor}' for '{req.component_id}' not found in {adr_label}"
                )
        matched_row = by_id.get(req.component_id)
        if matched_row is None:
            errors.append(
                f"Required proposed architecture component '{req.component_id}' is missing from "
                f"'{ARCH_HEADING}'"
            )
            continue
        for adr_label, _ in req.adr_anchors:
            if adr_label not in matched_row["ADR source"]:
                errors.append(f"Component '{req.component_id}' must cite {adr_label} in ADR source")

    for comp_id, row in by_id.items():
        disposition = row["Disposition"].strip().strip("`").lower()
        if disposition not in VALID_DISPOSITIONS:
            errors.append(
                f"Component '{comp_id}' has invalid disposition '{disposition}'; "
                f"expected one of {sorted(VALID_DISPOSITIONS)}"
            )
            continue
        if row["Proposed architecture resource"].strip().lower() in PLACEHOLDER_VALUES:
            errors.append(f"Component '{comp_id}' has an empty resource description")
        if row["Status and notes"].strip().lower() in PLACEHOLDER_VALUES:
            errors.append(f"Component '{comp_id}' has empty status/notes")
        if not _is_meaningful_owner(row["Named owner"]):
            errors.append(
                f"Component '{comp_id}' ({disposition}) is missing an explicit Named owner"
            )

        referenced_paths = _repo_paths_from_cell(row["Bicep template or artifact"])
        for rel_path in referenced_paths:
            if not (repo_root / rel_path).is_file():
                errors.append(
                    f"Component '{comp_id}' references missing repository file '{rel_path}'"
                )

        if disposition in {"bicep", "bicep-conditional"}:
            bicep_paths = [p for p in referenced_paths if p.endswith(".bicep")]
            if not bicep_paths:
                errors.append(
                    f"Component '{comp_id}' has disposition '{disposition}' but cites no .bicep "
                    f"template"
                )
                continue
            union_provisioned: set[str] = set()
            for bicep_path in bicep_paths:
                summary = bicep_tree.files.get(bicep_path)
                if summary is None:
                    errors.append(
                        f"Component '{comp_id}' cites unscanned Bicep file '{bicep_path}'"
                    )
                else:
                    union_provisioned.update(summary.provisioned_types)
            plane_cell = row["ARM resource types or external plane"]
            claimed_types = _arm_types_from_cell(plane_cell)
            is_guard = "compile-time parameter guard" in plane_cell.lower()
            if is_guard and not claimed_types:
                if union_provisioned:
                    errors.append(
                        f"Component '{comp_id}' claims compile-time parameter guard but "
                        f"provisions {sorted(union_provisioned)}"
                    )
            elif not claimed_types:
                errors.append(
                    f"Component '{comp_id}' ({disposition}) lists no microsoft.* ARM resource types"
                )
            else:
                missing_types = sorted(claimed_types - union_provisioned)
                if missing_types:
                    errors.append(
                        f"Component '{comp_id}' claims ARM resource types {missing_types} not "
                        f"provisioned by {bicep_paths}"
                    )
        else:
            if "@" not in row["Named owner"] and "Servera" not in row["Named owner"]:
                errors.append(
                    f"Manual/deferred component '{comp_id}' must name a concrete human/role owner "
                    f"(got '{row['Named owner']}')"
                )
    return errors


def verify_module_delivery_matrix(
    repo_root: Path,
    bicep_tree: BicepTree,
    rows: Sequence[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    actual_modules = {
        path.relative_to(repo_root.resolve()).as_posix()
        for path in sorted((repo_root.resolve() / "infra" / "modules").glob("*.bicep"))
    }
    by_module: dict[str, dict[str, str]] = {}
    for row in rows:
        mod_path = row["Module path"].strip().strip("`")
        if mod_path in by_module:
            errors.append(f"Duplicate module row in delivery matrix: {mod_path}")
            continue
        by_module[mod_path] = row

    missing_modules = sorted(actual_modules - set(by_module))
    extra_modules = sorted(set(by_module) - actual_modules)
    if missing_modules:
        errors.append(f"Modules on disk missing from delivery matrix: {missing_modules}")
    if extra_modules:
        errors.append(f"Delivery matrix lists non-existent module files: {extra_modules}")

    for mod_path in sorted(actual_modules & set(by_module)):
        row = by_module[mod_path]
        summary = bicep_tree.files[mod_path]
        status = row["Delivery status"].strip().strip("`")
        if status not in VALID_MODULE_STATUSES:
            errors.append(
                f"Module '{mod_path}' has invalid Delivery status '{status}'; "
                f"expected one of {sorted(VALID_MODULE_STATUSES)}"
            )
        if row["Notes and remaining gates"].strip().lower() in PLACEHOLDER_VALUES:
            errors.append(f"Module '{mod_path}' has empty Notes and remaining gates")

        claimed_callers = sorted(
            {
                p
                for p in _repo_paths_from_cell(row["Wired in entrypoint(s)"])
                if p.endswith(".bicep")
            }
        )
        expected_callers = list(bicep_tree.callers.get(mod_path, ()))
        if claimed_callers != expected_callers:
            errors.append(
                f"Module '{mod_path}' caller mismatch: README lists {claimed_callers}, "
                f"actual Bicep callers are {expected_callers}"
            )

        types_cell = row["Provisioned ARM resource types"].strip()
        if not summary.provisioned_types:
            if types_cell.strip("`").lower() != "none (compile-time guard)":
                errors.append(
                    f"Zero-resource guard module '{mod_path}' must record "
                    f"'none (compile-time guard)' in Provisioned ARM resource types"
                )
            if status != "delivered-guard":
                errors.append(
                    f"Zero-resource guard module '{mod_path}' must have status 'delivered-guard'"
                )
        else:
            if status == "delivered-guard":
                errors.append(
                    f"Resource-provisioning module '{mod_path}' cannot use 'delivered-guard'"
                )
            claimed_types = _arm_types_from_cell(types_cell)
            if claimed_types != set(summary.provisioned_types):
                missing_t = sorted(set(summary.provisioned_types) - claimed_types)
                extra_t = sorted(claimed_types - set(summary.provisioned_types))
                errors.append(
                    f"Module '{mod_path}' ARM resource type mismatch: missing={missing_t}, "
                    f"extra={extra_t}"
                )

        if (
            mod_path == "infra/modules/containerapps.bicep"
            and bicep_tree.placeholder_workers
            and status != "delivered-placeholder-workers"
        ):
            errors.append(
                "Module 'infra/modules/containerapps.bicep' must record status "
                "'delivered-placeholder-workers' while #144 placeholder worker defaults remain"
            )
    return errors


def load_rebuild_stages(repo_root: Path) -> tuple[tuple[str, ...], list[str]]:
    rebuild_path = repo_root / "src/orchestrator/src/zava_forward/orchestrator/rebuild.py"
    if not rebuild_path.is_file():
        return (), [f"Missing rebuild contract file: {rebuild_path}"]
    tree = ast.parse(rebuild_path.read_text(encoding="utf-8"), filename=str(rebuild_path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "STAGES"
                    and isinstance(node.value, ast.Tuple)
                ):
                    stages: list[str] = []
                    for elt in node.value.elts:
                        if (
                            isinstance(elt, ast.Call)
                            and elt.args
                            and isinstance(elt.args[0], ast.Constant)
                            and isinstance(elt.args[0].value, str)
                        ):
                            stages.append(elt.args[0].value)
                    if stages:
                        return tuple(stages), []
    return (), ["Could not parse STAGES tuple from rebuild.py"]


def load_pipeline_operations(repo_root: Path) -> tuple[tuple[str, ...], list[str]]:
    pipeline_path = repo_root / "infra/scripts/pipeline.py"
    if not pipeline_path.is_file():
        return (), ["Missing CI deployment script: infra/scripts/pipeline.py"]
    source = pipeline_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(pipeline_path))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_argument"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == "operation"
        ):
            for kw in node.keywords:
                if kw.arg == "choices" and isinstance(kw.value, (ast.Tuple, ast.List)):
                    ops = [
                        elt.value
                        for elt in kw.value.elts
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                    ]
                    if ops:
                        return tuple(ops), []
    return (), ["Could not parse positional 'operation' choices from infra/scripts/pipeline.py"]


def verify_deploy_script_contract(repo_root: Path) -> list[str]:
    deploy_path = repo_root / "infra/scripts/deploy.py"
    if not deploy_path.is_file():
        return ["Missing operator deployment script: infra/scripts/deploy.py"]
    source = deploy_path.read_text(encoding="utf-8")
    errors: list[str] = []
    if '"--apply"' not in source and "'--apply'" not in source:
        errors.append("infra/scripts/deploy.py does not define the --apply flag")
    if '"what-if"' not in source and "'what-if'" not in source:
        errors.append("infra/scripts/deploy.py does not retain default what-if preview mode")
    return errors


def verify_from_empty_sequence(
    repo_root: Path,
    rows: Sequence[dict[str, str]],
    rebuild_stages: Sequence[str],
    pipeline_operations: Sequence[str],
) -> list[str]:
    errors = verify_deploy_script_contract(repo_root)
    if not rows:
        errors.append(f"Section '{SEQUENCE_HEADING}' contains zero steps")
        return errors

    observed_stages: list[str] = []
    all_script_cells: list[str] = []
    known_stage_set = set(rebuild_stages)

    for expected_step, row in enumerate(rows, start=1):
        step_raw = row["Step"].strip().strip("`")
        if step_raw != str(expected_step):
            errors.append(
                f"From-empty sequence step numbering error: expected '{expected_step}', "
                f"got '{step_raw}'"
            )
        for col in (
            "Rebuild stage(s)",
            "Action",
            "Repository template or script",
            "Verification check",
        ):
            val = row[col].strip().lower()
            if val in PLACEHOLDER_VALUES:
                errors.append(f"From-empty sequence step {expected_step} has undocumented '{col}'")

        script_cell = row["Repository template or script"]
        all_script_cells.append(script_cell)
        paths = _repo_paths_from_cell(script_cell)
        if not paths:
            errors.append(
                f"From-empty sequence step {expected_step} cites no repository template or script"
            )
        for rel_path in paths:
            if not (repo_root / rel_path).is_file():
                errors.append(
                    f"From-empty sequence step {expected_step} cites missing file '{rel_path}'"
                )

        combined_prose = f"{row['Action']} {row['Verification check']}"
        if "prerequisite" in combined_prose.lower() and (
            "@jmservera" not in combined_prose and "Servera" not in combined_prose
        ):
            errors.append(
                f"From-empty prerequisite step {expected_step} must name owner @jmservera"
            )

        for token in _code_spans(row["Rebuild stage(s)"]):
            if token in known_stage_set:
                observed_stages.append(token)

    if tuple(observed_stages) != tuple(rebuild_stages):
        errors.append(
            f"From-empty sequence rebuild stage coverage/order {observed_stages!r} does not "
            f"match rebuild.py STAGES {list(rebuild_stages)!r}"
        )

    joined_scripts = "\n".join(all_script_cells)
    if "infra/scripts/deploy.py" not in joined_scripts:
        errors.append("From-empty sequence does not reference infra/scripts/deploy.py")
    if "infra/scripts/pipeline.py" not in joined_scripts:
        errors.append("From-empty sequence does not reference infra/scripts/pipeline.py")
    for op in pipeline_operations:
        if op not in joined_scripts:
            errors.append(f"From-empty sequence does not account for pipeline.py operation '{op}'")
    return errors


def verify_all(repo_root: Path) -> VerificationReport:
    root = repo_root.resolve()
    readme_path = root / "infra/README.md"
    if not readme_path.is_file():
        return VerificationReport(
            ok=False,
            errors=("Missing infra/README.md",),
            architecture_rows=0,
            module_rows=0,
            sequence_steps=0,
            rebuild_stages=(),
            pipeline_operations=(),
        )

    markdown = readme_path.read_text(encoding="utf-8")
    bicep_tree = scan_bicep_tree(root)
    arch_rows, arch_parse_errors = parse_markdown_section_table(
        markdown, ARCH_HEADING, ARCH_COLUMNS
    )
    mod_rows, mod_parse_errors = parse_markdown_section_table(
        markdown, MODULE_HEADING, MODULE_COLUMNS
    )
    seq_rows, seq_parse_errors = parse_markdown_section_table(
        markdown, SEQUENCE_HEADING, SEQUENCE_COLUMNS
    )
    rebuild_stages, stage_errors = load_rebuild_stages(root)
    pipeline_ops, pipe_errors = load_pipeline_operations(root)

    errors: list[str] = [
        *arch_parse_errors,
        *mod_parse_errors,
        *seq_parse_errors,
        *stage_errors,
        *pipe_errors,
    ]
    if not arch_parse_errors:
        errors.extend(verify_architecture_inventory(root, bicep_tree, arch_rows))
    if not mod_parse_errors:
        errors.extend(verify_module_delivery_matrix(root, bicep_tree, mod_rows))
    if not seq_parse_errors and not stage_errors and not pipe_errors:
        errors.extend(verify_from_empty_sequence(root, seq_rows, rebuild_stages, pipeline_ops))

    return VerificationReport(
        ok=not errors,
        errors=tuple(errors),
        architecture_rows=len(arch_rows),
        module_rows=len(mod_rows),
        sequence_steps=len(seq_rows),
        rebuild_stages=rebuild_stages,
        pipeline_operations=pipeline_ops,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify ADR 0001-0003 architecture-to-Bicep coverage, module delivery matrix, "
            "and from-empty deployment sequence reproducibility (#136)."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Workspace repository root (defaults to two directories above this script).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate repository Bicep inventory, module matrix, and deployment sequence.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit structured JSON verification report.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = verify_all(args.repo_root)
    if args.as_json:
        payload = {
            "ok": report.ok,
            "architecture_rows": report.architecture_rows,
            "module_rows": report.module_rows,
            "sequence_steps": report.sequence_steps,
            "rebuild_stages": list(report.rebuild_stages),
            "pipeline_operations": list(report.pipeline_operations),
            "errors": list(report.errors),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif report.ok:
        print(
            f"Issue #136 Bicep inventory verified: {report.architecture_rows} architecture rows, "
            f"{report.module_rows} Bicep modules, {report.sequence_steps} from-empty steps "
            f"({len(report.rebuild_stages)} rebuild stages)."
        )
    else:
        for err in report.errors:
            print(f"ERROR: {err}", file=sys.stderr)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
