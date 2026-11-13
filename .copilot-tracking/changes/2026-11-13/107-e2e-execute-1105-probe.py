"""Offline probe for #107: Assistants.execute end to end plus tariff-enabled ChatPanel, with a leak scan."""
import json
import sqlite3
import sys
import uuid

sys.path.insert(0, ".")
from test_ai_consumption_api import END, START, ConsumptionApi  # noqa: E402
from test_assistants import proposal  # noqa: E402
from zava_forward.core import assistants as A  # noqa: E402
from zava_forward.core.ai_consumption import reference  # noqa: E402
from zava_forward.core.chat_panel import TASK  # noqa: E402

N = uuid.uuid4().hex[:8]
S = dict(note=f"SENT-NOTE-{N}", doc=f"SENT-DOC-{N}", addr=f"SENT-ADDR-{N}",
         resp=f"SENT-RESP-{N}", chat_user=f"SENT-CHAT-USER-{N}", chat_reply=f"SENT-CHAT-REPLY-{N}")


def hits(text, names=None):
    return {k: text.count(v) for k, v in S.items() if (names is None or k in names) and v in text}


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


fx = ConsumptionApi("authority")
fx.setUp()
out = dict(sentinels=sorted(S), capabilities={}, chat={}, leaks={})
try:
    svc, pm, cons = fx.service, fx.pm, fx.service.consumption

    def seed(c):
        c["resident"]["note"] = S["note"]
        c["resident"]["adjustment"] = S["note"]
        c["handoff"]["note"] = S["note"]
        c["home"]["address"] = S["addr"]
        c["documents"] = [dict(id="SURVEY-1", kind="Survey", name=S["doc"], summary=S["doc"],
                               content_sha256="abc", version=1)]

    fx.fixture.case(seed)
    caps = sorted(A.REGISTRY)
    accepted, executed = set(), set()
    for cap in caps:
        fx.authority(cap)

        def reply(snapshot):
            value = proposal(snapshot)
            value["summary"] = f"Check supplied evidence. {S['resp']}"
            return value
        fx.response_text = A.canonical(reply({}))
        before = len(fx.requests)
        task = fx.fixture.run_ready(cap)
        executed.add(cap)
        sent = json.dumps(fx.requests[before:])
        check(len(fx.requests) == before + 1, f"{cap}: expected one provider request")
        check(S["addr"] in sent, f"{cap}: captured address sentinel never reached the provider")
        check(S["note"] not in sent and S["doc"] not in sent, f"{cap}: excluded content reached the provider")
        verified = svc.review(pm, task["id"], "verify", task["revision"], "Compared every cited source.",
                              source_verified=True)
        final = svc.review(pm, task["id"], "accept", verified["revision"], "Accepted after human check.")
        check(final["state"] == "accepted", f"{cap}: state {final['state']}")
        accepted.add(cap)
        env = final["envelope"]
        root = reference(task["id"])
        records = fx.records()
        res = [r for r in records if r["kind"] == "reserved" and r["id"] == env["meter_id"]]
        com = [r for r in records if r["kind"] == "completed" and r["id"] == env["meter_id"]]
        outp = [r for r in records if r["kind"] == "output" and r["root"] == root]
        rev = [r for r in records if r["kind"] == "review" and r["output"] == root and r["action"] == "accept"]
        check(len(res) == len(com) == len(outp) == len(rev) == 1, f"{cap}: join cardinality")
        check(res[0]["capability"] == cap and res[0]["root"] == root == env["meter_root"], f"{cap}: root/capability")
        check(res[0]["attempt"] == reference(f"{task['id']}:{task['fence']}"), f"{cap}: attempt")
        check(res[0]["configuration"] == env["configuration"] and res[0]["prompt"] == env["prompt_hash"], f"{cap}: cfg/prompt")
        check(com[0]["tokens"] == env["usage"], f"{cap}: tokens")
        check((env["usage"]["total_tokens"], env["usage"]["cached_tokens"]) == (120, 10), f"{cap}: usage values")
        check(outp[0]["eligible"] is True and outp[0]["output"] == root, f"{cap}: output eligibility")
        check(S["resp"] in json.dumps(final.get("output", final)), f"{cap}: response sentinel absent from task output")
        out["capabilities"][cap] = dict(meter_id=env["meter_id"][:12], root=root[:12], tokens=env["usage"]["total_tokens"],
                                        review_revision=rev[0]["revision"])
        check(hits(json.dumps(env)) == {}, f"{cap}: envelope leak {hits(json.dumps(env))}")
    check(executed == accepted == set(A.REGISTRY), "coverage differs from REGISTRY")

    rep_a = cons.report(start=START, end=END, as_of=END)
    check(rep_a["accepted_proposals"] == len(caps), f"accepted {rep_a['accepted_proposals']}")
    for cap in caps:
        m = rep_a["by_capability"][cap]
        check((m["calls"], m["proposals"], m["accepted_proposals"], m["total_tokens"], m["tokens_per_accepted_proposal"])
              == (1, 1, 1, 120, "120"), f"{cap}: by_capability {m}")
    check(rep_a["unjoined_outputs"] == 0 and rep_a["unjoined_reviews"] == 0, "unjoined rows")

    fx.store.ai = fx.inner
    fx.authority(TASK)
    panel = fx.chat_panel(fx.store)
    thread = fx.store.chat_create_thread(pm, "ZF-1")
    fx.response_text = json.dumps(dict(answer=f"Check the case stage. {S['chat_reply']}", citations=["ZF-1/stage"]))
    before = len(fx.requests)
    answer = panel.ask(pm, thread["id"], f"What is the stage? {S['chat_user']}")
    check(answer["kind"] == "answer", f"chat kind {answer['kind']}")
    check(len(fx.requests) == before + 1 and S["chat_user"] in json.dumps(fx.requests[before:]), "chat request content")
    receipt = answer["consumption"]
    check(bool(receipt.get("meter_root")) and receipt["model_calls"] == 1, "chat meter_root/model_calls")
    records = fx.records()
    latest = [r for r in records if r["kind"] == "reserved"][-1]
    check(latest["capability"] == TASK and latest["root"] == receipt["meter_root"] and latest["id"] == receipt["meter_id"], "chat join")
    msgs = fx.store.chat_resume(pm, thread["id"])["messages"]
    chat_out = next(r for r in records if r["kind"] == "output" and r["root"] == latest["root"])
    check(chat_out["output"] == reference(f"chat:{thread['id']}:{msgs[-1]['seq']}") and chat_out["eligible"] is False, "chat output join")
    check(S["chat_reply"] in json.dumps(msgs), "chat reply sentinel absent from thread")
    rep_b = cons.report(start=START, end=END, as_of=END)
    check(rep_b["accepted_proposals"] == len(caps), "chat changed accepted count")
    check(rep_b["by_capability"].get(TASK, {}).get("accepted_proposals", 0) == 0, "chat accepted")
    check(rep_b["calls"] == len(caps) + 1, f"calls {rep_b['calls']}")
    out["chat"] = dict(meter_root=receipt["meter_root"][:12], tokens=receipt["tokens"], eligible=chat_out["eligible"],
                       ledger_rows=len(records), by_capability=rep_b["by_capability"].get(TASK))

    db = sqlite3.connect(fx.fixture.dbpath)
    tables = [r[0] for r in db.execute("select name from sqlite_master where type='table'")]
    domain = {"cases", "chat_message", "chat_thread", "chat_memory", "chat_memory_control", "recommendations", "staff", "meta"}
    per_table = {}
    for t in tables:
        dump = json.dumps([[x.decode("utf8", "replace") if isinstance(x, bytes) else x for x in row]
                           for row in db.execute(f"select * from {t}")], default=str)
        per_table[t] = hits(dump)
    out["leaks"]["per_table_hits_informational"] = {k: v for k, v in per_table.items() if v}
    for t in tables:
        if t in domain or t in ("assistant_tasks", "assistant_events"):
            continue
        check(per_table[t] == {}, f"leak in table {t}: {per_table[t]}")
    nonledger = 0
    for tid, body in db.execute("select task_id, body from assistant_events"):
        b = json.loads(body)
        if tid == "ai-consumption":
            check(hits(body) == {}, f"ledger leak {hits(body)}")
            nonledger += 0
        else:
            b.pop("output", None)
            check(hits(json.dumps(b)) == {}, f"event leak {tid} {hits(json.dumps(b))}")
            nonledger += 1
    ledger_rows = db.execute("select count(*) from assistant_events where task_id='ai-consumption'").fetchone()[0]
    audit_rows = db.execute("select count(*) from audit").fetchone()[0]
    check(ledger_rows > 0 and audit_rows > 0 and nonledger > 0, "empty ledger/audit/events")
    for t in db.execute("select id, body from assistant_tasks"):
        body = json.loads(t[1])
        check(hits(json.dumps(body.get("envelope", {}))) == {}, f"task envelope leak {t[0]}")
    check(hits(json.dumps(rep_a, default=str) + json.dumps(rep_b, default=str)) == {}, "report leak")
    check(hits(json.dumps(receipt, default=str)) == {}, "chat receipt leak")
    out["leaks"].update(ledger_rows=ledger_rows, audit_rows=audit_rows, nonledger_events=nonledger,
                        report_calls=rep_b["calls"], report_accepted=rep_b["accepted_proposals"])
    print(json.dumps(out, indent=1, default=str))
    print("PROBE-OK")
finally:
    fx.doCleanups()
