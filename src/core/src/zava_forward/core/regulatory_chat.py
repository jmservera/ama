"""API-owned synthetic retrieval and isolated chat persistence; no inference or rule writes."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote

from zava_forward.core import projection
from zava_forward.core.chat_isolation import ChatForbidden, ChatIsolation
from zava_forward.core.chat_privacy import redact
from zava_forward.core.chatthreads import MAX_CONTENT, ChatNotFound, user_key
from zava_forward.core.rule_engine import citation_eligibility

TASK = "regulatory-home-chat"
SCHEMA = "regulatory-chat-v1"
OWNER = "Juan Manuel Servera"
MARKER = "synthetic-demo"
HAZARD_ROLES = (
    "Building Safety Liaison",
    "Resident Liaison Officer",
    "Retrofit Programme Manager",
)


def encode(value: dict[str, Any]) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    if len(text) > MAX_CONTENT:
        raise ValueError("Cited turn exceeds the storage bound; narrow the question.")
    return text


class RegulatoryChat:
    def __init__(
        self,
        isolation: ChatIsolation,
        law: Any,
        render: Callable[[dict[str, Any]], dict[str, Any]],
        classify: Callable[[str], str | None],
        refuse: Callable[[str], str | None],
        env: Any = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.iso, self.store, self.law = isolation, isolation.store, law
        self.render, self.classify, self.refuse = render, classify, refuse
        self.env = os.environ if env is None else env
        self.clock = clock or (lambda: datetime.now(UTC))

    def admit(self, user: dict[str, Any]) -> dict[str, Any]:
        marker = self.store.data.get("regulatory_chat_exercise")
        if hasattr(self.store, "assistant_connection"):
            with self.store.dblock:
                row = self.store.db.execute(
                    "SELECT value FROM meta WHERE key=?", ("regulatory_chat_exercise",)
                ).fetchone()
                person = self.store.db.execute(
                    "SELECT body FROM staff WHERE email=?", (user_key(user),)
                ).fetchone()
            marker = row[0] if row else None
            if not person:
                raise ChatForbidden("The staff principal is no longer provisioned.")
            user = json.loads(person[0])
        if (
            self.env.get("ZF_REGULATORY_CHAT") != MARKER
            or marker != MARKER
            or self.env.get("ZF_ENV", "test") not in ("test", "development")
        ):
            raise ChatForbidden(
                "Regulatory chat is restricted to an enabled synthetic-demo dataset."
            )
        for key in ("CHAT_DPIA_REF", "CHAT_LAWFUL_BASIS_REF", "CHAT_NOTICE_REF"):
            if not str(self.iso.env.get(key, "")).startswith("SYNTH-"):
                raise ChatForbidden(
                    "Synthetic-demo chat needs explicitly simulated privacy references."
                )
        self.iso.privacy._require()
        if hasattr(self.store, "assistant_connection"):
            if not projection.allowed(user, "chat"):
                raise ChatForbidden("The current staff role does not include chat.")
            return dict(user)
        return dict(self.iso.current_user(user))

    def thread(self, user: dict[str, Any], tid: str) -> tuple[dict[str, Any], dict[str, Any]]:
        user = self.admit(user)
        thread = self.store.chat_resume(user, tid)
        if not thread["title"].startswith(TASK + ":") or thread["owner_role"] != user["role"]:
            raise ChatForbidden("The current role cannot read this regulatory thread.")
        detail = self.store.detail(thread["case_id"], user)
        if detail is None:
            raise ChatNotFound(thread["case_id"])
        return user, thread

    def start(self, user: dict[str, Any], case_id: str) -> str:
        user = self.admit(user)
        if not case_id or self.store.detail(case_id, user) is None:
            raise ChatNotFound(case_id)
        row = self.store.chat_create_thread(
            user, case_id=case_id, title=TASK + ": synthetic-demo", model="offline-extractive"
        )
        return str(row["id"])

    def history(self, user: dict[str, Any], tid: str) -> dict[str, Any]:
        _, thread = self.thread(user, tid)
        return thread

    def _fact(self, cid: str, path: str, value: str, at: str) -> dict[str, Any]:
        digest = hashlib.sha256(f"{path}:{value}:{at}".encode()).hexdigest()[:16]
        return dict(
            id=f"{cid}/{path}@{digest}",
            text=f"{path}: {value}",
            status="recorded-synthetic-demo",
            effective=None,
            retrieved=at,
            observed_at=at,
            version=digest,
            case_id=cid,
            provenance="Role-projected case snapshot; effective date unknown",
            exercise=True,
        )

    def bundle(self, user: dict[str, Any], cid: str, question: str) -> dict[str, Any]:
        """Minimise after the normal server projection; never retrieve memory or private notes."""
        at = self.clock().isoformat(timespec="seconds")
        day = at[:10]
        kind = self.classify(question)
        result: dict[str, Any] = dict(
            sources=[], facts=[], cards=[], as_of=at, conflict=False, refusal=self.refuse(question)
        )
        if result["refusal"] or self.law is None:
            return result
        detail = self.store.detail(cid, user)
        if detail is None:
            raise ChatNotFound(cid)
        sources: dict[str, Any] = {}
        signatures = set()
        with self.law.sql.lock:
            for latest_card in self.law.rules.cards():
                active = self.law.rules.is_active(latest_card["card_id"], day)
                if active is None:
                    continue
                card = next(
                    c
                    for c in self.law.rules.history(latest_card["card_id"])
                    if c["version"] == active
                )
                if (
                    not card["exercise"]
                    or not card["approved_by"]
                    or not card["check"]
                    or card["check"]["kind"] != kind
                ):
                    continue
                _, eligible = citation_eligibility(self.law, card, day)
                if eligible != "active":
                    # A newer version is evidence of doubt, not authority to apply the old card.
                    changed = []
                    for pid in card["provisions"]:
                        try:
                            old = self.law.provision(pid)
                        except KeyError:
                            continue
                        current = self.law.source(old["source_id"])
                        if old["version"] != current["versions"][0]["version"]:
                            changed.append(old)
                            for p in current["provisions"]:
                                if p["ordinal"] == old["ordinal"]:
                                    changed.append(self.law.provision(p["id"]))
                    if changed:
                        result["conflict"] = True
                        for p in changed:
                            sources[p["id"]] = self._source(p)
                    continue
                if len(result["cards"]) >= 2 or len(sources) + len(card["provisions"]) > 4:
                    result["refusal"] = (
                        "Too many relevant sources; narrow the lookup for human review."
                    )
                    break
                result["cards"].append(
                    dict(
                        id=f"{card['card_id']}@v{active}",
                        status=card["state"],
                        approved_by=card["approved_by"],
                        approved_on=card["approved_on"],
                        effective=card["effective"],
                        exercise=True,
                        link="/api/law/cards/" + quote(card["card_id"], safe=""),
                        safe_default=card["safe_default"],
                        clock=card["clock"],
                    )
                )
                signatures.add((card["safe_default"], card["clock"]))
                for pid in card["provisions"]:
                    sources[pid] = self._source(self.law.provision(pid))
        result["conflict"] |= len(signatures) > 1
        result["sources"] = list(sources.values())
        if len(sources) > 4:
            result["refusal"] = "Too many conflicting versions; ask the named owner."
        if result["sources"] and not result["conflict"] and kind == "hazard-awareness-clock":
            if user["role"] in HAZARD_ROLES:
                for i, hazard in enumerate(detail.get("hazards", [])[:2]):
                    for field, allowed in (
                        ("category", ("Damp", "Damp and mould", "Mould", "Emergency")),
                        ("priority", ("Emergency", "P1", "P2", "P3", "Routine")),
                    ):
                        value = hazard.get(field)
                        if value in allowed:
                            result["facts"].append(
                                self._fact(cid, f"hazards.{i}.{field}", value, at)
                            )
        if not result["facts"]:
            result["unknown"] = "No permitted structured home fact selected for this purpose."
        return result

    @staticmethod
    def _source(p: dict[str, Any]) -> dict[str, Any]:
        return dict(
            id=p["id"],
            text=p["text"][:350],
            status=p["status"],
            version=p["version"],
            effective=p["effective"],
            retrieved=p["retrieved"],
            hash=p["hash"],
            review_status=p["review_status"],
            completeness=p["completeness"],
            exercise=p["authority_type"] == "exercise",
            link="/api/law/provisions/" + quote(p["id"], safe=""),
            caveats=p["caveats"],
            excerpt_truncated=len(p["text"]) > 350,
            currentness="Local snapshot only; live currentness not verified.",
        )

    def ask(self, user: dict[str, Any], tid: str, question: object) -> dict[str, Any]:
        user, thread = self.thread(user, tid)
        if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1000:
            raise ValueError("Question must contain 1 to 1000 characters.")
        masked: str = redact(question.strip())[0]
        reply = self.render(self.bundle(user, thread["case_id"], masked))
        text = encode(reply)
        repo = self.store.chat_repo
        with self.store.lock:
            before = copy.deepcopy(self.store.data.get("chat_threads", {}))
            try:
                with repo.txn():
                    fresh = repo.get(tid, user_key(user))
                    if (
                        fresh is None
                        or fresh["status"] != "active"
                        or fresh["rowversion"] != thread["rowversion"]
                    ):
                        raise self.store._chat_conflict(tid)
                    now = self.clock().isoformat(timespec="milliseconds")
                    seq = fresh["message_count"] + 2
                    if not repo.update(
                        tid,
                        user_key(user),
                        fresh["rowversion"],
                        message_count=seq,
                        updated_at=now,
                    ):
                        raise self.store._chat_conflict(tid)
                    for role, content, number, refs in (
                        ("user", masked, seq - 1, []),
                        ("assistant", text, seq, [c["id"] for c in reply["citations"]]),
                    ):
                        repo.add_message(
                            dict(
                                thread_id=tid,
                                seq=number,
                                role=role,
                                content=content,
                                evidence=refs,
                                model="offline-extractive",
                                task_version="",
                                created_at=now,
                            )
                        )
                    repo.commit()
            except BaseException:
                if not hasattr(self.store, "assistant_connection"):
                    self.store.data["chat_threads"] = before
                raise
        self.store._chat_event(
            user, "chat.regulatory.turn", dict(thread, message_count=seq), turn=seq
        )
        return dict(reply, turn=seq)

    def _owner(self, sender: dict[str, Any], case_id: str) -> dict[str, Any]:
        staff = list(self.store.staff.values())
        if hasattr(self.store, "assistant_connection"):
            with self.store.dblock:
                staff = [
                    json.loads(row[0])
                    for row in self.store.db.execute("SELECT body FROM staff").fetchall()
                ]
        owners = [
            s for s in staff if " ".join(s.get("name", "").split()).casefold() == OWNER.casefold()
        ]
        if len(owners) != 1:
            raise ValueError(
                "Named synthetic-demo owner is missing or ambiguous; no turn was sent."
            )
        owner = self.admit(owners[0])
        if sender["role"] in HAZARD_ROLES and owner["role"] not in HAZARD_ROLES:
            raise ChatForbidden("The named owner's current role cannot read these hazard facts.")
        if case_id and self.store.detail(case_id, owner) is None:
            raise ChatNotFound(case_id)
        return owner

    def doubt(self, user: dict[str, Any], tid: str, seq: object) -> dict[str, Any]:
        user, thread = self.thread(user, tid)
        if type(seq) is not int:
            raise ValueError("Select one stored assistant turn.")
        messages = thread["messages"]
        selected = next((m for m in messages if m["seq"] == seq and m["role"] == "assistant"), None)
        question = next((m for m in messages if m["seq"] == seq - 1 and m["role"] == "user"), None)
        if selected is None or question is None:
            raise ValueError("Select one stored question and cited answer pair.")
        payload = json.loads(selected["content"])
        if payload.get("schema") != SCHEMA:
            raise ValueError("Only a stored cited turn can be referred.")
        owner = self._owner(user, thread["case_id"])
        repo = self.store.chat_repo
        # MemoryRepo only locks; preserve its pre-image as SQL rollback does.
        with self.store.lock:
            before = copy.deepcopy(self.store.data.get("chat_threads", {}))
            try:
                with repo.txn():
                    fresh = repo.get(tid, user_key(user))
                    if (
                        fresh is None
                        or fresh["status"] != "active"
                        or fresh["rowversion"] != thread["rowversion"]
                    ):
                        raise self.store._chat_conflict(tid)
                    for message in repo.messages(tid):
                        if message["role"] == "assistant":
                            try:
                                prior = json.loads(message["content"])
                            except ValueError:
                                continue
                            if prior.get("referred_turn") == seq:
                                return dict(prior)
                    now = self.clock().isoformat(timespec="milliseconds")
                    inbox_id = "CT-" + uuid.uuid4().hex[:16]
                    inbox = dict(
                        thread,
                        id=inbox_id,
                        owner=user_key(owner),
                        owner_role=owner["role"],
                        title=TASK + ": doubt inbox synthetic-demo",
                        rowversion=1,
                        message_count=2,
                        created_at=now,
                        updated_at=now,
                    )
                    inbox.pop("messages")
                    repo.insert_thread(inbox)
                    for i, original in enumerate((question, selected), 1):
                        repo.add_message(dict(original, thread_id=inbox_id, seq=i, created_at=now))
                    receipt = dict(
                        referred_turn=seq,
                        owner=OWNER,
                        label=MARKER,
                        status="sent-to-exercise-inbox",
                        inbox_thread=inbox_id,
                    )
                    if not repo.update(
                        tid,
                        user_key(user),
                        fresh["rowversion"],
                        message_count=fresh["message_count"] + 1,
                        updated_at=now,
                    ):
                        raise self.store._chat_conflict(tid)
                    repo.add_message(
                        dict(
                            thread_id=tid,
                            seq=fresh["message_count"] + 1,
                            role="assistant",
                            content=encode(receipt),
                            evidence=[],
                            model="offline-extractive",
                            task_version="",
                            created_at=now,
                        )
                    )
                    repo.commit()
            except BaseException:
                if not hasattr(self.store, "assistant_connection"):
                    self.store.data["chat_threads"] = before
                raise
        self.store._chat_event(
            user,
            "chat.regulatory.doubt",
            dict(thread, message_count=thread["message_count"] + 1),
            turn=seq,
        )
        return receipt

    def inbox(self, user: dict[str, Any]) -> dict[str, Any]:
        user = self.admit(user)
        owner = self._owner(user, "")
        if user_key(owner) != user_key(user):
            raise ChatForbidden("Only the named exercise owner can read this inbox.")
        threads = []
        for row in self.store.chat_list_threads(user):
            if row["title"] == TASK + ": doubt inbox synthetic-demo":
                threads.append(self.history(user, row["id"]))
        return dict(label=MARKER, owner=OWNER, threads=threads)
