"""Capped real-AI acceptance harness for the five assistants (issue #107, CON-009/AC-057).

Prepares, and does not spend, a small owner-capped token batch. It reads the staff
``GET /api/assistants`` listing (saved JSON), and plans one synthetic, case-free call per assistant
whose release is in force. It fails closed: an invalid owner authorization, an assistant whose
release is absent or denied, a missing provider or a missing ``--execute-live`` dispatches nothing.
Before every call it reserves that call's worst-case tokens and USD and stops first if a cap would
be crossed; it never retries and charges a missing or malformed usage record at the worst case.

``dry-run`` uses the offline estimator of ``heldout_batch`` and is never measured evidence. The
command line has no network adapter: a live batch needs an injected ``call`` (see ``run``) after an
approved release exists (OQ-017), so no token can be spent by accident.
"""

import argparse
import json
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from decimal import Decimal
from typing import Any

from zava_forward.agents import heldout_batch  # type: ignore[import-untyped]

ASSISTANTS = (
    "stock-prioritisation",
    "assessment-preparation",
    "funding-evidence",
    "works-resident-coordination",
    "quality-evidence",
)
Call = Callable[[str, str, int, int], dict[str, Any]]
SYSTEM = "Synthetic acceptance probe. Reply with one short sentence. No case data is supplied."


def prompt_for(assistant: str) -> str:
    return f"Acceptance probe for the {assistant} assistant: say which assistant you are."


def admitted(entry: Mapping[str, Any]) -> bool:
    """The staff listing shows a release in force as the string "in force"; a denial is an object."""
    return entry.get("release") == "in force"


def plan(
    auth: Mapping[str, Any], listing: Mapping[str, Any], now: datetime | None = None
) -> dict[str, Any]:
    problems = heldout_batch.authorization_problems(auth, now)
    entries = {e.get("id"): e for e in listing.get("assistants") or [] if isinstance(e, Mapping)}
    ready: list[str] = []
    blocked: dict[str, str] = {}
    for name in ASSISTANTS:
        entry = entries.get(name)
        if entry is None:
            blocked[name] = "not listed"
        elif not admitted(entry):
            blocked[name] = "no approved release in force"
        else:
            ready.append(name)
    for name in ready:
        if len(prompt_for(name).encode()) + len(SYSTEM.encode()) > auth.get("max_prompt_tokens", 0):
            problems.append(f"prompt for {name} exceeds max_prompt_tokens")
    if not problems:
        per_call = heldout_batch.worst_case_usd(auth)
        tokens = auth["max_prompt_tokens"] + auth["max_completion_tokens"]
        if len(ready) > auth["max_calls"]:
            problems.append("more ready assistants than max_calls")
        if len(ready) * tokens > auth["max_total_tokens"]:
            problems.append("worst-case tokens for the ready assistants exceed max_total_tokens")
        if len(ready) * per_call > Decimal(str(auth["max_budget_usd"])):
            problems.append("worst-case cost for the ready assistants exceeds max_budget_usd")
    return dict(problems=problems, ready=ready, blocked=blocked)


def run(
    auth: Mapping[str, Any],
    listing: Mapping[str, Any],
    mode: str = "dry-run",
    call: Call | None = None,
    execute_live: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    chosen = plan(auth, listing, now)
    problems = list(chosen["problems"])
    if mode not in ("dry-run", "live"):
        problems.append(f"unknown mode {mode!r}")
    if mode == "live" and not (execute_live and call):
        problems.append("live needs --execute-live and an injected provider call")
    report: dict[str, Any] = dict(
        mode=mode,
        label=heldout_batch.LABEL_LIVE if mode == "live" else heldout_batch.LABEL_DRY,
        blocked=chosen["blocked"],
        calls=[],
        tokens=0,
        usd="0",
        outcome="refused" if problems else "blocked" if not chosen["ready"] else "completed",
        problems=problems,
    )
    if problems or not chosen["ready"]:
        return report
    send = call if mode == "live" and call else heldout_batch.dry_run_call
    per_call = heldout_batch.worst_case_usd(auth)
    per_tokens = auth["max_prompt_tokens"] + auth["max_completion_tokens"]
    spent = Decimal(0)
    for name in chosen["ready"]:
        if (
            len(report["calls"]) >= auth["max_calls"]
            or report["tokens"] + per_tokens > auth["max_total_tokens"]
            or spent + per_call > Decimal(str(auth["max_budget_usd"]))
        ):
            report["outcome"] = "stopped-at-cap"
            break
        envelope = send(SYSTEM, prompt_for(name), auth["max_completion_tokens"], 60)
        usage = heldout_batch._usage(envelope, auth)
        if usage is None:
            report["calls"].append(dict(assistant=name, usage="missing or malformed"))
            report["tokens"] += per_tokens
            spent += per_call
            report["outcome"] = "stopped-bad-usage"
            break
        report["calls"].append(dict(assistant=name, **usage))
        report["tokens"] += usage["prompt"] + usage["completion"]
        spent += heldout_batch._cost(auth, usage)
    report["usd"] = str(spent)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--listing", required=True)
    parser.add_argument("--mode", choices=("dry-run", "live"), default="dry-run")
    parser.add_argument("--execute-live", action="store_true")
    args = parser.parse_args(argv)
    with open(args.authorization, encoding="utf-8") as handle:
        auth = json.load(handle)
    with open(args.listing, encoding="utf-8") as handle:
        listing = json.load(handle)
    report = run(auth, listing, args.mode, None, args.execute_live)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["outcome"] == "completed" else heldout_batch.NOT_CONFIGURED


if __name__ == "__main__":
    sys.exit(main())
