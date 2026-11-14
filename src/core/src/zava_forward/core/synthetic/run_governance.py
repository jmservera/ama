"""Owner, time limit and GBP budget alert for a simulator run (issue #189).

Costs are caller-declared planning figures, not billing data. No Azure call is made here.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

from .sensor_stream import StreamError, accountable_text

MAX_TIME_LIMIT_SECONDS = 3600.0
_EXTRA_PLACEHOLDERS = frozenset({"tbc", "pending"})


def governed_text(value: object) -> bool:
    """Reject blank, template, overlong, and placeholder owner or alert identifiers."""
    if not isinstance(value, str) or not accountable_text(value):
        return False
    return value.strip().casefold() not in _EXTRA_PLACEHOLDERS


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
class RunGovernance:
    run_owner: str
    time_limit_seconds: float
    budget_alert_gbp: Decimal | int | str
    budget_cap_gbp: Decimal | int | str

    def validate(self) -> tuple[Decimal, Decimal]:
        if not governed_text(self.run_owner):
            raise StreamError("RUN_OWNER_REQUIRED")
        limit = self.time_limit_seconds
        if (
            type(limit) not in (int, float)
            or not math.isfinite(limit)
            or not 1 <= limit <= MAX_TIME_LIMIT_SECONDS
        ):
            raise StreamError("TIME_LIMIT_REQUIRED")
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
