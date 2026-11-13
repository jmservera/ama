"""Offline evaluation of the AI priority recommendation. No network, no model.

The model is replaced by a scripted answer from evals/ai_priority_golden.json.
Whatever the model says, these hold, and the harness fails if any does not:

* the deterministic ranking is identical before the run, after it and after a
  person answers it (AI never changes ranking);
* no case, owner, stage, queue or decision changes (AI never acts);
* the recommendation stays "Proposed" until a person answers; someone else
  cannot answer it; edit and reject need a reason (nothing without approval);
* only listed case ids, no duplicates, a reason each, no claim that anything
  was sent; invalid output falls back to the rules-based template;
* the run and each answer are in the audit ledger and the chain verifies;
* no case with an open safety issue is missing from the recommended top-k (critical misses: zero);
* every cited fact exists in the case data (citation validity: 100%);
* the workflow-only mode never calls the model, and every AI task leaves a comparison record.

It also measures, per scenario and in total: top-k overlap and Spearman rank
correlation against the deterministic order, run-to-run variation of the AI
order on identical input, latency per run, model and prompt version, reviewer
accept/edit/reject counts with reasons, and the AI's added value (recall of the
cases a person said must surface, AI minus deterministic order).

Run: python3 -m zava_forward.agents.ai_eval (with src/core and src/agents installed)
"""
import copy
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path

from zava_forward.agents import cohort_ranking_eval
from zava_forward.core import ai_tasks, ai_registry
from zava_forward.core.store import Store

# The golden file lives in the project evals/ folder, outside the package; an installed image sets ZF_AI_GOLDEN.
GOLDEN = Path(os.environ.get("ZF_AI_GOLDEN") or Path(__file__).resolve().parents[3] / "evals" / "ai_priority_golden.json")
OWNER = dict(code="EV-01", name="Eval Owner", email="owner@eval.example", role="Resident Liaison Officer")
OTHER = dict(code="EV-02", name="Eval Other", email="other@eval.example", role="Resident Liaison Officer")


def build_case(spec):
    hazards = [dict(category="Damp and mould", priority="Routine", noticed="2026-01-01", referred=None, repaired=None,
                    released=False, job="", owner="Eval Safe")] if spec.get("hazard") else []
    return dict(
        id=spec["id"], wave="Wave 1", closed=False, stage="Contacting resident", stage_since="2026-01-01",
        days_in_stage=spec.get("days", 10), waiting_on=OWNER["name"], reason="to agree a visit", owner_code=OWNER["code"],
        owner=OWNER["name"], owner_role=OWNER["role"],
        resident=dict(title="Ms", name=spec.get("name", "Eval Resident"), formal="Ms Eval", phone="01000 000000", email="",
                      preferred="Phone", adjustment="Large print" if spec.get("support") else "None",
                      priority_support=bool(spec.get("support")), unavailable="", representative=None),
        home=dict(address=f"{spec['id']} Eval Road", town="Evalton", postcode="EV1 1AA", area="Eval", type="Mid terrace",
                  built=1950, epc="D", tenure="Social rent", lat=54.9, lon=-1.6),
        measures="Loft insulation", contractor=dict(name="Eval Ltd", phone="0", scope="x", contact="Kim Builder"),
        decision=dict(status=spec.get("decision", "Not yet asked"), by=None, at=None), funding_ok=False,
        contacts=[], appointments=[], hazards=hazards, history=[])


def _state(store):
    return json.dumps(store.cases, sort_keys=True)


def _ranking(store):
    return json.dumps([(cid, e["rank"], e["reasons"]) for cid, e in sorted(store._ranking().items())])


def spearman(a, b):
    """Rank correlation of two orderings of the same items (no ties). None for fewer than two items."""
    common = [x for x in a if x in b]
    m = len(common)
    if m < 2:
        return None
    ra = {x: i for i, x in enumerate(common)}
    rb = {x: i for i, x in enumerate([x for x in b if x in ra])}
    d2 = sum((ra[x] - rb[x]) ** 2 for x in common)
    return round(1 - 6 * d2 / (m * (m * m - 1)), 3)


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else None


def _own_labels(case):
    return {" ".join(x.split()).casefold() for x in ai_tasks.source_labels(case, True)}


def run_scenario(sc, workdir, observed=None):
    """Returns (failures, measures). observed, when given, collects the dispatch and final-outcome records."""
    fails, measures = [], {}
    try:
        _run(sc, workdir, fails, measures, observed)
    except Exception as e:  # an unexpected error is itself a failed check
        fails.append(f"unexpected {type(e).__name__}: {e}")
    return fails, measures


# Per-task coverage statuses. They describe what this offline harness exercised with a scripted provider (dispatch
# plus control checks), never held-out semantic accuracy or live-model behaviour.
EXERCISED = "exercised offline (scripted provider; dispatch and control checks only)"
FALLBACK_ONLY = "template fallback only (no accepted scripted model output)"
NOT_EVALUATED = "not evaluated by this harness"
COVERAGE_NOTE = ("Offline dispatch and control checks with a scripted provider only; not held-out semantic accuracy, "
                 "not a live model, not human review. The five assistants dispatch through the core assistant planner, "
                 "not Ai.run or Ai.look_at, so this harness does not evaluate them; chat and the concern pack are likewise not evaluated here.")


def observe(store, observed):
    """Record each Ai.run and Ai.look_at call: the task it returned and whether the scripted model was reached.

    The spy sees only those two retained-path entry points; it cannot see the assistant planner.
    """
    if observed is None:
        return
    ai = store.ai

    def traced(real, via):
        def call(*args, **kwargs):
            reached = []
            chat = ai._chat
            ai._chat = lambda *a, **k: reached.append(1) or chat(*a, **k)
            try:
                result = real(*args, **kwargs)
            finally:
                ai._chat = chat
            task = args[0] if via == "run" and args else (result.get("task") or "read_document")
            observed.append(dict(kind="dispatch", task=task, via=via, source=result.get("source"), model_called=bool(reached)))
            return result
        return call
    ai.run = traced(ai.run, "run")
    ai.look_at = traced(ai.look_at, "look_at")


def _final(observed, task, view):
    """Record the outcome a person would see, so a late quarantine or hold cannot count as coverage."""
    if observed is not None:
        observed.append(dict(kind="final", task=task, source=view.get("source"), mode=view.get("mode"),
                             status=view.get("approval") or view.get("status"),
                             held=bool(view.get("financial_attribution"))))


def _eligible(f):
    return f["source"] == "ai" and f["mode"] == "ai" and f["status"] not in ("Quarantined", "Hold") and not f["held"]


def task_coverage(observed):
    """Per-task record derived from ai_registry.tasks(), so a registered task cannot be left out unstated."""
    observed = observed or []
    registry = ai_registry.tasks()
    retained = {k for k, v in registry.items() if v["kind"] == "retained-path"}
    tasks = {}
    for task_id, entry in registry.items():
        seen = [o for o in observed if o["task"] == task_id] if task_id in retained else []
        ran = any(o["kind"] == "dispatch" and o["model_called"] for o in seen)
        shown = any(o["kind"] == "final" and _eligible(o) for o in seen)
        status = EXERCISED if ran and shown else FALLBACK_ONLY if seen else NOT_EVALUATED
        tasks[task_id] = dict(kind=entry["kind"], status=status,
                              dispatches=sum(o["kind"] == "dispatch" for o in seen),
                              model_calls=sum(o["kind"] == "dispatch" and o["model_called"] for o in seen))
    return dict(
        tasks=tasks, note=COVERAGE_NOTE, namespace_errors=sorted({o["task"] for o in observed} - retained),
        failures=[f"{t}: {tasks[t]['status']}" for t in sorted(retained) if tasks[t]["status"] != EXERCISED],
        counts={s: sum(r["status"] == s for r in tasks.values()) for s in (EXERCISED, FALLBACK_ONLY, NOT_EVALUATED)})


def _scripted(store, outputs):
    if outputs is None:
        return
    store.ai.endpoint = "http://scripted-model.invalid"
    # This harness evaluates scripted output controls, not release authorization.
    store.release_block = lambda *a, **k: None
    store.release_context = lambda task, dep=None: dict(
        id=f"offline-output-test:{task}", version="scripted-output-v1",
        digest=ai_registry.digest(ai_registry.legacy_binding(
            task, store.ai, dep or ai_registry.legacy_deployment(task, store.ai))))
    store.ai.release = store.release_context
    seq = iter(range(10 ** 6))
    store.ai._chat = lambda *a, **k: outputs[next(seq) % len(outputs)]


def _run(sc, workdir, fails, measures, observed=None):
    data = dict(staff=[OWNER, OTHER], cases=[build_case(c) for c in sc["cases"]])
    p = Path(workdir) / "eval.json"
    p.write_text(json.dumps(data))
    store = Store(str(p), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl"))
    outs = sc.get("model_outputs") or ([sc["model_output"]] if sc.get("model_output") is not None else None)
    observe(store, observed)
    _scripted(store, outs)
    rank0, state0 = _ranking(store), _state(store)
    ids = {c["id"] for c in sc["cases"]}
    n = sc["n"]
    hazard = {c["id"] for c in sc["cases"] if c.get("hazard")}
    exp = sc["expect"]

    def check(ok, what):
        if not ok:
            fails.append(what)
    runs, recs, latencies = [], [], []
    for _ in range(sc.get("runs", len(outs) if outs and sc.get("model_outputs") else 1)):
        t0 = time.perf_counter()
        rec = store.ai_priority(OWNER, n)
        _final(observed, "priority", rec)
        latencies.append(round((time.perf_counter() - t0) * 1000, 2))
        recs.append(rec)
        runs.append([i["case_id"] for i in rec["items"]])
    rec, got = recs[-1], runs[-1]
    full = [cid for cid, _ in sorted(((i, e["rank"]) for i, e in store._ranking().items()), key=lambda x: x[1])]
    det = full[:n]

    for rec_i, got_i in zip(recs, runs):
        check(rec_i["status"] == "Proposed", "recommendation must start as Proposed")
        check(rec_i["label"] == Store.REC_LABEL, "recommendation must be labelled AI suggestion, not approved")
        check(set(got_i) <= ids and len(set(got_i)) == len(got_i) and got_i, "only listed case ids, no duplicates")
        check(all(i["reason"].strip() for i in rec_i["items"]), "every item needs a reason")
        check(not any("sent" in i["reason"].lower() and "not" not in i["reason"].lower() for i in rec_i["items"]), "no claim that something was sent")
        # critical misses, computed here and not by the store's own guard
        missed = hazard - set(got_i) if len(hazard) <= n else (set() if set(got_i) <= hazard else hazard - set(got_i))
        check(not missed, f"critical miss: open safety issue not in the recommended top {n}: {sorted(missed)}")
        # every cited fact must exist in the case data
        for it in rec_i["items"]:
            own = _own_labels(next(c for c in store.cases.values() if c["id"] == it["case_id"]))
            check(it["cites"], f"{it['case_id']} has no citation")
            for cite in it["cites"]:
                measures.setdefault("cites", []).append(" ".join(cite.split()).casefold() in own)
                check(" ".join(cite.split()).casefold() in own, f"citation does not exist in {it['case_id']}: {cite}")
        check(rec_i["source"] != "ai" or bool(rec_i["model"]), "model must be recorded for an AI run")
        check(bool(rec_i["prompt_version"]) and rec_i["latency_ms"] is not None, "prompt version and latency must be recorded")
        check(rec_i["workflow_items"] and "fallback_reason" in rec_i, "comparison record needs the workflow-only output and fallback reason")
        check(rec_i["source"] == "ai" or bool(rec_i["fallback_reason"]), "a fallback needs a reason")
    if "source" in exp:
        check(rec["source"] == exp["source"], f"source should be {exp['source']}, was {rec['source']}")
    if "validated" in exp:
        check(rec["validated"] == exp["validated"], "validated flag")
    if "ids_in_order" in exp:
        check(got == exp["ids_in_order"], f"ids {got} should be {exp['ids_in_order']}")
    if "dropped_uncited" in exp:
        check(rec["dropped_uncited"] == exp["dropped_uncited"], f"dropped_uncited should be {exp['dropped_uncited']}")
    if "max_distinct_orders" in exp:
        check(len({tuple(r) for r in runs}) <= exp["max_distinct_orders"], "AI order varies more than allowed on identical input")
    check(_ranking(store) == rank0, "ranking changed after the AI run")
    check(_state(store) == state0, "case data changed after the AI run")
    check(store.latest_priority(OWNER)["status"] == "Proposed", "must stay Proposed without a person's answer")
    try:
        store.resolve_priority(OTHER, rec["id"], "accept")
        check(False, "another user must not be able to answer")
    except PermissionError:
        pass
    for bad in ("reject", "edit"):
        try:
            store.resolve_priority(OWNER, rec["id"], bad, "")
            check(False, f"{bad} without a reason must be refused")
        except ValueError:
            pass
    check(store.latest_priority(OWNER)["status"] == "Proposed", "refused answers must leave it Proposed")
    ans = sc.get("answer") or dict(action="accept")
    store.resolve_priority(OWNER, rec["id"], ans["action"], ans.get("reason", ""),
                           [dict(case_id=got[0], reason="mine")] if ans["action"] == "edit" else None)
    check(_ranking(store) == rank0, "ranking changed after the person answered")
    check(_state(store) == state0, "case data changed after the person answered")
    actions = [e["action"] for e in store.audit_entries()]
    for needed in ("ai_run_start", "ai_run_end", f"ai_priority_{ans['action']}"):
        check(needed in actions, f"audit must contain {needed}")
    check(store.verify_audit(), "audit chain must verify")

    # workflow-only mode: the model must not be called, and the output is the rules-based one
    calls = []
    real = store.ai._chat
    store.ai._chat = lambda *a, **k: calls.append(1) or real(*a, **k)
    wf = store.ai_priority(OWNER, n, mode="workflow")
    check(not calls, "workflow-only mode must not call the model")
    check(wf["source"] == "template" and wf["mode"] == "workflow-only" and wf["fallback_reason"], "workflow-only mode must be recorded as such")
    check([i["case_id"] for i in wf["items"]] == [i["case_id"] for i in rec["workflow_items"]], "workflow-only output must equal the comparison record")

    surface = set(sc.get("should_surface", []))
    top = lambda xs: set(xs[:n])
    wf_ids = [i["case_id"] for i in rec["workflow_items"]]
    measures.update(
        source=rec["source"], model=rec["model"], prompt_version=rec["prompt_version"], k=n,
        overlap=round(len(top(got) & set(det)) / n, 3), spearman=spearman(got, full),
        critical_misses=sum(1 for g in runs if (hazard - set(g)) and not (len(hazard) > n and set(g) <= hazard)),
        deterministic_critical_misses=len(hazard - set(det)) if len(hazard) <= n else 0,
        latency_ms=latencies, model_latency_ms=[r["latency_ms"] for r in recs],
        runs=len(runs), distinct_orders=len({tuple(r) for r in runs}),
        run_results=[dict(run=i, recommendation_id=r["id"], source=r["source"], model=r["model"],
                          prompt_version=r["prompt_version"], latency_ms=latency, model_latency_ms=r["latency_ms"])
                     for i, (r, latency) in enumerate(zip(recs, latencies), 1)],
        review=dict(action=ans["action"], reason=ans.get("reason", ""),
                    reviewer=OWNER["email"], recommendation_id=rec["id"]),
        cites=measures.get("cites", []))
    if len(runs) > 1:
        pairs = [(a, b) for i, a in enumerate(runs) for b in runs[i + 1:]]
        measures["pairwise_overlap"] = _mean([len(top(a) & top(b)) / n for a, b in pairs])
        measures["pairwise_spearman"] = _mean([spearman(a, b) for a, b in pairs])
    if surface:
        rec_at = lambda xs: round(len(surface & top(xs)) / len(surface), 3)
        measures["recall"] = dict(deterministic=rec_at(det), workflow_only=rec_at(wf_ids), ai=rec_at(got))


TASK_CASE = dict(id="T-1", days=12, hazard=True, support=True)


def run_task_checks(workdir, observed=None):
    """Citation, Unverified, workflow-only, comparison-record and review checks, scripted provider only.

    Covers catch-me-up (summary), message and briefing here, and funding draft and document reading in their own
    isolated stores. It does not cover priority (the golden scenarios do), the five assistants, chat or the concern
    pack. It proves control behaviour on constructed input, not held-out semantic accuracy.
    """
    fails = []

    def check(ok, what):
        if not ok:
            fails.append(what)
    try:
        data = dict(staff=[OWNER, OTHER], cases=[build_case(TASK_CASE)])
        p = Path(workdir) / "eval.json"
        p.write_text(json.dumps(data))
        store = Store(str(p), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl"))
        observe(store, observed)
        state0, rank0 = _state(store), _ranking(store)
        _scripted(store, [""])
        script = {}
        store.ai._chat = lambda *a, **k: script["out"]

        script["out"] = "- At Contacting resident for 12 days [[Stage: Contacting resident]]\n- Open safety issue [[Open safety issues: 1]]"
        r = store.ai_run(OWNER, "T-1", "summary")
        check(r["source"] == "ai" and r["verified"] and r["approval"] == "Not reviewed", "a cited summary is verified and not yet reviewed")
        check("[[" not in r["text"] and len(r["citations"]) == 2, "citation markers are removed and listed")
        _final(observed, "summary", r)
        script["out"] = "- Stage is Survey booked [[Stage: Survey booked]]\n- Open safety issue [[Open safety issues: 1]]"
        r2 = store.ai_run(OWNER, "T-1", "summary")
        check(r2["dropped_uncited"] == 1 and "Survey booked" not in r2["text"], "a bullet citing a fact the case does not have is dropped")
        script["out"] = "Dear Ms Eval, we would like to visit. [[Case history 2031-01-01]]"
        r3 = store.ai_run(OWNER, "T-1", "message")
        check(not r3["verified"] and "Unverified" in r3["label"] and r3["unresolved"], "a draft whose citation does not resolve is Unverified")
        script["out"] = "Dear Ms Eval, we would like to visit."
        r4 = store.ai_run(OWNER, "T-1", "message")
        check(not r4["verified"], "a draft with no citation is Unverified")
        script["out"] = "Dear Ms Eval, we would like to visit [[Stage: Contacting resident]]."
        r5 = store.ai_run(OWNER, "T-1", "message", mode="workflow")
        check(r5["source"] == "template" and r5["mode"] == "workflow-only" and r5["verified"], "workflow-only returns the verified template")
        for x in (r, r2, r3, r4, r5):
            check(x["record_id"] and x["prompt_version"], "every output points to its comparison record")
        r6 = store.ai_run(OWNER, "T-1", "message")
        check(r6["source"] == "ai" and r6["verified"] and r6["mode"] == "ai" and r6["citations"] == ["Stage: Contacting resident"],
              "a cited message draft is verified, shown as the model's and not yet reviewed")
        _final(observed, "message", r6)
        recs = {x["id"]: x for x in store.data["recommendations"] if x.get("kind") == "ai_task"}
        rec5 = recs[r5["record_id"]]
        check(rec5["ai_output"] is None and rec5["workflow_output"] and rec5["fallback_reason"] == "workflow-only mode selected",
              "comparison record keeps the workflow-only output and the reason")
        check(recs[r3["record_id"]]["ai_output"] and recs[r3["record_id"]]["workflow_output"] and not recs[r3["record_id"]]["verified"],
              "comparison record keeps both outputs")
        script["out"] = "Briefing: ticket T-1 needs a visit today [[T-1: Stage: Contacting resident]]"
        b = store.briefing(OWNER)
        rec_of = lambda x: next((y for y in store.data["recommendations"] if y["id"] == x["record_id"]), {})
        check(b["source"] == "ai" and b["mode"] == "ai" and b["verified"] and "needs a visit today" in b["text"]
              and b["citations"] == ["T-1: Stage: Contacting resident"] and rec_of(b).get("ai_output"),
              "briefing shows the cited model answer and keeps it in its comparison record")
        _final(observed, "briefing", b)
        bw = store.briefing(OWNER, mode="workflow")
        check(bw["source"] == "template" and bw["mode"] == "workflow-only", "workflow-only briefing is the rules-based summary")
        try:
            store.review_ai(OTHER, r["record_id"], "accept")
            check(False, "another user must not review someone else's AI output")
        except PermissionError:
            pass
        for bad in ("reject", "edit"):
            try:
                store.review_ai(OWNER, r["record_id"], bad, "")
                check(False, f"{bad} without a reason must be refused")
            except ValueError:
                pass
        check(recs[r["record_id"]]["status"] == "Not reviewed", "stays unreviewed until a person answers")
        store.review_ai(OWNER, r["record_id"], "edit", "tone", "My version")
        check(recs[r["record_id"]]["override_text"] == "My version" and recs[r["record_id"]]["reviewer_reason"] == "tone", "override and reason recorded")
        check(_state(store) == state0 and _ranking(store) == rank0, "text tasks must not change cases or ranking")
        check(store.verify_audit(), "audit chain must verify")
        for name, runner in (("funding", run_funding_checks), ("document", run_document_checks)):
            with tempfile.TemporaryDirectory(dir=workdir) as sub:
                fails.extend(runner(sub, observed))
    except Exception as e:
        fails.append(f"unexpected {type(e).__name__}: {e}")
    return fails


PUBLIC_DOCUMENT = dict(
    name="public-guidance-note.txt", kind="Other",
    data=b"Constructed public fixture: a short note on loft insulation depth for a mid terrace home. It names no person and holds no private data.",
    metadata=dict(source="constructed public fixture", source_version="v1", reason="offline harness document"))
UNREAD_DOCUMENT = dict(name="constructed-register.xlsx", kind="Other", data=b"PK\x03\x04 constructed placeholder",
                       metadata=dict(source="constructed public fixture", source_version="v1", reason="offline harness document"))


def _isolated_store(workdir, observed):
    """A fresh one-case store with the scripted provider; returns (store, script) where script holds the next answer."""
    p = Path(workdir) / "eval.json"
    p.write_text(json.dumps(dict(staff=[OWNER, OTHER], cases=[build_case(TASK_CASE)])))
    store = Store(str(p), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl"))
    observe(store, observed)
    _scripted(store, [""])
    script = dict(out="", calls=0, sent=None)

    def chat(*args, **kwargs):
        script["calls"] += 1
        script["sent"] = args
        return script["out"]
    store.ai._chat = chat
    return store, script


def _without(store, field):
    return json.dumps({k: {f: v for f, v in c.items() if f != field} for k, c in store.cases.items()}, sort_keys=True)


def _record(store, view):
    return next((r for r in store.data["recommendations"] if r["id"] == view["record_id"]), {})


def run_funding_checks(workdir, observed=None):
    """Funding draft on constructed input: citation, Unverified, workflow-only, comparison record and review controls.

    The draft is wording for a person; nothing is approved, submitted or decided. Only the funding draft and status change.
    """
    fails = []

    def check(ok, what):
        if not ok:
            fails.append(f"funding draft: {what}")
    try:
        store, script = _isolated_store(workdir, observed)
        rank0, rest0 = _ranking(store), _without(store, "funding")
        script["out"] = ("Needs: costs from the contractor [[Address: T-1 Eval Road]] [[Home type: Mid terrace]] "
                         "[[Built: 1950]]")
        r = store.funding_draft(OWNER, "T-1")
        check(r["source"] == "ai" and r["mode"] == "ai" and r["verified"] and r["approval"] == "Not reviewed",
              "a cited draft is verified, shown as the model's and not yet reviewed")
        check("[[" not in r["text"] and len(r["citations"]) == 3 and not r["unresolved"], "citation markers are removed and listed")
        check("nothing is submitted" in r["label"], "the label says nothing is submitted until a person approves and submits it")
        _final(observed, "funding_draft", r)
        rec = _record(store, r)
        check(rec.get("ai_output") and rec.get("workflow_output") and rec.get("task") == "funding_draft",
              "the comparison record keeps both outputs")
        funding = store.cases["T-1"]["funding"]
        check(funding["draft"] == r["text"] and funding["status"] == "Draft ready" and not funding.get("reference"),
              "the draft is saved as Draft ready and nothing is approved or submitted")
        script["out"] = "Needs: costs [[Address: 99 Elsewhere Road]]"
        wrong = store.funding_draft(OWNER, "T-1")
        check(not wrong["verified"] and wrong["unresolved"] and "Unverified" in wrong["label"],
              "a citation the case does not have leaves the draft Unverified")
        script["out"] = "Needs: costs from the contractor"
        bare = store.funding_draft(OWNER, "T-1")
        check(not bare["verified"] and "Unverified" in bare["label"], "a draft with no citation is Unverified")
        script["out"] = "A free-form note with no list of what is needed"
        refused = store.funding_draft(OWNER, "T-1")
        check(refused["source"] == "template" and refused["text"].startswith("Funding application draft"),
              "an answer that fails the draft check falls back to the template")
        calls = script["calls"]
        script["out"] = "Needs: costs [[Address: T-1 Eval Road]]"
        wf = store.funding_draft(OWNER, "T-1", mode="workflow")
        wrec = _record(store, wf)
        check(script["calls"] == calls, "workflow-only mode must not call the model")
        check(wf["source"] == "template" and wf["mode"] == "workflow-only" and wf["verified"],
              "workflow-only returns the verified template")
        check(wrec.get("ai_output") is None and wrec.get("workflow_output") and wrec.get("fallback_reason") == "workflow-only mode selected",
              "the comparison record keeps the workflow-only output and the reason")
        latest = wf["record_id"]  # an earlier draft is stale once a later draft changes the case's funding facts
        try:
            store.review_ai(OTHER, latest, "accept")
            check(False, "another user must not review someone else's draft")
        except PermissionError:
            pass
        try:
            store.review_ai(OWNER, latest, "reject", "")
            check(False, "reject without a reason must be refused")
        except ValueError:
            pass
        store.review_ai(OWNER, latest, "accept")
        check(_record(store, wf).get("status") == "Accepted", "the owner's answer is recorded")
        check(store.cases["T-1"]["funding"]["status"] != "Submitted" and not store.cases["T-1"]["funding"].get("reference"),
              "accepting the review does not submit anything")
        check(_ranking(store) == rank0 and _without(store, "funding") == rest0, "a funding draft must not change ranking or any other case data")
        check(store.verify_audit(), "audit chain must verify")
    except Exception as e:
        fails.append(f"funding draft: unexpected {type(e).__name__}: {e}")
    return fails


def run_document_checks(workdir, observed=None):
    """Document reading on a constructed public text fixture: cited note, comparison record, workflow-only and unread types.

    The note is a filing aid; nothing is extracted into the case. Only the stored document summary changes.
    """
    fails = []

    def check(ok, what):
        if not ok:
            fails.append(f"document reading: {what}")
    try:
        store, script = _isolated_store(workdir, observed)
        doc = store.add_document(OWNER, "T-1", PUBLIC_DOCUMENT["name"], PUBLIC_DOCUMENT["kind"], PUBLIC_DOCUMENT["data"],
                                 metadata=dict(PUBLIC_DOCUMENT["metadata"]))
        unread = store.add_document(OWNER, "T-1", UNREAD_DOCUMENT["name"], UNREAD_DOCUMENT["kind"], UNREAD_DOCUMENT["data"],
                                    metadata=dict(UNREAD_DOCUMENT["metadata"]))
        rank0, rest0 = _ranking(store), _without(store, "documents")
        script["out"] = "A constructed public note about loft insulation depth for a mid terrace home."
        r = store.read_document(OWNER, "T-1", doc["id"])
        check(r["source"] == "ai" and r["mode"] == "ai" and r["verified"] and r["approval"] == "Not reviewed",
              "a note on a clean text file is verified, shown as the model's and not yet reviewed")
        check(r["citations"] == [f"Document: {doc['name']}"], "the note cites the document it describes")
        check(script["sent"] and PUBLIC_DOCUMENT["data"].decode() in script["sent"][2],
              "the scripted model received the constructed document text")
        _final(observed, "read_document", r)
        rec = _record(store, r)
        check(rec.get("ai_output") and rec.get("workflow_output") and rec.get("task") == "read_document",
              "the comparison record keeps both outputs")
        stored = next(d for d in store.cases["T-1"]["documents"] if d["id"] == doc["id"])
        check(stored["summary"] == r["text"], "the note is stored as the document summary only")
        calls = script["calls"]
        wf = store.read_document(OWNER, "T-1", doc["id"], mode="workflow")
        check(script["calls"] == calls, "workflow-only mode must not call the model")
        check(wf["source"] == "template" and wf["mode"] == "workflow-only", "workflow-only returns the template note")
        skipped = store.read_document(OWNER, "T-1", unread["id"])
        check(script["calls"] == calls and skipped["source"] == "template" and "not read" in skipped["text"],
              "a file type that is not read stays a template note and never reaches the model")
        check(_ranking(store) == rank0 and _without(store, "documents") == rest0,
              "reading a document must not change ranking or any other case data")
        check(store.verify_audit(), "audit chain must verify")
    except Exception as e:
        fails.append(f"document reading: unexpected {type(e).__name__}: {e}")
    return fails


def summarise(results):
    ms = [r["measures"] for r in results if r.get("measures") and "review" in r["measures"]]
    ai = [m for m in ms if m.get("source") == "ai"]
    runs = [run for m in ms for run in m["run_results"]]
    lat = [run["latency_ms"] for run in runs]
    cites = [c for m in ms for c in m.get("cites", [])]
    rv = {"accept": 0, "edit": 0, "reject": 0}
    reasons = []
    for m in ms:
        a = m["review"]
        rv[a["action"]] += 1
        if a["reason"]:
            reasons.append(dict(action=a["action"], reason=a["reason"]))
    rec = [m["recall"] for m in ai if "recall" in m]
    return dict(
        mean_overlap=_mean([m["overlap"] for m in ms]), mean_spearman=_mean([m["spearman"] for m in ms]),
        priority_scenarios=len(ms),
        ai_scenarios=sum(any(r["source"] == "ai" for r in m["run_results"]) for m in ms),
        template_scenarios=sum(any(r["source"] == "template" for r in m["run_results"]) for m in ms),
        recommendation_runs=len(runs),
        ai_runs=sum(r["source"] == "ai" for r in runs),
        template_runs=sum(r["source"] == "template" for r in runs),
        quality_scope="overlap, Spearman and recall use the final recommendation per scenario; critical and citation checks cover every recommendation run",
        critical_misses=sum(m["critical_misses"] for m in ms),
        deterministic_critical_misses=sum(m["deterministic_critical_misses"] for m in ms),
        citation_validity=round(sum(cites) / len(cites), 3) if cites else None, cited_facts=len(cites),
        variation=[dict(scenario=r["name"], runs=r["measures"]["runs"], distinct_orders=r["measures"]["distinct_orders"],
                        pairwise_overlap=r["measures"].get("pairwise_overlap"), pairwise_spearman=r["measures"].get("pairwise_spearman"))
                   for r in results if r.get("measures") and r["measures"].get("runs", 0) > 1],
        latency_ms=dict(mean=_mean(lat), max=max(lat) if lat else None, runs=len(lat)),
        models=sorted({r["model"] for r in runs if r["model"]}),
        prompt_versions=sorted({r["prompt_version"] for r in runs if r["prompt_version"]}),
        reviewer=dict(counts=rv, reasons=reasons),
        added_value=dict(scenarios=len(rec),
                         ai_minus_deterministic=_mean([x["ai"] - x["deterministic"] for x in rec]),
                         ai_minus_workflow_only=_mean([x["ai"] - x["workflow_only"] for x in rec]),
                         note="recall of the cases a person said must surface, AI minus the other order, on the same cases"))


# Items this offline harness cannot establish. Recorded, never invented.
OPEN_ITEMS = (
    "Foundry model names, versions and quotas are not confirmed in the chosen Azure region (owner or Azure retrieval needed)",
    "no live-model run: actual calls need a separate finite call, token, budget and expiry authorisation and serving attestation",
    "no independently labelled held-out split, approved thresholds or cohort sample sizes exist yet (owner decision)",
    "no authorised human participant protocol has run; role agents are not participant substitutes",
    "effort and cost comparison against manual/template and rules alternatives needs Finance validation",
)


def evidence_gate(raw, summary, scripted=True, coverage=None):
    """Frozen-input hashes, per-task coverage and the claims this run may and may not support."""
    ms = summary["models"]
    live = bool(ms) and not scripted
    return dict(
        golden_sha256=hashlib.sha256(raw).hexdigest(), prompt_version=ai_tasks.PROMPT_VERSION,
        provider="scripted" if scripted else "live", serving_models=ms,
        actual_model_evaluation="evaluated" if live else "not evaluated (scripted provider)",
        human_effectiveness="not evaluated (no authorised participants)",
        calibration="not applicable (no meaningful scored predictions)",
        benefit_claim="not permitted (no calibrated actual-model or human results)",
        task_coverage=coverage if coverage is not None else task_coverage([]),
        critical_misses=summary["critical_misses"], open_items=list(OPEN_ITEMS))


def cohort_report():
    """Per-cohort record for the deterministic ranking; AI-task cohorts are not yet evaluated."""
    rec = cohort_ranking_eval.run()
    dims = {d: {label: dict(n=row["n"], errors=row["errors"], review_burden=row["review_burden"],
                            sufficient=row["sufficient"]) for label, row in body["cohorts"].items()}
            for d, body in rec["dimensions"].items()}
    return dict(task_id=rec["task_id"], status=rec["status"], activation_allowed=rec["activation_allowed"],
                synthetic=rec["synthetic"], fairness_evidence=rec["fairness_evidence"], total_cases=rec["total_cases"],
                dimensions=dims, blockers=sorted({b["code"] for b in rec["blockers"]}), record_hash=rec["record_hash"],
                ai_task_cohorts="not evaluated (no approved AI-task cohort manifest)",
                note="synthetic, unapproved developer fixture (OQ-018); not fairness evidence and never averaged across cohorts")


def run_eval(golden=GOLDEN):
    with open(golden, "rb") as f:
        raw = f.read()
    spec = json.loads(raw.decode("utf-8"))
    results = []
    observed = []
    for sc in spec["scenarios"]:
        with tempfile.TemporaryDirectory() as tmp:
            fails, measures = run_scenario(copy.deepcopy(sc), tmp, observed)
        results.append(dict(name=sc["name"], passed=not fails, failures=fails, measures=measures))
    with tempfile.TemporaryDirectory() as tmp:
        fails = run_task_checks(tmp, observed)
    results.append(dict(name="text tasks: citations, Unverified, workflow-only, comparison record, review, funding draft, document reading",
                        passed=not fails, failures=fails, measures=None))
    summary = summarise(results)
    coverage = task_coverage(observed)
    return dict(version=spec["version"], prompt_version=ai_tasks.PROMPT_VERSION, scenarios=len(results),
                passed=all(r["passed"] for r in results) and summary["critical_misses"] == 0
                and not coverage["failures"] and not coverage["namespace_errors"],
                results=results, summary=summary, evidence=evidence_gate(raw, summary, coverage=coverage), cohorts=cohort_report())


def main(argv=None):
    rep = run_eval()
    if "--json" in (sys.argv[1:] if argv is None else argv):
        print(json.dumps(rep, indent=2))
        return 0 if rep["passed"] else 1
    for r in rep["results"]:
        print(("PASS " if r["passed"] else "FAIL ") + r["name"])
        for f in r["failures"]:
            print("   - " + f)
    print(f"{sum(r['passed'] for r in rep['results'])} of {rep['scenarios']} scenarios passed")
    s = rep["summary"]
    print(f"priority recommendations: {s['recommendation_runs']} runs ({s['ai_runs']} AI-sourced, {s['template_runs']} template/fallback), across {s['priority_scenarios']} scenarios; not provider-call counts")
    print(f"prompt version {rep['prompt_version']}; models {', '.join(s['models']) or 'none (scripted)'}")
    print(f"top-k overlap {s['mean_overlap']}, Spearman vs deterministic {s['mean_spearman']}")
    print(f"critical misses {s['critical_misses']} (deterministic order: {s['deterministic_critical_misses']}); citation validity {s['citation_validity']} over {s['cited_facts']} cited facts")
    print(f"latency per run ms: mean {s['latency_ms']['mean']}, max {s['latency_ms']['max']}")
    for v in s["variation"]:
        print(f"variation: {v['runs']} runs, {v['distinct_orders']} distinct orders, pairwise overlap {v['pairwise_overlap']}, Spearman {v['pairwise_spearman']} ({v['scenario']})")
    print(f"reviewer answers {s['reviewer']['counts']}")
    av = s["added_value"]
    print(f"added value on {av['scenarios']} scenarios: AI minus deterministic {av['ai_minus_deterministic']}, AI minus workflow-only {av['ai_minus_workflow_only']}")
    ev = rep["evidence"]
    print(f"golden sha256 {ev['golden_sha256'][:12]}; actual model: {ev['actual_model_evaluation']}; calibration: {ev['calibration']}")
    print(f"benefit claim: {ev['benefit_claim']}")
    tc = ev["task_coverage"]
    print(f"task coverage ({len(tc['tasks'])} registered): " + "; ".join(f"{n} {s.split(' (')[0]}" for s, n in tc["counts"].items()))
    for task_id, row in tc["tasks"].items():
        print(f"   {task_id}: {row['status'].split(' (')[0]}")
    print("task coverage note: " + tc["note"])
    co = rep["cohorts"]
    print(f"cohorts (ranking, synthetic): status {co['status']}, activation allowed {co['activation_allowed']}, fairness evidence {co['fairness_evidence']}; AI-task cohorts {co['ai_task_cohorts']}")
    for o in ev["open_items"]:
        print("open: " + o)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
