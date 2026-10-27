"""Loopback HTTP/Chromium sensor checks using fresh generator output, no SQL or private data."""

from __future__ import annotations

import threading
import urllib.request
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any

from playwright.sync_api import Page, sync_playwright
from zava_forward.core import resident_showcase as rs
from zava_forward.core.synthetic import sensor_backfill

from zava_forward.api.resident_demo import app as demo

NOW = datetime(2026, 10, 27, 12, tzinfo=UTC)
FAKE_PASSWORD = "FAKE-TEST-FIXTURE-ONLY-not-a-real-demo-password"


def fixture(case: str, stock: str, email: str) -> rs.ShowcaseRow:
    sensor = sensor_backfill.sensor_for({"id": stock})
    sensor["fault_profile"] = "none"
    source = list(sensor_backfill.readings(sensor, days=2, start=NOW - timedelta(days=2)))
    history = rs.parse_sensors(
        [
            {
                "home_id": r["home_id"],
                "observed_at": r["observed_at"],
                "temperature_c": float(r["temperature_c"]),
                "humidity_pct": float(r["humidity_pct"]),
                "source_type": r["source_type"],
                "injected_fault": r["injected_fault"],
            }
            for r in source
        ],
        stock,
    )
    return rs.ShowcaseRow(
        case,
        email,
        1,
        "fresh synthetic generator browser fixture",
        NOW - timedelta(days=1),
        rs.AUTHORITY_END,
        False,
        case + " Test Road",
        "Testtown",
        "TE1 1ST",
        "Survey",
        False,
        (),
        stock,
        history,
    )


class FixtureReader:
    def __init__(self) -> None:
        self.rows = {
            "CASE-A": fixture("CASE-A", "ZF-00000", "alice@example.com"),
            "CASE-B": fixture("CASE-B", "ZF-00001", "bob@example.com"),
        }

    def list_rows(self) -> list[rs.ShowcaseRow]:
        return list(self.rows.values())

    def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None:
        return self.rows.get(case_id)


def check(name: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(name)
    print("PASS " + name, flush=True)


def sign_in(page: Page, base: str, email: str) -> None:
    page.goto(base)
    page.get_by_label("Email address").fill(email)
    page.get_by_label("Email address").press("Tab")
    page.keyboard.type(FAKE_PASSWORD)
    page.keyboard.press("Enter")
    page.get_by_role("heading", name="Your home sensors", exact=True).wait_for()


def exercise(browser: Any, base: str, reader: FixtureReader) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on(
        "console", lambda message: errors.append(message.text) if message.type == "error" else None
    )
    context.route(
        "**/*",
        lambda route: route.continue_() if route.request.url.startswith(base) else route.abort(),
    )
    sign_in(page, base, "alice@example.com")
    latest = reader.rows["CASE-A"].sensors[-1]
    check("two semantic gauges", page.get_by_role("meter").count() == 2)
    check(
        "temperature matches generator",
        page.locator("#gauge-temperature_c").evaluate("(el) => el.value") == latest.temperature_c,
    )
    check(
        "humidity matches generator",
        page.locator("#gauge-humidity_pct").evaluate("(el) => el.value") == latest.humidity_pct,
    )
    check(
        "synthetic recorded not live copy",
        "not live measurements or safety advice" in page.inner_text("#content"),
    )
    check(
        "two named static plots",
        page.get_by_role("img", name="Synthetic", exact=False).count() == 2,
    )
    summary = page.get_by_text("Show sensor history as a table", exact=True)
    summary.focus()
    check(
        "keyboard focus visible",
        summary.evaluate("(el) => getComputedStyle(el).outlineStyle") != "none",
    )
    summary.press("Enter")
    check(
        "table matches all 48 source observations",
        page.locator(".sensor-table tbody tr").count() == 48,
    )
    check(
        "table includes latest value",
        page.locator(".sensor-table tbody tr").last.locator("td").first.inner_text()
        == page.locator("#gauge-temperature_c").get_attribute("aria-valuetext").split(",")[0],
    )
    check(
        "table date has exact UTC alternative",
        page.locator(".sensor-table tbody time").last.get_attribute("datetime")
        == latest.observed_at.isoformat().replace("+00:00", "Z"),
    )
    forged = page.evaluate("""async () => {
      const r = await fetch('/demo/view?case_id=CASE-B&home_id=ZF-00001', {headers: {'X-Home-Id':'ZF-00001'}});
      return await r.json();
    }""")
    check(
        "forged selector stays on own home",
        forged["sensors"]["history"][-1]["temperature_c"] == latest.temperature_c
        and "ZF-00001" not in str(forged),
    )
    for width in (320, 390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        check(
            f"no page overflow at {width}px",
            page.evaluate("document.documentElement.scrollWidth <= innerWidth"),
        )
    check(
        "reduced motion is static",
        page.locator(".sensor-chart svg").first.evaluate(
            "(el) => getComputedStyle(el).animationName"
        )
        == "none",
    )

    bob = browser.new_context()
    bob_page = bob.new_page()
    sign_in(bob_page, base, "bob@example.com")
    check(
        "second session sees its own generated values",
        bob_page.locator("#gauge-temperature_c").evaluate("(el) => el.value")
        == reader.rows["CASE-B"].sensors[-1].temperature_c,
    )
    check(
        "second home has distinct source values",
        reader.rows["CASE-B"].sensors != reader.rows["CASE-A"].sensors,
    )
    bob.close()

    original = reader.rows["CASE-A"]
    missing = replace(latest, temperature_c=None, temperature_status="Not recorded")
    reader.rows["CASE-A"] = replace(original, sensors=(missing,))
    page.reload()
    page.get_by_text("Not recorded", exact=True).first.wait_for()
    check(
        "missing channel has no fake zero gauge",
        page.get_by_role("meter").count() == 1
        and page.locator("#gauge-temperature_c").count() == 0,
    )
    check(
        "singleton has a visible humidity point", page.locator(".sensor-chart circle").count() == 1
    )
    for fault in ("Demo fault: outlier", "Demo fault: stuck reading"):
        reader.rows["CASE-A"] = replace(
            original,
            sensors=(
                replace(
                    latest,
                    temperature_c=None,
                    humidity_pct=None,
                    temperature_status=fault,
                    humidity_status=fault,
                ),
            ),
        )
        page.reload()
        page.get_by_text(fault, exact=True).first.wait_for()
        page.get_by_text("Show sensor history as a table", exact=True).click()
        check(
            f"{fault} has text/table and no normal marks",
            page.get_by_role("meter").count() == 0
            and page.locator(".sensor-chart circle").count() == 0
            and fault in page.locator(".sensor-table").inner_text(),
        )
    reader.rows["CASE-A"] = replace(original, sensors=())
    page.reload()
    page.get_by_text("No synthetic sensor readings", exact=False).wait_for()
    check(
        "empty state has no invented chart or gauge",
        page.get_by_role("meter").count() == 0 and page.locator(".sensor-chart").count() == 0,
    )
    check("no browser errors", not errors)
    context.close()


def main() -> None:
    reader = FixtureReader()
    codec = rs.SessionCodec(
        b"fake-browser-test-session-key-only", rs.AUTHORITY_END, lambda: NOW.timestamp()
    )
    app = demo.ResidentDemo(
        reader,
        rs.build_identity_map(reader.list_rows(), NOW),
        rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
        codec,
        rs.LoginLimiter(),
        ("127.0.0.1",),
        rs.AUTHORITY_END,
        port=0,
        clock=lambda: NOW.timestamp(),
    )
    server = demo.serve(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{app.port}/"
    try:
        with urllib.request.urlopen(base + "healthz", timeout=5) as response:
            check(
                "local application running and responsive",
                response.status == 200 and thread.is_alive(),
            )
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            exercise(browser, base, reader)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
