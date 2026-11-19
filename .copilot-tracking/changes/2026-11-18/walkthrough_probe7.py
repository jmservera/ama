"""Desktop sign-in and sensor-surface probe for the 1818 live walkthrough (no secrets printed).

Credentials are read at runtime from the owner's home files and never written anywhere. Only
status codes, key names and counts are printed; screenshots go to the evidence directory given
as argv[2] (outside the repository). Usage: walkthrough_probe.py employee|resident EVIDENCE_DIR
"""

import json
import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
HOME = Path.home()
DEMO = {"ZF-2025-0029", "ZF-2025-0030", "ZF-2025-0031"}


def credentials(role: str) -> tuple[str, str]:
    if role == "employee":
        user = (HOME / ".ama-test-user-id").read_text().strip()
        return user, (HOME / ".ama-test-user").read_text().splitlines()[0].strip()
    lines = (HOME / ".ama-resident-test-user").read_text().splitlines()
    return lines[0].strip(), lines[1].strip()


def sign_in(page, user: str, password: str) -> list[str]:
    steps = []
    page.goto(APP + "/sign-in", wait_until="domcontentloaded", timeout=120000)
    for _ in range(12):
        time.sleep(1.5)
        host = re.sub(r"^https?://([^/]+).*", r"\1", page.url)
        steps.append(host)
        if host.endswith("azurecontainerapps.io") and "/sign-in" not in page.url:
            break
        email = page.locator('input[name="loginfmt"]')
        pwd = page.locator('input[name="passwd"]:not([aria-hidden="true"])')
        if pwd.count() and pwd.is_visible():
            pwd.click()
            pwd.press_sequentially(password, delay=40)
            time.sleep(0.5)
            pwd.press("Enter")
        elif email.count() and email.is_visible():
            email.click()
            email.press_sequentially(user, delay=40)
            time.sleep(0.5)
            email.press("Enter")
        elif page.get_by_role("button", name="No").count():
            page.get_by_role("button", name="No").click()
        elif page.locator("#idBtn_Back").count():
            page.locator("#idBtn_Back").click()
    return steps


def shape(value, depth=0):
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in list(value.items())[:25]} if depth < 3 else "{}"
    if isinstance(value, list):
        return [len(value), shape(value[0], depth + 1) if value else None]
    return type(value).__name__


def main() -> int:
    role, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    user, password = credentials(role)
    result: dict[str, object] = {"role": role, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        result["hosts"] = sign_in(page, user, password)
        result["final_host"] = re.sub(r"^https?://([^/]+).*", r"\1", page.url)
        me = page.evaluate("async()=>{const r=await fetch('/api/me');let j=null;try{j=await r.json()}catch(e){};return {s:r.status,role:j&&j.user&&j.user.role,ukeys:j&&j.user?Object.keys(j.user):null,staff:j&&JSON.stringify(j.staff).slice(0,200),dom:j&&j.user&&j.user.email?j.user.email.split('@')[1]:null,elen:j&&j.user&&j.user.email?j.user.email.length:null}}")
        result["api_me"] = me
        if role == "employee" and me["s"] == 200:
            data = page.evaluate(
                "async()=>{const r=await fetch('/api/map');const t=await r.text();"
                "let j=null;try{j=JSON.parse(t)}catch(e){};return {s:r.status,j:j,n:t.length}}"
            )
            result["api_map"] = {"status": data["s"], "bytes": data["n"], "shape": shape(data["j"])}
            text = json.dumps(data["j"]) if data["j"] else ""
            result["api_map_mentions_sensor"] = text.lower().count("sensor")
            items = data["j"].get("items", data["j"]) if isinstance(data["j"], dict) else data["j"]
            demo = [i for i in items if isinstance(i, dict) and i.get("id") in DEMO]
            result["demo_items"] = [
                {k: v for k, v in i.items() if k in ("id", "stage", "sensor", "sensors")} for i in demo
            ]
            result["sensor_item_count"] = sum(1 for i in items if isinstance(i, dict) and i.get("sensor"))
            extra = page.evaluate(
                "async()=>{const r=await fetch('/api/cases/ZF-2025-0029/sensors');"
                "return {s:r.status,t:(await r.text()).slice(0,400)}}"
            )
            result["case_sensors"] = extra
            page.goto(APP + "/#/map", wait_until="networkidle", timeout=30000)
            time.sleep(3)
            page.screenshot(path=str(out / "employee-map.png"))
        elif me["s"] == 200:
            page.screenshot(path=str(out / "resident-home.png"))
        else:
            page.screenshot(path=str(out / f"{role}-blocked.png"))
        browser.close()
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
