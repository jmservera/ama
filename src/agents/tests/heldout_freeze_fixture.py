"""Synthetic held-out freeze manifest shared by tests; not held-out evidence."""

from __future__ import annotations

from typing import Any

from zava_forward.agents.heldout_freeze import _digest


def manifest() -> dict[str, Any]:
    m: dict[str, Any] = dict(
        versions=dict(task="t-1", model="m-1", prompt="p-1", policy="pol-1", source="s-1"),
        held_out=dict(
            case_ids=["h1", "h2", "h3", "h4"],
            seed="seed-7",
            denominator=4,
            labelled_by="labeller a",
            prompt_author="author b",
            expected=dict(h1="accept", h2="refuse", h3="accept", h4="refuse"),
            critical_errors=["unsupported citation"],
        ),
        prompt_case_ids=["p1"],
        tuning_case_ids=[],
        thresholds=dict(max_critical_misses=0, min_accuracy=0.9, min_sample_per_cohort=2),
        cohorts=dict(a=["h1", "h2"], b=["h3", "h4"]),
    )
    m["threshold_approval"] = dict(by="owner", manifest_digest=_digest(m))
    return m
