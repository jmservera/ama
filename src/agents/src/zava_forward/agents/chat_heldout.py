"""Freeze and leak gates for a held-out chat conversation set.

This module produces no held-out set and no labelling. It only decides whether a supplied set may
be treated as frozen and independent before it is scored: the scenarios must match a pinned digest,
carry a named labeller who is not the implementer, be versioned against the current task, model,
prompt, policy, source and memory bindings, and share no wording with the development set or the
system prompt. Any missing or stale item gives "insufficient" or "blocked", never a pass. Scoring
reuses the development harness; a held-out result is scripted and claims no actual-model or human
effectiveness.
"""

import copy
import hashlib
import json
import re
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from zava_forward.core import chat_panel

from zava_forward.agents import chat_eval

MIN_SHARED_WORDS = 6


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _strings(node: Any, keys: tuple[str, ...]) -> Iterator[str]:
    """Text a model or tuner could see: user turns, scripted replies and case fields."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in keys and isinstance(v, str):
                yield v
            else:
                yield from _strings(v, keys)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v, keys)


def _shingles(text: str) -> set[tuple[str, ...]]:
    w = _words(text)
    return {tuple(w[i : i + MIN_SHARED_WORDS]) for i in range(len(w) - MIN_SHARED_WORDS + 1)}


def leaks(heldout: dict[str, Any], development: dict[str, Any]) -> list[str]:
    """Held-out wording that already appears in the development set or the system prompt."""
    seen = _shingles(chat_panel.SYSTEM)
    for sc in development["scenarios"]:
        for text in _strings(sc, ("say", "answer", "stage", "measures")):
            seen |= _shingles(text)
    found = [
        f"{sc['id']}: shares {MIN_SHARED_WORDS} consecutive words with development material"
        for sc in heldout["scenarios"]
        if any(_shingles(t) & seen for t in _strings(sc, ("say", "answer", "stage", "measures")))
    ]
    dev_ids = {sc["id"] for sc in development["scenarios"]}
    found += [
        f"{sc['id']}: reuses a development scenario id"
        for sc in heldout["scenarios"]
        if sc["id"] in dev_ids
    ]
    return found


def freeze_problems(
    raw: bytes, manifest: dict[str, Any], *, implementer: str, development: dict[str, Any]
) -> list[str]:
    """Reasons the set cannot count as frozen and independent; empty means it may be scored."""
    problems = []
    if manifest.get("scenarios_sha256") != hashlib.sha256(raw).hexdigest():
        problems.append("scenarios differ from the frozen digest")
    labeller = str(manifest.get("labelled_by", "")).strip()
    if not labeller:
        problems.append("no named independent labeller")
    elif labeller.casefold() == implementer.strip().casefold():
        problems.append("labeller is the implementer, so labels are not independent")
    if not manifest.get("frozen_at"):
        problems.append("no freeze date")
    if not manifest.get("critical_errors"):
        problems.append("critical errors are not listed before testing")
    current = chat_eval.bindings(raw)
    frozen = manifest.get("bindings") or {}
    stale = sorted(k for k in current if k != "golden_sha256" and frozen.get(k) != current[k])
    if stale:
        problems.append("bindings changed since freeze: " + ", ".join(stale))
    spec = json.loads(raw.decode("utf-8"))
    problems += leaks(spec, development)
    return problems


def run_heldout(
    scenarios: Path,
    manifest: dict[str, Any],
    *,
    implementer: str,
    development: Path = chat_eval.GOLDEN,
) -> dict[str, Any]:
    """Score a frozen set with the scripted harness, or report why it was not scored."""
    raw = Path(scenarios).read_bytes()
    dev = json.loads(Path(development).read_text(encoding="utf-8"))
    problems = freeze_problems(raw, manifest, implementer=implementer, development=dev)
    if problems:
        return dict(outcome="insufficient", scored=False, problems=problems)
    results = []
    for sc in json.loads(raw.decode("utf-8"))["scenarios"]:
        with tempfile.TemporaryDirectory() as tmp:
            results.append(chat_eval.run_scenario(copy.deepcopy(sc), tmp))
    summary = chat_eval.summarise(results)
    ok = all(r["passed"] for r in results)
    return dict(
        outcome="pass" if ok else "fail",
        scored=True,
        problems=[],
        scenarios=len(results),
        failures=[f for r in results for f in r["failures"]],
        rates=summary["rates"],
        claim="scripted provider only; no actual-model or human effectiveness is claimed",
    )
