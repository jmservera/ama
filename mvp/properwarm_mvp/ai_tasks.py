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
import json
import os
import re
import time
import uuid
from datetime import datetime

from . import projection

PROMPT_VERSION = "2026-10-09.1"
CITE_RE = re.compile(r"\[\[(.+?)\]\]")
EMPTY_SOURCES = re.compile(r"(?im)^[ \t]*sources?[ \t]*:[\s;,]*$")
BULLET = re.compile(r"^\s*[-*\u2022]\s")
REVIEW_ACTIONS = {"accept": "Accepted", "edit": "Edited", "reject": "Rejected"}
NOT_REVIEWED = "Not reviewed"


def workflow_only(mode=None):
    """True when the person asked for the workflow-only path, or PW_AI=off is set."""
    if os.environ.get("PW_AI", "").strip().lower() in ("off", "workflow", "workflow-only"):
        return True
    return str(mode).strip().lower() in ("off", "workflow", "workflow-only", "true") if mode not in (None, False, "") else False


def norm(s):
    return " ".join(str(s).split()).casefold()


def source_labels(c, reason_ok=False):
    """Every citable fact of a case, as display labels."""
    r, h = c["resident"], c["home"]
    out = [f"Stage: {c['stage']}", f"Days in stage: {c['days_in_stage']}", f"Waiting on: {c['waiting_on']}",
           f"Owner: {c['owner']}", f"Resident decision: {c['decision']['status']}", f"Preferred contact: {r['preferred']}",
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
    has_adjustment = bool(r.get("adjustment")) and r["adjustment"] != "None"
    if r.get("priority_support") or has_adjustment:
        out.append("Extra support: needed")
    if reason_ok and has_adjustment:  # the reason is only visible to roles that may see it
        out.append(f"Extra support: {r['adjustment']}")
    if reason_ok and r.get("unavailable"):
        out.append(f"Unavailable: {r['unavailable']}")
    for k in c.get("contacts", [])[-10:]:
        d = str(k["at"])[:10]
        out += [f"Contact {d}: {k['outcome']}", f"Case history {d}"]
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
            + "\nAfter each claim add its source in double square brackets, "
            + ("prefixed with the case id, for example [[CASE-ID: Stage: Survey booked]]." if multi else "for example [[Stage: Survey booked]]."))


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
    clean = re.sub(r"[ \t]+([.,;:!?])", r"\1", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean).strip()
    return clean, good, bad, dropped


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


def add_record(store, user, *, persist=True, **fields):
    """Append a comparison record; transaction-owning callers may defer save."""
    with store.lock:
        rec = dict(id=uuid.uuid4().hex[:12], kind="ai_task", user=user["email"], created=_now(), status=NOT_REVIEWED,
                   prompt_version=PROMPT_VERSION, reviewer_action=None, reviewer_reason="", override_text=None,
                   resolved_by=None, resolved_at=None, **fields)
        store.data["recommendations"].append(rec)
        store.audit(user["email"], "ai_record", (rec["case_ids"] or ["-"])[0] if len(rec["case_ids"]) == 1 else "-",
                    f"{rec['task']} {rec['id']} mode={rec['mode']} source={rec['source']} verified={rec['verified']}")
        ranks, v0 = store._ranks, store.version
        if persist:
            store.save()
        if ranks and ranks[0] == v0:  # an AI record changes no case, so the ranking is still valid
            store._ranks = (store.version, ranks[1])
        return rec


def finish(store, user, task, case_ids, r, workflow_text, sources, template_cites=None, bullets=False, record_cites=None, *, persist=True):
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
    rec = add_record(store, user, persist=persist, task=task, case_ids=list(case_ids), mode=mode, source=r["source"], model=r.get("model"),
                     latency_ms=r.get("latency_ms"), ai_output=ai_output, workflow_output=workflow_text, shown_output=text,
                     fallback_reason=reason, verified=verified, citations=cites, unresolved=bad, dropped_uncited=dropped,
                     provider_success=r.get("provider_success", r["source"] == "ai"), provenance=r.get("provenance"),
                     assistance_status=r.get("assistance_status"))
    return dict(r, text=text, citations=cites, unresolved=bad, dropped_uncited=dropped, verified=verified,
                approval=NOT_REVIEWED, record_id=rec["id"], mode=mode, prompt_version=PROMPT_VERSION)


def run_text_task(store, user, task, cases, sysmsg, prompt, template, template_cites, strong=False, check=None, mode=None,
                  bullets=False):
    with store.lock:
        ok = projection.can_see_reason(user)
        sources = {c["id"]: source_labels(c, ok) for c in cases}
    r = store.ai.run(task, sysmsg, prompt + cite_instruction(sources), template, strong, check, off=workflow_only(mode))
    return finish(store, user, task, list(sources), r, template, sources, template_cites, bullets)


def run_document(store, user, case_id, doc, data, mode=None):
    off = workflow_only(mode)
    t0 = time.perf_counter()
    r = store.ai.look_at(doc["name"], data, doc["mime"], off=off)
    r.setdefault("reason", None if r["source"] == "ai" else "file type is stored but not read")
    r["latency_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    label = f"Document: {doc['name']}"
    with store.lock:
        sources = {case_id: source_labels(store._case(case_id), projection.can_see_reason(user))}
    return finish(store, user, "read_document", [case_id], r, "The file is stored. Add a short note about what it is.",
                  sources, record_cites=[label])


def review(store, user, rec_id, action, reason="", text=None, *, persist=True):
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
        if rec["task"] == "source_bound_narrative":
            case = store._case(rec["case_ids"][0])
            draft = case.get("forms", {}).get(rec.get("form_id"))
            if draft is None:
                raise ValueError("The narrative's authorized form snapshot is unavailable.")
            store._exercise_form_role(user, draft["form_type"])
            if draft["input_version"] != rec.get("input_version") or any(
                ref["id"] not in draft["sources"] or
                any(draft["sources"][ref["id"]][key] != ref[key] for key in ("version", "hash"))
                for ref in rec.get("source_refs", [])
            ):
                raise ValueError("Source-bound narrative is stale; regenerate or use the manual route.")
        if rec["status"] != NOT_REVIEWED:
            raise ValueError("This AI output has already been reviewed.")
        rec.update(status=REVIEW_ACTIONS[action], reviewer_action=action, reviewer_reason=reason,
                   override_text=str(text)[:6000] if action == "edit" and text is not None else None,
                   resolved_by=user["email"], resolved_at=_now())
        store.audit(user["email"], f"ai_review_{action}", rec["case_ids"][0] if len(rec["case_ids"]) == 1 else "-",
                    f"{rec['task']} {rec_id} {reason}".strip())
        if persist:
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
        t = tasks.setdefault(task, dict(total=0, ai=0, workflow=0, unverified=0, **{s: 0 for s in (NOT_REVIEWED, "Accepted", "Edited", "Rejected")}))
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
