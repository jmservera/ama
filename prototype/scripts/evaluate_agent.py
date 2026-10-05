"""Paired synthetic evaluation; offline doubles never count as live model evidence."""
import argparse
import json
import math
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from properwarm.agents import AgentError, configured_model, evidence_tools, run_agent, safe_snapshot


def evaluation_cases():
    base = {
        "candidate_id": "CAND-EVAL-001", "is_synthetic": True,
        "source_file": "evaluation-fixture", "source_row": 2,
        "scenario_stage": "01 Identified", "active": True,
        "safety_hold_active": False, "controls": {}, "eligible_count": 0,
        "threshold": 5, "threshold_version": 1, "review_required": False,
        "appointment_events": [],
    }
    return [
        ("missing-gate", base),
        ("ready", {**base, "controls": {"named_owner": True}}),
        ("safety-hold", {**base, "safety_hold_active": True}),
        ("investigation", {**base, "eligible_count": 6, "review_required": True}),
        ("closed", {**base, "active": False}),
        ("unmapped", {**base, "scenario_stage": "Unknown"}),
    ]


class ContractDouble:
    """Scripted transport contract double, not an AI model."""
    model = "offline-contract-double"

    def complete(self, messages, *, final):
        if not final:
            calls = [
                {"id": f"call-{index}", "type": "function",
                 "function": {"name": name, "arguments": "{}"}}
                for index, name in enumerate(("inspect_case", "inspect_gates", "inspect_appointments"))
            ]
            message = {"tool_calls": calls, "content": None}
        else:
            tool_results = [json.loads(item["content"]) for item in messages if item["role"] == "tool"]
            expected = {key: refs for item in tool_results for key, refs in item["required_findings"].items()}
            message = {"content": json.dumps({
                "summary": "Synthetic contract test handoff, not model-generated.",
                "recommended_owner": "Safety lead" if "safety_hold" in expected else "Programme manager",
                "findings": [
                    {"kind": key, "evidence_ids": refs, "next_action": "Human review of the cited evidence."}
                    for key, refs in expected.items()
                ],
            })}
        return {"choices": [{"message": message, "finish_reason": "stop" if final else "tool_calls"}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0}}


def evaluate(model):
    records = []
    for label, case in evaluation_cases():
        start = time.perf_counter()
        tools = evidence_tools(safe_snapshot(case))
        baseline = {key for value in tools.values() for key in value["required_findings"]}
        baseline_ms = (time.perf_counter() - start) * 1000
        run = run_agent(case, model)
        findings = {item["kind"] for item in (run["proposal"] or {}).get("findings", [])}
        records.append({
            "scenario": label, "workflow_only_findings": sorted(baseline),
            "workflow_only_ms": round(baseline_ms, 3),
            "model_contract_pass": run["state"] == "awaiting_review" and findings == baseline,
            "critical_findings_expected": sorted(baseline & {"safety_hold", "human_review_due"}),
            "critical_findings_returned": sorted(findings & {"safety_hold", "human_review_due"}),
            "run": run,
        })
    durations = sorted(row["run"]["duration_ms"] for row in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution": "offline-contract-only" if isinstance(model, ContractDouble) else "live-azure",
        "model": model.model,
        "cases": len(records),
        "contract_pass_rate": sum(row["model_contract_pass"] for row in records) / len(records),
        "resolved_models": sorted({row["run"]["resolved_model"] for row in records if row["run"].get("resolved_model")}),
        "measured": {
            "median_agent_ms": round(statistics.median(durations), 2),
            "p95_agent_ms": durations[math.ceil(len(durations) * 0.95) - 1],
            "median_workflow_only_ms": round(statistics.median(row["workflow_only_ms"] for row in records), 3),
            "total_prompt_tokens": sum(row["run"]["usage"]["prompt_tokens"] for row in records),
            "total_completion_tokens": sum(row["run"]["usage"]["completion_tokens"] for row in records),
            "total_model_calls": sum(row["run"]["model_calls"] for row in records),
            "total_tool_calls": sum(row["run"]["tool_calls"] for row in records),
            "scope": "Six sequential cases, no concurrency or human-effort measurement; nearest-rank p95.",
        },
        "human_review_effort": "Not measured; no incremental-value claim.",
        "cost": "Token usage recorded; apply current regional pricing, not an invented currency estimate.",
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    model = configured_model() if args.live else ContractDouble()
    if model is None:
        raise AgentError("Live evaluation requires Azure endpoint/deployment and Entra access.")
    report = evaluate(model)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}))
    if report["contract_pass_rate"] != 1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
