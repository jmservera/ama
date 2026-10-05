"""Headless local UI/API check using an explicitly labelled contract double."""
import argparse
import json
import statistics
import sys
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluate_agent import ContractDouble
from properwarm.agents import AgentError
from properwarm.server import PrototypeServer
from properwarm.storage import Store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--live-smoke", action="store_true", help="Real configured Azure handoff only; no doubles or failure injection.")
    args = parser.parse_args()
    if args.live_smoke:
        validate_live_handoff(args.out)
        return
    from playwright.sync_api import sync_playwright, expect

    screenshots = args.out.parent
    screenshots.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parents[1] / "seed" / "container-source"
    errors = []
    with tempfile.TemporaryDirectory() as temp, patch.dict(
        "os.environ", {"AZURE_OPENAI_ENDPOINT": "", "AZURE_OPENAI_DEPLOYMENT": ""},
    ):
        store = Store(Path(temp) / "smoke.sqlite3", source)
        server = PrototypeServer(("127.0.0.1", 0), store)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(url, wait_until="networkidle")
                expect(page.get_by_role("button", name="Request case review", exact=True)).to_be_disabled()
                page.get_by_role("button", name="Frontline coordination", exact=True).click()
                expect(page.get_by_role("button", name="Record outcome", exact=True)).to_be_enabled()
                page.get_by_role("button", name="Programme delivery", exact=True).click()
                page.wait_for_load_state("networkidle")
                expect(page.get_by_role("button", name="Request case review", exact=True)).to_be_visible()
                expect(page.get_by_role("button", name="Request case review", exact=True)).to_be_disabled()
                candidate = next(item["candidate_id"] for item in store.list_cases()
                                 if item["active"] and not item["safety_hold_active"])
                page.locator("#case-list").get_by_role("button").filter(has_text=candidate).click()
                expect(page.locator("#case-detail h2")).to_have_text(candidate)
                base = f"{url}/api/cases/{candidate}"
                request = page.request
                original_stage = request.get(base).json()["scenario_stage"]

                def post(path, data, status=200):
                    response = request.post(path, data=data)
                    assert response.status == status, response.text()
                    return response.json()

                post(base + "/agent-run", {"actor": "Local reviewer"}, 503)
                server.model = ContractDouble()
                page.wait_for_load_state("networkidle")
                page.reload(wait_until="networkidle")
                page.locator("#case-list").get_by_role("button").filter(has_text=candidate).click()
                expect(page.locator("#case-detail h2")).to_have_text(candidate)
                page.get_by_role("button", name="Request case review", exact=True).click()
                expect(page.locator(".agent-run").first).to_contain_text("awaiting_review", timeout=15000)
                page.get_by_role("button", name="Assurance & review", exact=True).click()
                page.wait_for_load_state("networkidle")
                expect(page.locator("#case-detail h2")).to_have_text(candidate)
                assert page.locator(".evidence-missing").count() == 0
                page.locator(".evidence-link").first.click()
                assert page.locator(".agent-source").first.get_attribute("open") is not None
                page.get_by_role("button", name="Accept suggestion", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("Human accepted disposition recorded")
                page.get_by_role("button", name="Programme delivery", exact=True).click()
                page.wait_for_load_state("networkidle")
                page.locator("#case-list").get_by_role("button").filter(has_text=candidate).click()
                expect(page.locator("#case-detail h2")).to_have_text(candidate)
                expect(page.locator(".agent-run").first).to_contain_text("accepted")
                assert request.get(base).json()["scenario_stage"] == original_stage

                page.get_by_role("button", name="Request case review", exact=True).click()
                expect(page.get_by_role("button", name="Accept suggestion", exact=True)).to_be_visible()
                post(url + "/api/settings", {"actor": "Local reviewer", "threshold": 4})
                page.get_by_role("button", name="Accept suggestion", exact=True).click()
                expect(page.locator(".agent-error")).to_contain_text("stale")
                page.get_by_role("button", name="Reject suggestion", exact=True).click()
                expect(page.locator(".agent-run").first).to_contain_text("rejected")

                class UnavailableModel(ContractDouble):
                    def complete(self, messages, *, final):
                        raise AgentError("Injected test-only inference outage.")

                server.model = UnavailableModel()
                page.get_by_role("button", name="Request case review", exact=True).click()
                expect(page.locator(".agent-run").first).to_contain_text("failed")
                assert request.get(base).json()["agent_runs"][0]["proposal"] is None
                page.screenshot(path=str(screenshots / "programme-contract-double.png"), full_page=True)
                page.get_by_role("button", name="Frontline coordination", exact=True).click()
                expect(page.get_by_role("button", name="Record outcome", exact=True)).to_be_visible()
                expect(page.locator("#case-gates")).to_be_hidden()
                for _ in range(5):
                    post(base + "/appointment", {
                        "actor": "Local reviewer", "outcome": "resident_no_access_verified",
                        "appointment_confirmed": True,
                    }, 201)
                assert request.get(base).json()["review_required"]
                page.get_by_role("button", name="Assurance & review", exact=True).click()
                expect(page.locator("#case-gates")).to_be_visible()
                expect(page.get_by_role("button", name="Record outcome", exact=True)).to_be_hidden()
                assert int(page.locator("#case-count").inner_text()) < 988
                page.screenshot(path=str(screenshots / "assurance-contract-double.png"), full_page=True)

                post(base + "/review", {"actor": "Local reviewer"}, 201)
                # The closure reason must remain the repository's supported synthetic code.
                settings = request.get(url + "/api/settings").json()
                post(base + "/close", {"actor": "Local reviewer", "reason": settings["closure_reasons"][0]})
                post(base + "/reopen", {"actor": "Local reviewer"})
                reopened = request.get(base).json()
                assert reopened["active"] and reopened["eligible_count"] == 0

                page.get_by_role("button", name="Operator & intake", exact=True).click()
                expect(page.locator("#import-section")).to_be_visible()
                assert page.evaluate(
                    "document.querySelector('#import-section').compareDocumentPosition(document.querySelector('.workbench')) & Node.DOCUMENT_POSITION_FOLLOWING"
                )
                page.locator('input[type="file"]').set_input_files(
                    str(Path(__file__).resolve().parents[1] / "seed" / "demo-import.xlsx"),
                )
                page.get_by_role("button", name="Preview rows", exact=True).click()
                expect(page.get_by_role("button", name="Commit accepted rows", exact=True)).to_be_enabled()
                page.get_by_role("button", name="Commit accepted rows", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("Workbook imported")
                bundle = request.get(url + "/api/export").json()
                assert len(bundle["agent_runs"]) == 3
                assert len(bundle["cases"]) == 991
                assert bundle["appointment_events"]
                assert not errors, errors
                page.set_viewport_size({"width": 390, "height": 844})
                page.screenshot(path=str(screenshots / "operator-mobile.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                measurements = []
                for _ in range(20):
                    start = time.perf_counter()
                    response = request.get(url + "/api/overview")
                    assert response.ok and response.headers.get("x-request-id")
                    measurements.append((time.perf_counter() - start) * 1000)
                browser.close()
                report = {
                    "execution": "local-ui-api-contract-double-only", "passed": True,
                    "checks": ["unconfigured", "proposal", "source-links", "accept", "stale", "reject",
                               "outage", "role-views", "investigation", "close-reopen", "import-export",
                               "mobile-overflow", "request-correlation", "browser-errors"],
                    "http_overview": {
                        "requests": len(measurements), "cases": 991, "concurrency": 1,
                        "median_ms": round(statistics.median(measurements), 2),
                        "p95_ms": round(sorted(measurements)[18], 2),
                        "scope": "Local sequential requests, not a production SLO or load test.",
                    },
                }
                args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(report))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


def validate_live_handoff(out):
    from playwright.sync_api import sync_playwright, expect
    source = Path(__file__).resolve().parents[1] / "seed" / "container-source"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        store = Store(Path(temp) / "live-smoke.sqlite3", source)
        server = PrototypeServer(("127.0.0.1", 0), store)
        if server.model is None:
            server.server_close()
            raise RuntimeError("Live UI smoke requires the approved Azure endpoint and Entra access.")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        errors = []
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{server.server_port}", wait_until="networkidle")
                page.locator("#actor").select_option("Synthetic scenario runner")
                candidate = next(item["candidate_id"] for item in store.list_cases()
                                 if item["active"] and not item["safety_hold_active"])
                page.locator("#case-list").get_by_role("button").filter(has_text=candidate).click()
                expect(page.locator("#case-detail h2")).to_have_text(candidate)
                before = store.get_case(candidate)
                page.get_by_role("button", name="Request case review", exact=True).click()
                expect(page.locator(".agent-run").first).to_contain_text("awaiting_review", timeout=150000)
                run = store.get_case(candidate)["agent_runs"][0]
                assert run["state"] == "awaiting_review", run["error"]
                assert run["resolved_model"] and run["usage"]["prompt_tokens"] > 0
                assert page.locator(".evidence-missing").count() == 0
                page.locator(".evidence-link").first.click()
                page.screenshot(path=str(out.parent / "live-agent-handoff.png"), full_page=True)
                page.get_by_role("button", name="Reject suggestion", exact=True).click()
                expect(page.locator(".agent-run").first).to_contain_text("rejected")
                after = store.get_case(candidate)
                assert after["scenario_stage"] == before["scenario_stage"]
                assert after["controls"] == before["controls"]
                assert after["appointment_events"] == before["appointment_events"]
                assert not errors, errors
                page.wait_for_load_state("networkidle")
                browser.close()
                report = {
                    "execution": "live-azure-ui-api", "passed": True,
                    "model": run["resolved_model"], "prompt_version": run["prompt_version"],
                    "duration_ms": run["duration_ms"], "usage": run["usage"],
                    "model_calls": run["model_calls"], "tool_calls": run["tool_calls"],
                    "findings": [finding["kind"] for finding in run["proposal"]["findings"]],
                    "checks": ["real-inference", "persisted-proposal", "source-links", "trace-provenance",
                               "synthetic-runner-rejection", "no-domain-writes", "no-browser-errors"],
                    "human_review_effort": "Not measured; automated UI rejection is not a human review study.",
                }
                out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(report))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    main()
