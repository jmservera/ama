"""Pre-run cost and quota estimate plus start, stop and scale-down controls for the simulator.

Planning figures are public list prices and the B1 quota decided in #140, not a billing quote.
No transport, credential or Azure call is made here.
"""

import argparse
import hashlib
import json
import math
import re
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path

from .run_governance import (
    BudgetAlertContract,
    RunGovernance,
    RunMeter,
    SimulatorRunControls,
    _gbp,
    governed_text,
    resolve_duration_seconds,
)
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
    budget_alert_gbp: str | None = None
    budget_cap_gbp: str | None = None
    planned_cost_gbp: str = "0"
    alert_owner: str | None = None
    alert_threshold_type: str = "Actual"

    @property
    def max_duration_seconds(self) -> float:
        return float(self.max_seconds)

    @property
    def time_limit_minutes(self) -> float:
        return round(float(self.max_seconds) / 60.0, 4)

    def budget_alert_contract(self, *, alert_owner: str | None = None) -> BudgetAlertContract:
        resolved_alert_owner = (
            alert_owner
            if alert_owner is not None
            else (self.alert_owner if self.alert_owner is not None else self.owner)
        )
        return BudgetAlertContract(
            threshold_percent=round(float(self.alert_threshold) * 100.0, 6),
            alert_rule_reference=self.alert_reference,
            alert_owner_reference=resolved_alert_owner,
            threshold_type=self.alert_threshold_type,
            budget_cap_usd=self.budget_usd,
            budget_alert_gbp=self.budget_alert_gbp,
            budget_cap_gbp=self.budget_cap_gbp,
        )

    def preflight_controls(self, *, alert_owner: str | None = None) -> SimulatorRunControls:
        return SimulatorRunControls(
            owner=self.owner,
            max_duration_seconds=self.max_seconds,
            time_limit_minutes=float(self.max_seconds) / 60.0,
            budget_alert=self.budget_alert_contract(alert_owner=alert_owner),
        )

    @classmethod
    def from_controls(
        cls,
        controls: SimulatorRunControls,
        *,
        homes: int,
        max_per_second: float = 100.0,
        budget_usd: float | None = None,
        records_per_home_day: int = 3,
        days: int = 1,
        message_bytes: int = 512,
        replay_speed: float = 1000.0,
        daily_used_units: int = 0,
        planned_cost_gbp: str = "0",
    ) -> "RunPlan":
        duration_seconds = controls.validate()
        alert = controls.budget_alert
        gbp_pair = alert.validate()
        resolved_usd = (
            budget_usd
            if budget_usd is not None
            else (alert.budget_cap_usd if alert.budget_cap_usd is not None else 5.0)
        )
        plan = cls(
            owner=controls.owner,
            homes=homes,
            max_seconds=duration_seconds,
            max_per_second=max_per_second,
            budget_usd=resolved_usd,
            alert_threshold=float(alert.threshold_percent) / 100.0,
            alert_reference=alert.alert_rule_reference,
            records_per_home_day=records_per_home_day,
            days=days,
            message_bytes=message_bytes,
            replay_speed=replay_speed,
            daily_used_units=daily_used_units,
            budget_alert_gbp=str(gbp_pair[0]) if gbp_pair is not None else None,
            budget_cap_gbp=str(gbp_pair[1]) if gbp_pair is not None else None,
            planned_cost_gbp=planned_cost_gbp,
            alert_owner=alert.alert_owner_reference,
            alert_threshold_type=alert.threshold_type,
        )
        plan.validate()
        return plan

    def governance(self) -> RunGovernance | None:
        """GBP governance is optional, but alert and cap must be declared together as strings."""
        if not isinstance(self.planned_cost_gbp, str):
            raise StreamError("INVALID_BUDGET")
        planned = _gbp(self.planned_cost_gbp, allow_zero=True)
        if self.budget_alert_gbp is None and self.budget_cap_gbp is None:
            if planned != 0:
                raise StreamError("INVALID_BUDGET")
            return None
        if not isinstance(self.budget_alert_gbp, str) or not isinstance(self.budget_cap_gbp, str):
            raise StreamError("INVALID_BUDGET")
        return RunGovernance(
            run_owner=self.owner,
            time_limit_seconds=self.max_seconds,
            budget_alert_gbp=self.budget_alert_gbp,
            budget_cap_gbp=self.budget_cap_gbp,
        )

    def validate(self) -> None:
        for text in (self.owner, self.alert_reference):
            if not governed_text(text):
                raise StreamError("RUN_OWNER_COST_ALERT_REQUIRED")
        if self.alert_owner is not None and not governed_text(self.alert_owner):
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
        if self.alert_threshold_type not in ("Actual", "Forecasted"):
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
        governance = self.governance()
        if governance is not None:
            RunMeter(governance, time.monotonic, self.planned_cost_gbp)
        self.preflight_controls().validate()

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
    plan_dict = asdict(plan)
    if plan.alert_owner is None:
        plan_dict.pop("alert_owner", None)
    if plan.alert_threshold_type == "Actual":
        plan_dict.pop("alert_threshold_type", None)
    return {
        "plan": plan_dict,
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
        plan.validate()
        governance = plan.governance()
        self._configured_alert_gbp: str | None = (
            str(governance.validate()[0]) if governance is not None else None
        )
        self.plan = plan
        self.clock = clock
        self.state = "idle"
        self.active_homes = plan.homes
        self.pacer: Pacer | None = None
        self.meter: RunMeter | None = None
        self.halt_reason: str | None = None
        self._started_at: float | None = None
        self._stopped_at: float | None = None

    def admit(self, cost_gbp: Decimal | int | str) -> None:
        """Record declared spend; alerts at the threshold and halts the run before the cap."""
        if self.state != "running" or self.meter is None:
            raise StreamError("RUN_NOT_RUNNING")
        try:
            self.meter.admit(cost_gbp)
        except StreamError:
            if self.meter.status == "halted":
                self.halt_reason = self.meter.halt_reason
                self._stopped_at = self.meter.ended
                self.stop()
            raise

    def check_time_limit(self) -> None:
        """Enforce the bounded run duration; stops the run and raises RUN_DEADLINE on expiry."""
        if self.state != "running":
            if self.halt_reason is not None:
                raise StreamError(self.halt_reason)
            raise StreamError("RUN_NOT_RUNNING")
        if self.meter is not None:
            try:
                self.meter.check_time_limit()
            except StreamError:
                self.halt_reason = self.meter.halt_reason
                self._stopped_at = self.meter.ended
                self.stop()
                raise
            return
        assert self._started_at is not None
        now = self.clock()
        if now - self._started_at >= self.plan.max_seconds:
            self.halt_reason = "RUN_DEADLINE"
            self._stopped_at = now
            self.stop()
            raise StreamError("RUN_DEADLINE")

    def _elapsed_seconds(self) -> float:
        if self._started_at is None:
            return 0.0
        end = self._stopped_at if self._stopped_at is not None else self.clock()
        return round(max(0.0, end - self._started_at), 3)

    def preflight(self) -> dict[str, object]:
        """Return validated owner, bounded duration, and linked budget-alert contract."""
        return self.plan.preflight_controls().preflight()

    def status(self) -> dict[str, object]:
        """Run state with its owner, time limit and budget alert position (USD + optional GBP)."""
        elapsed = self._elapsed_seconds()
        remaining = round(max(0.0, self.plan.max_seconds - elapsed), 3)
        base: dict[str, object] = {
            "state": self.state,
            "run_owner": self.plan.owner,
            "time_limit_seconds": self.plan.max_seconds,
            "max_duration_seconds": self.plan.max_duration_seconds,
            "time_limit_minutes": self.plan.time_limit_minutes,
            "elapsed_seconds": elapsed,
            "remaining_seconds": remaining,
            "active_homes": self.active_homes,
            "alert_reference": self.plan.alert_reference,
            "alert_fires_at_usd": round(self.plan.budget_usd * self.plan.alert_threshold, 2),
            "budget_alert_gbp": self._configured_alert_gbp,
            "budget_alert": self.plan.budget_alert_contract().as_dict(),
            "alert_raised": False,
            "halt_reason": self.halt_reason,
        }
        if self.meter is not None:
            base.update(self.meter.summary())
        return base

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
        governance = self.plan.governance()
        if governance is not None:
            self.meter = RunMeter(governance, self.clock, self.plan.planned_cost_gbp)
        self.pacer = Pacer(self.plan.budget(), speed=self.plan.replay_speed, clock=self.clock)
        self._started_at = self.meter.started if self.meter is not None else self.clock()
        self.state = "running"
        return self.pacer

    def stop(self) -> None:
        if self.state == "running" and self._stopped_at is None:
            self._stopped_at = self.clock()
        if self.meter is not None:
            self.meter.stop()
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


@dataclass(frozen=True)
class BicepNotificationContract:
    """Budget alert notification declared in Bicep."""

    name: str
    threshold_percent: int
    threshold_type: str
    enabled: bool
    contact_reference: str


@dataclass(frozen=True)
class BicepRunControlContract:
    """Verified Bicep owner-tag, bounded simulator-job, and budget-alert contract."""

    owner_tag_required: bool
    default_owner_tag: str
    alert_email_param_required: bool
    job_replica_timeout_seconds: int
    job_retry_limit: int
    job_runs_once: bool
    job_control_file: str
    hub_budget_resource_scoped: bool
    notifications: tuple[BicepNotificationContract, ...]


def _extract_brace_block(text: str, open_index: int) -> str:
    depth = 0
    for idx in range(open_index, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : idx]
    raise StreamError("BICEP_CONTRACT_MISMATCH")


def _parse_bicep_notifications(bicep_text: str) -> tuple[BicepNotificationContract, ...]:
    budget_match = re.search(
        r"resource\s+budget\s+'Microsoft\.Consumption/budgets@[\w-]+'\s*=\s*\{",
        bicep_text,
    )
    if budget_match is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    budget_body = _extract_brace_block(bicep_text, budget_match.end() - 1)
    notif_match = re.search(r"\bnotifications\s*:\s*\{", budget_body)
    if notif_match is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    notif_body = _extract_brace_block(budget_body, notif_match.end() - 1)
    pattern = re.compile(
        r"(\w+)\s*:\s*\{\s*"
        r"enabled\s*:\s*(true|false)\s+"
        r"operator\s*:\s*'GreaterThan'\s+"
        r"threshold\s*:\s*(\d+)\s+"
        r"thresholdType\s*:\s*'(\w+)'\s+"
        r"contactEmails\s*:\s*\[([^\]]*)\]\s*\}",
        re.DOTALL,
    )
    found: list[BicepNotificationContract] = []
    for match in pattern.finditer(notif_body):
        contact = match.group(5).strip()
        if not contact:
            raise StreamError("BICEP_CONTRACT_MISMATCH")
        found.append(
            BicepNotificationContract(
                name=match.group(1),
                enabled=match.group(2) == "true",
                threshold_percent=int(match.group(3)),
                threshold_type=match.group(4),
                contact_reference=contact,
            )
        )
    if not found:
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    return tuple(found)


def verify_bicep_run_controls(
    infra_dir: Path,
    controls: SimulatorRunControls | None = None,
) -> BicepRunControlContract:
    """Verify Bicep owner-tag, bounded job runtime, and budget-alert declarations."""
    try:
        governance_text = (infra_dir / "governance.bicep").read_text(encoding="utf-8")
        main_text = (infra_dir / "main.bicep").read_text(encoding="utf-8")
        iothub_text = (infra_dir / "modules" / "iothub.bicep").read_text(encoding="utf-8")
        job_text = (infra_dir / "live-simulator-job.bicep").read_text(encoding="utf-8")
    except OSError:
        raise StreamError("BICEP_CONTRACT_MISMATCH") from None

    req_tags_match = re.search(
        r"param\s+requiredTags\s+array\s*=\s*\[(.*?)\]", governance_text, re.DOTALL
    )
    if req_tags_match is None or re.search(r"'owner'", req_tags_match.group(1)) is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    owner_tag_match = re.search(
        r"^param\s+ownerTag\s+string\s*=\s*'([^']*)'\s*$", main_text, re.MULTILINE
    )
    if owner_tag_match is None or not governed_text(owner_tag_match.group(1)):
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    default_owner_tag = owner_tag_match.group(1)

    if (
        re.search(
            r"var\s+allTags\s*=\s*union\(\s*tags\s*,\s*\{[^}]*\bowner\s*:\s*ownerTag\b[^}]*\}\s*\)",
            main_text,
            re.DOTALL,
        )
        is None
    ):
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    if re.search(r"^param\s+alertEmail\s+string\s*$", main_text, re.MULTILINE) is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    if re.search(r"^param\s+alertEmail\s+string\s*$", iothub_text, re.MULTILINE) is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    iot_module_match = re.search(
        r"module\s+iotHub\s+'modules/iothub\.bicep'\s*=\s*\{.*?params\s*:\s*\{(.*?)\}\s*\}",
        main_text,
        re.DOTALL,
    )
    if (
        iot_module_match is None
        or re.search(r"\btags\s*:\s*allTags\b", iot_module_match.group(1)) is None
        or re.search(r"\balertEmail\s*:\s*alertEmail\b", iot_module_match.group(1)) is None
    ):
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    main_notifications = _parse_bicep_notifications(main_text)
    hub_notifications = _parse_bicep_notifications(iothub_text)
    for notifications in (main_notifications, hub_notifications):
        by_key = {
            (n.name, n.threshold_percent, n.threshold_type, n.enabled, n.contact_reference)
            for n in notifications
        }
        if ("actual80", 80, "Actual", True, "alertEmail") not in by_key or (
            "forecast100",
            100,
            "Forecasted",
            True,
            "alertEmail",
        ) not in by_key:
            raise StreamError("BICEP_CONTRACT_MISMATCH")

    if "name: 'ResourceId'" not in iothub_text:
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    timeout_match = re.search(r"\breplicaTimeout\s*:\s*(\d+)\b", job_text)
    retry_match = re.search(r"\breplicaRetryLimit\s*:\s*(\d+)\b", job_text)
    control_match = re.search(
        r"\{\s*name\s*:\s*'ZF_SIM_CONTROL_FILE'\s*,\s*value\s*:\s*'([^']+)'\s*\}", job_text
    )
    if timeout_match is None or retry_match is None or control_match is None:
        raise StreamError("BICEP_CONTRACT_MISMATCH")
    replica_timeout = int(timeout_match.group(1))
    retry_limit = int(retry_match.group(1))
    control_file = control_match.group(1)
    if (
        not 1 <= replica_timeout <= int(MAX_SECONDS)
        or retry_limit != 0
        or "'--once'" not in job_text
        or "!empty(trim(approvalReference))" not in job_text
        or "mountOptions: 'ro'" not in job_text
    ):
        raise StreamError("BICEP_CONTRACT_MISMATCH")

    if controls is not None:
        controls.preflight()
        aligned = any(
            n.enabled
            and n.threshold_type == controls.budget_alert.threshold_type
            and math.isclose(
                float(controls.budget_alert.threshold_percent),
                float(n.threshold_percent),
                rel_tol=0.0,
                abs_tol=1e-6,
            )
            for n in hub_notifications
        )
        if not aligned:
            raise StreamError("BICEP_CONTRACT_MISMATCH")

    return BicepRunControlContract(
        owner_tag_required=True,
        default_owner_tag=default_owner_tag,
        alert_email_param_required=True,
        job_replica_timeout_seconds=replica_timeout,
        job_retry_limit=retry_limit,
        job_runs_once=True,
        job_control_file=control_file,
        hub_budget_resource_scoped=True,
        notifications=hub_notifications,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record a simulator cost and quota estimate")
    parser.add_argument("--homes", type=int, required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--max-seconds", type=float, default=None)
    parser.add_argument("--time-limit-minutes", type=float, default=None)
    parser.add_argument("--max-per-second", type=float, default=100.0)
    parser.add_argument("--replay-speed", type=float, default=1000.0)
    parser.add_argument("--daily-used-units", type=int, default=0)
    parser.add_argument("--budget-usd", type=float, required=True)
    parser.add_argument("--alert-threshold", type=float, default=0.8)
    parser.add_argument("--alert-reference", required=True)
    parser.add_argument("--alert-owner", default=None)
    parser.add_argument("--budget-alert-gbp")
    parser.add_argument("--budget-cap-gbp")
    parser.add_argument("--planned-cost-gbp", default="0")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.max_seconds is None and args.time_limit_minutes is None:
            max_seconds = MAX_SECONDS
        else:
            max_seconds = resolve_duration_seconds(
                max_duration_seconds=args.max_seconds,
                time_limit_minutes=args.time_limit_minutes,
            )
        plan = RunPlan(
            owner=args.owner,
            homes=args.homes,
            max_seconds=max_seconds,
            max_per_second=args.max_per_second,
            budget_usd=args.budget_usd,
            alert_threshold=args.alert_threshold,
            alert_reference=args.alert_reference,
            replay_speed=args.replay_speed,
            daily_used_units=args.daily_used_units,
            budget_alert_gbp=args.budget_alert_gbp,
            budget_cap_gbp=args.budget_cap_gbp,
            planned_cost_gbp=args.planned_cost_gbp,
            alert_owner=args.alert_owner,
        )
        body = record(plan, args.out)
    except StreamError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    print(json.dumps(body["estimate"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
