"""Owner, time limit and GBP budget alert for a simulator run (issue #189).

Costs are caller-declared planning figures, not billing data. No Azure call is made here.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

from .sensor_stream import StreamError, accountable_text

MIN_TIME_LIMIT_SECONDS = 1.0
MAX_TIME_LIMIT_SECONDS = 3600.0
MAX_TIME_LIMIT_MINUTES = MAX_TIME_LIMIT_SECONDS / 60.0
_DURATION_ATOL_SECONDS = 1e-6
_THRESHOLD_TYPES = frozenset({"Actual", "Forecasted"})


def governed_text(value: object) -> bool:
    """Reject blank, template, overlong, non-identifier, and placeholder owner or alert names."""
    return isinstance(value, str) and accountable_text(value)


def _valid_duration_number(value: object) -> bool:
    return isinstance(value, (int, float)) and type(value) is not bool and math.isfinite(value)


def resolve_duration_seconds(
    *,
    max_duration_seconds: float | int | None = None,
    time_limit_minutes: float | int | None = None,
) -> float:
    """Resolve bounded simulator runtime from seconds, minutes, or agreeing pair."""
    if max_duration_seconds is None and time_limit_minutes is None:
        raise StreamError("TIME_LIMIT_REQUIRED")
    seconds: float | None = None
    if max_duration_seconds is not None:
        if not _valid_duration_number(max_duration_seconds):
            raise StreamError("TIME_LIMIT_REQUIRED")
        seconds = float(max_duration_seconds)
        if not MIN_TIME_LIMIT_SECONDS <= seconds <= MAX_TIME_LIMIT_SECONDS:
            raise StreamError("TIME_LIMIT_REQUIRED")
    if time_limit_minutes is not None:
        if not _valid_duration_number(time_limit_minutes):
            raise StreamError("TIME_LIMIT_REQUIRED")
        from_minutes = float(time_limit_minutes) * 60.0
        if not MIN_TIME_LIMIT_SECONDS <= from_minutes <= MAX_TIME_LIMIT_SECONDS:
            raise StreamError("TIME_LIMIT_REQUIRED")
        if seconds is not None and not math.isclose(
            seconds, from_minutes, rel_tol=0.0, abs_tol=_DURATION_ATOL_SECONDS
        ):
            raise StreamError("TIME_LIMIT_MISMATCH")
        if seconds is None:
            seconds = from_minutes
    assert seconds is not None
    return seconds


def _gbp(value: object, *, allow_zero: bool = False) -> Decimal:
    if type(value) is bool or not isinstance(value, (int, str, Decimal)):
        raise StreamError("INVALID_BUDGET")
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise StreamError("INVALID_BUDGET") from None
    if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
        raise StreamError("INVALID_BUDGET")
    return amount


@dataclass(frozen=True)
class BudgetAlertContract:
    """Linked budget-alert contract binding threshold, alert rule, and alert owner."""

    threshold_percent: float
    alert_rule_reference: str
    alert_owner_reference: str
    threshold_type: str = "Actual"
    budget_cap_usd: float | None = None
    budget_alert_gbp: Decimal | int | str | None = None
    budget_cap_gbp: Decimal | int | str | None = None

    def validate(self) -> tuple[Decimal, Decimal] | None:
        if not governed_text(self.alert_rule_reference) or not governed_text(
            self.alert_owner_reference
        ):
            raise StreamError("RUN_OWNER_COST_ALERT_REQUIRED")
        if self.threshold_type not in _THRESHOLD_TYPES:
            raise StreamError("INVALID_BUDGET")
        if (
            type(self.threshold_percent) not in (int, float)
            or not math.isfinite(self.threshold_percent)
            or not 0 < self.threshold_percent <= 100
        ):
            raise StreamError("INVALID_BUDGET")
        if self.budget_cap_usd is not None and (
            type(self.budget_cap_usd) not in (int, float)
            or not math.isfinite(self.budget_cap_usd)
            or self.budget_cap_usd <= 0
        ):
            raise StreamError("INVALID_BUDGET")
        if (self.budget_alert_gbp is None) != (self.budget_cap_gbp is None):
            raise StreamError("INVALID_BUDGET")
        if self.budget_alert_gbp is not None and self.budget_cap_gbp is not None:
            alert_gbp = _gbp(self.budget_alert_gbp)
            cap_gbp = _gbp(self.budget_cap_gbp)
            if alert_gbp >= cap_gbp:
                raise StreamError("BUDGET_ALERT_NOT_BELOW_CAP")
            return alert_gbp, cap_gbp
        return None

    @property
    def alert_fires_at_usd(self) -> float | None:
        self.validate()
        if self.budget_cap_usd is None:
            return None
        return round(float(self.budget_cap_usd) * (float(self.threshold_percent) / 100.0), 2)

    def as_dict(self) -> dict[str, Any]:
        gbp_pair = self.validate()
        fires_usd = (
            round(float(self.budget_cap_usd) * (float(self.threshold_percent) / 100.0), 2)
            if self.budget_cap_usd is not None
            else None
        )
        return {
            "threshold_percent": round(float(self.threshold_percent), 4),
            "threshold_type": self.threshold_type,
            "alert_rule_reference": self.alert_rule_reference.strip(),
            "alert_owner_reference": self.alert_owner_reference.strip(),
            "budget_cap_usd": (
                round(float(self.budget_cap_usd), 2) if self.budget_cap_usd is not None else None
            ),
            "alert_fires_at_usd": fires_usd,
            "budget_alert_gbp": str(gbp_pair[0]) if gbp_pair is not None else None,
            "budget_cap_gbp": str(gbp_pair[1]) if gbp_pair is not None else None,
        }


@dataclass(frozen=True)
class SimulatorRunControls:
    """Runtime preflight contract requiring owner, bounded duration, and linked budget alert."""

    owner: str
    budget_alert: BudgetAlertContract
    max_duration_seconds: float | None = None
    time_limit_minutes: float | None = None

    def validate(self) -> float:
        if not governed_text(self.owner):
            raise StreamError("RUN_OWNER_REQUIRED")
        duration_seconds = resolve_duration_seconds(
            max_duration_seconds=self.max_duration_seconds,
            time_limit_minutes=self.time_limit_minutes,
        )
        if not isinstance(self.budget_alert, BudgetAlertContract):
            raise StreamError("RUN_OWNER_COST_ALERT_REQUIRED")
        self.budget_alert.validate()
        return duration_seconds

    def preflight(self) -> dict[str, Any]:
        duration_seconds = self.validate()
        return {
            "owner": self.owner.strip(),
            "max_duration_seconds": duration_seconds,
            "time_limit_minutes": round(duration_seconds / 60.0, 4),
            "budget_alert": self.budget_alert.as_dict(),
        }


@dataclass(frozen=True)
class RunGovernance:
    run_owner: str
    time_limit_seconds: float
    budget_alert_gbp: Decimal | int | str
    budget_cap_gbp: Decimal | int | str

    @property
    def max_duration_seconds(self) -> float:
        return float(self.time_limit_seconds)

    @property
    def time_limit_minutes(self) -> float:
        return round(float(self.time_limit_seconds) / 60.0, 4)

    @classmethod
    def from_minutes(
        cls,
        *,
        run_owner: str,
        time_limit_minutes: float,
        budget_alert_gbp: Decimal | int | str,
        budget_cap_gbp: Decimal | int | str,
    ) -> "RunGovernance":
        seconds = resolve_duration_seconds(time_limit_minutes=time_limit_minutes)
        instance = cls(
            run_owner=run_owner,
            time_limit_seconds=seconds,
            budget_alert_gbp=budget_alert_gbp,
            budget_cap_gbp=budget_cap_gbp,
        )
        instance.validate()
        return instance

    def validate(self) -> tuple[Decimal, Decimal]:
        if not governed_text(self.run_owner):
            raise StreamError("RUN_OWNER_REQUIRED")
        resolve_duration_seconds(max_duration_seconds=self.time_limit_seconds)
        alert, cap = _gbp(self.budget_alert_gbp), _gbp(self.budget_cap_gbp)
        if alert >= cap:
            raise StreamError("BUDGET_ALERT_NOT_BELOW_CAP")
        return alert, cap


@dataclass
class RunMeter:
    """Accumulates declared run cost; alerts at the threshold and halts before the cap."""

    governance: RunGovernance
    clock: Callable[[], float]
    projected_cost_gbp: Decimal | int | str = 0
    events: list[dict[str, Any]] = field(default_factory=list)
    accumulated_gbp: Decimal = Decimal(0)
    status: str = "running"
    halt_reason: str | None = None
    ended: float | None = None

    def __post_init__(self) -> None:
        self.alert, self.cap = self.governance.validate()
        self.started = self.clock()
        projected = _gbp(self.projected_cost_gbp, allow_zero=True)
        if projected >= self.cap:
            self._halt("projected", projected)
            raise StreamError("RUN_BUDGET_HALT")
        if projected >= self.alert:
            self._alert("projected", projected)

    def _event(self, kind: str, basis: str, amount: Decimal) -> None:
        self.events.append(
            {
                "event": kind,
                "basis": basis,
                "run_owner": self.governance.run_owner,
                "amount_gbp": str(amount),
                "alert_gbp": str(self.alert),
                "cap_gbp": str(self.cap),
            }
        )

    def _alert(self, basis: str, amount: Decimal) -> None:
        if not any(e["event"] == "budget_alert" for e in self.events):
            self._event("budget_alert", basis, amount)

    def _halt(self, basis: str, amount: Decimal) -> None:
        self.status = "halted"
        self.halt_reason = "RUN_BUDGET_HALT"
        if self.ended is None:
            self.ended = self.clock()
        self._event("budget_halt", basis, amount)

    def _ensure_running(self) -> None:
        if self.status == "stopped":
            raise StreamError("RUN_STOPPED")
        if self.status != "running":
            raise StreamError(self.halt_reason or "RUN_BUDGET_HALT")

    def check_time_limit(self) -> None:
        """Enforce the bounded run duration even before a positive spend increment."""
        self._ensure_running()
        now = self.clock()
        if now - self.started >= self.governance.time_limit_seconds:
            self.status = "halted"
            self.halt_reason = "RUN_DEADLINE"
            self.ended = now
            self._event("time_limit_halt", "elapsed", self.accumulated_gbp)
            raise StreamError("RUN_DEADLINE")

    def stop(self) -> None:
        """Freeze elapsed runtime on manual operator stop without overwriting a halt."""
        if self.status == "running":
            self.status = "stopped"
            if self.ended is None:
                self.ended = self.clock()

    def summary(self) -> dict[str, Any]:
        """Owner-facing status: who owns the run, its time limit and where the budget stands."""
        end = self.ended if self.ended is not None else self.clock()
        elapsed = round(max(0.0, end - self.started), 3)
        remaining = round(max(0.0, self.governance.time_limit_seconds - elapsed), 3)
        alert = str(self.alert)
        return {
            "run_owner": self.governance.run_owner,
            "time_limit_seconds": self.governance.time_limit_seconds,
            "elapsed_seconds": elapsed,
            "remaining_seconds": remaining,
            "status": self.status,
            "halt_reason": self.halt_reason,
            "accumulated_gbp": str(self.accumulated_gbp),
            "budget_alert_gbp": alert,
            "alert_gbp": alert,
            "cap_gbp": str(self.cap),
            "alert_raised": any(e["event"] == "budget_alert" for e in self.events),
        }

    def admit(self, cost_gbp: Decimal | int | str) -> None:
        """Record the next spend; raises before it would breach the cap or the time limit."""
        self.check_time_limit()
        cost = _gbp(cost_gbp, allow_zero=True)
        total = self.accumulated_gbp + cost
        if total >= self.cap:
            self._halt("accumulated", total)
            raise StreamError("RUN_BUDGET_HALT")
        self.accumulated_gbp = total
        if total >= self.alert:
            self._alert("accumulated", total)
