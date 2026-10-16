"""Wholly constructed source, card, home and named-owner fixture; no real approval."""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core import lawstore, rulecards
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

NOW = datetime(2026, 10, 16, 12, tzinfo=UTC)
PID = "synthetic@v1#0001"
QUOTE = "Synthetic hazard reports go to a human reviewer; this fixture is not law."
ENV = dict(
    ZF_REGULATORY_CHAT="synthetic-demo",
    CHAT_DPIA_REF="SYNTH-DPIA",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB",
    CHAT_NOTICE_REF="SYNTH-NOTICE",
)


class Fixture:
    def __init__(self, root: str, *, sql: bool = False) -> None:
        self.root = Path(root)
        self.path = self.root / "synthetic.json"
        data: dict[str, Any] = copy.deepcopy(DATA)
        data["regulatory_chat_exercise"] = "synthetic-demo"
        data["staff"].append(
            dict(
                email="exercise-owner@example.test",
                name="Juan Manuel Servera",
                role="Building Safety Liaison",
                code="SYN-OWNER",
            )
        )
        data["cases"][0]["hazards"] = [
            dict(
                category="Damp and mould",
                priority="Emergency",
                owner="Juan Manuel Servera",
                noticed="2026-10-15",
                referred=None,
                repaired=None,
                job="SYN-JOB",
                source="PRIVATE-REPORT-CANARY",
                aware_at="2026-10-15T10:00:00Z",
                released=False,
                hold=dict(status="Active"),
            )
        ]
        data["cases"][0]["resident"]["adjustment"] = "PRIVATE-HEALTH-CANARY"
        self.path.write_text(json.dumps(data))
        self.sql = sql
        self.store: Any = self.open()
        if sql:
            self.store.db.execute(
                "INSERT INTO meta (key, value) VALUES (?,?)",
                ("regulatory_chat_exercise", "synthetic-demo"),
            )
        self.iso = ChatIsolation(self.store, env=ENV)
        self.user = self.store.staff["sam@example.test"]
        self.owner = self.store.staff["exercise-owner@example.test"]
        self.law: Any = lawstore.LawStore(str(self.root / "law.sqlite"), str(self.root / "blobs"))
        self.source()
        self.card()

    def open(self) -> Any:
        return (
            SqlStore(str(self.path), str(self.root / "state.sqlite"))
            if self.sql
            else Store(str(self.path))
        )

    def source(
        self,
        version: int = 1,
        *,
        status: str = "in_force",
        effective: str = "2026-01-01",
        reviewed: str = "reviewed",
        completeness: str = "full",
        text: str = QUOTE,
    ) -> None:
        with self.law.transaction():
            if version == 1:
                self.law.sql.run(
                    "INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        "synthetic",
                        "synthetic-demo source",
                        "https://example.test/source",
                        "exercise",
                        "exercise",
                        "Juan Manuel Servera",
                        "High",
                        "daily",
                        "none",
                    ),
                )
            self.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "synthetic",
                    version,
                    status,
                    effective,
                    "2026-10-16",
                    "2026-10-16",
                    reviewed,
                    lawstore.sha256(text.encode()),
                    "none",
                    "ok",
                    completeness,
                    None,
                ),
            )
            self.law.sql.run(
                "INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)",
                (
                    f"synthetic@v{version}#0001",
                    "synthetic",
                    version,
                    1,
                    "Synthetic hazard",
                    text,
                    lawstore.sha256(text.encode()),
                ),
            )

    def card(
        self,
        card_id: str = "synthetic-hazard",
        *,
        approve: bool = True,
        safe: str = "Ask the human hazard owner",
        pid: str = PID,
        kind: str = "hazard-awareness-clock",
    ) -> int:
        version: int = self.law.rules.propose(
            card_id,
            "synthetic-author@example.test",
            rulecards.AUTHOR,
            today="2026-10-16",
            title="synthetic-demo hazard",
            trigger="Synthetic hazard report",
            applicability="Synthetic homes only",
            provisions=[pid],
            clock="Fictional 48 hours",
            safe_default=safe,
            escalation_role="Exercise owner",
            approver="exercise-owner@example.test",
            effective="2026-01-01",
            check=(
                dict(kind=kind, hours=48, attention_hours=24)
                if kind == "hazard-awareness-clock"
                else dict(kind=kind)
            ),
        )
        if approve:
            self.law.rules.approve(
                card_id, version, "exercise-owner@example.test", rulecards.OWNER, "2026-10-16"
            )
            self.law.rules.activate(
                card_id, version, "exercise-owner@example.test", rulecards.OWNER, "2026-10-16"
            )
        return version

    def close(self) -> None:
        self.law.close()
        if self.sql:
            self.store.db.close()
