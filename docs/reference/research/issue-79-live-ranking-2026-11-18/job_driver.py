"""In-job driver for #79 (DEMO only). Runs inside a throwaway Container Apps job on the deployed API image.

Mirrors orchestrator.ranking_publish (not in the deployed image) using the deployed core runner.
The synthetic owner policy exists only in this process memory and is never written to the repository.
"""
import copy, datetime, hashlib, json, os, sys

from zava_forward.core import ranking, ranking_archive_blob, ranking_publication_runner as runner
from zava_forward.core.factory import open_store

def emit(label, obj):
    print("DEMO79", label, json.dumps(obj, sort_keys=True, default=str), flush=True)

store = open_store(os.environ)
with store.lock:
    cases = [copy.deepcopy(c) for c in store.cases.values()]
    as_of = store.as_of
cases = [c for c in cases if not c["closed"]]
emit("source", {"open_cases": len(cases), "as_of": as_of})
today = as_of
arch = ranking_archive_blob.open_ranking_archive(os.environ)
emit("archive_container", os.environ.get("ZF_RANKING_BLOB_CONTAINER"))

def brief(res):
    keys = ("operation", "status", "written", "as_of", "published_on", "source_current", "total", "policy", "problems", "refusals", "archive_name", "snapshot_hash", "latest", "count")
    return {k: res.get(k) for k in keys if k in res}

emit("unsigned_shipped_policy", brief(runner.run("publish", arch, today, cases=cases, as_of=as_of)))
emit("verify_after_refusal", brief(runner.run("verify", arch, today)))

pol = copy.deepcopy(ranking.POLICY_V1)
pol["owner"] = "DEMO-ONLY synthetic owner"
pol["signoff"] = dict(signed_by=pol["owner"], signed_on=today, rule_order_hash=ranking.rule_order_hash(pol))
pol["content_hash"] = ranking.policy_hash(pol)
reg = {pol["version"]: pol}
emit("demo_policy", {"owner": pol["owner"], "is_signed": ranking.is_signed(pol), "rule_order_hash": ranking.rule_order_hash(pol), "content_hash": pol["content_hash"]})

first = runner.run("publish", arch, today, cases=cases, as_of=as_of, registry=reg)
emit("publish_1", brief(first))
second = runner.run("publish", arch, today, cases=cases, as_of=as_of, registry=reg)
emit("publish_2_repeat", brief(second))
emit("verify", brief(runner.run("verify", arch, today, registry=reg)))
emit("schedule", brief(runner.run("schedule", arch, today, registry=reg)))
emit("rank_determinism", {"two_snapshots_equal": ranking.snapshot(cases, pol, as_of)["snapshot_hash"] == ranking.snapshot(list(reversed(cases)), pol, as_of)["snapshot_hash"]})
