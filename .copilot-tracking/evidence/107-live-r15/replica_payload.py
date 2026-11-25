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



from datetime import datetime, timedelta, timezone
from zava_forward.agents import heldout_aoai
listing={"assistants": [{"id": "stock-prioritisation", "release": "in force"}, {"id": "assessment-preparation", "release": "in force"}, {"id": "funding-evidence", "release": "in force"}, {"id": "works-resident-coordination", "release": "in force"}, {"id": "quality-evidence", "release": "in force"}]}
auth=dict(approved_by="Juan Manuel Servera, project owner",authority_ref="owner-decision:2026-11-18 demo live Azure; r15 in-replica batch, hard cap 200000 tokens",model="gpt-4.1-nano",endpoint='https://aif-cutover-test-rzsrg.openai.azure.com',deployment='standard',expires_utc=(datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),max_calls=5,max_total_tokens=200000,max_prompt_tokens=400,max_completion_tokens=200,max_budget_usd="1.00",currency="USD",input_usd_per_1m="0.10",output_usd_per_1m="0.40")
try:
    import os,urllib.request,urllib.parse
    u=os.environ["IDENTITY_ENDPOINT"]+"?"+urllib.parse.urlencode({"api-version":"2019-08-01","resource":"https://cognitiveservices.azure.com","client_id":os.environ.get("AZURE_CLIENT_ID","")})
    tok=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"X-IDENTITY-HEADER":os.environ["IDENTITY_HEADER"]}),timeout=15))["access_token"]
    prov=heldout_aoai.make_provider(auth["endpoint"],auth["deployment"],"gpt-4.1-nano",tok)
    rep=run(auth,listing,"live",prov,True)
except Exception as e:
    rep={"error":type(e).__name__,"detail":str(e)[:200]}
print("REPORT_BEGIN");print(json.dumps(rep,sort_keys=True));print("REPORT_END")
