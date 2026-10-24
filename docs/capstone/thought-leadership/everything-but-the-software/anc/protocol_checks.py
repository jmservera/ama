#!/usr/bin/env python3
"""Reproduce protocol arithmetic; optionally check agreement across documents."""

import argparse
import math
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
PROTOCOL = PACKAGE / "anc" / "mve-feature-consolidation-harness"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-documents", action="store_true")
    return parser


def main() -> int:
    args = create_parser().parse_args()
    for runs in (3, 4, 5):
        allocations = math.comb(2 * runs, runs)
        print(f"EXACT_TWO_SIDED_MANN_WHITNEY_FLOOR n_per_arm={runs} 2/C({2 * runs},{runs})=2/{allocations}={2 / allocations:.9f}")
    runs_per_arm, features = 4, 8
    feature_steps = 2 * runs_per_arm * features
    consolidation_steps = runs_per_arm * features
    change_steps = 2 * runs_per_arm
    minutes = feature_steps * 30 + consolidation_steps * 15 + change_steps * 45
    print(f"FIRST_PASS feature_steps={feature_steps} consolidation_steps={consolidation_steps} change_request_steps={change_steps}")
    print(f"FIRST_PASS minutes={minutes} agent_hours={minutes / 60:g} ideal_four_session_hours={minutes / 60 / 4:g}")
    print("ASSUMPTIONS S1; A/B; 4 runs/arm; F1-F8; scoped CR1; 30/15/45 minute budgets; no pilot or scheduling/measurement overhead")
    if not args.check_documents:
        return 0
    sources = {
        "main.tex": (PACKAGE / "main.tex").read_text(encoding="utf-8"),
        "experiment-design.md": (PROTOCOL / "experiment-design.md").read_text(encoding="utf-8"),
        "hypotheses.md": (PROTOCOL / "hypotheses.md").read_text(encoding="utf-8"),
        "mve-plan.md": (PROTOCOL / "mve-plan.md").read_text(encoding="utf-8"),
    }
    for name in ("context.md", "vetting.md"):
        path = PROTOCOL / name
        if path.exists():
            sources[name] = path.read_text(encoding="utf-8")
        else:
            print(f"UNAVAILABLE optional protocol note: {name}")
    required = {
        "main.tex": ("four runs per arm", "eight features", "suite as a fixed effect", "run as a random intercept", "whole interval below 5 points"),
        "experiment-design.md": ("4 runs each, N = 8", "64 feature + 32 consolidation + 8 CR steps", "46 hours", "11.5 hours", "suite as a fixed effect", "run as a random intercept"),
        "hypotheses.md": ("four runs per arm", "eight features", "post-feature step", "95%", "inconclusive"),
        "mve-plan.md": ("4 runs per arm", "8 features", "64 feature", "46 hours", "suite as a fixed effect", "run as a random intercept"),
        "context.md": ("exploratory case study",),
        "vetting.md": ("minimum useful effect", "Inconclusive", "Non-significance alone is not invalidation"),
    }
    failures = []
    for name, fragments in required.items():
        if name not in sources:
            continue
        normalised = " ".join(sources[name].split())
        failures.extend(f"{name}: missing {fragment!r}" for fragment in fragments if fragment not in normalised)
    intervention_required = {
        "main.tex": ("Human intervention rate (HIR)", "observed HIR", "intervention-demand rate", "attempted feature cycles", "active human minutes", "no new hypothesis threshold", "do not trigger replacement runs"),
        "experiment-design.md": ("Observed HIR", "intervention-demand rate", "attempted feature cycles", "active human minutes", "do not replace it", "resampling whole runs within suite and arm"),
        "hypotheses.md": ("Observed HIR", "Intervention-demand rate", "attempted feature cycles", "active human minutes", "without replacement"),
        "mve-plan.md": ("observed HIR", "intervention-demand rate", "attempted feature cycle", "active human minutes", "without replacement"),
    }
    for name, fragments in intervention_required.items():
        normalised = " ".join(sources[name].split())
        failures.extend(f"{name}: missing intervention rule {fragment!r}" for fragment in fragments if fragment not in normalised)
    for failure in failures:
        print(f"FAIL {failure}")
    print("PASS protocol consistency checks" if not failures else "FAIL protocol consistency checks")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
