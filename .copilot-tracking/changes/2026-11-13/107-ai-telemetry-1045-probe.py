import json, sys, tempfile
from pathlib import Path

sys.path.insert(0, "src/core/tests")
import dataset
import test_ai_consumption as T
from zava_forward.core import assistants as A
from zava_forward.core.ai_consumption import CallContext, Consumption, reference
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import MAX_QUESTION_CHARS, ChatPanel, ModelReply
from zava_forward.core.store import Store

S = ["SENTINEL_RAW_CASE_NOTE_991", "SENTINEL_RESIDENT_MSG_992", "SENTINEL_DOC_BODY_993"]
hits, checks = [], []
identity_passthrough = []


def scan(label, obj):
    text = json.dumps(obj, default=str, sort_keys=True)
    for s in S:
        if s in text:
            hits.append((label, s))
    checks.append((label, len(text)))
    return text


def check(name, cond):
    checks.append((name, bool(cond)))
    if not cond:
        hits.append(("ASSERT-FAILED", name))


caps = list(A.REGISTRY)
check("five assistants", len(caps) == 5)
work = tempfile.mkdtemp()
port = T.Port(Path(work) / "probe.sqlite")
led = Consumption(port)
price = led.price(source="https://prices.azure.com/api/retail/prices", source_hash=reference("p"),
                  retrieved=T.START, version="v1", model=T.MODEL, currency="USD", start=T.START, end=T.END,
                  input_rate="1", output_rate="2", cached_rate="0.5", synthetic=True)
for cap in caps:
    cfg = reference("cfg-" + cap)
    led.authorize(authority="a-" + cap, owner="o", evidence="e", price=price, capability=cap, configuration=cfg,
                  start=T.START, end=T.END, max_calls=2, max_depth=2,
                  budgets=[dict(id=reference("period"), calls=100, tokens=10**6, amount="100"),
                           dict(id=reference("task-" + cap), calls=100, tokens=10**6, amount="100")])
    root = reference(S[0] + cap)
    ctx = CallContext(root, reference(S[1] + cap), cap, "retrofit-case", cfg, reference(S[2]))
    rid = led.reserve(ctx, T.MODEL, 1000, 100)
    raw = dict(prompt_tokens=100, completion_tokens=20, total_tokens=120, cached_tokens=10,
               text=S[0], note=S[1], prompt_tokens_details=None, extra=S[2])
    led.complete(rid, raw, T.MODEL, "returned")
    led.output(root, S[2] + cap, eligible=True)
    led.review(S[2] + cap, "accept")
    for bad in S:
        try:
            CallContext(bad, bad, cap, "retrofit-case", cfg, bad).metadata()
            check("raw root refused " + bad, False)
        except ValueError:
            check("raw root refused " + bad, True)
with port.transaction() as db:
    records = led._read(db)
scan("ledger-events", records)
rep = led.report(start=T.START, end=T.END, as_of=T.END)
scan("report", rep)
by = rep["by_capability"]
check("per-assistant attribution", sorted(by) == sorted(caps))
check("per-accepted-proposal tokens", all(v["accepted_proposals"] == 1 and v["tokens_per_accepted_proposal"] == "120" for v in by.values()))
check("completed events nonzero tokens", sum(1 for r in records if r["kind"] == "completed" and r["tokens"]["total_tokens"] == 120) == 5)

mismatch = led.reserve(CallContext(reference("m"), reference("m"), caps[0], "retrofit-case", reference("cfg-" + caps[0]), reference("p")), T.MODEL, 1000, 100)
led.complete(mismatch, dict(prompt_tokens=1, completion_tokens=1, total_tokens=2), S[0], "returned")
with port.transaction() as db:
    scan("ledger-after-sentinel-model", led._read(db))

lim = A.Limits()
for cap in caps:
    task = dict(capability=cap, version="1", case_id="ZF-1", source_signature="s", snapshot={})
    result = dict(provider="azure", deployment="dep", model=T.MODEL, outcome="returned", source="ai",
                  usage=dict(prompt_tokens=5, completion_tokens=2, total_tokens=7, text=S[0]),
                  text=json.dumps(dict(summary=S[0], body=S[1], doc=S[2])), meter_id=S[0], leak=S[1])
    env, out, fail = A.shape_result(task, result, lim)
    scan("envelope-" + cap, env)
    check("envelope usage kept " + cap, env["usage"] == dict(prompt_tokens=5, completion_tokens=2, total_tokens=7, cached_tokens=None))
    idr = dict(result, provider=S[0], model=S[2])
    idenv = A.shape_result(task, idr, lim)[0]
    identity_passthrough.append((cap, S[0] in json.dumps(idenv), S[2] in json.dumps(idenv)))
    check("failure text generic " + cap, out is not None or (fail and not any(s in fail for s in S)))

path = Path(work) / "syn.json"
path.write_text(json.dumps(dataset.DATA))
store = Store(str(path))
user = store.data["staff"][0]
iso = ChatIsolation(store, env=dict(CHAT_DPIA_REF="SYN-DPIA", CHAT_LAWFUL_BASIS_REF="SYN-BASIS", CHAT_NOTICE_REF="SYN-NOTICE"))
calls = []


def model(system, prompt):
    calls.append(prompt)
    return ModelReply("{}", usage=dict(prompt_tokens=10, completion_tokens=3, total_tokens=13), calls=1)


panel = ChatPanel(iso, model)
tid = store.chat_create_thread(user)["id"]
r1 = panel.ask(user, tid, "Question " + " ".join(S), skill="general")
scan("chat-turn-reply-receipt", {k: v for k, v in r1.items() if k == "consumption"})
check("chat model ran", len(calls) == 1)
check("chat receipt present", isinstance(r1.get("consumption"), dict))
r2 = panel.ask(user, tid, ("x" * (MAX_QUESTION_CHARS + 1)) + S[0], skill="general")
scan("chat-limit-fallback-receipt", {k: v for k, v in r2.items() if k == "consumption"})
check("limit fallback model not called", len(calls) == 1)
scan("chat-audit-entries", [e for e in store.audit_entries() if str(e.get("action", "")).startswith("chat.")])
print("meter_root in chat receipt:", bool((r1.get("consumption") or {}).get("meter_root")))
print("chat receipt keys:", sorted((r1.get("consumption") or {})))
print("limit receipt keys:", sorted((r2.get("consumption") or {})))
print("INFO identity-field (provider/model) passthrough, not a content channel:", identity_passthrough)
print("checks:", len(checks), "hits:", hits)
sys.exit(1 if hits else 0)
