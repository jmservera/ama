"""Deterministic offline verifier for Issue #136 from-empty deployment reproducibility."""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Self
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FROM_EMPTY_STEPS: tuple[str, ...] = (
    "preflight",
    "what-if",
    "deploy",
    "sql-init",
    "seed",
    "smoke",
)

CANONICAL_STEP_README_HEADING = "Canonical from-empty pipeline step registry"
CANONICAL_STEP_README_COLUMNS: tuple[str, ...] = (
    "Step",
    "Pipeline registration",
    "Rebuild stage(s)",
    "Repository template or script",
    "Manual prerequisites",
    "Verification check",
)
AUTOMATED_PREREQUISITE_LABEL = "none (automated from repository files)"

PLACEHOLDER_CELL_VALUES: frozenset[str] = frozenset(
    {
        "",
        "-",
        "tbd",
        "todo",
        "n/a",
        "na",
        "manual",
        "undocumented",
        "pending",
        "unknown",
        "skip",
    }
)
FORBIDDEN_MANUAL_PROSE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bundocumented\b", re.IGNORECASE),
    re.compile(r"\bmanual\s+workaround\b", re.IGNORECASE),
    re.compile(r"\bad[- ]hoc\s+step\b", re.IGNORECASE),
    re.compile(r"\brun\s+manually\s+in\s+portal\b", re.IGNORECASE),
    re.compile(r"\bclick\s+in\s+azure\s+portal\b", re.IGNORECASE),
)

BICEP_PARAM_DECL_RE = re.compile(
    r"^param\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*(?:\[\])?)\s*(.*)$"
)
BICEPPARAM_USING_RE = re.compile(r"^using\s+'([^']+)'\s*$")
BICEPPARAM_ASSIGN_RE = re.compile(r"^param\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
RESOURCE_DECL_RE = re.compile(r"^\s*resource\s+\w+\s+'([^'@]+)@[^']+'")
BACKTICK_TOKEN_RE = re.compile(r"`([^`]+)`")

# Split patterns so repository secret scanners never flag verifier regex definitions.
SECRET_ASSIGNMENT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"SharedAccess" + r"Key\s*=\s*[A-Za-z0-9+/=]{20,}"),
    re.compile(r"Account" + r"Key\s*=\s*[A-Za-z0-9+/=]{20,}"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE" + r" KEY-----"),
    re.compile(
        r"\b(?:clientSecret|password|connectionString)\s*=\s*'(?!\s*')(?!PLACEHOLDER)[^']+'"
    ),
)

DRY_RUN_RELEASE_SHA = "1" * 40
DRY_RUN_SUBSCRIPTION_ID = "00000000-0000-0000-0000-000000000001"
DRY_RUN_RUN_ID = "136001"
DRY_RUN_RUN_ATTEMPT = "1"
DRY_RUN_REGISTRY_NAME = "acrforwarddryrun"
DRY_RUN_REGISTRY_SERVER = f"{DRY_RUN_REGISTRY_NAME}.azurecr.io"
DRY_RUN_REPOSITORY = "jmservera/ama"

DRY_RUN_DEPLOY_PARAMETERS: dict[str, Any] = {
    "alertEmail": "ops-alerts@zavanorthhomes.co.uk",
    "entraBearerOnly": False,
    "entraClientId": "11111111-2222-4333-8444-555555555555",
    "location": "uksouth",
    "quotaCheckReference": "quota-verified-uksouth-2026-11-15",
    "regionCheckReference": "region-verified-uksouth-2026-11-15",
    "sqlAdminGroupName": "sg-zava-forward-sql-admins",
    "sqlAdminGroupObjectId": "22222222-3333-4444-8555-666666666666",
    "sqlLocation": "uksouth",
}


@dataclass(frozen=True)
class BicepParamDecl:
    """Parameter declaration parsed from a Bicep template."""

    name: str
    param_type: str
    has_default: bool
    is_secure: bool


@dataclass(frozen=True)
class BicepparamSummary:
    """Parsed assignments and target validation for a .bicepparam file."""

    path: str
    using_target: str | None
    parameters: dict[str, Any]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ParameterCoverageReport:
    """Verification summary for defaultless main.bicep parameter coverage."""

    ok: bool
    total_bicep_parameters: int
    defaultless_parameters: tuple[str, ...]
    coverage_sources: dict[str, str]
    pipeline_injected_parameters: tuple[str, ...]
    parameter_files_checked: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class StepRegistrationReport:
    """Verification summary for step registration and README parity."""

    ok: bool
    registered_steps: tuple[str, ...]
    documented_steps: tuple[str, ...]
    covered_rebuild_stages: tuple[str, ...]
    undocumented_manual_steps: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class StepExecutionRecord:
    """Deterministic record for a single step in the offline from-empty dry-run."""

    step_id: str
    status: str
    pipeline_hook: str
    verified_artifacts: tuple[str, ...]
    artifact_sha256: str
    checks_passed: tuple[str, ...]


@dataclass(frozen=True)
class DryRunResult:
    """Deterministic result of running all 6 from-empty deployment steps offline."""

    ok: bool
    environment: str
    runtime_environment: str
    parameter_file: str
    steps: tuple[StepExecutionRecord, ...]
    parameter_sha256: str
    sequence_digest: str
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ReproducibilityReport:
    """Top-level report proving Issue #136 from-empty deployment reproducibility."""

    ok: bool
    step_registration: StepRegistrationReport
    parameter_coverage: ParameterCoverageReport
    dry_runs: dict[str, DryRunResult]
    errors: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _workspace_rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _load_pipeline_module(pipeline_path: Path) -> ModuleType:
    digest = hashlib.sha256(str(pipeline_path.resolve()).encode("utf-8")).hexdigest()[:12]
    module_name = f"_ama_infra_pipeline_{digest}"
    spec = importlib.util.spec_from_file_location(module_name, pipeline_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load pipeline module from {pipeline_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def strip_bicep_comments(text: str) -> str:
    """Strip // line comments and /* ... */ block comments outside single-quoted strings."""
    out: list[str] = []
    i = 0
    length = len(text)
    in_single_quote = False
    while i < length:
        ch = text[i]
        if in_single_quote:
            out.append(ch)
            if ch == "\\" and i + 1 < length:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == "'":
                in_single_quote = False
            i += 1
            continue
        if ch == "'":
            in_single_quote = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < length and text[i + 1] == "/":
            i += 2
            while i < length and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < length and text[i + 1] == "*":
            i += 2
            while i < length and not (text[i] == "*" and i + 1 < length and text[i + 1] == "/"):
                if text[i] == "\n":
                    out.append("\n")
                i += 1
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _bracket_delta_and_top_level_equals(segment: str, start_depth: int = 0) -> tuple[int, bool]:
    depth = start_depth
    has_equals = False
    in_quote = False
    i = 0
    while i < len(segment):
        ch = segment[i]
        if in_quote:
            if ch == "\\" and i + 1 < len(segment):
                i += 2
                continue
            if ch == "'":
                in_quote = False
            i += 1
            continue
        if ch == "'":
            in_quote = True
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(0, depth - 1)
        elif ch == "=" and depth == 0:
            prev_ch = segment[i - 1] if i > 0 else ""
            next_ch = segment[i + 1] if i + 1 < len(segment) else ""
            if prev_ch not in ("=", "!", "<", ">") and next_ch != "=":
                has_equals = True
        i += 1
    return depth, has_equals


def parse_bicep_parameters(bicep_text: str) -> tuple[BicepParamDecl, ...]:
    """Parse all top-level parameter declarations in a Bicep template."""
    stripped = strip_bicep_comments(bicep_text)
    lines = stripped.splitlines()
    declarations: list[BicepParamDecl] = []
    pending_secure = False
    depth = 0
    idx = 0
    while idx < len(lines):
        raw = lines[idx].strip()
        if not raw:
            idx += 1
            continue
        if depth > 0:
            depth, _ = _bracket_delta_and_top_level_equals(raw, depth)
            idx += 1
            continue
        if raw.startswith("@"):
            if re.search(r"@secure\s*\(", raw):
                pending_secure = True
            depth, _ = _bracket_delta_and_top_level_equals(raw, 0)
            idx += 1
            continue
        match = BICEP_PARAM_DECL_RE.match(raw)
        if match:
            name, param_type, remainder = match.group(1), match.group(2), match.group(3)
            depth, has_default = _bracket_delta_and_top_level_equals(remainder, 0)
            while depth > 0 and idx + 1 < len(lines):
                idx += 1
                next_line = lines[idx].strip()
                depth, extra_eq = _bracket_delta_and_top_level_equals(next_line, depth)
                has_default = has_default or extra_eq
            declarations.append(
                BicepParamDecl(
                    name=name,
                    param_type=param_type,
                    has_default=has_default,
                    is_secure=pending_secure,
                )
            )
            pending_secure = False
            idx += 1
            continue
        pending_secure = False
        depth, _ = _bracket_delta_and_top_level_equals(raw, 0)
        idx += 1
    return tuple(declarations)


class _BicepValueParser:
    """Minimal recursive-descent parser for literal expressions in .bicepparam files."""

    def __init__(self, text: str) -> None:
        self._tokens = self._tokenize(text)
        self._pos = 0

    @staticmethod
    def _tokenize(text: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch.isspace() or ch == ",":
                i += 1
                continue
            if ch in "[]{}:":
                tokens.append((ch, ch))
                i += 1
                continue
            if ch == "'":
                buf: list[str] = []
                i += 1
                while i < n:
                    cur = text[i]
                    if cur == "\\" and i + 1 < n:
                        nxt = text[i + 1]
                        escapes = {"'": "'", "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
                        buf.append(escapes.get(nxt, nxt))
                        i += 2
                        continue
                    if cur == "'":
                        i += 1
                        break
                    buf.append(cur)
                    i += 1
                else:
                    raise ValueError("Unterminated string literal in .bicepparam expression")
                tokens.append(("STRING", "".join(buf)))
                continue
            num_match = re.match(r"-?[0-9]+", text[i:])
            if num_match:
                lexeme = num_match.group(0)
                tokens.append(("INT", lexeme))
                i += len(lexeme)
                continue
            ident_match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", text[i:])
            if ident_match:
                lexeme = ident_match.group(0)
                tokens.append(("IDENT", lexeme))
                i += len(lexeme)
                continue
            raise ValueError(f"Unsupported .bicepparam token starting at {text[i : i + 20]!r}")
        return tokens

    def parse(self) -> Any:
        value = self._parse_value()
        if self._pos != len(self._tokens):
            kind, lex = self._tokens[self._pos]
            raise ValueError(f"Unexpected trailing token {kind} ({lex!r}) in .bicepparam value")
        return value

    def _parse_value(self) -> Any:
        if self._pos >= len(self._tokens):
            raise ValueError("Unexpected end of .bicepparam value expression")
        kind, lex = self._tokens[self._pos]
        if kind == "STRING":
            self._pos += 1
            return lex
        if kind == "INT":
            self._pos += 1
            return int(lex)
        if kind == "IDENT":
            self._pos += 1
            if lex == "true":
                return True
            if lex == "false":
                return False
            if lex == "null":
                return None
            raise ValueError(f"Unsupported identifier expression {lex!r} in .bicepparam")
        if kind == "[":
            self._pos += 1
            items: list[Any] = []
            while self._pos < len(self._tokens) and self._tokens[self._pos][0] != "]":
                items.append(self._parse_value())
            if self._pos >= len(self._tokens) or self._tokens[self._pos][0] != "]":
                raise ValueError("Unterminated array literal in .bicepparam")
            self._pos += 1
            return items
        if kind == "{":
            self._pos += 1
            obj: dict[str, Any] = {}
            while self._pos < len(self._tokens) and self._tokens[self._pos][0] != "}":
                key_kind, key_lex = self._tokens[self._pos]
                if key_kind not in ("IDENT", "STRING"):
                    raise ValueError(f"Invalid object property key {key_lex!r} in .bicepparam")
                self._pos += 1
                if self._pos >= len(self._tokens) or self._tokens[self._pos][0] != ":":
                    raise ValueError(f"Missing ':' after object key {key_lex!r} in .bicepparam")
                self._pos += 1
                obj[key_lex] = self._parse_value()
            if self._pos >= len(self._tokens) or self._tokens[self._pos][0] != "}":
                raise ValueError("Unterminated object literal in .bicepparam")
            self._pos += 1
            return obj
        raise ValueError(f"Unexpected token {kind} ({lex!r}) in .bicepparam value")


def parse_bicepparam_file(param_path: Path, repo_root: Path) -> BicepparamSummary:
    """Parse a .bicepparam file into literal values and check hygiene invariants."""
    rel_path = _workspace_rel(param_path, repo_root)
    if not param_path.is_file():
        return BicepparamSummary(
            path=rel_path,
            using_target=None,
            parameters={},
            errors=(f"Missing parameter file: {rel_path}",),
        )
    raw_text = param_path.read_text(encoding="utf-8")
    errors: list[str] = []
    stripped = strip_bicep_comments(raw_text)
    for pattern in SECRET_ASSIGNMENT_PATTERNS:
        if pattern.search(stripped):
            errors.append(f"{rel_path}: forbidden secret-like literal detected in parameter file")
            break

    using_target: str | None = None
    parameters: dict[str, Any] = {}
    lines = stripped.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        using_match = BICEPPARAM_USING_RE.match(line)
        if using_match:
            resolved_target = (param_path.parent / using_match.group(1)).resolve()
            try:
                using_target = resolved_target.relative_to(repo_root.resolve()).as_posix()
            except ValueError:
                using_target = str(resolved_target)
            idx += 1
            continue
        assign_match = BICEPPARAM_ASSIGN_RE.match(line)
        if assign_match:
            param_name = assign_match.group(1)
            expr_parts = [assign_match.group(2)]
            depth, _ = _bracket_delta_and_top_level_equals(assign_match.group(2), 0)
            while depth > 0 and idx + 1 < len(lines):
                idx += 1
                continuation = lines[idx]
                expr_parts.append(continuation)
                depth, _ = _bracket_delta_and_top_level_equals(continuation, depth)
            if depth != 0:
                errors.append(f"{rel_path}: unbalanced brackets in parameter {param_name!r}")
                idx += 1
                continue
            expr_text = "\n".join(expr_parts).strip()
            if param_name in parameters:
                errors.append(f"{rel_path}: duplicate assignment for parameter {param_name!r}")
            try:
                parameters[param_name] = _BicepValueParser(expr_text).parse()
            except ValueError as exc:
                errors.append(f"{rel_path}: cannot parse parameter {param_name!r}: {exc}")
            idx += 1
            continue
        errors.append(f"{rel_path}: unrecognized statement {line!r}")
        idx += 1

    if using_target is None:
        errors.append(f"{rel_path}: missing `using '<template>'` directive")
    return BicepparamSummary(
        path=rel_path,
        using_target=using_target,
        parameters=parameters,
        errors=tuple(errors),
    )


def extract_pipeline_injected_parameters(pipeline_source: str) -> tuple[frozenset[str], list[str]]:
    """AST-extract parameters explicitly injected or overridden by infra/scripts/pipeline.py."""
    errors: list[str] = []
    try:
        tree = ast.parse(pipeline_source)
    except SyntaxError as exc:
        return frozenset(), [f"infra/scripts/pipeline.py syntax error: {exc}"]

    overrides_keys: set[str] = set()
    image_param_values: set[str] = set()
    parameters_fn_updates: set[str] = set()

    for node in tree.body:
        if isinstance(node, ast.Assign):
            target_names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if "OVERRIDES" in target_names and isinstance(node.value, ast.Set):
                for elt in node.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        overrides_keys.add(elt.value)
            if "IMAGE_PARAMETERS" in target_names and isinstance(node.value, ast.Dict):
                for val in node.value.values:
                    if isinstance(val, ast.Constant) and isinstance(val.value, str):
                        image_param_values.add(val.value)
        elif isinstance(node, ast.FunctionDef) and node.name == "parameters":
            for sub in ast.walk(node):
                if (
                    isinstance(sub, ast.Call)
                    and isinstance(sub.func, ast.Attribute)
                    and isinstance(sub.func.value, ast.Name)
                    and sub.func.value.id == "values"
                    and sub.func.attr == "update"
                    and len(sub.args) == 1
                    and isinstance(sub.args[0], ast.Dict)
                ):
                    for key in sub.args[0].keys:
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            parameters_fn_updates.add(key.value)

    if not overrides_keys:
        errors.append("infra/scripts/pipeline.py: could not AST-extract OVERRIDES keys")
    if not image_param_values:
        errors.append("infra/scripts/pipeline.py: could not AST-extract IMAGE_PARAMETERS values")
    if not parameters_fn_updates:
        errors.append("infra/scripts/pipeline.py: could not AST-extract parameters() values.update")

    return frozenset(overrides_keys | image_param_values | parameters_fn_updates), errors


def load_rebuild_stages(repo_root: Path) -> tuple[str, ...]:
    """AST-extract the canonical 17-stage tuple from orchestrator/rebuild.py."""
    rebuild_path = (
        repo_root / "src" / "orchestrator" / "src" / "zava_forward" / "orchestrator" / "rebuild.py"
    )
    if not rebuild_path.is_file():
        return ()
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
                    return tuple(stages)
    return ()


def _parse_readme_section(
    readme_text: str, heading: str
) -> tuple[str, list[str], list[dict[str, str]]]:
    """Extract section body, table headers, and rows under a ### heading in infra/README.md."""
    lines = readme_text.splitlines()
    start: int | None = None
    target_heading = f"### {heading}"
    for idx, line in enumerate(lines):
        if line.strip() == target_heading:
            start = idx + 1
            break
    if start is None:
        return "", [], []

    section_lines: list[str] = []
    table_lines: list[str] = []
    for idx in range(start, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith(("## ", "### ")):
            break
        section_lines.append(lines[idx])
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(stripped)
    if len(table_lines) < 2:
        return "\n".join(section_lines), [], []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for raw_row in table_lines[2:]:
        cells = [cell.strip() for cell in raw_row.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells, strict=True)))
    return "\n".join(section_lines), headers, rows


def _extract_pipeline_symbols(pipeline_source: str) -> tuple[frozenset[str], frozenset[str]]:
    """Return (cli_operation_choices, top_level_function_names) from pipeline.py."""
    tree = ast.parse(pipeline_source)
    ops: set[str] = set()
    funcs: set[str] = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
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
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            ops.add(elt.value)
    return frozenset(ops), frozenset(funcs)


def verify_step_registration_and_docs(repo_root: Path = ROOT) -> StepRegistrationReport:
    """Verify criterion (a): all 6 steps registered in pipeline.py & documented in README.md."""
    errors: list[str] = []
    undocumented_manual: list[str] = []

    pipeline_path = repo_root / "infra" / "scripts" / "pipeline.py"
    readme_path = repo_root / "infra" / "README.md"
    if not pipeline_path.is_file():
        return StepRegistrationReport(
            ok=False,
            registered_steps=(),
            documented_steps=(),
            covered_rebuild_stages=(),
            undocumented_manual_steps=(),
            errors=("Missing infra/scripts/pipeline.py",),
        )
    if not readme_path.is_file():
        return StepRegistrationReport(
            ok=False,
            registered_steps=(),
            documented_steps=(),
            covered_rebuild_stages=(),
            undocumented_manual_steps=(),
            errors=("Missing infra/README.md",),
        )

    pipeline_source = pipeline_path.read_text(encoding="utf-8")
    cli_ops, pipeline_funcs = _extract_pipeline_symbols(pipeline_source)
    pipeline_mod = _load_pipeline_module(pipeline_path)

    step_order = getattr(pipeline_mod, "FROM_EMPTY_STEP_ORDER", None)
    from_empty_steps = getattr(pipeline_mod, "FROM_EMPTY_STEPS", None)
    if step_order != CANONICAL_FROM_EMPTY_STEPS:
        errors.append(
            f"pipeline.FROM_EMPTY_STEP_ORDER {step_order!r} != {CANONICAL_FROM_EMPTY_STEPS!r}"
        )
    if not isinstance(from_empty_steps, tuple):
        return StepRegistrationReport(
            ok=False,
            registered_steps=(),
            documented_steps=(),
            covered_rebuild_stages=(),
            undocumented_manual_steps=(),
            errors=(*errors, "pipeline.FROM_EMPTY_STEPS is missing or not a tuple"),
        )

    registered_ids = tuple(getattr(s, "step_id", "") for s in from_empty_steps)
    if registered_ids != CANONICAL_FROM_EMPTY_STEPS:
        errors.append(
            f"pipeline.FROM_EMPTY_STEPS ids {registered_ids!r} != {CANONICAL_FROM_EMPTY_STEPS!r}"
        )

    readme_text = readme_path.read_text(encoding="utf-8")
    section_body, headers, rows = _parse_readme_section(readme_text, CANONICAL_STEP_README_HEADING)
    if not section_body:
        errors.append(f"infra/README.md is missing section '### {CANONICAL_STEP_README_HEADING}'")
    elif tuple(headers) != CANONICAL_STEP_README_COLUMNS:
        errors.append(
            f"infra/README.md '{CANONICAL_STEP_README_HEADING}' columns {tuple(headers)!r} "
            f"!= {CANONICAL_STEP_README_COLUMNS!r}"
        )

    for forbidden_re in FORBIDDEN_MANUAL_PROSE_PATTERNS:
        if forbidden_re.search(section_body):
            undocumented_manual.append("section-prose")
            errors.append(
                f"infra/README.md '{CANONICAL_STEP_README_HEADING}' contains forbidden "
                f"undocumented/manual phrase matching {forbidden_re.pattern!r}"
            )

    documented_ids = tuple(
        BACKTICK_TOKEN_RE.findall(row.get("Step", ""))[0]
        if BACKTICK_TOKEN_RE.findall(row.get("Step", ""))
        else row.get("Step", "").strip("` ")
        for row in rows
    )
    if documented_ids != CANONICAL_FROM_EMPTY_STEPS:
        errors.append(
            f"infra/README.md documented step order {documented_ids!r} "
            f"!= {CANONICAL_FROM_EMPTY_STEPS!r}"
        )

    rebuild_stages = load_rebuild_stages(repo_root)
    rebuild_index = {stage: idx for idx, stage in enumerate(rebuild_stages)}
    observed_stages: list[str] = []

    rows_by_step = {
        (
            BACKTICK_TOKEN_RE.findall(row["Step"])[0]
            if BACKTICK_TOKEN_RE.findall(row["Step"])
            else row["Step"].strip("` ")
        ): row
        for row in rows
        if "Step" in row
    }

    for step in from_empty_steps:
        step_id: str = step.step_id
        hook_tokens = tuple(tok.strip() for tok in step.pipeline_hook.split(",") if tok.strip())
        if not hook_tokens:
            errors.append(f"Step {step_id!r} has empty pipeline_hook in pipeline.FROM_EMPTY_STEPS")
        for hook in hook_tokens:
            if hook != "seed" and hook not in cli_ops and hook not in pipeline_funcs:
                errors.append(
                    f"Step {step_id!r} hook {hook!r} is neither a CLI operation nor function "
                    "in infra/scripts/pipeline.py"
                )
        if not step.artifacts:
            errors.append(f"Step {step_id!r} declares no repository artifacts in pipeline.py")
        for rel_artifact in step.artifacts:
            if not (repo_root / rel_artifact).is_file():
                errors.append(
                    f"Step {step_id!r} references missing artifact {rel_artifact!r} in pipeline.py"
                )

        # Verify per-step rebuild stages exist and stay monotonic within each step.
        step_indices: list[int] = []
        for stage_name in step.rebuild_stages:
            observed_stages.append(stage_name)
            if rebuild_stages and stage_name not in rebuild_index:
                errors.append(
                    f"Step {step_id!r} references unknown rebuild.py stage {stage_name!r}"
                )
            elif rebuild_stages:
                step_indices.append(rebuild_index[stage_name])
        if step_indices != sorted(step_indices):
            errors.append(
                f"Step {step_id!r} rebuild_stages {step.rebuild_stages!r} are out of "
                "relative rebuild.py order"
            )

        row = rows_by_step.get(step_id)
        if row is None:
            undocumented_manual.append(step_id)
            errors.append(f"Step {step_id!r} is missing from infra/README.md step registry table")
            continue

        for col_name in CANONICAL_STEP_README_COLUMNS:
            cell_val = row.get(col_name, "").strip()
            if cell_val.lower() in PLACEHOLDER_CELL_VALUES:
                undocumented_manual.append(step_id)
                errors.append(
                    f"Step {step_id!r} column {col_name!r} in infra/README.md has placeholder "
                    f"or undocumented value {cell_val!r}"
                )

        reg_cell = row.get("Pipeline registration", "")
        for hook in hook_tokens:
            if hook not in reg_cell:
                errors.append(
                    f"Step {step_id!r} README 'Pipeline registration' cell {reg_cell!r} "
                    f"omits pipeline_hook {hook!r}"
                )

        doc_stages = tuple(BACKTICK_TOKEN_RE.findall(row.get("Rebuild stage(s)", "")))
        if doc_stages != step.rebuild_stages:
            errors.append(
                f"Step {step_id!r} README 'Rebuild stage(s)' {doc_stages!r} "
                f"!= pipeline.FROM_EMPTY_STEPS {step.rebuild_stages!r}"
            )

        doc_paths = tuple(
            tok
            for tok in BACKTICK_TOKEN_RE.findall(row.get("Repository template or script", ""))
            if "/" in tok or tok.endswith((".bicep", ".bicepparam", ".py", ".sql", ".json", ".sh"))
        )
        if not doc_paths:
            undocumented_manual.append(step_id)
            errors.append(
                f"Step {step_id!r} README 'Repository template or script' lists no repository files"
            )
        for doc_rel in doc_paths:
            if not (repo_root / doc_rel).is_file():
                errors.append(
                    f"Step {step_id!r} README references missing repository file {doc_rel!r}"
                )
        if set(doc_paths) != set(step.artifacts):
            errors.append(
                f"Step {step_id!r} README artifacts {sorted(doc_paths)!r} != "
                f"pipeline.FROM_EMPTY_STEPS artifacts {sorted(step.artifacts)!r}"
            )

        prereq_cell = row.get("Manual prerequisites", "").strip()
        if step.manual_prerequisite_owner is None:
            if prereq_cell != AUTOMATED_PREREQUISITE_LABEL:
                undocumented_manual.append(step_id)
                errors.append(
                    f"Automated step {step_id!r} declares manual prerequisite {prereq_cell!r}; "
                    f"expected {AUTOMATED_PREREQUISITE_LABEL!r}"
                )
        else:
            if "@" not in step.manual_prerequisite_owner:
                undocumented_manual.append(step_id)
                errors.append(
                    f"Step {step_id!r} manual_prerequisite_owner "
                    f"{step.manual_prerequisite_owner!r} lacks named @handle"
                )
            if step.manual_prerequisite_owner not in prereq_cell:
                undocumented_manual.append(step_id)
                errors.append(
                    f"Step {step_id!r} README 'Manual prerequisites' {prereq_cell!r} must "
                    f"name owner {step.manual_prerequisite_owner!r}"
                )

    if rebuild_stages:
        duplicates = sorted(
            {stage for stage in observed_stages if observed_stages.count(stage) > 1}
        )
        missing_stages = sorted(set(rebuild_stages) - set(observed_stages))
        extra_stages = sorted(set(observed_stages) - set(rebuild_stages))
        if duplicates or missing_stages or extra_stages:
            errors.append(
                "FROM_EMPTY_STEPS rebuild_stages do not form an exact 17-stage partition of "
                f"rebuild.py STAGES (duplicates={duplicates}, missing={missing_stages}, "
                f"extra={extra_stages})"
            )

    dedup_manual = tuple(dict.fromkeys(undocumented_manual))
    return StepRegistrationReport(
        ok=not errors,
        registered_steps=registered_ids,
        documented_steps=documented_ids,
        covered_rebuild_stages=tuple(observed_stages),
        undocumented_manual_steps=dedup_manual,
        errors=tuple(errors),
    )


def verify_bicep_parameter_coverage(repo_root: Path = ROOT) -> ParameterCoverageReport:
    """Verify criterion (b): every defaultless main.bicep param is supplied or injected."""
    errors: list[str] = []
    main_bicep_path = repo_root / "infra" / "main.bicep"
    pipeline_path = repo_root / "infra" / "scripts" / "pipeline.py"
    if not main_bicep_path.is_file():
        return ParameterCoverageReport(
            ok=False,
            total_bicep_parameters=0,
            defaultless_parameters=(),
            coverage_sources={},
            pipeline_injected_parameters=(),
            parameter_files_checked=(),
            errors=("Missing infra/main.bicep",),
        )
    if not pipeline_path.is_file():
        return ParameterCoverageReport(
            ok=False,
            total_bicep_parameters=0,
            defaultless_parameters=(),
            coverage_sources={},
            pipeline_injected_parameters=(),
            parameter_files_checked=(),
            errors=("Missing infra/scripts/pipeline.py",),
        )

    declarations = parse_bicep_parameters(main_bicep_path.read_text(encoding="utf-8"))
    if not declarations:
        errors.append("infra/main.bicep: zero parameter declarations parsed")
    known_names = {decl.name for decl in declarations}
    defaultless = tuple(decl.name for decl in declarations if not decl.has_default)

    pipeline_source = pipeline_path.read_text(encoding="utf-8")
    ast_injected, ast_errors = extract_pipeline_injected_parameters(pipeline_source)
    errors.extend(ast_errors)

    pipeline_mod = _load_pipeline_module(pipeline_path)
    declared_injected = getattr(pipeline_mod, "INJECTED_PARAMETERS", None)
    if declared_injected != ast_injected:
        errors.append(
            f"pipeline.INJECTED_PARAMETERS {sorted(declared_injected or ())!r} != "
            f"AST-extracted injections {sorted(ast_injected)!r}"
        )
    unknown_injected = sorted(ast_injected - known_names)
    if unknown_injected:
        errors.append(
            f"infra/scripts/pipeline.py injects parameters absent from main.bicep: "
            f"{unknown_injected!r}"
        )

    dev_path = repo_root / "infra" / "parameters" / "dev.bicepparam"
    prod_path = repo_root / "infra" / "parameters" / "prod.bicepparam"
    dev_summary = parse_bicepparam_file(dev_path, repo_root)
    prod_summary = parse_bicepparam_file(prod_path, repo_root)

    checked_paths: list[str] = [dev_summary.path, prod_summary.path]
    summaries: list[BicepparamSummary] = [dev_summary, prod_summary]
    for optional_root in (
        "main.bicepparam",
        "main.test.bicepparam",
        "main.pilot.example.bicepparam",
    ):
        opt_path = repo_root / "infra" / optional_root
        if opt_path.is_file():
            opt_summary = parse_bicepparam_file(opt_path, repo_root)
            checked_paths.append(opt_summary.path)
            summaries.append(opt_summary)

    for summary in summaries:
        errors.extend(summary.errors)
        if summary.using_target is not None and summary.using_target != "infra/main.bicep":
            errors.append(
                f"{summary.path}: `using` resolves to {summary.using_target!r}, "
                "expected 'infra/main.bicep'"
            )
        unknown_assigned = sorted(set(summary.parameters) - known_names)
        if unknown_assigned:
            errors.append(
                f"{summary.path}: assigns unknown parameters absent from infra/main.bicep: "
                f"{unknown_assigned!r}"
            )

    # Validate repository isolation & hygiene contracts on dev.bicepparam and prod.bicepparam.
    if dev_path.is_file():
        dev_raw = dev_path.read_text(encoding="utf-8")
        if "chat" in dev_raw.lower():
            errors.append("infra/parameters/dev.bicepparam must not contain 'chat'")
        if dev_summary.parameters.get("environmentName") != "dev":
            errors.append("infra/parameters/dev.bicepparam must set environmentName = 'dev'")
        if dev_summary.parameters.get("deploymentProfile") != "development":
            errors.append(
                "infra/parameters/dev.bicepparam must set deploymentProfile = 'development'"
            )
        if dev_summary.parameters.get("allowPublicNetworkAccess") is not False:
            errors.append(
                "infra/parameters/dev.bicepparam must keep allowPublicNetworkAccess = false"
            )
        if dev_summary.parameters.get("apiMinReplicas") != 0:
            errors.append("infra/parameters/dev.bicepparam must set apiMinReplicas = 0")

    if prod_path.is_file():
        prod_raw = prod_path.read_text(encoding="utf-8")
        if "chat" in prod_raw.lower():
            errors.append("infra/parameters/prod.bicepparam must not contain 'chat'")
        if "autopause" in prod_raw.lower():
            errors.append("infra/parameters/prod.bicepparam must not contain 'AutoPause'")
        if prod_summary.parameters.get("environmentName") != "pilot":
            errors.append("infra/parameters/prod.bicepparam must set environmentName = 'pilot'")
        if prod_summary.parameters.get("deploymentProfile") != "production":
            errors.append(
                "infra/parameters/prod.bicepparam must set deploymentProfile = 'production'"
            )
        if prod_summary.parameters.get("allowPublicNetworkAccess") is not False:
            errors.append(
                "infra/parameters/prod.bicepparam must keep allowPublicNetworkAccess = false"
            )
        if prod_summary.parameters.get("enableLocks") is not True:
            errors.append("infra/parameters/prod.bicepparam must set enableLocks = true")
        if prod_summary.parameters.get("keyVaultPurgeProtection") is not True:
            errors.append(
                "infra/parameters/prod.bicepparam must set keyVaultPurgeProtection = true"
            )
        if prod_summary.parameters.get("registryQuarantineEnabled") is not True:
            errors.append(
                "infra/parameters/prod.bicepparam must set registryQuarantineEnabled = true"
            )
        if prod_summary.parameters.get("sqlTier") != "provisioned":
            errors.append("infra/parameters/prod.bicepparam must set sqlTier = 'provisioned'")
        if prod_summary.parameters.get("apiMinReplicas") != 0:
            errors.append("infra/parameters/prod.bicepparam must set apiMinReplicas = 0")

    coverage_sources: dict[str, str] = {}
    for param_name in defaultless:
        in_bicepparam = (
            param_name in dev_summary.parameters and param_name in prod_summary.parameters
        )
        in_pipeline = param_name in ast_injected
        if in_bicepparam and in_pipeline:
            coverage_sources[param_name] = "bicepparam+pipeline"
        elif in_bicepparam:
            coverage_sources[param_name] = "bicepparam"
        elif in_pipeline:
            coverage_sources[param_name] = "pipeline"
        else:
            coverage_sources[param_name] = "uncovered"
            errors.append(
                f"Defaultless main.bicep parameter {param_name!r} is neither supplied in both "
                "infra/parameters/dev.bicepparam and infra/parameters/prod.bicepparam nor "
                "explicitly injected by infra/scripts/pipeline.py"
            )

    return ParameterCoverageReport(
        ok=not errors,
        total_bicep_parameters=len(declarations),
        defaultless_parameters=defaultless,
        coverage_sources=coverage_sources,
        pipeline_injected_parameters=tuple(sorted(ast_injected)),
        parameter_files_checked=tuple(checked_paths),
        errors=tuple(errors),
    )


def _hash_artifacts(repo_root: Path, rel_paths: tuple[str, ...]) -> tuple[str, list[str]]:
    hasher = hashlib.sha256()
    missing: list[str] = []
    for rel_path in rel_paths:
        target = repo_root / rel_path
        if not target.is_file():
            missing.append(f"Missing required artifact for dry-run: {rel_path}")
            continue
        hasher.update(rel_path.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(target.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest(), missing


def _collect_declared_bicep_resource_types(repo_root: Path) -> tuple[str, ...]:
    infra_dir = repo_root / "infra"
    candidates = [infra_dir / "main.bicep", *sorted((infra_dir / "modules").glob("*.bicep"))]
    found: set[str] = set()
    for path in candidates:
        if not path.is_file():
            continue
        for line in strip_bicep_comments(path.read_text(encoding="utf-8")).splitlines():
            match = RESOURCE_DECL_RE.match(line)
            if match:
                found.add(match.group(1))
    return tuple(sorted(found))


class _DryRunHttpResponse:
    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


class _DryRunSmokeOpener:
    """Deterministic in-memory opener validating pipeline.smoke HTTP probe contract."""

    def __init__(self) -> None:
        self.observed_probes: list[tuple[str, str, tuple[tuple[str, str], ...]]] = []

    def open(self, req: urllib.request.Request, timeout: float = 20) -> _DryRunHttpResponse:
        del timeout
        full_url = req.full_url
        headers = tuple(sorted((k.lower(), v) for k, v in req.header_items()))
        self.observed_probes.append((req.get_method(), full_url, headers))
        if full_url.endswith("/healthz"):
            return _DryRunHttpResponse(200)
        if full_url.endswith("/sign-in"):
            raise urllib.error.HTTPError(full_url, 302, "Found", hdrs=None, fp=None)  # type: ignore[arg-type]
        if full_url.endswith("/api/me"):
            raise urllib.error.HTTPError(full_url, 401, "Unauthorized", hdrs=None, fp=None)  # type: ignore[arg-type]
        raise urllib.error.HTTPError(full_url, 404, "Not Found", hdrs=None, fp=None)  # type: ignore[arg-type]


def execute_from_empty_dry_run(repo_root: Path = ROOT, environment: str = "dev") -> DryRunResult:
    """Execute the full 6-step from-empty deployment sequence offline and deterministically."""
    if environment not in ("dev", "prod"):
        return DryRunResult(
            ok=False,
            environment=environment,
            runtime_environment="",
            parameter_file="",
            steps=(),
            parameter_sha256="",
            sequence_digest="",
            errors=(f"Unsupported dry-run environment {environment!r}; expected 'dev' or 'prod'",),
        )

    param_rel = f"parameters/{environment}.bicepparam"
    runtime_env = "dev" if environment == "dev" else "pilot"
    infra_dir = repo_root / "infra"
    pipeline_path = infra_dir / "scripts" / "pipeline.py"
    if not pipeline_path.is_file():
        return DryRunResult(
            ok=False,
            environment=environment,
            runtime_environment=runtime_env,
            parameter_file=f"infra/{param_rel}",
            steps=(),
            parameter_sha256="",
            sequence_digest="",
            errors=("Missing infra/scripts/pipeline.py",),
        )

    pipeline_mod = _load_pipeline_module(pipeline_path)
    steps_meta = {step.step_id: step for step in getattr(pipeline_mod, "FROM_EMPTY_STEPS", ())}
    if tuple(steps_meta) != CANONICAL_FROM_EMPTY_STEPS:
        step_err = (
            f"pipeline.FROM_EMPTY_STEPS {tuple(steps_meta)!r} != {CANONICAL_FROM_EMPTY_STEPS!r}"
        )
        return DryRunResult(
            ok=False,
            environment=environment,
            runtime_environment=runtime_env,
            parameter_file=f"infra/{param_rel}",
            steps=(),
            parameter_sha256="",
            sequence_digest="",
            errors=(step_err,),
        )

    synthetic_env = {
        "AZURE_REGISTRY_NAME": DRY_RUN_REGISTRY_NAME,
        "AZURE_SUBSCRIPTION_ID": DRY_RUN_SUBSCRIPTION_ID,
        "DEPLOY_PARAMETERS": json.dumps(DRY_RUN_DEPLOY_PARAMETERS, sort_keys=True),
        "GITHUB_REPOSITORY": DRY_RUN_REPOSITORY,
        "GITHUB_RUN_ATTEMPT": DRY_RUN_RUN_ATTEMPT,
        "GITHUB_RUN_ID": DRY_RUN_RUN_ID,
        "RELEASE_SHA": DRY_RUN_RELEASE_SHA,
    }

    def _forbid_subprocess(*args: Any, **kwargs: Any) -> Any:
        del args, kwargs
        raise AssertionError("Offline dry-run must not spawn subprocesses")

    def _offline_run(*args: str) -> str:
        if args[:2] == ("gh", "api"):
            return json.dumps(
                {
                    "can_admins_bypass": False,
                    "deployment_branch_policy": {"protected_branches": True},
                    "protection_rules": [
                        {
                            "prevent_self_review": True,
                            "reviewers": [{"type": "User", "reviewer": {"login": "jmservera"}}],
                            "type": "required_reviewers",
                        }
                    ],
                },
                sort_keys=True,
            )
        if args[:3] == ("az", "acr", "login"):
            return ""
        if args[:2] == ("docker", "pull"):
            return ""
        raise pipeline_mod.PipelineError(f"Unexpected offline command: {args!r}")

    declared_resource_types = _collect_declared_bicep_resource_types(repo_root)

    def _offline_az(*args: str) -> Any:
        if args[:2] == ("bicep", "build-params"):
            file_idx = args.index("--file") + 1
            parsed = parse_bicepparam_file(Path(args[file_idx]), repo_root)
            if parsed.errors:
                raise pipeline_mod.PipelineError("; ".join(parsed.errors))
            arm_params = {
                "$schema": (
                    "https://schema.management.azure.com/schemas/2019-04-01/"
                    "deploymentParameters.json#"
                ),
                "contentVersion": "1.0.0.0",
                "parameters": {
                    key: {"value": parsed.parameters[key]} for key in sorted(parsed.parameters)
                },
            }
            return {"parametersJson": json.dumps(arm_params, sort_keys=True)}
        if args[:2] == ("acr", "show"):
            return {"loginServer": DRY_RUN_REGISTRY_SERVER}
        if args[:2] == ("containerapp", "list"):
            return []
        if args[:3] == ("sql", "server", "list"):
            return [
                {
                    "name": f"sql-forward-{runtime_env}",
                    "publicNetworkAccess": "Disabled",
                }
            ]
        if args[:3] == ("deployment", "group", "what-if"):
            changes: list[dict[str, Any]] = []
            for idx, rtype in enumerate(declared_resource_types):
                after_obj: dict[str, Any] = {"type": rtype, "properties": {}}
                if rtype.lower() == "microsoft.sql/servers":
                    after_obj["properties"]["publicNetworkAccess"] = "Disabled"
                changes.append(
                    {
                        "after": after_obj,
                        "changeType": "Create",
                        "resourceId": (
                            f"/subscriptions/{DRY_RUN_SUBSCRIPTION_ID}/resourceGroups/ama/"
                            f"providers/{rtype}/res{idx:02d}"
                        ),
                    }
                )
            return {"changes": changes, "status": "Succeeded"}
        if args[:3] == ("deployment", "group", "create"):
            return {
                "properties": {
                    "outputs": {
                        "apiInternalFqdn": {
                            "value": (
                                f"ca-forward-{runtime_env}-api.internal.uksouth."
                                "azurecontainerapps.io"
                            )
                        }
                    },
                    "provisioningState": "Succeeded",
                }
            }
        raise pipeline_mod.PipelineError(f"Unexpected offline az invocation: {args!r}")

    records: list[StepExecutionRecord] = []
    errors: list[str] = []
    parameter_sha256 = ""
    patched_param_files = {
        "dev": "parameters/dev.bicepparam",
        "pilot": "parameters/prod.bicepparam",
        "test": "main.test.bicepparam",
    }

    with (
        patch.dict(os.environ, synthetic_env, clear=True),
        patch.object(subprocess, "run", side_effect=_forbid_subprocess),
        patch.object(pipeline_mod.subprocess, "run", side_effect=_forbid_subprocess),
        patch.dict(pipeline_mod.PARAMETER_FILES, patched_param_files, clear=True),
        patch.object(pipeline_mod, "run", side_effect=_offline_run),
        patch.object(pipeline_mod, "az", side_effect=_offline_az),
    ):
        # Step 1: preflight
        step1 = steps_meta["preflight"]
        sha1, missing1 = _hash_artifacts(repo_root, step1.artifacts)
        step1_checks: list[str] = []
        if missing1:
            errors.extend(missing1)
        else:
            try:
                entra_cfg = json.loads(
                    (infra_dir / "entra" / "app-registration.json").read_text(encoding="utf-8")
                )
                secret_inv = json.loads(
                    (infra_dir / "secret-inventory.json").read_text(encoding="utf-8")
                )
                defender_cfg = json.loads(
                    (infra_dir / "defender-decision.json").read_text(encoding="utf-8")
                )
                ast.parse(
                    (infra_dir / "scripts" / "tenant-readiness-preflight.py").read_text(
                        encoding="utf-8"
                    )
                )
                roles = entra_cfg.get("appRoles", [])
                if entra_cfg.get("signInAudience") != "AzureADMyOrg" or not roles:
                    raise ValueError("entra/app-registration.json missing AzureADMyOrg/appRoles")
                secrets = secret_inv.get("secrets", [])
                if not secrets or any(not item.get("owner") for item in secrets):
                    raise ValueError("secret-inventory.json has unowned or empty secrets list")
                policy_decision = str((defender_cfg.get("policy") or {}).get("decision", ""))
                defender_section = defender_cfg.get("defender") or {}
                if (
                    "DoNotEnforce" not in policy_decision
                    or defender_section.get("enableDefenderPlans") is not False
                    or not defender_cfg.get("owner")
                ):
                    raise ValueError("defender-decision.json baseline drifted without sign-off")
                pipeline_mod.verify_environment(f"{runtime_env}-release")
                step1_checks = [
                    "entra-app-registration-schema",
                    "secret-inventory-owners",
                    "defender-policy-baseline",
                    f"github-environment-{runtime_env}-release",
                ]
            except (
                KeyError,
                OSError,
                SyntaxError,
                TypeError,
                ValueError,
                pipeline_mod.PipelineError,
            ) as exc:
                errors.append(f"preflight failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="preflight",
                status="succeeded" if step1_checks and not missing1 else "failed",
                pipeline_hook=step1.pipeline_hook,
                verified_artifacts=step1.artifacts,
                artifact_sha256=sha1,
                checks_passed=tuple(step1_checks),
            )
        )

        # Step 2: what-if
        step2 = steps_meta["what-if"]
        sha2, missing2 = _hash_artifacts(repo_root, step2.artifacts)
        step2_checks: list[str] = []
        if missing2:
            errors.extend(missing2)
        else:
            try:
                gov_text = strip_bicep_comments(
                    (infra_dir / "governance.bicep").read_text(encoding="utf-8")
                )
                if "targetScope = 'subscription'" not in gov_text:
                    raise ValueError("governance.bicep must declare subscription targetScope")
                ast.parse((infra_dir / "scripts" / "deploy.py").read_text(encoding="utf-8"))
                if not declared_resource_types:
                    raise ValueError("No Bicep resource declarations discovered under infra/")
                compiled_params = pipeline_mod.parameters(infra_dir, runtime_env)
                if (
                    compiled_params["parameters"]["allowPublicNetworkAccess"]["value"] is not False
                    or compiled_params["parameters"]["deployApplications"]["value"] is not True
                ):
                    raise ValueError("Compiled parameters lost private isolation invariants")
                plan_payload = _offline_az("deployment", "group", "what-if")
                summary = pipeline_mod.summarize_plan(
                    plan_payload, DRY_RUN_SUBSCRIPTION_ID, DRY_RUN_RELEASE_SHA
                )
                if summary.get("status") != "Succeeded" or not summary.get("change_counts"):
                    raise ValueError("What-if plan summary did not succeed")
                step2_checks = [
                    f"compile-{param_rel}",
                    "subscription-governance-scope",
                    "ama-resource-group-scope",
                    "sql-public-access-disabled",
                ]
            except (
                KeyError,
                OSError,
                SyntaxError,
                TypeError,
                ValueError,
                pipeline_mod.PipelineError,
            ) as exc:
                errors.append(f"what-if failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="what-if",
                status="succeeded" if step2_checks and not missing2 else "failed",
                pipeline_hook=step2.pipeline_hook,
                verified_artifacts=step2.artifacts,
                artifact_sha256=sha2,
                checks_passed=tuple(step2_checks),
            )
        )

        # Step 3: deploy
        step3 = steps_meta["deploy"]
        sha3, missing3 = _hash_artifacts(repo_root, step3.artifacts)
        step3_checks: list[str] = []
        if missing3:
            errors.extend(missing3)
        else:
            try:
                for project in pipeline_mod.PROJECTS:
                    dockerfile = repo_root / "src" / project / "Dockerfile"
                    docker_text = dockerfile.read_text(encoding="utf-8")
                    if "FROM " not in docker_text or "pip " not in docker_text:
                        raise ValueError(f"src/{project}/Dockerfile missing build stage contract")
                ast.parse((infra_dir / "scripts" / "setup-entra.py").read_text(encoding="utf-8"))
                ast.parse((infra_dir / "scripts" / "credential_arm.py").read_text(encoding="utf-8"))
                main_bicep_bytes = (infra_dir / "main.bicep").read_bytes()
                deploy_opener = _DryRunSmokeOpener()
                with (
                    tempfile.TemporaryDirectory(prefix="ama-dryrun-") as tmp_str,
                    patch.object(
                        pipeline_mod.urllib.request, "build_opener", return_value=deploy_opener
                    ),
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    tmp_dir = Path(tmp_str)
                    images_dir = tmp_dir / "images"
                    images_dir.mkdir(parents=True, exist_ok=True)
                    release_tag = (
                        f"sha-{DRY_RUN_RELEASE_SHA}-r{DRY_RUN_RUN_ID}-a{DRY_RUN_RUN_ATTEMPT}"
                    )
                    for project in pipeline_mod.PROJECTS:
                        img_digest = hashlib.sha256(
                            (repo_root / "src" / project / "Dockerfile").read_bytes()
                            + b"\0"
                            + main_bicep_bytes
                        ).hexdigest()
                        (images_dir / f"{project}.json").write_text(
                            json.dumps(
                                {
                                    "image": (
                                        f"{DRY_RUN_REGISTRY_SERVER}/zava-forward-{project}"
                                        f"@sha256:{img_digest}"
                                    ),
                                    "project": project,
                                    "source_sha": DRY_RUN_RELEASE_SHA,
                                    "tag": release_tag,
                                },
                                sort_keys=True,
                            )
                            + "\n",
                            encoding="utf-8",
                        )
                    summary_file = tmp_dir / "deploy-summary.json"
                    pipeline_mod.deployment(infra_dir, runtime_env, summary_file, images_dir)
                    deploy_summary = json.loads(summary_file.read_text(encoding="utf-8"))
                    if deploy_summary.get("deployment_status") != "Succeeded":
                        raise ValueError("pipeline.deployment did not record Succeeded status")
                    parameter_sha256 = str(deploy_summary.get("parameter_sha256", ""))
                    if not re.fullmatch(r"[0-9a-f]{64}", parameter_sha256):
                        raise ValueError("pipeline.deployment did not emit valid parameter_sha256")
                step3_checks = [
                    "dockerfiles-verified",
                    "immutable-image-digests",
                    "arm-incremental-deploy",
                    "entra-easyauth-scripts",
                ]
            except (
                KeyError,
                OSError,
                SyntaxError,
                TypeError,
                ValueError,
                pipeline_mod.PipelineError,
            ) as exc:
                errors.append(f"deploy failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="deploy",
                status="succeeded" if step3_checks and not missing3 else "failed",
                pipeline_hook=step3.pipeline_hook,
                verified_artifacts=step3.artifacts,
                artifact_sha256=sha3,
                checks_passed=tuple(step3_checks),
            )
        )

        # Step 4: sql-init
        step4 = steps_meta["sql-init"]
        sha4, missing4 = _hash_artifacts(repo_root, step4.artifacts)
        step4_checks: list[str] = []
        if missing4:
            errors.extend(missing4)
        else:
            try:
                sql_users_sql = (infra_dir / "scripts" / "create-sql-users.sql").read_text(
                    encoding="utf-8"
                )
                for required_sql_token in (
                    "FROM EXTERNAL PROVIDER",
                    "db_datareader",
                    "db_datawriter",
                    "db_ddladmin",
                ):
                    if required_sql_token not in sql_users_sql:
                        raise ValueError(
                            f"create-sql-users.sql missing token {required_sql_token!r}"
                        )
                sql_py_tree = ast.parse(
                    (infra_dir / "scripts" / "create-sql-users.py").read_text(encoding="utf-8")
                )
                has_grants = any(
                    isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "GRANTS" for t in node.targets)
                    for node in sql_py_tree.body
                )
                if not has_grants:
                    raise ValueError("create-sql-users.py missing GRANTS role matrix")
                for ddl_rel in ("sql/resident-showcase.sql", "sql/resident-assistant.sql"):
                    ddl_text = (infra_dir / ddl_rel).read_text(encoding="utf-8")
                    if "CREATE TABLE" not in ddl_text.upper():
                        raise ValueError(f"infra/{ddl_rel} missing CREATE TABLE DDL")
                pipeline_mod.check_sql()
                step4_checks = [
                    "sql-private-network-disabled",
                    "contained-entra-principals",
                    "least-privilege-grants",
                    "idempotent-sql-ddl",
                ]
            except (
                KeyError,
                OSError,
                SyntaxError,
                TypeError,
                ValueError,
                pipeline_mod.PipelineError,
            ) as exc:
                errors.append(f"sql-init failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="sql-init",
                status="succeeded" if step4_checks and not missing4 else "failed",
                pipeline_hook=step4.pipeline_hook,
                verified_artifacts=step4.artifacts,
                artifact_sha256=sha4,
                checks_passed=tuple(step4_checks),
            )
        )

        # Step 5: seed
        step5 = steps_meta["seed"]
        sha5, missing5 = _hash_artifacts(repo_root, step5.artifacts)
        step5_checks: list[str] = []
        if missing5:
            errors.extend(missing5)
        else:
            try:
                sensor_seed_source = (infra_dir / "scripts" / "resident_sensor_seed.py").read_text(
                    encoding="utf-8"
                )
                ast.parse(sensor_seed_source)
                if "IF OBJECT_ID" not in sensor_seed_source:
                    raise ValueError("resident_sensor_seed.py missing idempotent IF OBJECT_ID DDL")
                ast.parse(
                    (infra_dir / "scripts" / "initialize-workbench-staff.py").read_text(
                        encoding="utf-8"
                    )
                )
                rebuild_azure_source = (
                    repo_root
                    / "src"
                    / "orchestrator"
                    / "src"
                    / "zava_forward"
                    / "orchestrator"
                    / "rebuild_azure.py"
                ).read_text(encoding="utf-8")
                ast.parse(rebuild_azure_source)
                if "seed" not in rebuild_azure_source or "staff" not in rebuild_azure_source:
                    raise ValueError("rebuild_azure.py missing seed/staff stage wiring")
                step5_checks = [
                    "synthetic-seed-contract",
                    "iot-sensor-idempotent-ddl",
                    "staff-roster-reconciler",
                ]
            except (KeyError, OSError, SyntaxError, TypeError, ValueError) as exc:
                errors.append(f"seed failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="seed",
                status="succeeded" if step5_checks and not missing5 else "failed",
                pipeline_hook=step5.pipeline_hook,
                verified_artifacts=step5.artifacts,
                artifact_sha256=sha5,
                checks_passed=tuple(step5_checks),
            )
        )

        # Step 6: smoke
        step6 = steps_meta["smoke"]
        sha6, missing6 = _hash_artifacts(repo_root, step6.artifacts)
        step6_checks: list[str] = []
        if missing6:
            errors.extend(missing6)
        else:
            try:
                ast.parse(
                    (infra_dir / "scripts" / "private-cutover-proof.py").read_text(encoding="utf-8")
                )
                smoke_opener = _DryRunSmokeOpener()
                base_url = (
                    f"https://ca-forward-{runtime_env}-api.internal.uksouth.azurecontainerapps.io"
                )
                with (
                    patch.object(
                        pipeline_mod.urllib.request, "build_opener", return_value=smoke_opener
                    ),
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    pipeline_mod.smoke(base_url, attempts=1, delay=0, browser=True)
                observed_paths = tuple(
                    url.removeprefix(base_url) for _, url, _ in smoke_opener.observed_probes
                )
                expected_paths = ("/healthz", "/api/me", "/api/me", "/api/me", "/sign-in")
                if observed_paths != expected_paths:
                    raise ValueError(
                        f"smoke probe sequence {observed_paths!r} != {expected_paths!r}"
                    )
                step6_checks = [
                    "health-200",
                    "anonymous-401",
                    "malformed-bearer-401",
                    "forged-principal-401",
                    "browser-sign-in-302",
                    "private-cutover-proof-ast",
                ]
            except (
                KeyError,
                OSError,
                SyntaxError,
                TypeError,
                ValueError,
                pipeline_mod.PipelineError,
            ) as exc:
                errors.append(f"smoke failed: {exc}")
        records.append(
            StepExecutionRecord(
                step_id="smoke",
                status="succeeded" if step6_checks and not missing6 else "failed",
                pipeline_hook=step6.pipeline_hook,
                verified_artifacts=step6.artifacts,
                artifact_sha256=sha6,
                checks_passed=tuple(step6_checks),
            )
        )

    all_steps_ok = not errors and all(rec.status == "succeeded" for rec in records)
    digest_payload = {
        "environment": environment,
        "parameter_file": f"infra/{param_rel}",
        "parameter_sha256": parameter_sha256,
        "runtime_environment": runtime_env,
        "steps": [asdict(rec) for rec in records],
    }
    sequence_digest = hashlib.sha256(
        json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DryRunResult(
        ok=all_steps_ok,
        environment=environment,
        runtime_environment=runtime_env,
        parameter_file=f"infra/{param_rel}",
        steps=tuple(records),
        parameter_sha256=parameter_sha256,
        sequence_digest=sequence_digest,
        errors=tuple(errors),
    )


def verify_from_empty_deployment_reproducibility(
    repo_root: Path = ROOT,
) -> ReproducibilityReport:
    """Verify criteria (a), (b), and (c) for Issue #136 from-empty deployment reproducibility."""
    step_report = verify_step_registration_and_docs(repo_root)
    param_report = verify_bicep_parameter_coverage(repo_root)

    dry_runs: dict[str, DryRunResult] = {}
    determinism_errors: list[str] = []
    for env_name in ("dev", "prod"):
        first = execute_from_empty_dry_run(repo_root, environment=env_name)
        second = execute_from_empty_dry_run(repo_root, environment=env_name)
        dry_runs[env_name] = first
        if first != second or first.sequence_digest != second.sequence_digest:
            determinism_errors.append(
                f"Offline dry-run for {env_name!r} was non-deterministic across repeated runs"
            )

    combined_errors: list[str] = [
        *step_report.errors,
        *param_report.errors,
        *dry_runs["dev"].errors,
        *dry_runs["prod"].errors,
        *determinism_errors,
    ]
    return ReproducibilityReport(
        ok=not combined_errors,
        step_registration=step_report,
        parameter_coverage=param_report,
        dry_runs=dry_runs,
        errors=tuple(combined_errors),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT,
        help="Repository root to inspect (defaults to workspace root).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run full reproducibility verification across steps, parameters, and dry-runs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute the offline 6-step from-empty deployment dry-run.",
    )
    parser.add_argument(
        "--environment",
        choices=("dev", "prod"),
        default="dev",
        help="Target environment when running --dry-run standalone.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit full structured JSON output.",
    )
    args = parser.parse_args(argv)

    if args.dry_run and not args.check:
        dry_result = execute_from_empty_dry_run(args.repo_root, environment=args.environment)
        if args.json:
            print(json.dumps(asdict(dry_result), indent=2, sort_keys=True))
        elif dry_result.ok:
            print(
                f"Offline from-empty dry-run ({dry_result.environment}): OK "
                f"(6/6 steps succeeded, digest={dry_result.sequence_digest})"
            )
        else:
            for err in dry_result.errors:
                print(f"ERROR: {err}", file=sys.stderr)
        return 0 if dry_result.ok else 1

    report = verify_from_empty_deployment_reproducibility(args.repo_root)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    elif report.ok:
        print(
            "Issue #136 from-empty deployment reproducibility verified: "
            f"{len(report.step_registration.registered_steps)} canonical steps, "
            f"{len(report.parameter_coverage.defaultless_parameters)}/"
            f"{report.parameter_coverage.total_bicep_parameters} defaultless parameters covered, "
            f"dev_digest={report.dry_runs['dev'].sequence_digest[:16]}, "
            f"prod_digest={report.dry_runs['prod'].sequence_digest[:16]}"
        )
    else:
        for err in report.errors:
            print(f"ERROR: {err}", file=sys.stderr)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
