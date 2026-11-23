"""Audit deployed container hardening from recorded receipts (offline, Refs #144).

Two inputs, no Azure call and no secret read:

* `specs`: JSON from `az containerapp list` or `az containerapp job list`. Each
  container must set `ZF_CONTAINER_HARDENING=enforced`, the switch that makes the
  in-process guard refuse to start when it is not hardened.
* `status`: the text of `/proc/1/status` (the application process) from a live
  replica, optionally with `/proc/mounts`. The process must be non-root, have
  `NoNewPrivs` set and empty inheritable, permitted, effective and ambient
  capability sets. A root file system that is mounted read-write is reported, not
  hidden: Container Apps exposes no `readOnlyRootFilesystem` setting.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

GUARD = "ZF_CONTAINER_HARDENING"
ZERO_SETS = ("CapInh", "CapPrm", "CapEff", "CapAmb")
READ_ONLY_NOTE = "not enforceable: Container Apps has no readOnlyRootFilesystem setting"


def audit_specs(resources: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for resource in resources:
        template = (resource.get("properties") or {}).get("template") or {}
        for container in template.get("containers") or []:
            env = {e.get("name"): e.get("value") for e in container.get("env") or []}
            rows.append(
                {
                    "resource": resource.get("name"),
                    "guard": env.get(GUARD),
                    "enforced": env.get(GUARD) == "enforced",
                    "security_context_declared": container.get("securityContext") is not None,
                }
            )
    return {"containers": rows, "all_enforced": bool(rows) and all(r["enforced"] for r in rows)}


def parse_status(text: str) -> dict[str, str]:
    fields = {}
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def root_options(mounts: str) -> list[str] | None:
    for line in mounts.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[1] == "/":
            return parts[3].split(",")
    return None


def audit_status(status: str, mounts: str | None = None) -> dict[str, Any]:
    fields = parse_status(status)
    uid = fields.get("Uid", "").split()
    nonzero = {name: bool(re.fullmatch(r"0+", fields.get(name, "x"))) for name in ZERO_SETS}
    checks = {
        "non_root": bool(uid) and all(u.isdigit() and int(u) != 0 for u in uid),
        "no_new_privs": fields.get("NoNewPrivs") == "1",
        **{f"{name}_empty": ok for name, ok in nonzero.items()},
    }
    report: dict[str, Any] = {
        "checks": checks,
        "cap_bounding_set": fields.get("CapBnd"),
        "all_passed": all(checks.values()),
    }
    if mounts is not None:
        options = root_options(mounts)
        report["root_filesystem"] = {
            "options": options,
            "read_only": options is not None and "ro" in options,
            "note": READ_ONLY_NOTE,
        }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    specs = sub.add_parser("specs")
    specs.add_argument("json_file", nargs="*", help="az list output files; stdin when omitted")
    status = sub.add_parser("status")
    status.add_argument("status_file", help="saved /proc/1/status text")
    status.add_argument("--mounts", help="saved /proc/mounts text")
    args = parser.parse_args(argv)
    if args.mode == "specs":
        resources: list[dict[str, Any]] = []
        for path in args.json_file or ["-"]:
            text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
            data = json.loads(text)
            resources.extend(data if isinstance(data, list) else [data])
        report = audit_specs(resources)
        ok = report["all_enforced"]
    else:
        mounts = Path(args.mounts).read_text(encoding="utf-8") if args.mounts else None
        report = audit_status(Path(args.status_file).read_text(encoding="utf-8"), mounts)
        ok = report["all_passed"]
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
