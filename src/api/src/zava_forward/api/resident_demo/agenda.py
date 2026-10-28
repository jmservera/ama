"""Explicitly local synthetic callback inventory, never operational works appointments."""

import argparse
import secrets
import sqlite3
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("Europe/London")
NOTICE = (
    "Synthetic callback only. Nobody will call you. This is not a works booking "
    "or consent to works. Operational appointments and works consent are not available here."
)
MANUAL = (
    "To book or cancel with a person, phone your housing officer using your usual number, "
    "or write to or visit your local office. Quote the callback reference if you have one."
)


class AgendaConflict(ValueError):
    """A proposal or booking is no longer available."""


class Agenda:
    def __init__(self, path: Path):
        if not path.is_absolute() or path.is_symlink() or not path.is_file():
            raise ValueError("Use an existing absolute local synthetic agenda file.")
        self.path = path
        with self._transaction() as db:
            if db.execute("PRAGMA user_version").fetchone()[0] != 520:
                raise ValueError("This is not a synthetic callback agenda.")

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path.as_uri() + "?mode=rw", uri=True, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @classmethod
    def create(cls, path: Path, slots: Sequence[tuple[datetime, datetime]]) -> "Agenda":
        """Operator/test setup only; never called implicitly by the HTTP service."""
        ordered = sorted(slots)
        for index, (start, end) in enumerate(ordered):
            if (
                start.utcoffset() is None
                or end.utcoffset() is None
                or end <= start
                or (index and start < ordered[index - 1][1])
            ):
                raise ValueError("Supply aware, positive, non-overlapping callback slots.")
        with path.open("xb"):
            path.chmod(0o600)
        db = sqlite3.connect(path)
        try:
            db.executescript(
                """
                PRAGMA user_version=520;
                CREATE TABLE slots(
                  id INTEGER PRIMARY KEY, starts REAL NOT NULL, ends REAL NOT NULL);
                CREATE TABLE offers(
                  token TEXT PRIMARY KEY, owner TEXT NOT NULL, slot INTEGER NOT NULL,
                  expires REAL NOT NULL);
                CREATE TABLE bookings(
                  reference TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, owner TEXT NOT NULL,
                  slot INTEGER NOT NULL, cancelled INTEGER NOT NULL DEFAULT 0);
                CREATE UNIQUE INDEX free_slot ON bookings(slot) WHERE cancelled=0;
                CREATE UNIQUE INDEX one_callback ON bookings(owner) WHERE cancelled=0;
                """
            )
            db.executemany(
                "INSERT INTO slots(starts,ends) VALUES(?,?)",
                [(s.timestamp(), e.timestamp()) for s, e in ordered],
            )
            db.commit()
        finally:
            db.close()
        return cls(path)

    @staticmethod
    def _slot(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "start": datetime.fromtimestamp(row["starts"], UTC).isoformat(),
            "end": datetime.fromtimestamp(row["ends"], UTC).isoformat(),
            "time_zone": "Europe/London",
        }

    def find(
        self,
        owner: str,
        now: datetime,
        earliest: str,
        period: str,
        authorised: Callable[[], bool],
    ) -> list[dict[str, Any]]:
        try:
            first = date.fromisoformat(earliest)
        except (ValueError, TypeError):
            raise ValueError("Choose a valid earliest callback date.") from None
        if period not in ("any", "morning", "afternoon"):
            raise ValueError("Choose any time, morning or afternoon.")
        if (
            not now.astimezone(ZONE).date()
            <= first
            <= now.astimezone(ZONE).date() + timedelta(days=90)
        ):
            raise ValueError("Choose a date from today to 90 days ahead.")
        with self._transaction() as db:
            db.execute("DELETE FROM offers WHERE expires<=?", (now.timestamp(),))
            db.execute("DELETE FROM offers WHERE owner=?", (owner,))
            rows = db.execute(
                "SELECT s.* FROM slots s WHERE starts>? AND NOT EXISTS "
                "(SELECT 1 FROM bookings b WHERE b.slot=s.id AND b.cancelled=0) "
                "ORDER BY starts,id",
                (now.timestamp(),),
            )
            found = []
            for row in rows:
                local = datetime.fromtimestamp(row["starts"], ZONE)
                if (
                    local.date() < first
                    or (period == "morning" and local.hour >= 12)
                    or (period == "afternoon" and local.hour < 12)
                ):
                    continue
                token = secrets.token_urlsafe(24)
                db.execute(
                    "INSERT INTO offers VALUES(?,?,?,?)",
                    (token, owner, row["id"], (now + timedelta(minutes=10)).timestamp()),
                )
                found.append(dict(self._slot(row), proposal=token))
                if len(found) == 3:
                    break
            if not authorised():
                raise PermissionError("Please sign in again.")
            return found

    def own(self, owner: str) -> list[dict[str, Any]]:
        with self._transaction() as db:
            rows = db.execute(
                "SELECT s.*,b.reference FROM bookings b JOIN slots s ON s.id=b.slot "
                "WHERE b.owner=? AND b.cancelled=0 ORDER BY starts,s.id",
                (owner,),
            )
            return [dict(self._slot(row), reference=row["reference"]) for row in rows]

    def book(
        self,
        owner: str,
        proposal: str,
        now: datetime | Callable[[], datetime],
        authorised: Callable[[], bool],
    ) -> dict[str, Any]:
        with self._transaction() as db:
            instant = now() if callable(now) else now
            previous = db.execute(
                "SELECT s.*,b.reference,b.cancelled FROM bookings b JOIN slots s ON s.id=b.slot "
                "WHERE b.owner=? AND b.token=?",
                (owner, proposal),
            ).fetchone()
            if previous is not None:
                if not authorised():
                    raise PermissionError("Please sign in again.")
                if previous["cancelled"]:
                    raise AgendaConflict("This callback was cancelled. Find a new time.")
                return dict(self._slot(previous), reference=previous["reference"])
            row = db.execute(
                "SELECT s.* FROM offers o JOIN slots s ON s.id=o.slot "
                "WHERE o.token=? AND o.owner=? AND o.expires>? AND s.starts>?",
                (proposal, owner, instant.timestamp(), instant.timestamp()),
            ).fetchone()
            if row is None:
                raise AgendaConflict("This proposed time has ended. Find a new time.")
            reference = secrets.token_urlsafe(16)
            try:
                db.execute(
                    "INSERT INTO bookings(reference,token,owner,slot) VALUES(?,?,?,?)",
                    (reference, proposal, owner, row["id"]),
                )
            except sqlite3.IntegrityError:
                raise AgendaConflict(
                    "This time is no longer free, or you already have a callback. "
                    "Check your callbacks, then find another time."
                ) from None
            if not authorised():
                raise PermissionError("Please sign in again.")
            if row["starts"] <= (now() if callable(now) else now).timestamp():
                raise AgendaConflict("This proposed time has ended. Find a new time.")
            return dict(self._slot(row), reference=reference)

    def cancel(self, owner: str, reference: str, authorised: Callable[[], bool]) -> None:
        with self._transaction() as db:
            row = db.execute(
                "SELECT 1 FROM bookings WHERE owner=? AND reference=?",
                (owner, reference),
            ).fetchone()
            if row is None:
                raise AgendaConflict("This callback is not available. Ask your housing officer.")
            db.execute(
                "UPDATE bookings SET cancelled=1 WHERE owner=? AND reference=?",
                (owner, reference),
            )
            if not authorised():
                raise PermissionError("Please sign in again.")

    def assisted_cancel(self, reference: str) -> None:
        """Local operator with file access; never exposed as resident HTTP authority."""
        with self._transaction() as db:
            row = db.execute(
                "SELECT owner FROM bookings WHERE reference=?",
                (reference,),
            ).fetchone()
            if row is None:
                raise AgendaConflict("Callback reference not found.")
            db.execute("UPDATE bookings SET cancelled=1 WHERE reference=?", (reference,))


def main() -> None:
    parser = argparse.ArgumentParser(description=NOTICE)
    parser.add_argument("path", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--seed-from", type=date.fromisoformat)
    actions.add_argument("--cancel")
    parser.add_argument("--verified-synthetic-request", action="store_true")
    args = parser.parse_args()
    if not args.path.is_absolute():
        parser.error("Use an absolute local path.")
    if args.seed_from:
        slots = []
        for offset in range(7):
            day = args.seed_from + timedelta(days=offset)
            if day.weekday() < 5:
                for hour in (9, 11, 14):
                    start = datetime(day.year, day.month, day.day, hour, tzinfo=ZONE)
                    slots.append((start, start + timedelta(minutes=30)))
        Agenda.create(args.path, slots)
        print("Created synthetic callback inventory. " + NOTICE)
    else:
        if not args.verified_synthetic_request:
            parser.error("Verify the synthetic resident's cancellation request first.")
        Agenda(args.path).assisted_cancel(args.cancel)
        print("Synthetic callback cancelled. No live service was contacted.")


if __name__ == "__main__":
    main()
