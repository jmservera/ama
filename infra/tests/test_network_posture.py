"""Focused policy-as-code tests for network posture, private endpoints, and Key Vault secrets."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from typing import Any, ClassVar

REPO_ROOT = Path(__file__).resolve().parents[2]
INFRA_DIR = REPO_ROOT / "infra"
INVENTORY_PATH = INFRA_DIR / "network-posture-inventory.json"
SECRET_INVENTORY_PATH = INFRA_DIR / "secret-inventory.json"
DOC_PATH = REPO_ROOT / "docs" / "architecture" / "network-posture.md"
ARCH_README_PATH = REPO_ROOT / "docs" / "architecture" / "README.md"
INFRA_README_PATH = INFRA_DIR / "README.md"

PLACEHOLDER_STRINGS = frozenset(
    {"", "-", "none", "n/a", "na", "tbd", "todo", "unknown", "unassigned", "undocumented"}
)

STORE_RESOURCE_TYPES = frozenset(
    {
        "microsoft.sql/servers",
        "microsoft.storage/storageaccounts",
        "microsoft.keyvault/vaults",
        "microsoft.containerregistry/registries",
        "microsoft.devices/iothubs",
        "microsoft.eventhub/namespaces",
        "microsoft.cognitiveservices/accounts",
        "microsoft.insights/privatelinkscopes",
        "microsoft.operationalinsights/workspaces",
        "microsoft.insights/components",
    }
)

FORBIDDEN_BICEP_SECRET_FUNCTIONS = (
    "listKeys",
    "listAccountSas",
    "listServiceSas",
    "listCredentials",
    "listSecrets",
    "administratorLoginPassword",
)

SECRET_ENV_NAME_PATTERN = re.compile(
    r"(SECRET|PASSWORD|PASSWD|VERIFIER|SESSION_KEY|SAS_URL|SAS_TOKEN|CONNECTION_STRING|API_KEY|CLIENT_SECRET)",
    re.IGNORECASE,
)
ALLOWED_NON_SECRET_ENV_NAMES = frozenset(
    {
        "AUTH_TOKEN_STORE_ROTATION",
    }
)
LITERAL_SECRET_VALUE_PATTERN = re.compile(
    r"(AccountKey=[^$\s{\"';]{4,}|SharedAccessKey=[^$\s{\"';]{4,}|SharedAccessSignature=sr="
    r"|(?<![A-Za-z])sig=[A-Za-z0-9%+/=]{8,}|(?:Password|Pwd)\s*=\s*[^$\s{\"';]{4,}"
    r"|Bearer\s+[A-Za-z0-9._\-]{12,})",
    re.IGNORECASE,
)

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def _load_bicep_inventory_module() -> Any:
    module_path = INFRA_DIR / "scripts" / "bicep_inventory.py"
    spec = importlib.util.spec_from_file_location("bicep_inventory_under_test", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _bicep_command_prefix() -> list[str]:
    bicep_bin = shutil.which("bicep")
    if bicep_bin:
        return [bicep_bin]
    local_candidate = Path.home() / ".local" / "bin" / "bicep"
    if local_candidate.exists():
        return [str(local_candidate)]
    az_candidate = Path.home() / ".azure" / "bin" / "bicep"
    if az_candidate.exists():
        return [str(az_candidate)]
    return ["az", "bicep"]


def compile_bicep_file(rel_infra_path: str) -> dict[str, Any]:
    prefix = _bicep_command_prefix()
    target = str(INFRA_DIR / rel_infra_path)
    cmd = (
        [*prefix, "build", target, "--stdout"]
        if prefix[0] != "az"
        else [*prefix, "build", "--file", target, "--stdout"]
    )
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(f"Bicep build failed for {rel_infra_path}: {result.stderr}")
    compiled: dict[str, Any] = json.loads(result.stdout)
    return compiled


def compile_bicepparam_file(rel_infra_path: str) -> dict[str, Any]:
    prefix = _bicep_command_prefix()
    target = str(INFRA_DIR / rel_infra_path)
    cmd = (
        [*prefix, "build-params", target, "--stdout"]
        if prefix[0] != "az"
        else [*prefix, "build-params", "--file", target, "--stdout"]
    )
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(f"Bicep build-params failed for {rel_infra_path}: {result.stderr}")
    outer: dict[str, Any] = json.loads(result.stdout)
    params_doc: dict[str, Any] = json.loads(outer["parametersJson"])
    parameters: dict[str, Any] = params_doc.get("parameters", {})
    return parameters


def iter_arm_resources(template: dict[str, Any]) -> list[dict[str, Any]]:
    raw_items = template.get("resources", [])
    items = list(raw_items.values()) if isinstance(raw_items, dict) else list(raw_items)
    collected: list[dict[str, Any]] = []
    for item in items:
        props = item.get("properties", {})
        if item.get("type") == "Microsoft.Resources/deployments" and "template" in props:
            collected.extend(iter_arm_resources(props["template"]))
        else:
            collected.append(item)
    return collected


def iter_nested_deployments(
    template: dict[str, Any], prefix: tuple[str, ...] = ()
) -> list[tuple[tuple[str, ...], dict[str, Any], dict[str, Any]]]:
    raw_items = template.get("resources", [])
    items = list(raw_items.values()) if isinstance(raw_items, dict) else list(raw_items)
    found: list[tuple[tuple[str, ...], dict[str, Any], dict[str, Any]]] = []
    for item in items:
        props = item.get("properties", {})
        if item.get("type") == "Microsoft.Resources/deployments" and "template" in props:
            sub_tpl: dict[str, Any] = props["template"]
            path = (*prefix, str(item.get("name", "")))
            found.append((path, item, sub_tpl))
            found.extend(iter_nested_deployments(sub_tpl, path))
    return found


def _is_meaningful_text(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip()
    return len(normalized) >= 3 and normalized.lower() not in PLACEHOLDER_STRINGS


def _expected_compiled_pe_name(pe_deployment_name: str) -> str:
    if "${name}" in pe_deployment_name:
        pattern = pe_deployment_name.replace("${name}", "{0}")
        return f"[format('{pattern}', parameters('name'))]"
    return pe_deployment_name


def validate_data_store_posture(
    inventory: dict[str, Any],
    bicep_tree: Any,
    compiled_main: dict[str, Any],
    main_bicepparams: dict[str, dict[str, Any]],
) -> list[str]:
    """Return all AC1 contract violations (empty list means fully conformant)."""
    errors: list[str] = []

    data_stores = inventory.get("dataStores", [])
    exceptions = inventory.get("exerciseExceptions", [])
    existing_refs = inventory.get("existingStoreReferences", [])
    dns_zone_keys = {z["key"] for z in inventory.get("privateDnsZones", [])}

    store_ids = {s["id"] for s in data_stores}
    exception_ids = {e["id"] for e in exceptions}

    for exc in exceptions:
        exc_id = exc.get("id", "<missing-id>")
        if not _is_meaningful_text(exc.get("owner")):
            errors.append(f"Exception {exc_id} is missing a valid named owner.")
        if not _is_meaningful_text(exc.get("rationale")) or len(str(exc["rationale"]).strip()) < 20:
            errors.append(f"Exception {exc_id} is missing a substantive rationale.")
        controls = exc.get("compensatingControls")
        if (
            not isinstance(controls, list)
            or not controls
            or not all(_is_meaningful_text(c) for c in controls)
        ):
            errors.append(f"Exception {exc_id} must record non-empty compensatingControls.")
        bicep_path = exc.get("bicepPath", "")
        if not (REPO_ROOT / bicep_path).is_file():
            errors.append(f"Exception {exc_id} references missing file {bicep_path}.")

    provisioned_covered: set[tuple[str, str]] = set()
    for store in data_stores:
        sid = store.get("id", "<missing>")
        if store.get("posture") != "private-endpoint":
            errors.append(f"Data store {sid} has unsupported posture {store.get('posture')!r}.")
        if store.get("subnetId") != "snet-pe":
            errors.append(f"Data store {sid} must target subnetId 'snet-pe'.")
        bicep_path = str(store.get("bicepPath", ""))
        rtype = str(store.get("resourceType", "")).lower()
        provisioned_covered.add((bicep_path, rtype))
        for zkey in store.get("dnsZoneKeys", []):
            if zkey not in dns_zone_keys:
                errors.append(f"Data store {sid} references unknown dnsZoneKey {zkey!r}.")
        for scoped in store.get("scopedResources", []):
            provisioned_covered.add(
                (str(scoped.get("bicepPath", "")), str(scoped.get("resourceType", "")).lower())
            )

    for exc in exceptions:
        bicep_path = str(exc.get("bicepPath", ""))
        rtype = str(exc.get("resourceType", "")).lower()
        if rtype in STORE_RESOURCE_TYPES:
            provisioned_covered.add((bicep_path, rtype))

    existing_covered: dict[tuple[str, str], dict[str, Any]] = {}
    for ref in existing_refs:
        key = (str(ref.get("bicepPath", "")), str(ref.get("resourceType", "")).lower())
        existing_covered[key] = ref
        kind = ref.get("coverageKind")
        target = ref.get("coveredBy")
        if kind == "dataStore" and target not in store_ids:
            errors.append(f"existingStoreReference {key} points to unknown dataStore {target!r}.")
        elif kind == "exerciseException" and target not in exception_ids:
            errors.append(
                f"existingStoreReference {key} points to unknown exerciseException {target!r}."
            )
        elif kind not in ("dataStore", "exerciseException"):
            errors.append(f"existingStoreReference {key} has invalid coverageKind {kind!r}.")

    for rel_path, summary in sorted(bicep_tree.files.items()):
        for prov_type in sorted(summary.provisioned_types):
            if prov_type.lower() in STORE_RESOURCE_TYPES:
                tup = (rel_path, prov_type.lower())
                if tup not in provisioned_covered:
                    errors.append(
                        f"Provisioned store {rel_path} ({prov_type}) lacks private endpoint or "
                        "recorded exercise exception."
                    )
        for ex_type in sorted(summary.existing_types):
            if ex_type.lower() in STORE_RESOURCE_TYPES:
                tup = (rel_path, ex_type.lower())
                if tup not in existing_covered:
                    errors.append(
                        f"Existing store reference {rel_path} ({ex_type}) is unaccounted in "
                        "existingStoreReferences."
                    )

    nested_by_path = {
        path: (dep, sub_tpl) for path, dep, sub_tpl in iter_nested_deployments(compiled_main)
    }
    pe_deployments_in_main = {
        path: (dep, sub_tpl)
        for path, (dep, sub_tpl) in nested_by_path.items()
        if any(
            r.get("type") == "Microsoft.Network/privateEndpoints"
            for r in sub_tpl.get("resources", [])
        )
    }

    expected_pe_paths: set[tuple[str, ...]] = set()
    for store in data_stores:
        sid = store["id"]
        mod_name = store["mainModuleName"]
        expected_dep_name = _expected_compiled_pe_name(store["peDeploymentName"])
        pe_path = (mod_name, expected_dep_name)
        expected_pe_paths.add(pe_path)
        if pe_path not in pe_deployments_in_main:
            errors.append(
                f"Data store {sid} missing compiled privateEndpoint deployment {pe_path} in "
                "infra/main.bicep."
            )
            continue
        dep_item, sub_tpl = pe_deployments_in_main[pe_path]
        params = dep_item.get("properties", {}).get("parameters", {})
        if params.get("groupId", {}).get("value") != store["groupId"]:
            errors.append(
                f"Data store {sid} compiled groupId {params.get('groupId')} != "
                f"{store['groupId']!r}."
            )
        subnet_expr = str(params.get("subnetId", {}).get("value", ""))
        if "peSubnetId" not in subnet_expr:
            errors.append(f"Data store {sid} subnetId {subnet_expr!r} does not bind peSubnetId.")
        sub_types = {r.get("type") for r in sub_tpl.get("resources", [])}
        if "Microsoft.Network/privateEndpoints/privateDnsZoneGroups" not in sub_types:
            errors.append(f"Data store {sid} privateEndpoint lacks privateDnsZoneGroups resource.")

        parent_entry = nested_by_path.get((mod_name,))
        if parent_entry is not None:
            parent_dep, _ = parent_entry
            parent_subnet_expr = str(
                parent_dep.get("properties", {})
                .get("parameters", {})
                .get("peSubnetId", {})
                .get("value", "")
            )
            if (
                "reference(resourceId('Microsoft.Resources/deployments', 'network')"
                not in (parent_subnet_expr)
                or "peSubnetId" not in parent_subnet_expr
            ):
                errors.append(
                    f"Module {mod_name} in main.bicep does not wire network.outputs.peSubnetId."
                )

    unexpected_pes = set(pe_deployments_in_main) - expected_pe_paths
    if unexpected_pes:
        errors.append(f"Uninventoried privateEndpoint deployments in main.bicep: {unexpected_pes}")

    all_main_resources = iter_arm_resources(compiled_main)
    sql_servers = [r for r in all_main_resources if r.get("type") == "Microsoft.Sql/servers"]
    if not sql_servers or sql_servers[0].get("properties", {}).get("publicNetworkAccess") != (
        "Disabled"
    ):
        errors.append(
            "Azure SQL Server must set publicNetworkAccess to 'Disabled' unconditionally."
        )

    eh_namespaces = [
        r for r in all_main_resources if r.get("type") == "Microsoft.EventHub/namespaces"
    ]
    if not eh_namespaces or eh_namespaces[0].get("properties", {}).get("publicNetworkAccess") != (
        "Disabled"
    ):
        errors.append(
            "Telemetry Event Hub namespace must set publicNetworkAccess to 'Disabled' "
            "unconditionally."
        )

    ampls_list = [
        r for r in all_main_resources if r.get("type") == "microsoft.insights/privateLinkScopes"
    ]
    if not ampls_list:
        errors.append("AMPLS resource missing from compiled main.bicep.")
    else:
        access_mode = ampls_list[0].get("properties", {}).get("accessModeSettings", {})
        if (
            access_mode.get("ingestionAccessMode") != "PrivateOnly"
            or access_mode.get("queryAccessMode") != "PrivateOnly"
        ):
            errors.append("AMPLS must enforce PrivateOnly ingestion and query access modes.")

    for bparam_name, params in sorted(main_bicepparams.items()):
        pna = params.get("allowPublicNetworkAccess", {}).get("value")
        if pna is not False:
            errors.append(f"{bparam_name} must set allowPublicNetworkAccess = false (got {pna!r}).")

    return errors


def _split_top_level_args(arg_str: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    in_quote = False
    i = 0
    while i < len(arg_str):
        ch = arg_str[i]
        if ch == "'":
            if in_quote and i + 1 < len(arg_str) and arg_str[i + 1] == "'":
                current.append("''")
                i += 2
                continue
            in_quote = not in_quote
            current.append(ch)
        elif not in_quote:
            if ch == "(":
                depth += 1
                current.append(ch)
            elif ch == ")":
                depth -= 1
                current.append(ch)
            elif ch == "," and depth == 0:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        else:
            current.append(ch)
        i += 1
    if current:
        parts.append("".join(current).strip())
    return parts


def _parse_arm_create_objects(expr: str) -> list[dict[str, str]]:
    marker = "createObject("
    objects: list[dict[str, str]] = []
    pos = 0
    while True:
        idx = expr.find(marker, pos)
        if idx == -1:
            break
        start = idx + len(marker)
        depth = 1
        in_quote = False
        cursor = start
        while cursor < len(expr) and depth > 0:
            ch = expr[cursor]
            if ch == "'":
                if in_quote and cursor + 1 < len(expr) and expr[cursor + 1] == "'":
                    cursor += 2
                    continue
                in_quote = not in_quote
            elif not in_quote:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
            cursor += 1
        inner = expr[start : cursor - 1]
        args = _split_top_level_args(inner)
        if len(args) >= 2 and len(args) % 2 == 0:
            parsed: dict[str, str] = {}
            for k_idx in range(0, len(args), 2):
                key_tok = args[k_idx].strip()
                val_tok = args[k_idx + 1].strip()
                if key_tok.startswith("'") and key_tok.endswith("'"):
                    key_tok = key_tok[1:-1]
                if val_tok.startswith("'") and val_tok.endswith("'"):
                    val_tok = val_tok[1:-1]
                parsed[key_tok] = val_tok
            objects.append(parsed)
        pos = cursor
    return objects


def _extract_secret_entries_from_arm(secrets_prop: Any) -> list[dict[str, str]]:
    """Extract secret dicts from either a static ARM list or a compiled createObject expression."""
    if isinstance(secrets_prop, list):
        extracted: list[dict[str, str]] = []
        for entry in secrets_prop:
            if not isinstance(entry, dict):
                continue
            item = {str(k): str(v) for k, v in entry.items()}
            extracted.append(item)
        return extracted
    if isinstance(secrets_prop, str):
        return [
            obj
            for obj in _parse_arm_create_objects(secrets_prop)
            if "keyVaultUrl" in obj or "value" in obj
        ]
    return []


def _extract_env_entries_from_arm(env_prop: Any) -> list[dict[str, Any]]:
    if isinstance(env_prop, list):
        return [e for e in env_prop if isinstance(e, dict)]
    if isinstance(env_prop, str):
        return [
            obj
            for obj in _parse_arm_create_objects(env_prop)
            if "name" in obj and ("value" in obj or "secretRef" in obj)
        ]
    return []


def validate_secret_bindings_and_env(
    inventory: dict[str, Any],
    secret_inventory: dict[str, Any],
    compiled_workloads: dict[str, dict[str, Any]],
    all_bicepparams: dict[str, dict[str, Any]],
    bicep_tree: Any,
) -> list[str]:
    """Return all AC2 contract violations (empty list means zero literal secrets and MI-only KV)."""
    errors: list[str] = []

    lifecycle_names = {s["name"] for s in secret_inventory.get("secrets", [])}
    declared_bindings = inventory.get("secretBindings", [])
    if not declared_bindings:
        errors.append("inventory secretBindings must not be empty.")

    for binding in declared_bindings:
        kv_name = binding.get("keyVaultSecretName")
        if kv_name not in lifecycle_names:
            errors.append(
                f"secretBinding {binding.get('containerSecretName')!r} references "
                f"keyVaultSecretName {kv_name!r} absent from infra/secret-inventory.json."
            )

    observed_kv_secret_count = 0
    for template_label, compiled in sorted(compiled_workloads.items()):
        for res in iter_arm_resources(compiled):
            rtype = res.get("type")
            if rtype not in ("Microsoft.App/containerApps", "Microsoft.App/jobs"):
                continue
            rname = str(res.get("name", "<unnamed>"))
            identity_type = res.get("identity", {}).get("type")
            if identity_type != "UserAssigned":
                errors.append(
                    f"{template_label}:{rname} must use identity.type == 'UserAssigned' "
                    f"(got {identity_type!r})."
                )

            config = res.get("properties", {}).get("configuration", {})
            for reg in config.get("registries", []):
                if "passwordSecretRef" in reg or not reg.get("identity"):
                    errors.append(
                        f"{template_label}:{rname} registry pull must use managed identity, "
                        "never passwordSecretRef."
                    )

            secrets_prop = config.get("secrets", [])
            if isinstance(secrets_prop, str) and "'value'" in secrets_prop:
                errors.append(
                    f"{template_label}:{rname} configuration.secrets expression contains "
                    "a forbidden literal 'value' property."
                )
            parsed_secrets = _extract_secret_entries_from_arm(secrets_prop)
            declared_secret_names: set[str] = set()
            for sec in parsed_secrets:
                observed_kv_secret_count += 1
                sec_name = sec.get("name", "<unnamed>")
                declared_secret_names.add(sec_name)
                if "value" in sec:
                    errors.append(
                        f"{template_label}:{rname} secret {sec_name!r} uses literal 'value' "
                        "instead of Key Vault keyVaultUrl."
                    )
                if not sec.get("keyVaultUrl") or "secrets/" not in sec.get("keyVaultUrl", ""):
                    errors.append(
                        f"{template_label}:{rname} secret {sec_name!r} lacks a valid Key Vault "
                        "keyVaultUrl."
                    )
                if not sec.get("identity"):
                    errors.append(
                        f"{template_label}:{rname} secret {sec_name!r} lacks a user-assigned "
                        "managed identity reference."
                    )

            containers = res.get("properties", {}).get("template", {}).get("containers", [])
            for container in containers:
                for env_item in _extract_env_entries_from_arm(container.get("env", [])):
                    env_name = str(env_item.get("name", ""))
                    if "secretRef" in env_item:
                        if "value" in env_item:
                            errors.append(
                                f"{template_label}:{rname} env {env_name!r} cannot set both "
                                "secretRef and value."
                            )
                        sref = str(env_item["secretRef"])
                        if sref not in declared_secret_names:
                            errors.append(
                                f"{template_label}:{rname} env {env_name!r} references undeclared "
                                f"secretRef {sref!r}."
                            )
                    else:
                        raw_val = str(env_item.get("value", ""))
                        if (
                            SECRET_ENV_NAME_PATTERN.search(env_name)
                            and env_name not in ALLOWED_NON_SECRET_ENV_NAMES
                        ):
                            errors.append(
                                f"{template_label}:{rname} secret-like env {env_name!r} must use "
                                "secretRef rather than a literal value."
                            )
                        if LITERAL_SECRET_VALUE_PATTERN.search(raw_val):
                            errors.append(
                                f"{template_label}:{rname} env {env_name!r} value matches a "
                                "forbidden credential/key pattern."
                            )

    if observed_kv_secret_count != len(declared_bindings):
        errors.append(
            f"Compiled Container Apps secret count ({observed_kv_secret_count}) != "
            f"inventory secretBindings count ({len(declared_bindings)})."
        )

    for bparam_label, params in sorted(all_bicepparams.items()):
        for pname, pobj in sorted(params.items()):
            pval = pobj.get("value")
            if isinstance(pval, str) and LITERAL_SECRET_VALUE_PATTERN.search(pval):
                errors.append(
                    f"{bparam_label} parameter {pname!r} contains a forbidden credential/secret "
                    "value."
                )
            if SECRET_ENV_NAME_PATTERN.search(pname) and isinstance(pval, str) and pval.strip():
                if not pname.lower().endswith("secretname"):
                    errors.append(
                        f"{bparam_label} secret-named parameter {pname!r} sets a literal value."
                    )

    for rel_path, summary in sorted(bicep_tree.files.items()):
        for fn_name in FORBIDDEN_BICEP_SECRET_FUNCTIONS:
            if re.search(rf"\b{re.escape(fn_name)}\s*\(", summary.uncommented_source):
                errors.append(
                    f"{rel_path} invokes forbidden credential helper {fn_name}() instead of "
                    "managed identity."
                )

    return errors


def validate_network_diagram_parity(
    inventory: dict[str, Any],
    doc_text: str,
    arch_readme_text: str,
    infra_readme_text: str,
    compiled_main: dict[str, Any],
    compiled_publisher: dict[str, Any],
) -> list[str]:
    """Return all AC3 parity violations between Bicep, inventory JSON, and network-posture.md."""
    errors: list[str] = []

    mermaid_match = MERMAID_BLOCK_RE.search(doc_text)
    if mermaid_match is None:
        return ["docs/architecture/network-posture.md is missing a ```mermaid diagram block."]
    mermaid_body = mermaid_match.group(1)

    nested_by_path = {
        path: (dep, sub_tpl) for path, dep, sub_tpl in iter_nested_deployments(compiled_main)
    }
    net_entry = nested_by_path.get(("network",))
    if net_entry is None:
        return ["Compiled main.bicep is missing the 'network' module deployment."]
    _, net_tpl = net_entry

    vnet_res = next(
        (
            r
            for r in net_tpl.get("resources", [])
            if r.get("type") == "Microsoft.Network/virtualNetworks"
        ),
        None,
    )
    if vnet_res is None:
        return ["Compiled network.bicep is missing Microsoft.Network/virtualNetworks."]

    vnet_default_cidr = (
        net_tpl.get("parameters", {}).get("vnetAddressPrefix", {}).get("defaultValue")
    )
    if vnet_default_cidr != inventory["vnet"]["defaultCidr"]:
        errors.append(
            f"VNet default CIDR {vnet_default_cidr!r} != inventory "
            f"{inventory['vnet']['defaultCidr']!r}."
        )
    if inventory["vnet"]["defaultCidr"] not in mermaid_body:
        errors.append("Mermaid diagram is missing VNet default CIDR.")

    subnets_expr = json.dumps(vnet_res.get("properties", {}).get("subnets", ""))
    param_defaults = {
        "snet-aca": net_tpl.get("parameters", {}).get("acaSubnetPrefix", {}).get("defaultValue"),
        "snet-pe": net_tpl.get("parameters", {})
        .get("privateEndpointSubnetPrefix", {})
        .get("defaultValue"),
        "snet-aca-demo": net_tpl.get("parameters", {})
        .get("demoAcaSubnetPrefix", {})
        .get("defaultValue"),
    }
    for snet in inventory["vnet"]["subnets"]:
        sname = snet["name"]
        if f"'{sname}'" not in subnets_expr and f'"{sname}"' not in subnets_expr:
            errors.append(f"Subnet {sname!r} missing from compiled network.bicep VNet.")
        if param_defaults.get(sname) != snet["defaultCidr"]:
            errors.append(
                f"Subnet {sname!r} default CIDR {param_defaults.get(sname)!r} != "
                f"{snet['defaultCidr']!r}."
            )
        for target_label, text_blob in (
            ("Mermaid diagram", mermaid_body),
            ("Markdown tables", doc_text),
        ):
            if sname not in text_blob or snet["defaultCidr"] not in text_blob:
                errors.append(
                    f"Subnet {sname!r} ({snet['defaultCidr']}) missing from {target_label} in "
                    "docs/architecture/network-posture.md."
                )
            if snet["nsgNameExpression"] not in text_blob:
                errors.append(
                    f"NSG {snet['nsgNameExpression']!r} missing from {target_label} in "
                    "docs/architecture/network-posture.md."
                )

    pub_subnets = [
        r
        for r in iter_arm_resources(compiled_publisher)
        if r.get("type") == "Microsoft.Network/virtualNetworks/subnets"
    ]
    pub_stem = str(compiled_publisher.get("variables", {}).get("stem", ""))
    resolved_pub_subnets = [
        (
            str(r.get("name", "")).replace("{0}", pub_stem),
            str(r.get("properties", {}).get("addressPrefix", "")),
        )
        for r in pub_subnets
    ]
    for standalone in inventory["vnet"].get("standaloneChildSubnets", []):
        st_name = standalone["name"]
        matching_pub = [cidr for cand_name, cidr in resolved_pub_subnets if st_name in cand_name]
        if not matching_pub:
            errors.append(
                f"Standalone child subnet {st_name!r} missing from compiled "
                f"{standalone['bicepPath']}."
            )
        elif matching_pub[0] != standalone["defaultCidr"]:
            errors.append(
                f"Standalone child subnet {st_name!r} default CIDR {matching_pub[0]!r} != "
                f"{standalone['defaultCidr']!r}."
            )
        if st_name not in mermaid_body or standalone["defaultCidr"] not in doc_text:
            errors.append(
                f"Standalone child subnet {st_name!r} missing from "
                "docs/architecture/network-posture.md."
            )

    compiled_dns_zones: list[str] = list(net_tpl.get("variables", {}).get("dnsZones", []))
    static_inv_zones = [
        z for z in inventory["privateDnsZones"] if z["bicepPath"] == "infra/modules/network.bicep"
    ]
    if len(compiled_dns_zones) != len(static_inv_zones):
        errors.append(
            f"Compiled network.bicep dnsZones count ({len(compiled_dns_zones)}) != "
            f"inventory count ({len(static_inv_zones)})."
        )

    vnet_links = [
        r
        for r in net_tpl.get("resources", [])
        if r.get("type") == "Microsoft.Network/privateDnsZones/virtualNetworkLinks"
    ]
    if (
        not vnet_links
        or vnet_links[0].get("properties", {}).get("registrationEnabled") is not False
    ):
        errors.append(
            "network.bicep virtualNetworkLinks must exist and set registrationEnabled: false."
        )

    env_dns_candidates = [
        sub_tpl
        for path, (_, sub_tpl) in nested_by_path.items()
        if path[0] == "containerapps"
        and any(
            r.get("type") == "Microsoft.Network/privateDnsZones"
            for r in sub_tpl.get("resources", [])
        )
    ]
    if not env_dns_candidates:
        errors.append("Compiled containerapps module is missing conditional envDns privateDnsZone.")

    for zone in inventory["privateDnsZones"]:
        zkey = zone["key"]
        zname = zone["zoneName"]
        vlink = zone["vnetLinkNameExpression"]
        if zkey not in mermaid_body or zname not in mermaid_body:
            errors.append(
                f"Private DNS zone {zkey!r} ({zname}) missing from Mermaid diagram in "
                "docs/architecture/network-posture.md."
            )
        if f"| `{zkey}` |" not in doc_text or zname not in doc_text or vlink not in doc_text:
            errors.append(
                f"Private DNS zone {zkey!r} ({zname}) or VNet link {vlink!r} missing from "
                "Markdown table in docs/architecture/network-posture.md."
            )
        if vlink not in mermaid_body:
            errors.append(f"VNet link {vlink!r} missing from Mermaid diagram.")

    for store in inventory["dataStores"]:
        sid = store["id"]
        gid = store["groupId"]
        pe_dep = store["peDeploymentName"]
        if f"groupId: {gid}" not in mermaid_body:
            errors.append(
                f"Private endpoint groupId {gid!r} for store {sid!r} missing from Mermaid diagram."
            )
        if (
            f"| `{sid}` |" not in doc_text
            or f"`{pe_dep}`" not in doc_text
            or f"`{gid}`" not in doc_text
        ):
            errors.append(
                f"Data store {sid!r} ({pe_dep}, groupId={gid}) missing from data-store table in "
                "docs/architecture/network-posture.md."
            )

    edge_entry = nested_by_path.get(("edge",))
    if edge_entry is None:
        errors.append("Compiled main.bicep is missing conditional 'edge' deployment.")
    else:
        _, edge_tpl = edge_entry
        origins = [
            r
            for r in edge_tpl.get("resources", [])
            if r.get("type") == "Microsoft.Cdn/profiles/originGroups/origins"
        ]
        spl_group = (
            origins[0].get("properties", {}).get("sharedPrivateLinkResource", {}).get("groupId")
            if origins
            else None
        )
        if spl_group != "managedEnvironments":
            errors.append(
                f"Front Door origin sharedPrivateLinkResource groupId {spl_group!r} != "
                "'managedEnvironments'."
            )
        if "sharedPrivateLinkResource" not in mermaid_body or "managedEnvironments" not in doc_text:
            errors.append(
                "Front Door sharedPrivateLinkResource (managedEnvironments) missing from "
                "docs/architecture/network-posture.md."
            )

    for exc in inventory["exerciseExceptions"]:
        eid = exc["id"]
        if f"| `{eid}` |" not in doc_text:
            errors.append(
                f"Exercise exception {eid!r} missing from Recorded Exercise Exceptions table in "
                "docs/architecture/network-posture.md."
            )

    for binding in inventory["secretBindings"]:
        kv_sec = binding["keyVaultSecretName"]
        if f"`{kv_sec}`" not in doc_text:
            errors.append(
                f"Key Vault secret binding {kv_sec!r} missing from secret table in "
                "docs/architecture/network-posture.md."
            )

    if "./network-posture.md" not in arch_readme_text:
        errors.append("docs/architecture/README.md must link to ./network-posture.md.")
    if "network-posture-inventory.json" not in infra_readme_text:
        errors.append("infra/README.md must document network-posture-inventory.json.")

    return errors


class TestNetworkPosture(unittest.TestCase):
    bicep_mod: ClassVar[Any]
    bicep_tree: ClassVar[Any]
    inventory: ClassVar[dict[str, Any]]
    secret_inventory: ClassVar[dict[str, Any]]
    compiled_main: ClassVar[dict[str, Any]]
    compiled_workloads: ClassVar[dict[str, dict[str, Any]]]
    compiled_publisher: ClassVar[dict[str, Any]]
    main_bicepparams: ClassVar[dict[str, dict[str, Any]]]
    all_bicepparams: ClassVar[dict[str, dict[str, Any]]]
    doc_text: ClassVar[str]
    arch_readme_text: ClassVar[str]
    infra_readme_text: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.bicep_mod = _load_bicep_inventory_module()
        cls.bicep_tree = cls.bicep_mod.scan_bicep_tree(REPO_ROOT)
        cls.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        cls.secret_inventory = json.loads(SECRET_INVENTORY_PATH.read_text(encoding="utf-8"))
        cls.compiled_main = compile_bicep_file("main.bicep")
        cls.compiled_workloads = {
            "main.bicep": cls.compiled_main,
            "resident-demo.bicep": compile_bicep_file("resident-demo.bicep"),
            "live-simulator-job.bicep": compile_bicep_file("live-simulator-job.bicep"),
            "live-receiver-job.bicep": compile_bicep_file("live-receiver-job.bicep"),
        }
        cls.compiled_publisher = compile_bicep_file("private-proof-publisher.bicep")
        cls.main_bicepparams = {
            name: compile_bicepparam_file(name)
            for name in (
                "main.bicepparam",
                "main.test.bicepparam",
                "main.pilot.example.bicepparam",
            )
        }
        cls.all_bicepparams = {
            **cls.main_bicepparams,
            "iot-hub-live.bicepparam": compile_bicepparam_file("iot-hub-live.bicepparam"),
        }
        cls.doc_text = DOC_PATH.read_text(encoding="utf-8")
        cls.arch_readme_text = ARCH_README_PATH.read_text(encoding="utf-8")
        cls.infra_readme_text = INFRA_README_PATH.read_text(encoding="utf-8")

    def test_ac1_every_data_store_has_private_endpoint_or_owned_exception(self) -> None:
        self.assertEqual(len(self.bicep_tree.files), 30)
        required_ids = {c.component_id for c in self.bicep_mod.REQUIRED_ARCHITECTURE_COMPONENTS}
        for expected_component in (
            "network-vnet-nsg-dns-pe",
            "key-vault-resource",
            "key-vault-secret-values",
            "storage-blobs-worm-queues",
            "entra-token-store",
            "container-registry",
            "azure-sql-and-ledger",
            "microsoft-foundry-models",
            "iot-hub-and-eventhub-adapter",
            "monitoring-logs-ampls-alerts",
            "public-edge-frontdoor-waf",
        ):
            self.assertIn(expected_component, required_ids)

        errors = validate_data_store_posture(
            self.inventory,
            self.bicep_tree,
            self.compiled_main,
            self.main_bicepparams,
        )
        self.assertEqual(errors, [])

    def test_ac2_secrets_read_from_key_vault_via_managed_identity_zero_literal_secrets(
        self,
    ) -> None:
        errors = validate_secret_bindings_and_env(
            self.inventory,
            self.secret_inventory,
            self.compiled_workloads,
            self.all_bicepparams,
            self.bicep_tree,
        )
        self.assertEqual(errors, [])

        runtime_files = {
            "src/orchestrator/src/zava_forward/orchestrator/token_store.py": (
                "entra-token-store-sas",
                "get_user_delegation_key",
                "get_token",
            ),
            "src/core/src/zava_forward/core/mssqlstore.py": (
                "ZF_SQL_AUTH",
                "msi",
            ),
            "src/api/src/zava_forward/api/iot_stream.py": ("ManagedIdentityCredential",),
            "src/agents/src/zava_forward/agents/heldout_aoai.py": ("managed-identity",),
            "src/api/src/zava_forward/api/resident_demo/aoai.py": ("ManagedIdentityCredential",),
        }
        for rel_py, required_tokens in runtime_files.items():
            py_source = (REPO_ROOT / rel_py).read_text(encoding="utf-8")
            for token in required_tokens:
                self.assertIn(token, py_source, f"{rel_py} missing expected MI token {token!r}")
            self.assertIsNone(
                LITERAL_SECRET_VALUE_PATTERN.search(py_source),
                f"{rel_py} contains a literal credential pattern",
            )
            self.assertNotIn(
                "SecretClient",
                py_source,
                f"{rel_py} must not read Key Vault directly via SecretClient on request paths",
            )

    def test_ac3_network_diagram_matches_bicep_modules(self) -> None:
        errors = validate_network_diagram_parity(
            self.inventory,
            self.doc_text,
            self.arch_readme_text,
            self.infra_readme_text,
            self.compiled_main,
            self.compiled_publisher,
        )
        self.assertEqual(errors, [])

        forbidden_tracking_marker = ".copilot" + "-tracking/"
        for clean_path in (INVENTORY_PATH, DOC_PATH, Path(__file__)):
            content = clean_path.read_text(encoding="utf-8")
            self.assertNotIn(
                forbidden_tracking_marker,
                content,
                f"{clean_path} must not contain internal tracking references",
            )

    def test_negative_unprotected_data_store_or_ownerless_exception_fails_closed(self) -> None:
        mutated_missing_store = deepcopy(self.inventory)
        mutated_missing_store["dataStores"] = [
            s for s in mutated_missing_store["dataStores"] if s["id"] != "sql"
        ]
        errors_missing = validate_data_store_posture(
            mutated_missing_store,
            self.bicep_tree,
            self.compiled_main,
            self.main_bicepparams,
        )
        self.assertTrue(
            any("infra/modules/sql.bicep" in err for err in errors_missing),
            errors_missing,
        )

        mutated_bad_exception = deepcopy(self.inventory)
        mutated_bad_exception["exerciseExceptions"][0]["owner"] = "TBD"
        mutated_bad_exception["exerciseExceptions"][0]["rationale"] = "none"
        errors_exc = validate_data_store_posture(
            mutated_bad_exception,
            self.bicep_tree,
            self.compiled_main,
            self.main_bicepparams,
        )
        self.assertTrue(any("missing a valid named owner" in err for err in errors_exc))
        self.assertTrue(any("missing a substantive rationale" in err for err in errors_exc))

        mutated_missing_existing = deepcopy(self.inventory)
        mutated_missing_existing["existingStoreReferences"].pop()
        errors_existing = validate_data_store_posture(
            mutated_missing_existing,
            self.bicep_tree,
            self.compiled_main,
            self.main_bicepparams,
        )
        self.assertTrue(
            any("unaccounted in existingStoreReferences" in err for err in errors_existing)
        )

    def test_negative_literal_secret_in_container_app_or_env_fails_closed(self) -> None:
        mutated_workloads = deepcopy(self.compiled_workloads)
        rd_resources = mutated_workloads["resident-demo.bicep"]["resources"]
        ca_app = next(r for r in rd_resources if r["type"] == "Microsoft.App/containerApps")
        ca_app["properties"]["configuration"]["secrets"].append(
            {"name": "rogue-inline-secret", "value": "super-secret-plaintext"}
        )
        ca_app["properties"]["template"]["containers"][0]["env"].append(
            {
                "name": "STORAGE_CONNECTION_STRING",
                "value": "DefaultEndpointsProtocol=https;AccountName=x;AccountKey=abc123==",
            }
        )
        errors = validate_secret_bindings_and_env(
            self.inventory,
            self.secret_inventory,
            mutated_workloads,
            self.all_bicepparams,
            self.bicep_tree,
        )
        self.assertTrue(any("uses literal 'value'" in err for err in errors), errors)
        self.assertTrue(any("lacks a valid Key Vault keyVaultUrl" in err for err in errors), errors)
        self.assertTrue(any("STORAGE_CONNECTION_STRING" in err for err in errors), errors)

    def test_negative_network_diagram_drift_fails_closed(self) -> None:
        drifted_doc = self.doc_text.replace("privatelink.servicebus.windows.net", "removed.zone")
        drifted_doc = drifted_doc.replace("groupId: sqlServer", "groupId: driftedGroup")
        errors = validate_network_diagram_parity(
            self.inventory,
            drifted_doc,
            self.arch_readme_text,
            self.infra_readme_text,
            self.compiled_main,
            self.compiled_publisher,
        )
        self.assertTrue(
            any("iotHubEndpoint" in err for err in errors),
            errors,
        )
        self.assertTrue(
            any("sqlServer" in err for err in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
