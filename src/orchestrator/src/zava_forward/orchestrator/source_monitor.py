"""Bounded offline source discovery job. No network, approval or activation commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from zava_forward.core import lawstore, rulecards
from zava_forward.core.source_monitor import SourceMonitor


def run(
    monitor: SourceMonitor,
    observations: dict[str, dict[str, Any]],
    *,
    today: str,
    limit: int = 100,
    after: str = "",
) -> dict[str, Any]:
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("source page limit must be from 1 to 100")
    sources = monitor.sql.all(
        "SELECT DISTINCT source_id FROM reg_monitor_config WHERE source_id>? ORDER BY source_id",
        (after,),
    )
    page = sources[:limit]
    report: dict[str, Any] = dict(changes=[], failures=[], skipped=[], checked=[])
    for row in page:
        sid = row["source_id"]
        if not monitor.due(sid, today):
            report["skipped"].append(sid)
            continue
        observation = observations.get(sid)
        if observation is None:
            cid = monitor.observe(
                sid,
                today=today,
                content=None,
                metadata={},
                provenance="offline job: no local observation supplied",
                method="local-fixture",
                error="No observation supplied for a due source",
            )
            report["failures"].append(dict(source_id=sid, change_id=cid))
        else:
            if not isinstance(observation, dict):
                raise ValueError("each source observation must be a JSON object")
            if set(observation) - {"content", "metadata", "provenance", "method", "error"}:
                raise ValueError("unknown observation fields")
            text = observation.get("content")
            if text is not None and not isinstance(text, str):
                raise ValueError("local observation content must be UTF-8 text")
            cid = monitor.observe(
                sid,
                today=today,
                content=text.encode() if text is not None else None,
                metadata=observation.get("metadata", {}),
                provenance=observation.get("provenance", ""),
                method=observation.get("method", "local-fixture"),
                error=observation.get("error"),
            )
            if observation.get("error"):
                report["failures"].append(dict(source_id=sid, change_id=cid))
        report["checked"].append(sid)
        if cid:
            report["changes"].append(cid)
    report["next_after"] = page[-1]["source_id"] if len(sources) > limit else None
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations", type=Path, help="explicit local observation JSON file")
    parser.add_argument("--today", required=True, help="exercise observation date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--after", default="")
    args = parser.parse_args(argv)
    law = lawstore.LawStore.from_env()
    if law is None:
        parser.error("configure ZF_LAW_DB (offline) or the existing Azure law store settings")
    try:
        observations = json.loads(args.observations.read_text(encoding="utf-8"))
        if not isinstance(observations, dict):
            raise ValueError("observations must be a source-keyed JSON object")
        result = run(
            SourceMonitor(law), observations, today=args.today, limit=args.limit, after=args.after
        )
        print(json.dumps(result, sort_keys=True))
        return 1 if result["failures"] else 0
    except (ValueError, rulecards.RuleError, OSError) as exc:
        parser.exit(1, f"SOURCE_MONITOR_ERROR: {exc}\n")
    finally:
        law.close()


if __name__ == "__main__":
    raise SystemExit(main())
