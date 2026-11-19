"""Classify deployed container image references (read-only, offline, Refs #144).

Input is the JSON printed by `az containerapp list` or `az containerapp job list`
(a file path or stdin). The script makes no Azure call and reads no secret. It
reports whether each image is a real, immutable, registry-hosted reference. It
cannot prove that the pipeline published the image or that a tag exists, so the
report always says provenance is unproven.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_MARKERS = ("quickstart", "helloworld")
DIGEST = re.compile(r"@sha256:[0-9a-f]{64}$")


def classify(image: str, registry: str | None) -> str:
    lowered = image.lower()
    if any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        return "placeholder"
    if registry and not lowered.startswith(f"{registry.lower()}/"):
        return "foreign-registry"
    if DIGEST.search(lowered):
        return "digest-pinned"
    last = lowered.rsplit("/", 1)[-1]
    if ":" not in last or last.endswith(":latest"):
        return "latest"
    return "tag-only"


def audit(resources: list[dict[str, Any]], registry: str | None = None) -> dict[str, Any]:
    rows = []
    for resource in resources:
        template = (resource.get("properties") or {}).get("template") or {}
        for container in template.get("containers") or []:
            image = str(container.get("image", ""))
            rows.append(
                {
                    "resource": resource.get("name"),
                    "repository": image.split("@", 1)[0].split(":", 1)[0].rsplit("/", 1)[-1],
                    "digest": image.split("@", 1)[1][:19] if "@" in image else None,
                    "kind": classify(image, registry),
                }
            )
    return {
        "containers": rows,
        "all_real_and_immutable": bool(rows) and all(r["kind"] == "digest-pinned" for r in rows),
        "provenance": "unproven: registry tags and pipeline runs are not checked here",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", nargs="*", help="az list output files; stdin when omitted")
    parser.add_argument("--registry", help="expected login server, for example x.azurecr.io")
    args = parser.parse_args(argv)
    resources: list[dict[str, Any]] = []
    for path in args.json_file or ["-"]:
        text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
        resources.extend(data if isinstance(data, list) else [data])
    report = audit(resources, args.registry)
    print(json.dumps(report, indent=2))
    return 0 if report["all_real_and_immutable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
