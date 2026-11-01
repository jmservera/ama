"""Bounded learning record of synthetic demo chat turns, kept in a local SQLite file.

Synthetic demo only. It stores the question text because every resident here is synthetic.
Real-resident use needs DPO and Legal approval first (#163 is deferred). It never stores the
resident identity, case id, email or answer text.

Operator summary: python -m zava_forward.api.resident_demo.chat_log summary PATH
"""

import argparse
import hashlib
import re
import sqlite3
import sys
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

SCHEMA_VERSION = 521
MAX_ROWS = 2000
RETENTION_SECONDS = 14 * 24 * 3600
MAX_QUESTION = 200
UNROUTED = ("unrouted", "refused")
NOTICE = (
    "Synthetic demo only: questions you type may be saved, without your name or email, to "
    "improve this chat. Only emails, postcodes and long numbers are masked, so do not type "
    "names, addresses or other real personal details."
)

_REDACTIONS = (
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[email]"),
    (re.compile(r"\b[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}\b", re.I), "[postcode]"),
    (re.compile(r"\bzf-?\w*\d\w*\b", re.I), "[case]"),
    (re.compile(r"\+?\d[\d\s\-()]{4,}\d"), "[number]"),
)


def clean(question: str) -> str:
    """Bound the text and mask obvious contact details a resident might paste in."""
    text = " ".join(question.split())
    for pattern, mask in _REDACTIONS:
        text = pattern.sub(mask, text)
    return text[:MAX_QUESTION]


def pseudonym(session_id: str) -> str:
    """One-way id for a sign-in session; it cannot be linked back to a resident."""
    return hashlib.sha256(b"chat-learning|" + session_id.encode()).hexdigest()[:12]


class ChatLog:
    def __init__(self, path: Path):
        if not path.is_absolute() or path.is_symlink():
            raise ValueError("Use an absolute local file path that is not a symbolic link.")
        self.path = path
        if not path.exists():
            with path.open("xb"):
                path.chmod(0o600)
            with self._transaction() as db:
                db.executescript(
                    f"""
                    PRAGMA user_version={SCHEMA_VERSION};
                    CREATE TABLE turns(
                      id INTEGER PRIMARY KEY, at REAL NOT NULL, session TEXT NOT NULL,
                      topic TEXT NOT NULL, ai INTEGER NOT NULL, question TEXT NOT NULL);
                    CREATE INDEX turns_topic ON turns(topic);
                    """
                )
        with self._transaction() as db:
            if db.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
                raise ValueError("This is not a synthetic chat learning record.")

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path.as_uri() + "?mode=rw", uri=True, timeout=5)
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def record(
        self, now: datetime, session_id: str, topic: str, ai_enabled: bool, question: str
    ) -> None:
        """Add one turn, then drop expired rows and anything beyond the row cap."""
        with self._transaction() as db:
            db.execute(
                "INSERT INTO turns(at,session,topic,ai,question) VALUES(?,?,?,?,?)",
                (
                    now.timestamp(),
                    pseudonym(session_id),
                    topic[:40],
                    int(ai_enabled),
                    clean(question),
                ),
            )
            db.execute("DELETE FROM turns WHERE at<?", (now.timestamp() - RETENTION_SECONDS,))
            db.execute(
                "DELETE FROM turns WHERE id NOT IN (SELECT id FROM turns ORDER BY id DESC LIMIT ?)",
                (MAX_ROWS,),
            )

    def summary(self, top: int = 10) -> dict[str, object]:
        """Counts by topic and the most common unrouted or refused phrasings."""
        with self._transaction() as db:
            rows = db.execute("SELECT topic, question FROM turns").fetchall()
        topics = Counter(topic for topic, _ in rows)
        phrasings: dict[str, Counter[str]] = {name: Counter() for name in UNROUTED}
        for topic, question in rows:
            if topic in phrasings and question:
                phrasings[topic][" ".join(re.findall(r"[\w'\[\]]+", question.lower()))] += 1
        return {
            "turns": len(rows),
            "topics": dict(topics.most_common()),
            "unrouted": topics["unrouted"],
            "refused": topics["refused"],
            "top_unrouted": phrasings["unrouted"].most_common(top),
            "top_refused": phrasings["refused"].most_common(top),
        }


def render(summary: dict[str, object]) -> str:
    """Plain-language summary for the team that improves the chat."""
    lines = [
        "Resident chat learning summary (synthetic demo only)",
        f"Questions saved: {summary['turns']}",
        f"Not understood (unrouted): {summary['unrouted']}",
        f"Declined (refused): {summary['refused']}",
        "",
        "Questions by topic:",
    ]
    topics = summary["topics"]
    assert isinstance(topics, dict)
    lines += [f"  {name}: {count}" for name, count in topics.items()] or ["  none yet"]
    for title, key in (
        ("Most common not-understood questions:", "top_unrouted"),
        ("Most common declined questions:", "top_refused"),
    ):
        lines += ["", title]
        entries = summary[key]
        assert isinstance(entries, list)
        lines += [f"  {count} x {text}" for text, count in entries] or ["  none yet"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarise the synthetic chat learning record.")
    parser.add_argument("command", choices=("summary",))
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        if not args.path.is_file():
            raise ValueError("missing file")
        print(render(ChatLog(args.path.resolve()).summary()))
    except (ValueError, sqlite3.Error, OSError) as error:
        print(f"Cannot read the chat learning record: {type(error).__name__}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
