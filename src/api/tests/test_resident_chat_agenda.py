"""Constructed callback inventory only; no real records, SQL Server or model calls."""

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

from zava_forward.api.resident_demo.agenda import ZONE, Agenda, AgendaConflict

NOW = datetime(2026, 10, 25, 12, tzinfo=UTC)


class AgendaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "agenda.sqlite"
        self.starts = [datetime(2026, 10, 26, hour, tzinfo=ZONE) for hour in (14, 9, 12, 11, 16)]
        self.agenda = Agenda.create(
            self.path, [(s, s + timedelta(minutes=30)) for s in self.starts]
        )

    def find(self, owner: str = "one", period: str = "any") -> list[dict[str, object]]:
        return self.agenda.find(owner, NOW, "2026-10-25", period, lambda: True)

    def test_first_three_sorted_preferences_dates_and_match_counts(self) -> None:
        any_time = self.find()
        self.assertEqual(len(any_time), 3)
        self.assertEqual(
            [datetime.fromisoformat(str(s["start"])).hour for s in any_time], [9, 11, 12]
        )
        self.assertEqual(len(self.find(period="morning")), 2)
        self.assertEqual(len(self.find(period="afternoon")), 3)
        self.assertEqual(self.agenda.find("one", NOW, "2026-10-27", "any", lambda: True), [])
        for count in (0, 1, 2, 3):
            path = Path(self.temp.name) / f"count-{count}.sqlite"
            agenda = Agenda.create(
                path, [(s, s + timedelta(minutes=30)) for s in sorted(self.starts)[:count]]
            )
            self.assertEqual(len(agenda.find("one", NOW, "2026-10-25", "any", lambda: True)), count)

    def test_confirmation_is_persistent_idempotent_and_owner_bound(self) -> None:
        proposal = str(self.find()[0]["proposal"])
        self.assertEqual(self.agenda.own("one"), [])
        with self.assertRaises(AgendaConflict):
            self.agenda.book("two", proposal, NOW, lambda: True)
        booked = self.agenda.book("one", proposal, NOW, lambda: True)
        self.assertEqual(Agenda(self.path).own("one"), [booked])
        self.assertEqual(self.agenda.own("two"), [])
        self.assertEqual(self.agenda.book("one", proposal, NOW, lambda: True), booked)
        with self.assertRaises(AgendaConflict):
            self.agenda.cancel("two", booked["reference"], lambda: True)
        self.agenda.cancel("one", booked["reference"], lambda: True)
        self.agenda.cancel("one", booked["reference"], lambda: True)
        self.assertEqual(self.agenda.own("one"), [])
        with self.assertRaises(AgendaConflict):
            self.agenda.book("one", proposal, NOW, lambda: True)
        self.assertEqual(len(self.find()), 3)

    def test_racing_residents_cannot_double_book(self) -> None:
        offers = {owner: str(self.find(owner)[0]["proposal"]) for owner in ("one", "two")}

        def reserve(owner: str) -> str:
            try:
                self.agenda.book(owner, offers[owner], NOW, lambda: True)
            except AgendaConflict:
                return "conflict"
            return "booked"

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(reserve, offers)), ["booked", "conflict"])

    def test_expired_past_and_replaced_proposals_cannot_book(self) -> None:
        proposal = str(self.find()[0]["proposal"])
        with self.assertRaises(AgendaConflict):
            self.agenda.book("one", proposal, NOW + timedelta(minutes=10), lambda: True)
        self.find()
        with self.assertRaises(AgendaConflict):
            self.agenda.book("one", proposal, NOW, lambda: True)
        at_start = sorted(self.starts)[0]
        found = self.agenda.find(
            "one", at_start - timedelta(minutes=1), "2026-10-26", "any", lambda: True
        )
        with self.assertRaises(AgendaConflict):
            self.agenda.book("one", found[0]["proposal"], at_start, lambda: True)

    def test_revocation_rolls_back_find_book_and_cancel(self) -> None:
        with self.assertRaises(PermissionError):
            self.agenda.find("one", NOW, "2026-10-25", "any", lambda: False)
        proposal = str(self.find()[0]["proposal"])
        with self.assertRaises(PermissionError):
            self.agenda.book("one", proposal, NOW, lambda: False)
        self.assertEqual(self.agenda.own("one"), [])
        booked = self.agenda.book("one", proposal, NOW, lambda: True)
        with self.assertRaises(PermissionError):
            self.agenda.cancel("one", booked["reference"], lambda: False)
        self.assertEqual(self.agenda.own("one"), [booked])
        with self.assertRaises(AgendaConflict):
            self.agenda.assisted_cancel("unknown")
        self.agenda.assisted_cancel(booked["reference"])
        self.agenda.assisted_cancel(booked["reference"])
        self.assertEqual(Agenda(self.path).own("one"), [])

    def test_slot_becoming_past_during_confirmation_rolls_back(self) -> None:
        start = sorted(self.starts)[0]
        now = start - timedelta(seconds=1)
        offers = self.agenda.find("one", now, "2026-10-26", "any", lambda: True)
        times = iter((now, start))
        with self.assertRaises(AgendaConflict):
            self.agenda.book("one", offers[0]["proposal"], lambda: next(times), lambda: True)
        self.assertEqual(self.agenda.own("one"), [])

    def test_proposal_expiring_during_authorisation_rolls_back(self) -> None:
        expiry = NOW + timedelta(minutes=10)
        for offset in (-1, 0, 1):
            with self.subTest(microseconds_from_expiry=offset):
                path = Path(self.temp.name) / f"expiry-{offset}.sqlite"
                agenda = Agenda.create(path, [(s, s + timedelta(minutes=30)) for s in self.starts])
                proposal = agenda.find("one", NOW, "2026-10-25", "any", lambda: True)[0]["proposal"]
                clock = Mock(return_value=expiry - timedelta(seconds=1))
                confirmed_at = expiry + timedelta(microseconds=offset)

                def authorised(clock: Mock = clock, confirmed_at: datetime = confirmed_at) -> bool:
                    clock.return_value = confirmed_at
                    return True

                if offset < 0:
                    booked = agenda.book("one", proposal, clock, authorised)
                    self.assertEqual(Agenda(path).own("one"), [booked])
                    self.assertEqual(agenda.book("one", proposal, expiry, lambda: True), booked)
                else:
                    with self.assertRaisesRegex(AgendaConflict, "proposed time has ended"):
                        agenda.book("one", proposal, clock, authorised)
                    self.assertEqual(Agenda(path).own("one"), [])
                    other = agenda.find("two", confirmed_at, "2026-10-25", "any", lambda: True)[0]
                    self.assertEqual(
                        other["start"], sorted(self.starts)[0].astimezone(UTC).isoformat()
                    )
                    agenda.book("two", other["proposal"], confirmed_at, lambda: True)
                self.assertEqual(clock.return_value, confirmed_at)
                self.assertEqual(clock.call_count, 2)

    def test_invalid_filters_and_timezone_boundaries(self) -> None:
        for earliest, period in (
            ("yesterday", "any"),
            ("2026-10-24", "any"),
            ("2027-10-25", "any"),
            ("2026-10-25", "evening"),
        ):
            with self.assertRaises(ValueError):
                self.agenda.find("one", NOW, earliest, period, lambda: True)
        path = Path(self.temp.name) / "summer.sqlite"
        # 11 UTC is noon in London in summer, regardless of browser/host timezone.
        start = datetime(2026, 7, 1, 11, tzinfo=UTC)
        agenda = Agenda.create(path, [(start, start + timedelta(minutes=30))])
        now = start - timedelta(hours=2)
        self.assertEqual(agenda.find("one", now, "2026-07-01", "morning", lambda: True), [])
        self.assertEqual(len(agenda.find("one", now, "2026-07-01", "afternoon", lambda: True)), 1)
        with self.assertRaises(ValueError):
            Agenda.create(Path(self.temp.name) / "bad.sqlite", [(NOW, NOW)])


if __name__ == "__main__":
    unittest.main()
