"""Pre-run cost and quota estimate plus start, stop and scale-down controls for the simulator.

Planning figures are public list prices and the B1 quota decided in #140, not a billing quote.
No transport, credential or Azure call is made here.
"""

import argparse
import hashlib
import json
import math
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from .sensor_stream import Pacer, RunBudget, StreamError

TIER = "B1"
UNITS = 1
B1_DAILY_MESSAGES = 400_000
B1_MONTHLY_USD = 10.0
METER_BYTES = 4096
PROPERTY_BYTES = 1024
RESERVED_HEADROOM = 40_000
MAX_SECONDS = 3600.0
MAX_RUN_MESSAGES = 100_000
PUBLISH_CLEANUP_SECONDS = 0.5
PRICE_BASIS = "Azure Retail Prices API list price, uksouth, retrieved 2026-10-27 (infra/README.md)"


@dataclass(frozen=True)
class Estimate:
    tier: str
    units: int
    homes: int
    records_per_home_day: int
    days: int
    message_bytes: int
    messages_per_day: int
    metered_units_per_day: int
    total_messages: int
    quota_units_per_day: int
    headroom_units_per_day: int
    estimated_cost_usd: float
    price_basis: str


@dataclass(frozen=True)
class RunPlan:
    owner: str
    homes: int
    max_seconds: float
    max_per_second: float
    budget_usd: float
    alert_threshold: float
    alert_reference: str
    records_per_home_day: int = 3
    days: int = 1
    message_bytes: int = 512
    replay_speed: float = 1000.0
    daily_used_units: int = 0

    def validate(self) -> None:
        for text in (self.owner, self.alert_reference):
            if not isinstance(text, str) or not text.strip() or len(text) > 160:
                raise StreamError("RUN_OWNER_COST_ALERT_REQUIRED")
        numbers = (
            self.max_seconds,
            self.max_per_second,
            self.budget_usd,
            self.alert_threshold,
            self.replay_speed,
        )
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in numbers):
            raise StreamError("INVALID_RUN_LIMIT")
        if not 1 <= self.max_seconds <= MAX_SECONDS or not 0 < self.max_per_second <= 100:
            raise StreamError("INVALID_RUN_LIMIT")
        if not 0 < self.replay_speed <= 1000:
            raise StreamError("INVALID_REPLAY_SPEED")
        if self.budget_usd <= 0 or not 0 < self.alert_threshold <= 1:
            raise StreamError("INVALID_BUDGET")
        for count, ceiling in (
            (self.homes, 1_000_000),
            (self.records_per_home_day, 1440),
            (self.days, 366),
            (self.message_bytes, 250_000),
        ):
            if type(count) is not int or not 1 <= count <= ceiling:
                raise StreamError("INVALID_SCALE")
        if type(self.daily_used_units) is not int or not 0 <= self.daily_used_units <= 10_000_000:
            raise StreamError("INVALID_DAILY_USAGE")

    def estimate(self) -> Estimate:
        self.validate()
        per_day = self.homes * self.records_per_home_day
        units = per_day * math.ceil((self.message_bytes + PROPERTY_BYTES) / METER_BYTES)
        total = per_day * self.days
        # All days replay in one run of at most MAX_SECONDS, so count the whole run against a day.
        available = B1_DAILY_MESSAGES * UNITS - self.daily_used_units
        headroom = available - units * self.days - RESERVED_HEADROOM
        if headroom < 0:
            raise StreamError("B1_QUOTA_HEADROOM")
        if total > MAX_RUN_MESSAGES:
            raise StreamError("RUN_MESSAGE_LIMIT")
        # The publisher waits for replay spacing, then for the send slot, frame by frame, and
        # reserves PUBLISH_CLEANUP_SECONDS before the deadline, so the pacing costs add up.
        replay = self.days * 86400 / self.replay_speed
        if total / self.max_per_second + replay + PUBLISH_CLEANUP_SECONDS > self.max_seconds:
            raise StreamError("RUN_TIME_LIMIT_TOO_SHORT")
        # Billing follows the provisioned hub time (whole days), not the simulated replay span.
        cost = round(B1_MONTHLY_USD * UNITS * math.ceil(self.max_seconds / 86400) / 30, 2)
        if cost > self.budget_usd:
            raise StreamError("BUDGET_CAP_EXCEEDED")
        return Estimate(
            tier=TIER,
            units=UNITS,
            homes=self.homes,
            records_per_home_day=self.records_per_home_day,
            days=self.days,
            message_bytes=self.message_bytes,
            messages_per_day=per_day,
            metered_units_per_day=units,
            total_messages=total,
            quota_units_per_day=B1_DAILY_MESSAGES * UNITS,
            headroom_units_per_day=headroom,
            estimated_cost_usd=cost,
            price_basis=PRICE_BASIS,
        )

    def budget(self) -> RunBudget:
        return RunBudget(
            owner=self.owner,
            cost_reference=f"estimate:{self.estimate().estimated_cost_usd}USD",
            alert_reference=self.alert_reference,
            max_messages=self.homes * self.records_per_home_day * self.days,
            max_seconds=self.max_seconds,
            max_per_second=self.max_per_second,
            daily_used_units=self.daily_used_units,
        )


def _digest(body: dict[str, object]) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def _body(plan: RunPlan) -> dict[str, object]:
    return {
        "plan": asdict(plan),
        "estimate": asdict(plan.estimate()),
        "alert_fires_at_usd": round(plan.budget_usd * plan.alert_threshold, 2),
    }


def record(plan: RunPlan, path: Path) -> dict[str, object]:
    """Write the estimate before any run; the controller refuses to start without it."""
    body = _body(plan)
    body["sha256"] = _digest(body)
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return body


class RunController:
    """One run at a time with a hard deadline; no resume after stop."""

    def __init__(self, plan: RunPlan, *, clock: Callable[[], float] = time.monotonic) -> None:
        self.plan = plan
        self.clock = clock
        self.state = "idle"
        self.active_homes = plan.homes
        self.pacer: Pacer | None = None

    def start(self, estimate_path: Path) -> Pacer:
        if self.state != "idle":
            raise StreamError("RUN_ALREADY_STARTED")
        try:
            body = json.loads(estimate_path.read_text(encoding="utf-8"))
            if not isinstance(body, dict):
                raise ValueError
            claimed = body.pop("sha256")
        except (OSError, ValueError, KeyError):
            raise StreamError("ESTIMATE_NOT_RECORDED") from None
        expected = _body(self.plan)
        if claimed != _digest(body) or body != expected:
            raise StreamError("ESTIMATE_MISMATCH")
        self.pacer = Pacer(self.plan.budget(), speed=self.plan.replay_speed, clock=self.clock)
        self.state = "running"
        return self.pacer

    def stop(self) -> None:
        if self.pacer is not None:
            self.pacer.stopped = True
        self.state = "stopped"

    def scale_down(self, factor: float) -> int:
        """Reduce active homes and send rate; never scales up. Returns the new home count."""
        if self.state != "running" or self.pacer is None:
            raise StreamError("RUN_NOT_RUNNING")
        if type(factor) not in (int, float) or not 0 < factor < 1:
            raise StreamError("INVALID_SCALE_DOWN")
        self.active_homes = max(1, math.floor(self.active_homes * factor))
        self.pacer.set_max_per_second(self.pacer.max_per_second * factor)
        return self.active_homes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record a simulator cost and quota estimate")
    parser.add_argument("--homes", type=int, required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--max-seconds", type=float, default=MAX_SECONDS)
    parser.add_argument("--max-per-second", type=float, default=100.0)
    parser.add_argument("--replay-speed", type=float, default=1000.0)
    parser.add_argument("--daily-used-units", type=int, default=0)
    parser.add_argument("--budget-usd", type=float, required=True)
    parser.add_argument("--alert-threshold", type=float, default=0.8)
    parser.add_argument("--alert-reference", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    plan = RunPlan(
        owner=args.owner,
        homes=args.homes,
        max_seconds=args.max_seconds,
        max_per_second=args.max_per_second,
        budget_usd=args.budget_usd,
        alert_threshold=args.alert_threshold,
        alert_reference=args.alert_reference,
        replay_speed=args.replay_speed,
        daily_used_units=args.daily_used_units,
    )
    try:
        body = record(plan, args.out)
    except StreamError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    print(json.dumps(body["estimate"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
