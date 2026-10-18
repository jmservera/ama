"""Recorded appointment agreements, not a scheduler or operational policy approval."""

import hashlib
import json
from copy import deepcopy
from datetime import UTC, date, datetime
from typing import Any

from .change_provenance import _actor, append_event
from .documents import DocumentStoreError


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _today() -> str:
    return date.today().isoformat()


CHECKS = ("confirmation", "notice", "attendance", "adjustments", "contact", "circumstances")
CAUSES = ("Resident", "Provider", "Cancelled", "Rescheduled", "Unknown")


class AppointmentCommittedError(RuntimeError):
    """The durable operation succeeded; reconcile rather than executing again."""


def mark_committed(store: Any) -> None:
    context = getattr(store.local, "procurement_validation", None)
    if context is not None:
        context["persisted"] = True


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 500:
        raise ValueError(f"Enter {label} (1 to 500 characters).")
    return value.strip()


def day(value: Any) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError, ValueError):
        raise ValueError("Enter a valid appointment date.") from None


def case_version(case: Any) -> str:
    return hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest()


class AppointmentMixin:
    def _active_appointment_outcomes(self: Any, cid: str) -> Any:
        outcomes = self._proc().get("appointment_outcomes", [])
        closures = self.cases[cid].get("home_case_closures", [])
        boundary = closures[-1]["outcome_boundary"] if closures else 0
        return [e for e in outcomes[boundary:] if e["case_id"] == cid]

    def _appointment_close_case(self: Any, actor: Any, w: Any, c: Any, b: Any) -> None:
        from .store import ConflictError

        if {"actor", "at", "version", "changes"} & b.keys():
            raise ValueError("The server records the human actor, decision time and history.")
        if b.get("case_id") != c["id"] or b.get("confirmed") is not True:
            raise ValueError("Explicitly confirm the supplied human closure of this home case.")
        if b.get("expected_case_version") != case_version(c):
            raise ConflictError(
                "The underlying home case changed. Reload before recording closure."
            )
        if c.get("closed") is not False:
            raise ValueError("This underlying home case is already closed or not evidenced active.")
        self.guard_case_event(c)
        source = text(b.get("source"), "the supplied human closure decision source")
        reason = text(b.get("reason"), "the human closure reason")
        source_version = text(b.get("source_version"), "the human decision source version")
        closures = c.get("home_case_closures", [])
        event = append_event(
            c,
            "home_case_closures",
            actor,
            "human_home_case_closed",
            source,
            case_id=c["id"],
            reason=reason,
            previous_closed=False,
            closed=True,
            expected_case_version=b["expected_case_version"],
            outcome_boundary=len(self._proc().get("appointment_outcomes", [])),
            event_ref=b["event_ref"],
            order=w["id"],
            investigation=deepcopy(self._proc().get("appointment_investigations", {}).get(c["id"])),
            previous_closure_version=len(closures),
        )
        event["source_version"] = source_version
        c["closed"] = True

    def _appointment_binding(self: Any, w: Any) -> Any:
        p, cur = self._package(w["package"]), w["versions"][-1]
        return deepcopy(
            dict(
                order=w["id"],
                case_id=w["case_id"],
                home=deepcopy(self.cases[w["case_id"]]["home"]),
                package=p["id"],
                scope=cur["scope"],
                scope_version=p["scope_version"],
                order_scope_version=cur["scope_version"],
                resident_bindings=cur.get("resident_bindings"),
                contract_ref=p["contract_ref"],
                contract_version=p["contract_version"],
                period_from=p["period_from"],
                period_to=p["period_to"],
            )
        )

    def _appointment_authority(self: Any, w: Any, offer: Any, ref: str) -> Any:
        authority = w.get("appointment_authorities", {}).get(ref)
        if (
            not authority
            or authority["revoked"]
            or authority["binding"] != offer["binding"]
            or authority["offer"] != offer["id"]
            or not authority["valid_from"] <= _today() <= authority["valid_to"]
            or not authority["valid_from"] <= offer["date"] <= authority["valid_to"]
        ):
            raise ValueError("Current appointment-specific representative authority is required.")
        return authority

    def appointment_status(self: Any, w: Any) -> Any:
        offer = w.get("appointment_offer")
        missing: list[str] = []
        if not offer:
            return dict(status="Unknown", missing=["No verified appointment offer"])
        if self.cases[w["case_id"]].get("closed") is not False:
            missing.append("Underlying home case is not evidenced active")
        if offer["binding"] != self._appointment_binding(w):
            missing.append("Home, scope, order or period changed")
        if offer["paused"] or offer["deferred"]:
            missing.append("Household pause or deferral")
        if offer.get("ended"):
            missing.append("Appointment ended; agree a new offer")
        for kind in ("resident", "staff", "capacity"):
            if kind not in offer["confirmations"]:
                missing.append(f"{kind.capitalize()} confirmation missing")
        resident = offer["confirmations"].get("resident")
        if resident and resident.get("representative_ref"):
            try:
                current = self._appointment_authority(w, offer, resident["representative_ref"])
                if current != resident["authority"]:
                    missing.append("Representative authority changed")
            except ValueError as error:
                missing.append(str(error))
        staff = offer["confirmations"].get("staff")
        if staff:
            try:
                actor = _actor(self, staff["actor"])
                authority = self._contract_authority(
                    actor, self._package(w["package"]), "appointment", w["contractor"]
                )
                if authority != staff["authority"]:
                    missing.append("Staff authority changed")
                context = getattr(self, "_proc_context", None)
                if context is not None:
                    context["authorities"].append(
                        (
                            actor,
                            deepcopy(self._package(w["package"])),
                            "appointment",
                            w["contractor"],
                            authority,
                        )
                    )
            except (PermissionError, ValueError):
                missing.append("Staff authority is no longer current")
        capacity = offer["confirmations"].get("capacity")
        if capacity:
            try:
                current = self._existing_capacity(w, offer["date"])
                if current != capacity["commitment"]:
                    missing.append("Contractor capacity confirmation changed")
            except (ValueError, PermissionError, DocumentStoreError) as error:
                missing.append(str(error))
        return dict(status="Offer" if missing else "Committed", missing=missing)

    def require_appointment_commitment(self: Any, w: Any) -> None:
        result = self.appointment_status(w)
        if result["status"] != "Committed":
            raise ValueError("Appointment is not committed: " + "; ".join(result["missing"]))

    def appointment_control(self: Any, user: Any, wid: str, body: Any) -> Any:
        if not isinstance(body, dict) or "status" in body:
            raise ValueError("Supply an appointment action, not a client commitment status.")
        with self._proc_operation(user, "appointment", wid=wid) as actor:
            w = self._work_order(wid)
            c = self._case(w["case_id"])
            if hasattr(self, "db"):
                self._proc_context["cases"][c["id"]] = self._rv[c["id"]]
            action = body.get("action")
            ref = text(body.get("event_ref"), "a unique event reference")
            events = w.setdefault("appointment_events", [])
            previous = next((e for e in events if e["ref"] == ref), None)
            if previous:
                if previous["body"] != body or previous["actor"] != actor:
                    raise ValueError("Event reference already used with different evidence.")
                return deepcopy(previous)
            if action == "offer":
                self._appointment_offer(actor, w, c, body, ref)
            elif action == "authority":
                self._appointment_grant(actor, w, body)
            elif action == "confirm":
                self._appointment_confirm(actor, w, body)
            elif action == "outcome":
                self._appointment_outcome(actor, w, c, body, ref)
            elif action == "close_case":
                self._appointment_close_case(actor, w, c, body)
            elif action == "configure":
                threshold = body.get("threshold")
                if type(threshold) is not int or not 0 <= threshold <= 100000:
                    raise ValueError("Threshold must be a nonnegative whole number.")
                configs = self._proc().setdefault("appointment_configurations", [])
                configs.append(
                    dict(
                        version=len(configs) + 1,
                        threshold=threshold,
                        basis=text(body.get("basis"), "the configuration evidence"),
                        actor=actor,
                        at=_now(),
                        provisional=True,
                    )
                )
            elif action == "investigation":
                investigation = self._proc().get("appointment_investigations", {}).get(c["id"])
                if not investigation or investigation.get("closure_version", 0) != len(
                    c.get("home_case_closures", [])
                ):
                    raise ValueError("No human investigation exists for this home case.")
                checks = body.get("checks")
                if not isinstance(checks, dict) or set(checks) != set(CHECKS):
                    raise ValueError("Record all human checks as evidence or explicit Unknown.")
                investigation.setdefault("history", []).append(
                    dict(
                        actor=actor,
                        at=_now(),
                        checks={k: text(checks[k], k + " evidence or Unknown") for k in CHECKS},
                        corrective_action=text(body.get("corrective_action"), "corrective action"),
                        next_update=text(body.get("next_update"), "the next resident update"),
                        disposition=text(body.get("disposition"), "the task disposition"),
                    )
                )
            else:
                raise ValueError(
                    "Choose offer, authority, confirm, outcome, configure, investigation "
                    "or close_case."
                )
            event = dict(ref=ref, body=deepcopy(body), actor=actor, at=_now())
            events.append(event)
            self._proc_save(actor, "appointment_" + action, c["id"], f"{wid}: {ref}")
            return deepcopy(event)

    def _appointment_offer(self: Any, actor: Any, w: Any, c: Any, b: Any, ref: str) -> None:
        if w["state"] not in ("Issued", "Appointed") or c.get("closed") is not False:
            raise ValueError("Offer an appointment only for an open order and active home case.")
        update = c.get("resident_update") or {}
        if not update.get("version") or not update.get("owner_identity"):
            raise ValueError(
                "Record a named resident-update commitment using resident services first."
            )
        options = b.get("options")
        if not isinstance(options, list) or not options:
            raise ValueError("Record the household options offered.")
        when = day(b.get("date"))
        p = self._package(w["package"])
        if not p["period_from"] <= when <= p["period_to"]:
            raise ValueError("The offer date must be within the package period.")
        for key in ("paused", "deferred", "bundle"):
            if type(b.get(key)) is not bool:
                raise ValueError(f"Record {key} explicitly.")
        bundle = b["bundle"]
        if bundle and (
            b.get("bundle_agreed") is not True
            or not isinstance(b.get("competence"), dict)
            or b["competence"].get("scope") != self._appointment_binding(w)
            or not b["competence"].get("source")
        ):
            raise ValueError(
                "A bundle needs explicit resident agreement and scope-bound competence evidence."
            )
        old = w.get("appointment_offer")
        if b.get("expected_offer_id") != (old["id"] if old else None):
            raise ValueError("The appointment offer changed. Reload before replacing it.")
        if old:
            w.setdefault("appointment_offer_history", []).append(deepcopy(old))
        w["appointment_offer"] = dict(
            id=ref,
            binding=self._appointment_binding(w),
            date=when,
            period=text(b.get("period"), "the visit period"),
            options=[text(v, "an offered option") for v in options],
            constraints=text(b.get("constraints"), "household constraints or Unknown"),
            instructions=text(b.get("instructions"), "necessary provider instructions or Unknown"),
            paused=b["paused"],
            deferred=b["deferred"],
            bundle=bundle,
            bundle_agreed=b.get("bundle_agreed") is True,
            competence=deepcopy(b.get("competence")),
            update_owner=deepcopy(update["owner_identity"]),
            resident_update_version=update["version"],
            confirmations={},
            actor=actor,
            at=_now(),
        )
        if w["state"] == "Appointed":
            self._wo_move(w, "Issued", actor, "New offer needs new appointment agreement")

    def _appointment_grant(self: Any, actor: Any, w: Any, b: Any) -> None:
        offer = w.get("appointment_offer")
        if not offer or b.get("offer_id") != offer["id"]:
            raise ValueError("Record authority against the current specific appointment offer.")
        ref = text(b.get("representative_ref"), "the representative reference")
        start, end = day(b.get("valid_from")), day(b.get("valid_to"))
        if start > end or type(b.get("revoked")) is not bool:
            raise ValueError("Record a valid authority period and explicit revocation state.")
        w.setdefault("appointment_authorities", {})[ref] = dict(
            representative=text(b.get("person"), "the authorized representative"),
            source=text(b.get("source"), "appointment-specific authority evidence"),
            task="Appointment agreement",
            binding=deepcopy(offer["binding"]),
            offer=offer["id"],
            valid_from=start,
            valid_to=end,
            revoked=b["revoked"],
            actor=actor,
            at=_now(),
        )

    def _appointment_confirm(self: Any, actor: Any, w: Any, b: Any) -> None:
        if (
            w["state"] not in ("Issued", "Appointed")
            or self.cases[w["case_id"]].get("closed") is not False
        ):
            raise ValueError("Confirm only an open order in an evidenced active home case.")
        offer = w.get("appointment_offer")
        if not offer or b.get("offer_id") != offer["id"]:
            raise ValueError("Confirm the current specific appointment offer.")
        if offer["binding"] != self._appointment_binding(w):
            raise ValueError("Scope changed. Record a new offer.")
        kind = b.get("kind")
        if kind not in ("resident", "staff", "capacity"):
            raise ValueError("Choose resident, staff or capacity confirmation.")
        evidence = dict(
            source=text(b.get("source"), "the confirmation source"),
            channel=text(b.get("channel"), "the confirmation channel, including manual routes"),
            person=text(b.get("person"), "the confirming person"),
            actor=actor,
            at=_now(),
            offer=offer["id"],
        )
        if kind == "resident":
            representative = b.get("representative_ref")
            if representative:
                authority = self._appointment_authority(w, offer, representative)
                if evidence["person"] != authority["representative"]:
                    raise ValueError(
                        "The confirming person differs from the authorized representative."
                    )
                evidence.update(representative_ref=representative, authority=deepcopy(authority))
            elif evidence["person"] != self.cases[w["case_id"]]["resident"]["name"]:
                raise ValueError(
                    "Record the resident or an explicitly authorized appointment representative."
                )
        elif kind == "staff":
            if evidence["person"] != actor["name"]:
                raise ValueError(
                    "The currently authorized staff member must confirm their own action."
                )
            evidence["authority"] = deepcopy(self._proc_context["authority"])
        else:
            evidence["commitment"] = deepcopy(self._existing_capacity(w, offer["date"]))
        offer["confirmations"][kind] = evidence
        if self.appointment_status(w)["status"] == "Committed":
            self.require_safety_clear(self.cases[w["case_id"]])
            self._resident_work_order_clear(w)
            self.require_building_clear(self.cases[w["case_id"]], w["package"])
            if w["state"] == "Issued":
                self._wo_move(w, "Appointed", actor, "Three scoped appointment confirmations")

    def _appointment_outcome(self: Any, actor: Any, w: Any, c: Any, b: Any, ref: str) -> None:
        cause = b.get("cause")
        if cause not in CAUSES:
            raise ValueError("Choose the evidenced cause, or Unknown.")
        for key in ("verified", "no_access", "preference_breach", "abortive"):
            if type(b.get(key)) is not bool:
                raise ValueError(f"Record {key} explicitly; do not infer no-access.")
        offer = w.get("appointment_offer")
        if not offer or b.get("offer_id") != offer["id"]:
            raise ValueError("Record the outcome against the specific current offer.")
        commitment = self.appointment_status(w)
        owner = text(b.get("owner"), "the cause owner or Unknown")
        configs = self._proc().get("appointment_configurations", [])
        config = configs[-1] if configs else dict(version=0, threshold=5, provisional=True)
        eligible = (
            cause == "Resident"
            and b["verified"]
            and b["no_access"]
            and commitment["status"] == "Committed"
            and c.get("closed") is False
            and w["state"] == "Appointed"
        )
        outcomes = self._proc().setdefault("appointment_outcomes", [])
        if any(e["ref"] == ref for e in outcomes):
            raise ValueError("Outcome event reference was already consumed by another order.")
        if any(e["order"] == w["id"] and e["offer"] == offer["id"] for e in outcomes):
            raise ValueError(
                "This visit already has an outcome. Do not recount the same appointment."
            )
        outcomes.append(
            dict(
                ref=ref,
                case_id=c["id"],
                order=w["id"],
                offer=offer["id"],
                cause=cause,
                owner=owner,
                verified=b["verified"],
                no_access=b["no_access"],
                preference_breach=b["preference_breach"],
                abortive=b["abortive"],
                source=text(b.get("source"), "the verification source or Unknown"),
                commitment=deepcopy(commitment),
                agreement=deepcopy(offer),
                eligible=eligible,
                configuration=deepcopy(config),
                actor=actor,
                at=_now(),
            )
        )
        active = self._active_appointment_outcomes(c["id"])
        count = sum(e["eligible"] for e in active)
        investigations = self._proc().setdefault("appointment_investigations", {})
        epoch = len(c.get("home_case_closures", []))
        if (
            eligible
            and count > config["threshold"]
            and (
                c["id"] not in investigations
                or investigations[c["id"]].get("closure_version", 0) != epoch
            )
        ):
            investigations[c["id"]] = dict(
                owner=deepcopy((c.get("resident_update") or {}).get("owner_identity")),
                case_id=c["id"],
                events=[e["ref"] for e in active if e["eligible"]],
                closure_version=epoch,
                configuration=deepcopy(config),
                history=[],
                at=_now(),
                next_action="Human investigation only; no consent or priority consequence",
            )
        offer["ended"] = True
        if w["state"] == "Appointed":
            self._wo_move(w, "Issued", actor, "Appointment outcome recorded")

    def appointment_summary(self: Any, w: Any, provider: bool) -> Any:
        offer = w.get("appointment_offer")
        result = self.appointment_status(w)
        if provider:
            return dict(
                **result,
                date=offer["date"] if offer else None,
                period=offer["period"] if offer else None,
                instructions=offer["instructions"] if offer else "Unknown",
            )
        outcomes = [
            e for e in self._proc().get("appointment_outcomes", []) if e["case_id"] == w["case_id"]
        ]
        c = self.cases[w["case_id"]]
        closures = c.get("home_case_closures", [])
        investigation = self._proc().get("appointment_investigations", {}).get(w["case_id"])
        if investigation and investigation.get("closure_version", 0) != len(closures):
            investigation = None
        totals: dict[str, Any] = {"preference_breach": {}, "abortive": {}}
        for event in outcomes:
            for fact in totals:
                if event[fact]:
                    key = event["cause"] + " / " + event["owner"]
                    totals[fact][key] = totals[fact].get(key, 0) + 1
        return dict(
            **result,
            offer=deepcopy(offer),
            current_update_owner=deepcopy(
                (self.cases[w["case_id"]].get("resident_update") or {}).get("owner_identity")
            ),
            current_binding=self._appointment_binding(w),
            eligible_no_access=sum(
                e["eligible"] for e in self._active_appointment_outcomes(w["case_id"])
            ),
            counts=totals,
            reporting_threshold="Unknown",
            case_reset=(
                "Only an explicitly recorded human underlying home-case closure "
                "resets the active count."
            ),
            case_id=c["id"],
            case_closed=c.get("closed"),
            case_version=case_version(c),
            closure_history=deepcopy(closures),
            investigation=deepcopy(investigation),
        )
