#!/usr/bin/env python3
"""Read-only timing analysis of verified full-gate receipts (issue #1830).

Reports observed wall time, waits and an observational critical chain, and refuses
unlike-for-like before/after comparisons. It never runs the gate, never verifies a
receipt (rpi-checks.py --verify-receipt does that) and writes nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

NOTE = (
    "Observational and descriptive, not causal and not a guarantee. The sha256 binding checks "
    "file integrity only; it is not a gate verification (use rpi-checks.py --verify-receipt)."
)
EXIT_INPUT, EXIT_NONCOMPARABLE = 2, 3


class TimingError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def load_receipt(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise TimingError(EXIT_INPUT, f"Not a regular receipt file: {path}")
    digest = path.parent / "receipt.sha256"
    if (
        not digest.is_file()
        or digest.read_text().strip() != hashlib.sha256(path.read_bytes()).hexdigest()
    ):
        raise TimingError(EXIT_INPUT, f"receipt.sha256 is missing or does not match: {path}")
    try:
        receipt = json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise TimingError(EXIT_INPUT, f"Receipt is not valid JSON: {path}: {error}") from error
    if (
        not isinstance(receipt, dict)
        or receipt.get("schema") != 4
        or receipt.get("status") != "passed"
        or receipt.get("scope") != "full"
    ):
        raise TimingError(
            EXIT_INPUT, f"Only passed schema 4 full-scope receipts are analysed: {path}"
        )
    jobs = receipt.get("jobs")
    if not isinstance(jobs, int) or isinstance(jobs, bool) or jobs < 1:
        raise TimingError(EXIT_INPUT, f"Receipt jobs is missing or invalid: {path}")
    if not isinstance(receipt.get("image_cache"), str):
        raise TimingError(EXIT_INPUT, f"Receipt image_cache is missing or invalid: {path}")
    aware_timestamp(receipt.get("sealed"), "sealed")
    return receipt  # type: ignore[no-any-return]


def is_setup(argv: list[str]) -> bool:
    head = argv[:6]
    return (
        "venv" in head
        or "pip" in head
        or (head[:1] == ["docker"] and head[1:2] in (["build"], ["pull"]))
        or ("playwright" in head and "install" in head)
    )


def aware_timestamp(value: Any, label: str) -> float:
    try:
        moment = datetime.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise TimingError(EXIT_INPUT, f"Unparseable command {label} time: {value!r}") from error
    if moment.tzinfo is None:
        raise TimingError(EXIT_INPUT, f"Command {label} time has no timezone: {value!r}")
    return moment.timestamp()


def commands_of(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    items = receipt.get("commands")
    if not isinstance(items, list) or not items:
        raise TimingError(EXIT_INPUT, "Receipt has no commands")
    result = []
    for item in items:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("group"), str)
            or not isinstance(item.get("argv"), list)
        ):
            raise TimingError(EXIT_INPUT, "Receipt command lacks a group or argv list")
        start = aware_timestamp(item.get("started"), "started")
        end = aware_timestamp(item.get("finished"), "finished")
        if end < start:
            raise TimingError(EXIT_INPUT, f"Command finished before it started: {item['group']}")
        result.append({"group": item["group"], "argv": item["argv"], "start": start, "end": end})
    return result


def histogram(commands: list[dict[str, Any]]) -> dict[int, float]:
    events = sorted([(c["start"], 1) for c in commands] + [(c["end"], -1) for c in commands])
    result: dict[int, float] = {}
    active, last = 0, events[0][0]
    for moment, delta in events:
        result[active] = result.get(active, 0.0) + (moment - last)
        active += delta
        last = moment
    return {key: round(value, 1) for key, value in sorted(result.items())}


def critical_chain(
    commands: list[dict[str, Any]], origin: float, threshold: float
) -> list[dict[str, Any]]:
    """Walk back from the last finisher through the latest command that ended before each start."""
    current = max(commands, key=lambda c: c["end"])
    steps = []
    while True:
        steps.append(current)
        # Strict (end, start) ordering guarantees the walk ends on coincident zero-length commands.
        earlier = [
            c
            for c in commands
            if c["end"] <= current["start"]
            and (c["end"], c["start"]) < (current["end"], current["start"])
        ]
        if not earlier:
            break
        current = max(earlier, key=lambda c: c["end"])
    steps.reverse()
    segments: list[dict[str, Any]] = []
    cursor = origin
    for step in steps:
        gap = step["start"] - cursor
        if gap > threshold:
            segments.append({"kind": "wait", "group": step["group"], "seconds": round(gap, 1)})
            cursor = step["start"]
        if segments and segments[-1]["kind"] == "run" and segments[-1]["group"] == step["group"]:
            segments[-1]["seconds"] = round(segments[-1]["seconds"] + step["end"] - cursor, 1)
        else:
            segments.append(
                {
                    "kind": "run",
                    "group": step["group"],
                    "seconds": round(step["end"] - cursor, 1),
                }
            )
        cursor = step["end"]
    return segments


def repeated_commands(commands: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """List identical commands run more than once; candidates for review, not proof of redundancy."""
    seen: dict[str, list[dict[str, Any]]] = {}
    for item in commands:
        seen.setdefault(json.dumps(normalize_argv(item["argv"])), []).append(item)
    rows = [
        {
            "argv": items[0]["argv"][:6],
            "runs": len(items),
            "seconds": round(sum(i["end"] - i["start"] for i in items), 1),
            "groups": sorted({i["group"] for i in items}),
            "setup": is_setup(items[0]["argv"]),
        }
        for items in seen.values()
        if len(items) > 1
    ]
    return sorted(rows, key=lambda row: -row["seconds"])[:10]


def analyse(receipt: dict[str, Any], log: Path | None, gap: float) -> dict[str, Any]:
    commands = commands_of(receipt)
    retries = receipt.get("retries") or []
    origin = min(c["start"] for c in commands)
    finish = max(c["end"] for c in commands)
    groups: dict[str, dict[str, Any]] = {}
    for group in sorted({c["group"] for c in commands}):
        items = sorted((c for c in commands if c["group"] == group), key=lambda c: c["start"])
        idle, reach = [], items[0]["end"]
        for item in items[1:]:
            if item["start"] - reach > gap:
                idle.append(round(item["start"] - reach, 1))
            reach = max(reach, item["end"])
        groups[group] = {
            "start": round(items[0]["start"] - origin, 1),
            "end": round(max(i["end"] for i in items) - origin, 1),
            "wall": round(max(i["end"] for i in items) - items[0]["start"], 1),
            "command_seconds": round(sum(i["end"] - i["start"] for i in items), 1),
            "idle_gaps": idle,
        }
    total = sum(c["end"] - c["start"] for c in commands)
    setup = sum(c["end"] - c["start"] for c in commands if is_setup(c["argv"]))
    chain = critical_chain(commands, origin, gap)
    result: dict[str, Any] = {
        "repeated_commands": repeated_commands(commands),
        "note": NOTE,
        "jobs": receipt["jobs"],
        "image_cache": receipt["image_cache"],
        "commands": len(commands),
        "retries": len(retries),
        "retried_groups": sorted({str(row.get("group")) for row in retries}),
        "span_seconds": round(finish - origin, 1),
        "summed_command_seconds": round(total, 1),
        "setup_command_seconds": round(setup, 1),
        "groups": groups,
        "concurrency_seconds": histogram(commands),
        "longest_commands": [
            {
                "group": c["group"],
                "seconds": round(c["end"] - c["start"], 1),
                "argv": c["argv"][:6],
            }
            for c in sorted(commands, key=lambda c: c["start"] - c["end"])[:10]
        ],
        "critical_chain": chain,
        "chain_seconds": round(sum(item["seconds"] for item in chain), 1),
    }
    if log is not None:
        try:
            lines = log.read_text().splitlines()
        except (OSError, UnicodeDecodeError) as error:
            raise TimingError(EXIT_INPUT, f"Cannot read gate log {log}: {error}") from error
        if not lines:
            raise TimingError(EXIT_INPUT, f"Gate log is empty: {log}")
        first = lines[0]
        match = re.match(r"Lock queued (\S+); acquired (\S+);", first)
        if match:
            try:
                queued, acquired = (datetime.fromisoformat(v).timestamp() for v in match.groups())
            except ValueError as error:
                raise TimingError(EXIT_INPUT, f"Unparseable lock line in {log}: {error}") from error
            if acquired < queued:
                raise TimingError(EXIT_INPUT, f"Lock acquired before it was queued in {log}")
            sealed = datetime.fromisoformat(receipt["sealed"]).timestamp()
            result["queue_wait_seconds"] = round(acquired - queued, 3)
            result["lock_to_seal_seconds"] = round(sealed - acquired, 1)
        else:
            result["queue_wait_seconds"] = None
            result["queue_wait_unavailable"] = "first log line is not a 'Lock queued' line"
    return result


def host_manifest() -> dict[str, Any]:
    cpu = None
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
        memory = int(re.search(r"MemTotal:\s+(\d+)", Path("/proc/meminfo").read_text()).group(1))  # type: ignore[union-attr]
    except (OSError, AttributeError):
        memory = None
    try:
        docker = (
            subprocess.run(
                ["docker", "version", "--format", "{{.Server.Version}}"],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                check=False,
            ).stdout.strip()
            or None
        )
    except OSError:
        docker = None
    return {
        "cpu_model": cpu,
        "vcpus": os.cpu_count(),
        "memory_kib": memory,
        "docker_server": docker,
        "load_average": list(os.getloadavg()),
    }


HEX_ID = re.compile(r"[0-9a-f]{64}")
OWNER_LABEL = re.compile(r"((?:--label=)?ama\.rpi\.owner=).+")
CONTAINER_VERBS = ("inspect", "rm", "logs", "stop", "kill")
PER_RUN_ENV = {"ZF_SQL_PORT": "<port>"}
CONTRACT_FLAGS = ("cwd", "timeout_seconds", "suite", "integration", "probe", "attempts")
TEXT_KEYS = ("cpu_model", "docker_server")
NUMBER_KEYS = ("vcpus", "memory_kib")
MANIFEST_KEYS = ("cpu_model", "vcpus", "memory_kib", "docker_server")
IMAGE_ID = re.compile(r"sha256:[0-9a-f]{64}")


def image_reasons(receipts: list[dict[str, Any]]) -> list[str]:
    """Refuse missing or unlike image identity; built-image ids are recorded, not compared."""
    reasons: list[str] = []
    ids: list[dict[str, Any]] = []
    for receipt in receipts:
        images = receipt.get("images")
        groups = {item["group"] for item in receipt["commands"]}
        required = {g for g in groups if g == "mssql" or g == "logo-0600" or g.startswith("image-")}
        if not isinstance(images, dict) or not required <= set(images):
            reasons.append("receipt images lack an identity for an executed image group")
            continue
        found = {
            name: image
            if name == "mssql"
            else (image.get("id") if isinstance(image, dict) else None)
            for name, image in images.items()
        }
        if not all(isinstance(v, str) and IMAGE_ID.fullmatch(v) for v in found.values()):
            reasons.append("receipt image identity is malformed")
        ids.append(found)
    if any(set(item) != set(ids[0]) for item in ids):
        reasons.append("receipt image sets differ")
    if any(item.get("mssql") != ids[0].get("mssql") for item in ids):
        reasons.append("mssql base image identity differs")
    return reasons


def complete_manifest(manifest: Any) -> bool:
    if not isinstance(manifest, dict):
        return False
    text = all(isinstance(manifest.get(k), str) and manifest[k].strip() for k in TEXT_KEYS)
    numbers = all(
        isinstance(manifest.get(k), int) and not isinstance(manifest[k], bool) and manifest[k] > 0
        for k in NUMBER_KEYS
    )
    return text and numbers


def normalize_argv(argv: list[str]) -> list[str]:
    """Mask only per-run container operands and owner label tokens; image ids stay distinct."""
    result = [OWNER_LABEL.sub(r"\1<token>", item) for item in argv]
    if (
        len(result) >= 3
        and result[0] == "docker"
        and result[1] in CONTAINER_VERBS
        and HEX_ID.fullmatch(result[-1])
    ):
        result[-1] = "<container-id>"
    return result


def command_contract(receipt: dict[str, Any]) -> dict[str, list[str]]:
    """Per group, sorted command records: normalized argv, cwd, flags and scrubbed env."""
    contract: dict[str, list[str]] = {}
    for item in receipt["commands"]:
        env = item.get("env") or {}
        record = {
            "argv": normalize_argv(item["argv"]),
            "env": {key: PER_RUN_ENV.get(key, value) for key, value in sorted(env.items())},
            **{flag: item.get(flag) for flag in CONTRACT_FLAGS},
        }
        contract.setdefault(item["group"], []).append(json.dumps(record, sort_keys=True))
    return {group: sorted(values) for group, values in contract.items()}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise TimingError(EXIT_INPUT, f"Cannot read JSON {path}: {error}") from None


def verification_problems(records: Any, receipts: list[Path], arm: str) -> list[str]:
    found = {Path(r.get("receipt", "")).resolve(): r for r in records if isinstance(r, dict)}
    problems = []
    for path in receipts:
        record = found.get(path.resolve())
        if (
            not record
            or record.get("exit") != 0
            or not record.get("command")
            or not record.get("checkout")
        ):
            problems.append(
                f"{arm}: no exit-0 verification record with command and checkout for {path}"
            )
    return problems


def tree_delta(repo: Path, before: str, after: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", before, after],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise TimingError(EXIT_INPUT, f"git diff {before} {after} failed in {repo}")
    return result.stdout.split()


def compare(args: argparse.Namespace) -> dict[str, Any]:
    arms = {
        "before": [Path(p) for p in args.before],
        "after": [Path(p) for p in args.after],
    }
    reasons: list[str] = []
    loaded = {arm: [load_receipt(p) for p in paths] for arm, paths in arms.items()}
    manifests = {
        "before": read_json(args.host_manifest_before) if args.host_manifest_before else None,
        "after": read_json(args.host_manifest_after) if args.host_manifest_after else None,
    }
    records = {
        "before": read_json(args.verification_before) if args.verification_before else None,
        "after": read_json(args.verification_after) if args.verification_after else None,
    }
    for arm, paths in arms.items():
        if len({p.resolve() for p in paths}) < 2 or len({r["sealed"] for r in loaded[arm]}) < 2:
            reasons.append(f"{arm}: at least two distinct receipts per arm are required")
        if manifests[arm] is None:
            reasons.append(f"{arm}: host manifest missing")
        if records[arm] is None:
            reasons.append(f"{arm}: verification record missing")
        else:
            reasons += verification_problems(records[arm], paths, arm)
        if len({r["identity"]["head"] for r in loaded[arm]}) > 1:
            reasons.append(f"{arm}: receipts are from different heads")
    if reasons:
        return {"verdict": "NONCOMPARABLE", "reasons": reasons}
    sample = {arm: loaded[arm][0] for arm in arms}
    everything = loaded["before"] + loaded["after"]
    shared = {p.resolve() for p in arms["before"]} & {p.resolve() for p in arms["after"]}
    if shared:
        reasons.append("a receipt appears in both arms")
    for key in ("selection", "jobs", "image_cache", "tools"):
        if any(r[key] != everything[0][key] for r in everything):
            reasons.append(f"{key} differs")
    contracts = [command_contract(r) for r in everything]
    if any(set(c) != set(contracts[0]) for c in contracts):
        reasons.append("executed group set differs")
    elif any(c != contracts[0] for c in contracts):
        reasons.append("per-group command contract differs")
    reasons += list(dict.fromkeys(image_reasons(everything)))
    for arm, manifest in manifests.items():
        if not complete_manifest(manifest):
            reasons.append(f"{arm}: host manifest lacks {', '.join(MANIFEST_KEYS)}")
    if reasons:
        return {"verdict": "NONCOMPARABLE", "reasons": reasons}
    for key in MANIFEST_KEYS:
        if (manifests["before"] or {})[key] != (manifests["after"] or {})[key]:
            reasons.append(f"host {key} differs")
    heads = {arm: sample[arm]["identity"]["head"] for arm in arms}
    if heads["before"] != heads["after"]:
        if args.allow_tree_delta != "RUNNER_ONLY" or args.repo is None:
            reasons.append(
                "heads differ and --allow-tree-delta RUNNER_ONLY with --repo is not given"
            )
        else:
            changed = tree_delta(args.repo, heads["before"], heads["after"])
            extra = [
                p for p in changed if p not in ("tools/rpi-checks.py", "tools/test_rpi_checks.py")
            ]
            if extra:
                reasons.append("tree differs beyond the runner and its test: " + ", ".join(extra))
    if reasons:
        return {"verdict": "NONCOMPARABLE", "reasons": reasons}
    report: dict[str, Any] = {
        "verdict": "COMPARABLE",
        "note": NOTE,
        "run_order_recommendation": "ABBA (before, after, after, before) to avoid cache bias",
    }
    for arm, paths in arms.items():
        analyses = [analyse(r, None, 5.0) for r in loaded[arm]]
        spans = [a["span_seconds"] for a in analyses]
        walls: dict[str, list[float]] = {}
        chain: dict[str, list[float]] = {}
        for analysis in analyses:
            for name, group in analysis["groups"].items():
                walls.setdefault(name, []).append(group["wall"])
            totals: dict[str, float] = {}
            for segment in analysis["critical_chain"]:
                label = f"{segment['kind']}:{segment['group']}"
                totals[label] = totals.get(label, 0.0) + segment["seconds"]
            for label, value in totals.items():
                chain.setdefault(label, []).append(value)
        report[arm] = {
            "receipts": [str(p) for p in paths],
            "spans": spans,
            "retries": sum(a["retries"] for a in analyses),
            "span_median": statistics.median(spans),
            "span_min": min(spans),
            "span_max": max(spans),
            "group_wall_median": {k: statistics.median(v) for k, v in sorted(walls.items())},
            "chain_median": {k: statistics.median(v) for k, v in sorted(chain.items())},
        }
    report["span_median_delta"] = round(
        report["after"]["span_median"] - report["before"]["span_median"], 1
    )
    return report


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compare report as a table for a PR description."""
    lines = [f"Verdict: {report['verdict']}", ""]
    if report["verdict"] != "COMPARABLE":
        lines += [f"* {reason}" for reason in report["reasons"]]
        return "\n".join(lines)
    lines += [
        "| Arm | Receipts | Span median (s) | Min (s) | Max (s) | Retries |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for arm in ("before", "after"):
        item = report[arm]
        lines.append(
            f"| {arm} | {len(item['receipts'])} | {item['span_median']} | "
            f"{item['span_min']} | {item['span_max']} | {item['retries']} |"
        )
    lines += [
        "",
        f"Median span delta (after minus before): {report['span_median_delta']} s",
        "",
        report["note"],
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("report")
    rep.add_argument("receipt", type=Path)
    rep.add_argument("--log", type=Path)
    rep.add_argument("--gap", type=float, default=5.0)
    sub.add_parser("host-manifest")
    cmp_ = sub.add_parser("compare")
    cmp_.add_argument("--before", nargs="+", required=True)
    cmp_.add_argument("--after", nargs="+", required=True)
    cmp_.add_argument("--host-manifest-before", type=Path)
    cmp_.add_argument("--host-manifest-after", type=Path)
    cmp_.add_argument("--verification-before", type=Path)
    cmp_.add_argument("--verification-after", type=Path)
    cmp_.add_argument("--allow-tree-delta", choices=["RUNNER_ONLY"])
    cmp_.add_argument("--repo", type=Path)
    cmp_.add_argument("--markdown", action="store_true", help="print a PR-ready table, not JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "report":
            output = analyse(load_receipt(args.receipt), args.log, args.gap)
            code = 0
        elif args.command == "host-manifest":
            output, code = host_manifest(), 0
        else:
            output = compare(args)
            code = 0 if output["verdict"] == "COMPARABLE" else EXIT_NONCOMPARABLE
    except TimingError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return error.code
    if args.command == "compare" and args.markdown:
        print(render_markdown(output))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
