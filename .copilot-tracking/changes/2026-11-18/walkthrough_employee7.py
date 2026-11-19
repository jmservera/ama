"""Round 7 desktop employee map proof for #1818 (no secrets printed). Usage: walkthrough_employee7.py EVIDENCE_DIR"""

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

import walkthrough_probe7 as probe

MAP_JS = "async()=>{const r=await fetch('/api/map');const j=await r.json();return {s:r.status,j:j}}"


def main() -> int:
    out = Path(sys.argv[1])
    tag = sys.argv[2] if len(sys.argv) > 2 else "fresh"
    user, password = probe.credentials("employee")
    result: dict[str, object] = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "homes": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        probe.sign_in(page, user, password)
        page.goto(probe.APP + "/app#/overview", wait_until="networkidle", timeout=30000)
        time.sleep(6)
        data = page.evaluate(MAP_JS)
        result["api_map_status"] = data["s"]
        items = {i["id"]: i for i in data["j"]["items"]}
        keys = sorted(data["j"]["items"][0].keys())
        result["item_keys"] = keys
        demo = {k: v for k, v in items.items() if v.get("case_id", v.get("id")) in probe.DEMO or v.get("id") in probe.DEMO}
        states = {}
        for i in data["j"]["items"]:
            s = i.get("sensor") or {}
            states[s.get("state")] = states.get(s.get("state"), 0) + 1
        result["sensor_state_counts_all_homes"] = states
        page.screenshot(path=str(out / f"employee-map-overview-{tag}.png"))
        for hid, item in demo.items():
            result["homes"][hid] = {"sensor": item.get("sensor")}
            marker = page.locator(f'.map-marker[title^="{item["name"]},"][title*="{item["sensor"]["temperature_c"]}"]').first
            marker.focus()
            page.keyboard.press("Enter")
            time.sleep(1.5)
            card = page.locator(".map-home-card")
            text = card.inner_text()
            (out / f"employee-card-{hid}-{tag}.txt").write_text(text)
            result["homes"][hid]["card_has_sensor_status"] = "Sensor status" in text
            result["homes"][hid]["card_text_lines"] = [ln for ln in text.splitlines() if ln.strip()][-8:]
            card.screenshot(path=str(out / f"employee-card-{hid}-{tag}.png"))
            page.keyboard.press("Escape")
        # accessible list and sensor-alert filter
        page.locator("details.maplist summary").click()
        time.sleep(1)
        lis = page.locator("details.maplist li")
        result["list_items"] = lis.count()
        hits = [ln for ln in page.locator("details.maplist").inner_text().splitlines() if "ensor" in ln]
        result["list_sensor_lines_sample"] = hits[:6]
        page.screenshot(path=str(out / f"employee-maplist-{tag}.png"))
        page.locator("#map-sensor-alerts").check()
        time.sleep(1.5)
        result["filter_note"] = page.locator(".map-sensor-filter p[aria-live]").inner_text()
        page.screenshot(path=str(out / f"employee-sensor-filter-{tag}.png"))
        browser.close()
    (out / f"employee-result-{tag}.json").write_text(json.dumps(result, indent=1))
    print(json.dumps(result, indent=1)[:3500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
