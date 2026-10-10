"""Measured fictional HTTP workloads and clean backup, not full PRD/RPO acceptance."""
from __future__ import annotations

import argparse
import itertools
import base64
from concurrent.futures import ThreadPoolExecutor
from http.cookiejar import CookieJar
from http.server import ThreadingHTTPServer
import json
from hashlib import sha256
import math
import os
from pathlib import Path
import sqlite3
import threading
import time
import urllib.request
from unittest.mock import patch

from properwarm_mvp.factory import open_store
from properwarm_mvp.server import App, make_handler
from properwarm_mvp import exercise
from properwarm_mvp.sqlstore import SqlStore


def data_contract_check(state: Path, output: Path) -> int:
    """Measure real 500-row import and 25-case batch on the separate scale fixture."""
    from test_exercise_data import workbook
    with patch.dict(os.environ, {"PW_EXERCISE": "1", "PW_AI": "off", "PW_STATE": str(state)}, clear=True):
        store = SqlStore(str(state / "scale.json"), str(state / "properwarm.sqlite"))
        try:
            if len(store.cases) != 60_000 or any(
                    not c.get("exercise") or not c["id"].startswith(("EX-SCALE-HOME-", "EX-HOME-"))
                    for c in store.cases.values()):
                raise ValueError("Data probe requires the named wholly fictional 60,000-home fixture.")
            actor = next(u for u in store.staff.values() if u["code"] == "EX-PSO-01")
            ids = [f"EX-SCALE-HOME-{i:06d}" for i in range(59_501, 60_001)]
            controlled_keys = ("home", "resident", "decision", "hazards", "funding", "funding_ok", "finance",
                               "forms", "measure_decisions", "technical", "quality")
            baseline = {cid: {key: store.cases[cid].get(key) for key in controlled_keys} for cid in ids}
            baseline = json.loads(json.dumps(baseline))
            raw = workbook([[cid, "Fictional 500-row source coordination", "2026-10-12"] for cid in ids])
            digest = sha256(raw).hexdigest()
            start = time.perf_counter()
            preview = store.exercise_data_action(actor, dict(action="import-preview", filename="exercise500.xlsx",
                fields=["coordination_note", "task_due_date"], reason="Independent exact 500-row input probe"),
                workbook=raw)
            elapsed = time.perf_counter() - start
            if len(preview["rows"]) != 500 or any(row["status"] != "ready" for row in preview["rows"]):
                raise AssertionError("Exactly 500 independent known rows must be ready.")
            commit = store.exercise_data_action(actor, dict(action="commit", token=preview["token"],
                input_hash=preview["input_hash"],
                expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]}))
            if commit["committed"] != 500 or commit["errors"]:
                raise AssertionError("Every selected 500-row outcome must succeed independently.")
            bulk = store.exercise_data_action(actor, dict(action="bulk-preview", case_ids=ids[-25:],
                changes={"coordination_note": "Fictional explicit 25-case bulk"},
                reason="Exact selected 25-case coordination-only batch"))
            result = store.exercise_data_action(actor, dict(action="commit", token=bulk["token"],
                input_hash=bulk["input_hash"],
                expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in bulk["rows"]}))
            current = {cid: {key: store.cases[cid].get(key) for key in controlled_keys} for cid in ids}
            unchanged = current == baseline
            source_same = digest == sha256(raw).hexdigest()
            intact = store.verify_ledger()["intact"]
            passed = elapsed <= 10 and result["committed"] == 25 and not result["errors"] and unchanged and source_same and intact
            evidence = dict(kind="exact-fictional-data-contract", import_rows=500, import_preview_seconds=elapsed,
                import_committed=commit["committed"], bulk_selected=25, bulk_committed=result["committed"],
                source_sha256=digest, source_bytes_unchanged=source_same, controlled_fields_unchanged=unchanged,
                audit_intact=intact, result="Pass" if passed else "Fail",
                boundary="Separate Store-level scale-fixture probe, not the concurrent HTTP core import path")
            output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(evidence))
            return int(not passed)
        finally:
            store.db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=int, default=0, help="Optional five-session/two-writer steady run in seconds")
    parser.add_argument("--rate", type=float, default=5, help="Scheduled HTTP requests/second on scale, interactions/second on core")
    parser.add_argument("--scale", action="store_true", help="Generate separate fictional 60,000-home/600,000-event workload with twenty sessions")
    parser.add_argument("--mixed-core", action="store_true", help="Core session with 500-row HTTP import, 25-case batch, 20 documents and seeded events")
    parser.add_argument("--data-check", action="store_true", help="Probe 500-row/25-case data contracts in an existing caller scale-test directory")
    args = parser.parse_args()
    if args.mixed_core and (args.scale or args.duration < 1800):
        raise ValueError("Mixed core requires a separate at-least-1800-second non-scale run.")
    state = args.state.resolve()
    if args.data_check:
        return data_contract_check(state, args.output)
    if state.exists():
        raise SystemExit("Use a new explicit state directory; existing data is never removed.")
    results = {}
    with patch.dict(os.environ, {"PW_EXERCISE": "1", "PW_STATE": str(state), "PW_STORE": "sqlite",
                                  "PW_DOC_STORE": "local", "PW_AI": "off", "PW_PASSWORD": "fictional-local-only"}, clear=True):
        if args.scale:
            state.mkdir(parents=True)
            seed = state / "scale.json"
            baseline = exercise.dataset()
            traces = exercise.iter_scale_events()
            with seed.open("w", encoding="utf-8") as stream:
                stream.write('{"staff":' + json.dumps(baseline["staff"]) + ',"cases":[')
                for index, generated in enumerate(exercise.iter_scale_homes()):
                    case = baseline["cases"][index] if index < 2 else generated
                    events = [next(traces) for _ in range(10)]
                    for event in events:
                        event["home_id"] = case["id"]
                    case["exercise"]["scale_events"] = events
                    if index:
                        stream.write(",")
                    json.dump(case, stream)
                stream.write('],"as_of":' + json.dumps(exercise.AS_OF) + '}')
            os.environ["PW_AS_OF"] = exercise.AS_OF
            store = SqlStore(str(seed), str(state / "properwarm.sqlite"),
                             docs_dir=str(state / "docs"), digest_dir=str(state / "digests"))
            if len(store.cases) != 60_000 or sum(len(c["exercise"]["scale_events"]) for c in store.cases.values()) != 600_000:
                raise AssertionError("Scale population must have exactly 60,000 homes and 600,000 distinct linked traces.")
        elif args.mixed_core:
            state.mkdir(parents=True)
            seed = state / "mixed-core.json"
            baseline = exercise.dataset()
            extra = list(itertools.islice(exercise.iter_scale_homes(), 500))
            for home in extra:
                home["exercise"]["population"] = "core-import"
            baseline["cases"].extend(extra)
            seed.write_text(json.dumps(baseline), encoding="utf-8")
            os.environ["PW_AS_OF"] = exercise.AS_OF
            store = SqlStore(str(seed), str(state / "properwarm.sqlite"),
                             docs_dir=str(state / "docs"), digest_dir=str(state / "digests"))
            actor = next(u for u in store.staff.values() if u["code"] == "EX-PSO-01")
            document_limit = min(store.MAX_BYTES, 5_000_000)
            document = (b"Wholly fictional local evidence. " + b"x" * document_limit)[:document_limit]
            documents = [store.add_document(actor, "EX-HOME-001", f"fictional-{i}.txt", "Other", document)
                         for i in range(20)]
            for i in range(130):
                store.audit(actor["email"], "exercise_fixture_note", "EX-HOME-001",
                            f"Wholly fictional supplied historical coordination note {i}; no approval")
            store.save()
            results["core-fixture"] = dict(population=len(store.cases), import_targets=500,
                documents=len(documents), bytes_per_document=len(document),
                total_evidence_bytes=len(document) * len(documents), supplied_coordination_events=130,
                note="20 actual document-upload events plus 130 explicitly constructed audit notes; no approvals",
                result="Pass")
        else:
            store = open_store()
        app = App(store, password="fictional-local-only")
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        print(json.dumps({"phase": "listening", "loopback_port": server.server_port,
                          "population": len(store.cases)}), flush=True)
        client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

        def request(path, body=None, *, opener=client):
            data = json.dumps(body).encode() if body is not None else None
            req = urllib.request.Request(base + path, data=data, headers={"Content-Type": "application/json"})
            with opener.open(req, timeout=10) as response:
                return json.load(response)

        try:
            request("/api/login", {"email": "ex-pso-01@example.test", "password": "fictional-local-only"})
            operations = {
                "list": ("/api/cases?view=all&limit=50", None, 1),
                "detail": ("/api/cases/EX-HOME-001/exercise", None, 1),
                "dashboard": ("/api/exercise", None, 3),
                "write": ("/api/cases/EX-HOME-001/exercise",
                          {"action": "resident-update", "channel": "Phone", "evidence": "Fictional sampled coordination",
                           "next_update": "Named case team checks next weekday"}, 2),
            }
            if args.duration < 0 or args.rate <= 0 or args.rate > 20:
                raise ValueError("Duration must be nonnegative and rate in (0,20].")
            for name, (path, body, threshold) in operations.items() if not args.duration else ():
                request(path, body)
                samples = []
                for _ in range(200):
                    started = time.perf_counter()
                    request(path, body)
                    samples.append(time.perf_counter() - started)
                p95 = sorted(samples)[math.ceil(.95 * len(samples)) - 1]
                results[name] = {"samples": len(samples), "warm_http_p95_seconds": p95,
                                 "threshold_seconds": threshold, "result": "Pass" if p95 <= threshold else "Fail"}
            if args.duration:
                sessions = []
                roster = ("ex-pso-01", "ex-pso-02", "ex-pm-01", "ex-rc-01", "ex-rlo-01")
                session_count = 20 if args.scale else 5
                for session in range(session_count):
                    email = roster[session % len(roster)]
                    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
                    request("/api/login", {"email": email + "@example.test", "password": "fictional-local-only"}, opener=opener)
                    sessions.append(opener)
                samples = {name: [] for name in operations}
                failures = []
                session_locks = [threading.Lock() for _ in sessions]
                ids = sorted(cid for cid in store.cases if not args.mixed_core or cid.startswith("EX-SCALE-HOME-"))
                warm_start = time.perf_counter()
                for opener in sessions:
                    for path in (operations["list"][0], operations["detail"][0], operations["dashboard"][0]):
                        request(path, opener=opener)
                results["read-warmup"] = dict(requests=3 * session_count,
                    seconds=time.perf_counter() - warm_start, boundary="Explicit read warm-up; write first-use remains included",
                    result="Pass")
                started = time.perf_counter()

                def interaction_name(sequence):
                    session = sequence % session_count
                    cycle = sequence // session_count
                    return ("write" if session < 2 and cycle % (2 if args.scale else 5) == 0 else
                            "dashboard" if cycle % 10 == 1 else "detail" if cycle % 3 == 0 else "list")

                def interaction(sequence):
                    session = sequence % session_count
                    cycle = sequence // session_count
                    name = interaction_name(sequence)
                    path, body, _ = operations[name]
                    if name == "write":
                        cid = ids[(cycle // 5 * 2 + session) % len(ids)]
                        path = "/api/exercise/data"
                        body = dict(action="bulk-preview", case_ids=[cid],
                                    changes={"coordination_note": f"Fictional measured interaction {sequence}"},
                                    reason="Nonconsequential steady-session validation")
                    before = time.perf_counter()
                    try:
                        with session_locks[session]:
                            if args.mixed_core and sequence == 0:
                                from test_exercise_data import workbook
                                target_ids = [f"EX-SCALE-HOME-{i:06d}" for i in range(1, 501)]
                                raw = workbook([[cid, "Fictional core HTTP import", "2026-10-12"] for cid in target_ids])
                                source_hash = sha256(raw).hexdigest()
                                import_start = time.perf_counter()
                                preview = request("/api/exercise/data", dict(action="import-preview",
                                    filename="core500.xlsx", workbook_base64=base64.b64encode(raw).decode(),
                                    fields=["coordination_note", "task_due_date"],
                                    reason="Actual 500-row core HTTP import"), opener=sessions[session])
                                preview_seconds = time.perf_counter() - import_start
                                committed = request("/api/exercise/data", dict(action="commit", token=preview["token"],
                                    input_hash=preview["input_hash"],
                                    expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]}),
                                    opener=sessions[session])
                                batch = request("/api/exercise/data", dict(action="bulk-preview", case_ids=target_ids[-25:],
                                    changes={"coordination_note": "Explicit 25-case core HTTP batch"},
                                    reason="Actual core concurrent coordination batch"), opener=sessions[session])
                                bulk = request("/api/exercise/data", dict(action="commit", token=batch["token"],
                                    input_hash=batch["input_hash"],
                                    expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in batch["rows"]}),
                                    opener=sessions[session])
                                valid = (len(preview["rows"]) == 500 and committed["committed"] == 500
                                    and committed["errors"] == 0 and bulk["committed"] == 25 and bulk["errors"] == 0
                                    and preview_seconds <= 10 and sha256(raw).hexdigest() == source_hash)
                                results["core-http-import-and-bulk"] = dict(import_rows=len(preview["rows"]),
                                    import_committed=committed["committed"], preview_seconds=preview_seconds,
                                    source_sha256=source_hash, source_bytes_unchanged=sha256(raw).hexdigest() == source_hash,
                                    bulk_committed=bulk["committed"], result="Pass" if valid else "Fail")
                                if not valid:
                                    raise ValueError("Exact core HTTP import/bulk contract failed.")
                            response = request(path, body, opener=sessions[session])
                            if name == "write":
                                committed = request(path, dict(action="commit", token=response["token"], input_hash=response["input_hash"],
                                    expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in response["rows"]}),
                                    opener=sessions[session])
                                if committed["errors"] or committed["committed"] != 1:
                                    raise ValueError("Coordination write did not commit exactly one successful row.")
                        return name, time.perf_counter() - before, None
                    except (urllib.error.URLError, TimeoutError, ValueError) as error:
                        return name, time.perf_counter() - before, type(error).__name__

                # One outstanding interaction per session keeps its cookie/session state isolated.
                futures = []
                with ThreadPoolExecutor(max_workers=session_count) as pool:
                    sequence = 0
                    scheduled_requests = 0
                    while time.perf_counter() - started < args.duration:
                        units = scheduled_requests if args.scale else sequence
                        target = started + units / args.rate
                        if target >= started + args.duration:
                            break
                        if target > time.perf_counter():
                            time.sleep(target - time.perf_counter())
                        futures.append(pool.submit(interaction, sequence))
                        scheduled_requests += 2 if interaction_name(sequence) == "write" else 1
                        sequence += 1
                    for future in futures:
                        name, elapsed, error = future.result()
                        samples[name].append(elapsed)
                        if error:
                            failures.append(dict(operation=name, error=error))
                if time.perf_counter() < started + args.duration:
                    time.sleep(started + args.duration - time.perf_counter())
                for name, timings in samples.items():
                    p95 = sorted(timings)[math.ceil(.95 * len(timings)) - 1] if timings else None
                    threshold = operations[name][2]
                    op_errors = sum(f["operation"] == name for f in failures)
                    results[name] = dict(samples=len(timings), warm_http_p95_seconds=p95, threshold_seconds=threshold,
                                         p50_seconds=sorted(timings)[math.ceil(.5 * len(timings)) - 1] if timings else None,
                                         max_seconds=max(timings) if timings else None, errors=op_errors,
                                         result="Not run" if len(timings) < 200 else
                                                "Pass" if not op_errors and p95 is not None and p95 <= threshold else "Fail")
                results["steady-session"] = dict(seconds=time.perf_counter() - started, sessions=session_count, writers=2,
                    rate_basis="HTTP requests" if args.scale else "interactions",
                    aggregate_scheduled_rate=args.rate, interactions=sequence, scheduled_http_requests=scheduled_requests,
                    mix={key: len(value) for key, value in samples.items()}, failures=failures,
                    population=len(store.cases), trace_events=600_000 if args.scale else 0,
                    controls="Only coordination note preview/commit; no inference or controlled approvals",
                    result="Fail" if failures else "Pass" if args.duration >= 1800 else "Not run")
            before = json.loads(json.dumps(store._case("EX-HOME-001")))
            with sqlite3.connect(state / "backup.sqlite") as target:
                store.db.backup(target)
            start = time.perf_counter()
            store.db.close()
            reopened = SqlStore(str(seed), str(state / "properwarm.sqlite")) if args.scale or args.mixed_core else open_store()
            try:
                same = reopened._case("EX-HOME-001") == before
                integrity = reopened.db.execute("PRAGMA integrity_check").fetchone()[0]
                rows = reopened.db.execute("SELECT body FROM cases WHERE id='EX-HOME-001'").fetchone()[0]
            finally:
                reopened.db.close()
            results["clean-restart"] = {"seconds": time.perf_counter() - start,
                                        "exact_case_retained": same, "integrity": integrity,
                                        "result": "Pass" if same and integrity == "ok" else "Fail"}
            with sqlite3.connect(state / "backup.sqlite") as source, sqlite3.connect(state / "restored.sqlite") as target:
                source.backup(target)
                restored = target.execute("SELECT body FROM cases WHERE id='EX-HOME-001'").fetchone()[0]
                audit_same = source.execute("SELECT count,hash FROM audit_head").fetchall() == target.execute(
                    "SELECT count,hash FROM audit_head").fetchall()
                results["backup-restore"] = {"exact_stored_case": restored == rows, "exact_audit_head": audit_same,
                                             "result": "Pass" if restored == rows and audit_same else "Fail"}
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "kind": "local-http-and-clean-backup-engineering",
        "population": "60,000 fictional homes/600,000 traces; twenty sessions/two coordination writers" if args.scale else
                      "518 fictional homes (18 baseline plus 500 import targets); five sessions/two coordination writers" if args.mixed_core else
                      "18 fictional homes; five sessions/two coordination writers" if args.duration else
                      "18 fictional homes; one HTTP session, one writer; 201 updates on story home",
        "core_30_minute_workload": "Mixed HTTP import/bulk and document fixture; inspect exact results" if args.mixed_core else
            "Steady session recorded; 500-row import/25-case batch not part of this run" if args.duration >= 1800 and not args.scale else "Not run",
        "scale_30_minute_workload": "Executed separate declared scale; inspect per-operation results and integrity" if args.duration >= 1800 and args.scale else "Not run",
        "crash_and_response_loss": "Not run", "rpo_and_reconciliation": "Not run",
        "results": results,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results))
    return int(any(value["result"] == "Fail" for value in results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
