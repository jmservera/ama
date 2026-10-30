"""Citations, workflow-only mode and the comparison record for every AI task.

Every material AI output (briefing, message, catch-me-up summary, funding
wording, document reading, priority recommendation) carries citations that
must resolve to a real field or record of the case. Citations are checked on
the server. Output whose citations do not resolve is marked Unverified, and
uncited priority items or summary bullets are dropped. Output stays
"Not reviewed" until a person accepts, edits or rejects it.

Each task also leaves one comparison record in the recommendation store (same
for the JSON and SQLite stores): the input case ids, the AI output, the
workflow-only output, why there was a fallback, and what the reviewer did.
"""
import hashlib
import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from . import projection, ai_prompts, export_fields
from .resident_decisions import resident_status
from .stock import support_status

PROMPT_VERSION = "2026-10-09.1"
CITE_RE = re.compile(r"\[\[(.+?)\]\]")
EMPTY_SOURCES = re.compile(r"(?im)^[ \t]*sources?[ \t]*:[\s;,]*$")
BULLET = re.compile(r"^\s*[-*\u2022]\s")
STATEMENT_END = r"""[.!?\u2026][.!?\u2026"'\u2019\u201d)\]}]*"""
STATEMENT_ABBREVIATION = re.compile(
    r"\b(?:Mr|Mrs|Ms|Mx|Dr|Prof|Rev|Sr|Jr|St|e\.g|i\.e|vs|cf|approx|etc)\.(?=[ \t]+\w)",
    re.IGNORECASE,
)
REVIEW_ACTIONS = {"accept": "Accepted", "edit": "Edited", "reject": "Rejected"}
NOT_REVIEWED = "Not reviewed"
HOLD = "Hold"
QUARANTINED = "Quarantined"


def workflow_only(mode=None):
    """True when the person asked for the workflow-only path, or ZF_AI=off is set."""
    if os.environ.get("ZF_AI", "").strip().lower() in ("off", "workflow", "workflow-only"):
        return True
    return str(mode).strip().lower() in ("off", "workflow", "workflow-only", "true") if mode not in (None, False, "") else False


def norm(s):
    return " ".join(str(s).split()).casefold()


def source_labels(c, reason_ok=False):
    """Every citable fact of a case, as display labels."""
    export_fields.prompt_case(c)
    r, h = c["resident"], c["home"]
    out = [f"Stage: {c['stage']}", f"Days in stage: {c['days_in_stage']}", f"Waiting on: {c['waiting_on']}",
           f"Owner: {c['owner']}", f"Resident decision: {resident_status(c)}", f"Preferred contact: {r['preferred']}",
           f"Address: {h['address']}", f"Home type: {h['type']}", f"EPC band: {h['epc']}", f"Built: {h['built']}"]
    m = c.get("measures")
    if m:
        out.append(f"Measures: {', '.join(m) if isinstance(m, list) else m}")
    f = c.get("funding")
    if f:
        out += [f"Funding: {f['route']} ({f['status']})", f"Funding route: {f['route']}"]
    open_h = [x for x in c.get("hazards", []) if not x["released"]]
    out.append(f"Open safety issues: {len(open_h)}")
    out += [f"Safety issue: {x['category']}" for x in c.get("hazards", [])]
    has_adjustment = bool(r.get("adjustment")) and r["adjustment"] not in ("None", "Unknown")
    if support_status(r) == "Yes":
        out.append("Extra support: needed")
    elif support_status(r) == "Unknown":
        out.append("Extra support: Unknown")
    if reason_ok and has_adjustment:  # the reason is only visible to roles that may see it
        out.append(f"Extra support: {r['adjustment']}")
    if reason_ok and r.get("unavailable"):
        out.append(f"Unavailable: {r['unavailable']}")
    for k in c.get("contacts", [])[-10:]:
        d = str(k["at"])[:10]
        out += [f"Contact {d}: {k['outcome'] if reason_ok else k['channel']}", f"Case history {d}"]
    for e in (c.get("history") or [])[-10:]:
        if isinstance(e, dict) and e.get("at"):
            out.append(f"Case history {str(e['at'])[:10]}")
    out += [f"Document: {d['name']}" for d in c.get("documents", [])]
    return out


def cites_for(c, *prefixes, reason_ok=False):
    """Template citations: the case's own labels that start with any of the prefixes."""
    return [lab for lab in source_labels(c, reason_ok) if any(lab.startswith(p) for p in prefixes)]


def cite_instruction(sources):
    """Tell the model which labels it may cite, per case."""
    lines = []
    for cid, labels in sources.items():
        lines.append(f"{cid}: " + "; ".join(labels[:14]))
    multi = len(sources) > 1
    return ("\n\nCitable facts (cite only these, copied exactly): \n" + "\n".join(lines)
            + ai_prompts.CITATION_RULE[0]
            + ai_prompts.CITATION_RULE[1 if multi else 2])


def resolve(label, sources):
    """sources: {case_id: [labels]}. A label resolves when a case really has that field or record."""
    label = " ".join(str(label).split())
    cid, rest = None, label
    if ": " in label and label.split(": ", 1)[0] in sources:
        cid, rest = label.split(": ", 1)
    elif len(sources) == 1:
        cid = next(iter(sources))
    if cid is None:
        return False
    return norm(rest) in {norm(x) for x in sources[cid]}


def analyse(text, sources, bullets=False):
    """Split model text into clean text, resolved citations, unresolved citations, dropped uncited bullets."""
    dropped = 0
    if bullets:
        kept = []
        for line in text.splitlines():
            if BULLET.match(line):
                marks = CITE_RE.findall(line)
                if not marks or not all(resolve(m, sources) for m in marks):
                    dropped += 1
                    continue
            kept.append(line)
        text = "\n".join(kept)
    marks = [m.strip() for m in CITE_RE.findall(text)]
    good = list(dict.fromkeys(m for m in marks if resolve(m, sources)))
    bad = list(dict.fromkeys(m for m in marks if not resolve(m, sources)))
    clean = CITE_RE.sub("", text)
    clean = EMPTY_SOURCES.sub("", clean)
    clean = re.sub(r"[ \t]+([.,;:!?\u2026])", r"\1", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean).strip()
    return clean, good, bad, dropped


def statement_sources(text: str, sources: Any, bullets: bool = False) -> list[dict[str, Any]]:
    """Keep declared references with their statement, without guessing missing ones."""
    if bullets:
        text = "\n".join(line for line in text.splitlines()
                         if not analyse(line, sources, bullets=True)[3])
    marks: list[str] = []

    def protect(match: re.Match[str]) -> str:
        marks.append(match.group())
        return f"\x00{len(marks) - 1}\x00"

    protected = CITE_RE.sub(protect, text)
    # A model may place the citation after the sentence's punctuation.
    protected = re.sub(
        rf"({STATEMENT_END})\s*(\x00\d+\x00(?:\s*\x00\d+\x00)*)([.!?\u2026\"'\u2019\u201d)\]}}]*)",
        lambda match: " " + " ".join(match[2].split()) + match[1] + match[3] + " ",
        protected,
    )

    def protect_abbreviation(match: re.Match[str]) -> str:
        word = match.group().casefold()
        following = match.string[match.end():].lstrip(" \t")
        if word in ("approx.", "etc.") and not (following[0].islower() or following[0].isdigit()):
            return match.group()
        if word in ("jr.", "sr.") and following[0].isupper():
            # A suffix after a name can end a claim; titles before a name stay medial.
            if re.search(r"\b[A-Z][\w'\u2019-]*[ \t]+[A-Z][\w'\u2019-]*[ \t]+$",
                         match.string[:match.start()]):
                return match.group()
        if word == "st.":
            preceding = re.search(r"(\w+)[ \t]+$", match.string[:match.start()])
            # A capitalized street suffix is ambiguous; do not merge its next claim.
            if preceding and preceding[1][0].isupper() and not re.match(r"\w+['\u2019]s\b", following):
                return match.group()
        return match.group().replace(".", "\x01")

    protected = STATEMENT_ABBREVIATION.sub(protect_abbreviation, protected)
    statements = []
    separated = re.sub(rf"({STATEMENT_END})\s+", r"\1\n", protected)
    for piece in re.split(r"\n+", separated):
        raw = re.sub(r"\x00(\d+)\x00", lambda m: marks[int(m[1])], piece).replace("\x01", ".").strip()
        if not raw:
            continue
        clean, good, bad, _ = analyse(raw, sources)
        if clean:
            statements.append(dict(text=clean, citations=good, unresolved=bad))
    return statements


def priority_items(text, n, sources):
    """Validate priority JSON. Returns (items, dropped, error). Items without resolving citations are dropped."""
    try:
        got = json.loads(text)
    except ValueError:
        return None, 0, "not JSON"
    if not isinstance(got, list) or not got or not all(isinstance(g, dict) for g in got):
        return None, 0, "not a list of objects"
    ids = [g.get("case_id") for g in got]
    if len(set(ids)) != len(ids) or any(i not in sources for i in ids):
        return None, 0, "duplicate or unknown case id"
    if not all(isinstance(g.get("reason"), str) and g["reason"].strip() for g in got):
        return None, 0, "missing reason"
    items, dropped = [], 0
    for g in got:
        cites = g.get("cites")
        cites = [str(x).strip() for x in cites] if isinstance(cites, list) else []
        if not cites or not all(resolve(f"{g['case_id']}: {x}", sources) for x in cites):
            dropped += 1
            continue
        items.append(dict(case_id=g["case_id"], reason=g["reason"].strip()[:300], cites=cites))
    if not items or len(items) > n:
        return None, dropped, "no cited items or too many"
    return items, dropped, None


def critical_misses(shown_ids, hazard_ids, k):
    """Open-safety cases that the recommended top-k leaves out. When there are more than k, the list must be all safety cases."""
    hazard_ids, shown = set(hazard_ids), set(shown_ids)
    if len(hazard_ids) > k:
        return [] if shown <= hazard_ids else sorted(hazard_ids - shown)
    return sorted(hazard_ids - shown)


def _now():
    return datetime.now().isoformat(timespec="seconds")


def add_record(store, user, **fields):
    with store.lock:
        rec = dict(id=uuid.uuid4().hex[:12], kind="ai_task", user=user["email"], created=_now(), status=NOT_REVIEWED,
                   prompt_version=ai_prompts.version(fields["task"]), reviewer_action=None, reviewer_reason="", override_text=None,
                   resolved_by=None, resolved_at=None)
        rec.update(fields)
        store.data["recommendations"].append(rec)
        store.audit(user["email"], "ai_record", (rec["case_ids"] or ["-"])[0] if len(rec["case_ids"]) == 1 else "-",
                    f"{rec['task']} {rec['id']} mode={rec['mode']} source={rec['source']} verified={rec['verified']}")
        ranks, v0 = store._ranks, store.version
        store.save()
        if ranks and ranks[0] == v0:  # an AI record changes no case, so the ranking is still valid
            store._ranks = (store.version, ranks[1])
        return rec


def source_hashes(store, user, case_ids):
    """Current per-case source hashes as seen by this user; the same function stamps and rechecks a record."""
    ok = projection.can_see_reason(user)
    return source_snapshot_hashes({cid: source_labels(store._case(cid), ok) for cid in case_ids})


def source_snapshot_hashes(sources):
    return {cid: hashlib.sha256("\n".join(sorted(labels)).encode()).hexdigest()[:16]
            for cid, labels in sources.items()}


def finish(store, user, task, case_ids, r, workflow_text, sources, template_cites=None, bullets=False, record_cites=None, epoch0=None):
    """Turn an Ai result into the shown output, with citations checked, plus its comparison record."""
    ai_output = r["text"] if r["source"] == "ai" else r.get("ai_text")
    dropped = 0
    if r["source"] == "ai" and record_cites is None:
        text, cites, bad, dropped = analyse(r["text"], sources, bullets)
        verified = bool(cites) and not bad and bool(text)
    else:
        text = r["text"]
        cites = list(record_cites if record_cites is not None else template_cites or [])
        bad = [x for x in cites if not resolve(x, sources)]
        cites = [x for x in cites if x not in bad]
        verified = bool(cites) and not bad
    reason = r.get("reason")
    mode = "workflow-only" if reason == "workflow-only mode selected" else "ai"
    from . import ai_registry
    env = ai_registry.envelope(task, case_ids, {cid: hashlib.sha256("\n".join(sorted(labels)).encode()).hexdigest()[:16]
                                               for cid, labels in sources.items()},
                               dict(r, prompt_version=ai_prompts.version(task)), store.version)
    def publish(late):
        why = "late result quarantined after a suspension or restart" if late else reason
        shown, citations, checked = (workflow_text, [], False) if late else (text, cites, verified)
        rec = add_record(store, user, task=task, case_ids=list(case_ids), mode=mode, source=r["source"], model=r.get("model"),
                         latency_ms=r.get("latency_ms"), ai_output=ai_output, workflow_output=workflow_text, shown_output=shown,
                         fallback_reason=why, envelope=env, release=r.get("release"), verified=checked, instruction_status="Not an instruction",
                         status=QUARANTINED if late else NOT_REVIEWED,
                         continuity_epoch=epoch0, quarantine=dict(reason=why, at=_now()) if late else None,
                         provenance=dict(citation_resolved=checked, source_verified=False, human_reviewed=False,
                                         source_hashes=env["source_versions"], case_version=store.version, hold=None), citations=citations, unresolved=bad, dropped_uncited=dropped)
        result = dict(r, source="template", model=None, reason=why) if late else r
        return dict(result, text=shown, citations=citations, unresolved=bad, dropped_uncited=dropped, verified=checked,
                    approval=rec["status"], instruction_status="Not an instruction", envelope=env, record_id=rec["id"],
                    continuity_epoch=epoch0, mode=mode, prompt_version=ai_prompts.version(task),
                    generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    source_case_ids=list(sources),
                    statements=statement_sources(r["text"], sources, bullets)
                    if not late and r["source"] == "ai" else [
                        dict(text=shown, citations=citations, unresolved=[] if late else bad)])
    return store.continuity_publish(task, epoch0, r["source"], publish)


def require_registered(task):
    from . import ai_registry
    if ai_registry.get(task) is None:
        raise ValueError("This AI task is not registered. Use the manual route.")


def run_text_task(store, user, task, cases, sysmsg, prompt, template, template_cites, strong=False, check=None, mode=None,
                  bullets=False):
    require_registered(task)
    with store.lock:
        ok = projection.can_see_reason(user)
        sources = {c["id"]: source_labels(c, ok) for c in cases}
    epoch0 = store.continuity_epoch()
    r = store.ai.run(task, sysmsg, prompt + cite_instruction(sources), template, strong, check, off=workflow_only(mode))
    return finish(store, user, task, list(sources), r, template, sources, template_cites, bullets, epoch0=epoch0)


def run_document(store, user, case_id, doc, data, mode=None):
    require_registered("read_document")
    export_fields.scalars(doc, ("name", "mime"))
    with store.lock:
        sources = {case_id: source_labels(store._case(case_id), projection.can_see_reason(user))}
    off = workflow_only(mode)
    epoch0 = store.continuity_epoch()
    t0 = time.perf_counter()
    r = store.ai.look_at(doc["name"], data, doc["mime"], off=off)
    r.setdefault("reason", None if r["source"] == "ai" else "file type is stored but not read")
    r["latency_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    label = f"Document: {doc['name']}"
    return finish(store, user, "read_document", [case_id], r, "The file is stored. Add a short note about what it is.",
                  sources, record_cites=[label], epoch0=epoch0)


def review(store, user, rec_id, action, reason="", text=None):
    if action not in REVIEW_ACTIONS:
        raise ValueError("Choose accept, edit or reject.")
    reason = (reason or "").strip()[:300]
    if action in ("edit", "reject") and not reason:
        raise ValueError("Say why.")
    with store.lock:
        rec = next((r for r in store.data["recommendations"] if r["id"] == rec_id and r.get("kind") == "ai_task"), None)
        if not rec:
            raise KeyError(rec_id)
        if rec["user"] != user["email"]:
            raise PermissionError("This AI output was made for someone else.")
        if rec["status"] == QUARANTINED:
            raise PermissionError("This AI output was quarantined after a suspension or restart and cannot be relied on.")
        if rec["status"] != NOT_REVIEWED:
            raise ValueError("This AI output has already been reviewed.")
        if action != "reject" and store.continuity_suspension(rec["task"]):
            raise PermissionError(store.continuity_block(rec["task"]))
        if action != "reject" and rec["source"] == "ai":
            if not store.ai_epoch_current(rec):
                raise PermissionError("AI output epoch changed or is unavailable; use fresh work or the manual route.")
            store.continuity_fence()
        if action != "reject" and rec["source"] == "ai" and not store.release_current(
                rec["task"], rec.get("release"), rec.get("model")):
            store.audit(user["email"], "ai_release_denied", "-", f"{rec['task']} {rec_id}; use the manual route")
            raise PermissionError("Release changed; use the ordinary case controls.")
        prov = rec.setdefault("provenance", dict(citation_resolved=rec.get("verified", False), source_verified=False,
                                                 human_reviewed=False, source_hashes={}, hold=None))
        try:
            now_hashes = source_hashes(store, user, rec["case_ids"])
        except (KeyError, PermissionError):
            now_hashes = None
        if prov.get("source_hashes") and now_hashes != prov["source_hashes"]:
            # Changed, missing or no-longer-visible source: nothing is accepted; an owned hold stays visible.
            prov["hold"] = dict(owner=rec["user"], reason="source changed or unavailable since the proposal", at=_now())
            rec["status"] = HOLD
            store.audit(user["email"], "ai_review_hold", "-", f"{rec['task']} {rec_id}")
            store.save()
            raise ValueError("The source changed since this proposal; it is on hold for a fresh review.")
        rec.update(status=REVIEW_ACTIONS[action], reviewer_action=action, reviewer_reason=reason,
                   override_text=str(text)[:6000] if action == "edit" and text is not None else None,
                   resolved_by=user["email"], resolved_at=_now())
        prov["human_reviewed"] = True
        rec["review_evidence"] = dict(reviewer=user["email"], disposition=action, reason=reason,
                                      compared=dict(ai=rec.get("ai_output"), workflow=rec.get("workflow_output")),
                                      source_hashes=now_hashes, case_version=store.version,
                                      effect="Not an instruction; records the review only; any task or draft is created separately by the person")
        store.audit(user["email"], f"ai_review_{action}", rec["case_ids"][0] if len(rec["case_ids"]) == 1 else "-",
                    f"{rec['task']} {rec_id} {reason}".strip())
        store.save()
        return dict(rec)


def live_report(store):
    """Reviewer outcomes and fallback reasons across everything recorded so far."""
    with store.lock:
        recs = list(store.data["recommendations"])
    tasks, reasons, fallbacks = {}, [], {}
    for r in recs:
        task = "priority" if r.get("kind") != "ai_task" else r["task"]
        status = NOT_REVIEWED if r["status"] == "Proposed" else r["status"]
        t = tasks.setdefault(task, dict(total=0, ai=0, workflow=0, unverified=0, **{s: 0 for s in (NOT_REVIEWED, "Accepted", "Edited", "Rejected", HOLD, QUARANTINED)}))
        t["total"] += 1
        t["ai" if r["source"] == "ai" else "workflow"] += 1
        t["unverified"] += 0 if r.get("verified", r.get("validated", True)) else 1
        t[status] += 1
        why = r.get("fallback_reason")
        if why:
            fallbacks[why] = fallbacks.get(why, 0) + 1
        if status in ("Edited", "Rejected") and r.get("reason", r.get("reviewer_reason")):
            reasons.append(dict(task=task, action=status, reason=r.get("reason") or r.get("reviewer_reason")))
    return dict(prompt_version=PROMPT_VERSION, tasks=tasks, fallback_reasons=fallbacks, reviewer_reasons=reasons[-50:])
