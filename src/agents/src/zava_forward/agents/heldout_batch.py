"""Bounded held-out token measurement and cost-cap runner (#432 AC3, #435 AC4, refs #108).

Measures prompt, cached and completion tokens per held-out proposal under an explicit finite
owner authorization with a hard USD ceiling. It fails closed: nothing is dispatched unless the
authorization, the frozen held-out manifest and the proposals all check out, and before every
call it reserves the worst-case cost and tokens of that call, stopping first if any limit would
be crossed.

``dry-run`` uses an offline deterministic estimator and is never measured evidence. ``live``
needs an explicit ``--execute-live`` plus an injected provider (``AgentWorker.provider_call``);
the command line wires none, so no live call can happen by accident. The prompt bound uses UTF-8
byte length, an upper bound on token count, so an accepted request cannot exceed
``max_prompt_tokens``. The runner never retries, and a missing, malformed or out-of-bound usage
record is charged at the worst case and stops the batch. This is a measurement tool, not an
approval of a model or of any later spend.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import statistics
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from zava_forward.agents.heldout_freeze import check_freeze

HARD_CAP_USD = Decimal("5.00")
MAX_CALLS = 50
NOT_CONFIGURED = 2
PER_MILLION = Decimal(1_000_000)
LABEL_LIVE = "measured held-out batch"
LABEL_DRY = "dry-run simulation - not measured evidence"
SOURCE_LIVE = "provider usage envelope via AgentWorker.provider_call"
SOURCE_DRY = "offline deterministic estimator (characters / 4); no provider call"
TIMEOUT_SECONDS = 60
TEXT_FIELDS = ("approved_by", "authority_ref", "model")
Call = Callable[[str, str, int, int], dict[str, Any]]


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _decimal(value: Any) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, int | float | str | Decimal):
        return None
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    return number if number.is_finite() else None


def authorization_problems(auth: Mapping[str, Any], now: datetime | None = None) -> list[str]:
    """Every reason the authorization cannot permit a batch; empty means it may proceed."""
    problems = [
        f"{key} missing"
        for key in TEXT_FIELDS
        if not isinstance(auth.get(key), str) or not auth[key].strip()
    ]
    expires = auth.get("expires_utc")
    try:
        when = datetime.fromisoformat(expires) if isinstance(expires, str) else None
    except ValueError:
        when = None
    if when is None or when.tzinfo is None:
        problems.append("expires_utc missing or not an ISO timestamp with timezone")
    elif when <= (now or datetime.now(UTC)):
        problems.append("authorization expired")
    calls = auth.get("max_calls")
    if not isinstance(calls, int) or isinstance(calls, bool) or not 0 < calls <= MAX_CALLS:
        problems.append(f"max_calls must be an integer from 1 to {MAX_CALLS}")
    for key in ("max_total_tokens", "max_prompt_tokens", "max_completion_tokens"):
        if not _is_int(auth.get(key)) or auth[key] <= 0:
            problems.append(f"{key} must be a positive integer")
    budget = _decimal(auth.get("max_budget_usd"))
    if budget is None or not 0 < budget <= HARD_CAP_USD:
        problems.append(f"max_budget_usd must be above 0 and at most {HARD_CAP_USD}")
    if auth.get("currency") != "USD":
        problems.append("currency must be USD")
    for key in ("input_usd_per_1m", "output_usd_per_1m"):
        rate = _decimal(auth.get(key))
        if rate is None or rate <= 0:
            problems.append(f"{key} must be a positive number")
    if auth.get("cached_input_usd_per_1m") is not None:
        cached = _decimal(auth["cached_input_usd_per_1m"])
        if cached is None or cached < 0:
            problems.append("cached_input_usd_per_1m must be a non-negative number")
    return problems


def _rates(auth: Mapping[str, Any]) -> tuple[Decimal, Decimal, Decimal]:
    rate_in = Decimal(str(auth["input_usd_per_1m"]))
    rate_out = Decimal(str(auth["output_usd_per_1m"]))
    cached = auth.get("cached_input_usd_per_1m")
    return rate_in, rate_out, rate_in if cached is None else Decimal(str(cached))


def worst_case_usd(auth: Mapping[str, Any]) -> Decimal:
    """Cost of one call at the maximum prompt and completion, at the higher prompt rate."""
    rate_in, rate_out, rate_cached = _rates(auth)
    cost: Decimal = (
        auth["max_prompt_tokens"] * max(rate_in, rate_cached)
        + auth["max_completion_tokens"] * rate_out
    ) / PER_MILLION
    return cost


def _usage(envelope: Any, auth: Mapping[str, Any]) -> dict[str, int] | None:
    if not isinstance(envelope, dict) or envelope.get("outcome") != "returned":
        return None
    usage = envelope.get("usage")
    if not isinstance(usage, dict):
        return None
    prompt, completion = usage.get("prompt_tokens"), usage.get("completion_tokens")
    total, cached = usage.get("total_tokens"), usage.get("cached_tokens", 0)
    if not (
        isinstance(prompt, int)
        and isinstance(completion, int)
        and isinstance(total, int)
        and isinstance(cached, int)
        and all(_is_int(v) and v >= 0 for v in (prompt, completion, total, cached))
    ):
        return None
    if total != prompt + completion or cached > prompt:
        return None
    if prompt > auth["max_prompt_tokens"] or completion > auth["max_completion_tokens"]:
        return None
    return dict(prompt=prompt, completion=completion, cached=cached)


def _cost(auth: Mapping[str, Any], use: Mapping[str, int]) -> Decimal:
    rate_in, rate_out, rate_cached = _rates(auth)
    fresh = use["prompt"] - use["cached"]
    return (
        fresh * rate_in + use["cached"] * rate_cached + use["completion"] * rate_out
    ) / PER_MILLION


def spread(values: Sequence[int]) -> dict[str, Any]:
    ordered = sorted(values)
    if not ordered:
        return dict(count=0, min=None, p50=None, mean=None, p90=None, max=None)
    return dict(
        count=len(ordered),
        min=ordered[0],
        p50=round(float(statistics.median(ordered)), 2),
        mean=round(sum(ordered) / len(ordered), 2),
        p90=ordered[math.ceil(0.9 * len(ordered)) - 1],
        max=ordered[-1],
    )


def dry_run_call(system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
    """Deterministic offline stand-in for a provider; never touches the network."""
    tokens = math.ceil((len(system) + len(prompt)) / 4)
    completion = min(max_tokens, max(1, tokens // 2))
    return dict(
        outcome="returned",
        text=None,
        usage=dict(
            prompt_tokens=tokens, completion_tokens=completion, total_tokens=tokens + completion
        ),
    )


def _gate_problems(
    auth: Mapping[str, Any],
    manifest: Mapping[str, Any],
    proposals: Sequence[Mapping[str, Any]],
    mode: str,
    provider_model: str | None,
    now: datetime | None,
) -> list[str]:
    if mode not in ("dry-run", "live"):
        return [f"unknown mode {mode!r}"]
    problems = authorization_problems(auth, now)
    freeze = check_freeze(manifest)
    if freeze["outcome"] != "frozen":
        problems.append("held-out set is not frozen: " + "; ".join(freeze["gaps"]))
    versions = manifest.get("versions")
    frozen_model = versions.get("model") if isinstance(versions, Mapping) else None
    if auth.get("model") != frozen_model:
        problems.append("authorized model differs from the frozen manifest model")
    if mode == "live" and provider_model != auth.get("model"):
        problems.append("live provider model is not the authorized model")
    held_out = manifest.get("held_out")
    known = set(held_out.get("case_ids") or []) if isinstance(held_out, Mapping) else set()
    if any(not isinstance(p, Mapping) for p in proposals):
        problems.append("every proposal must be an object")
        return problems
    ids = [p.get("id") for p in proposals]
    if not proposals:
        problems.append("no proposals to measure")
    if len(set(ids)) != len(ids):
        problems.append("duplicate proposal ids")
    unknown = sorted(str(i) for i in ids if i not in known)
    if unknown:
        problems.append("proposals outside the frozen held-out set: " + ", ".join(unknown))
    if any(not isinstance(p.get("prompt"), str) for p in proposals):
        problems.append("every proposal needs a prompt string")
    return problems


def _drift(
    auth: Mapping[str, Any],
    manifest: Mapping[str, Any],
    frozen: tuple[Any, Any],
    tick: Callable[[], datetime],
) -> str | None:
    """Stop reason when authorization or the frozen set changed since the gate; fail closed."""
    try:
        issues = authorization_problems(auth, tick())
        if "authorization expired" in issues:
            return "authorization-expired"
        if issues:
            return "authorization-invalid"
        freeze = check_freeze(manifest)
        if (
            freeze["outcome"] != "frozen"
            or (
                freeze["manifest_digest"],
                manifest.get("threshold_approval"),
            )
            != frozen
        ):
            return "freeze-drift"
    except Exception:
        return "check-failed"
    return None


def run_batch(
    auth: Mapping[str, Any],
    manifest: Mapping[str, Any],
    proposals: Sequence[Mapping[str, Any]],
    call: Call,
    *,
    mode: str,
    provider_model: str | None = None,
    clock: Callable[[], datetime] | None = None,
) -> dict[str, Any]:
    """Measure tokens per proposal, or refuse. ``mode`` is ``dry-run`` or ``live``.

    Authorization expiry and the frozen manifest are re-checked before every dispatch. A dry-run
    always uses the offline estimator, whatever ``call`` is supplied.
    """
    tick = clock or (lambda: datetime.now(UTC))
    proposals = proposals if isinstance(proposals, Sequence) else []
    try:
        problems = _gate_problems(auth, manifest, proposals, mode, provider_model, tick())
    except Exception as error:
        problems = [f"gate check failed: {type(error).__name__}"]
    live = mode == "live"
    if not live:
        call = dry_run_call
    report: dict[str, Any] = dict(
        outcome="refused" if problems else "completed",
        problems=problems,
        stop_reason="refused" if problems else None,
        mode=mode,
        evidence_label=LABEL_DRY,
        source=SOURCE_LIVE if live else SOURCE_DRY,
        spend_authority_ref=str(auth.get("authority_ref", "")),
        approved_by=str(auth.get("approved_by", "")),
        model=str(auth.get("model", "")),
        currency="USD",
        budget_usd=str(auth.get("max_budget_usd", "")),
        calls=0,
        accrued_usd="0.000000",
        tokens=dict(input=0, cached=0, output=0, total=0),
        rows=[],
    )
    report["spread"] = {k: spread([]) for k in ("total", "input", "output")}
    if problems:
        return report
    frozen = (
        check_freeze(manifest)["manifest_digest"],
        copy.deepcopy(manifest.get("threshold_approval")),
    )
    limit = Decimal(str(auth["max_budget_usd"]))
    worst = worst_case_usd(auth)
    reserve = auth["max_prompt_tokens"] + auth["max_completion_tokens"]
    accrued, tokens = Decimal(0), dict(input=0, cached=0, output=0, total=0)
    rows: list[dict[str, Any]] = []
    stop = "exhausted"
    for proposal in proposals:
        system, prompt = str(proposal.get("system", "")), proposal["prompt"]
        drift = _drift(auth, manifest, frozen, tick)
        if drift:
            stop = drift
        elif len(rows) >= auth["max_calls"]:
            stop = "max_calls"
        elif tokens["total"] + reserve > auth["max_total_tokens"]:
            stop = "max_total_tokens"
        elif accrued + worst > limit:
            stop = "budget"
        elif len((system + prompt).encode("utf-8")) > auth["max_prompt_tokens"]:
            stop = "prompt-too-large"
        else:
            try:
                envelope = call(system, prompt, auth["max_completion_tokens"], TIMEOUT_SECONDS)
            except Exception:
                envelope = {}
            use = _usage(envelope, auth)
            if use is None:
                accrued += worst
                tokens["total"] += reserve
                rows.append(dict(id=proposal["id"], measured=False, usd=f"{worst:.6f}"))
                stop = "unmeasured-call"
            else:
                spent = _cost(auth, use)
                accrued += spent
                tokens["input"] += use["prompt"] - use["cached"]
                tokens["cached"] += use["cached"]
                tokens["output"] += use["completion"]
                tokens["total"] += use["prompt"] + use["completion"]
                rows.append(
                    dict(
                        id=proposal["id"],
                        measured=True,
                        input=use["prompt"] - use["cached"],
                        cached=use["cached"],
                        output=use["completion"],
                        total=use["prompt"] + use["completion"],
                        usd=f"{spent:.6f}",
                    )
                )
                continue
        break
    measured = [r for r in rows if r["measured"]]
    report.update(
        stop_reason=stop,
        outcome="completed" if stop == "exhausted" else "stopped",
        calls=len(rows),
        accrued_usd=f"{accrued:.6f}",
        tokens=tokens,
        rows=rows,
        spread=dict(
            total=spread([r["total"] for r in measured]),
            input=spread([r["input"] + r["cached"] for r in measured]),
            output=spread([r["output"] for r in measured]),
        ),
    )
    if live and measured:
        report["evidence_label"] = LABEL_LIVE
    return report


def render_json(report: Mapping[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Held-out token measurement",
        "",
        f"* Evidence label: {report['evidence_label']}",
        f"* Source: {report['source']}",
        f"* Spend authority: {report['spend_authority_ref']} (approved by {report['approved_by']})",
        f"* Outcome: {report['outcome']} ({report['stop_reason']}); calls: {report['calls']}",
        f"* Accrued: USD {report['accrued_usd']} of USD {report['budget_usd']}",
        "* Tokens: input {input}, cached {cached}, output {output}, total {total}".format(
            **report["tokens"]
        ),
    ]
    lines += [f"* Problem: {p}" for p in report["problems"]]
    lines += [
        "",
        "| tokens | count | min | p50 | mean | p90 | max |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, row in report["spread"].items():
        cells = " | ".join(str(row[k]) for k in ("count", "min", "p50", "mean", "p90", "max"))
        lines.append(f"| {name} | {cells} |")
    return "\n".join(lines) + "\n"


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(
    argv: list[str] | None = None,
    *,
    provider: Call | None = None,
    provider_model: str | None = None,
) -> int:
    parser = argparse.ArgumentParser(prog="python -m zava_forward.agents.heldout_batch")
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--proposals", required=True)
    parser.add_argument("--json-out")
    parser.add_argument("--markdown", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--execute-live", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if args.execute_live and provider is None:
        print("heldout_batch: no provider is configured; no live call was made.", file=sys.stderr)
        return NOT_CONFIGURED
    report = run_batch(
        _load(args.authorization),
        _load(args.manifest),
        _load(args.proposals),
        provider if args.execute_live and provider else dry_run_call,
        mode="live" if args.execute_live else "dry-run",
        provider_model=provider_model,
    )
    if args.json_out:
        Path(args.json_out).write_text(render_json(report), encoding="utf-8")
    print(render_markdown(report) if args.markdown else render_json(report), end="")
    return 1 if report["outcome"] == "refused" else 0


if __name__ == "__main__":
    raise SystemExit(main())
