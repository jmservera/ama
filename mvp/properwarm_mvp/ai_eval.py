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
* the run and each answer are in the audit ledger and the chain verifies.

Run: cd mvp && PYTHONPATH=. python3 -m properwarm_mvp.ai_eval
"""
import copy
import json
import os
import sys
import tempfile
from pathlib import Path

from .store import Store

GOLDEN = Path(__file__).resolve().parents[1] / "evals" / "ai_priority_golden.json"
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


def run_scenario(sc, workdir):
    fails = []
    try:
        _run(sc, workdir, fails)
    except Exception as e:  # an unexpected error is itself a failed check
        fails.append(f"unexpected {type(e).__name__}: {e}")
    return fails


def _run(sc, workdir, fails):
    data = dict(staff=[OWNER, OTHER], cases=[build_case(c) for c in sc["cases"]])
    p = Path(workdir) / "eval.json"
    p.write_text(json.dumps(data))
    store = Store(str(p), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl"))
    out = sc["model_output"]
    if out is not None:
        store.ai.endpoint = "http://scripted-model.invalid"
        store.ai._chat = lambda *a, **k: out
    rank0, state0 = _ranking(store), _state(store)
    ids = {c["id"] for c in sc["cases"]}
    rec = store.ai_priority(OWNER, sc["n"])
    got = [i["case_id"] for i in rec["items"]]

    def check(ok, what):
        if not ok:
            fails.append(what)
    check(rec["status"] == "Proposed", "recommendation must start as Proposed")
    check(rec["label"] == Store.REC_LABEL, "recommendation must be labelled AI-drafted, human-approved")
    check(set(got) <= ids and len(set(got)) == len(got) and got, "only listed case ids, no duplicates")
    check(all(i["reason"].strip() for i in rec["items"]), "every item needs a reason")
    check(not any("sent" in i["reason"].lower() and "not" not in i["reason"].lower() for i in rec["items"]), "no claim that something was sent")
    exp = sc["expect"]
    if "source" in exp:
        check(rec["source"] == exp["source"], f"source should be {exp['source']}, was {rec['source']}")
    if "validated" in exp:
        check(rec["validated"] == exp["validated"], "validated flag")
    if "ids_in_order" in exp:
        check(got == exp["ids_in_order"], f"ids {got} should be {exp['ids_in_order']}")
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
    store.resolve_priority(OWNER, rec["id"], "accept")
    check(_ranking(store) == rank0, "ranking changed after the person accepted")
    check(_state(store) == state0, "case data changed after the person accepted")
    actions = [e["action"] for e in store.audit_entries()]
    for needed in ("ai_run_start", "ai_run_end", "ai_priority_accept"):
        check(needed in actions, f"audit must contain {needed}")
    check(store.verify_audit(), "audit chain must verify")


def run_eval(golden=GOLDEN):
    with open(golden, encoding="utf-8") as f:
        spec = json.load(f)
    results = []
    for sc in spec["scenarios"]:
        with tempfile.TemporaryDirectory() as tmp:
            fails = run_scenario(copy.deepcopy(sc), tmp)
        results.append(dict(name=sc["name"], passed=not fails, failures=fails))
    return dict(version=spec["version"], scenarios=len(results), passed=all(r["passed"] for r in results), results=results)


def main():
    rep = run_eval()
    for r in rep["results"]:
        print(("PASS " if r["passed"] else "FAIL ") + r["name"])
        for f in r["failures"]:
            print("   - " + f)
    print(f"{sum(r['passed'] for r in rep['results'])} of {rep['scenarios']} scenarios passed")
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
