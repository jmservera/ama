"""Real HTTPS Playwright checks without owner credentials; never changes Azure ingress."""

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
WEB = Path(__file__).resolve().parents[4] / "src/api/src/zava_forward/api/resident_demo/web"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results = []

    def check(name, condition):
        results.append({"check": name, "status": "Passed" if condition else "Failed"})
        if not condition:
            raise AssertionError(name)

    failure = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(type(error).__name__))
            response = page.goto(BASE, wait_until="networkidle", timeout=90000)
            check("Real HTTPS sign-in responds200", response.status == 200)
            page.locator("#signin:not([hidden])").wait_for()
            text = page.inner_text("body")
            check("Synthetic banner and shared demonstration limits visible",
                  "Synthetic showcase - not a live resident service" in text
                  and "not proof of who you are" in text)
            check("Native labelled fake-email and password controls",
                  page.get_by_label("Email address").count() == 1
                  and page.get_by_label("Password", exact=True).count() == 1)
            check("Resident content and account hidden before login",
                  not page.locator("#content").is_visible()
                  and not page.locator("#account").is_visible())
            session = context.request.get(BASE + "/demo/session").json()
            check("Session endpoint confirms signed out", session["signed_in"] is False)
            headers = {"Origin": BASE, "X-CSRF-Token": session["csrf"],
                       "Sec-Fetch-Site": "same-origin"}
            invalid = {"email": "no.live.acceptance@example.com",
                       "password": "INVALID-FIXTURE-NOT-OWNER-CREDENTIAL"}
            denied = context.request.post(BASE + "/demo/login", headers=headers, data=invalid)
            check("Fake email with invalid fixture credential denies generically",
                  denied.status == 401 and denied.json() ==
                  {"error": "We could not sign you in with those details."})
            unknown = context.request.post(BASE + "/demo/login", headers=headers,
                                          data={**invalid, "email": "other.unregistered@example.com"})
            check("Unknown fake email gives identical error",
                  unknown.status == 401 and unknown.json() == denied.json())
            check("Missing CSRF denies403",
                  context.request.post(BASE + "/demo/login", headers={"Origin": BASE},
                                       data=invalid).status == 403)
            check("Cross-origin denies403",
                  context.request.post(BASE + "/demo/login",
                                       headers={**headers, "Origin": "https://invalid.example"},
                                       data=invalid).status == 403)
            check("Anonymous own-view denies401",
                  context.request.get(BASE + "/demo/view").status == 401)
            check("Anonymous assistant denies401",
                  context.request.post(BASE + "/demo/assistant", headers=headers,
                                       data={"topic": "status"}).status == 401)
            check("Client case selector cannot grant anonymous authority",
                  context.request.get(BASE + "/demo/view?case_id=SYN-OTHER",
                                      headers={"X-Case-ID": "SYN-OTHER"}).status == 401)
            for path in ("/api/cases", "/api/me", "/auth/login/aad", "/.auth/login/aad"):
                check("Employee route absent " + path,
                      context.request.get(BASE + path).status == 404)
            forged = browser.new_context()
            forged.add_cookies([{"name": "__Host-zfdemo", "value": "v1.forged.1.expired.invalid",
                                "url": BASE, "secure": True, "httpOnly": True,
                                "sameSite": "Strict"}])
            check("Forged session denies401, not genuine expiry proof",
                  forged.request.get(BASE + "/demo/view").status == 401)
            forged.close()
            check("No-store, nosniff, framing and CSP response headers",
                  response.headers.get("cache-control") == "no-store"
                  and response.headers.get("x-content-type-options") == "nosniff"
                  and response.headers.get("x-frame-options") == "DENY"
                  and "default-src 'none'" in response.headers.get("content-security-policy", ""))
            for asset in ("index.html", "demo.css", "demo.js", "assistant.js"):
                remote = context.request.get(BASE + ("/" if asset == "index.html" else "/" + asset))
                check("Source asset byte parity " + asset,
                      remote.status == 200 and hashlib.sha256(remote.body()).digest() ==
                      hashlib.sha256((WEB / asset).read_bytes()).digest())
            check("Account/sign-out are in top header markup, not positive render proof",
                  page.locator("header.top #account #signout").count() == 1)
            page.keyboard.press("Tab")
            check("Skip link receives keyboard focus",
                  page.evaluate("document.activeElement.classList.contains('skip')"))
            page.keyboard.press("Enter")
            check("Skip link moves focus to main",
                  page.evaluate("document.activeElement.id === 'main'"))
            page.screenshot(path=str(args.out / "signin-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 320, "height": 800})
            check("Anonymous320px layout has no horizontal page overflow",
                  page.evaluate("document.documentElement.scrollWidth <= 320"))
            check("Mobile login targets at least44px",
                  page.locator("#signin-button").bounding_box()["height"] >= 44)
            page.screenshot(path=str(args.out / "signin-320.png"), full_page=True)
            page.get_by_label("Email address").fill(invalid["email"])
            page.get_by_label("Password", exact=True).fill(invalid["password"])
            page.get_by_role("button", name="Sign in", exact=True).click()
            page.locator("#signin-error:not([hidden])").wait_for()
            check("Real UI invalid-login feedback renders and is focused",
                  "We could not sign you in" in page.locator("#signin-error").inner_text()
                  and page.evaluate("document.activeElement.id === 'signin-error'"))
            check("No page script exceptions", not errors)
            context.close()
            browser.close()
    except Exception as error:
        failure = type(error).__name__ + ": " + str(error)
    blocked = [
        "Registered positive fake-email login: owner-held password unavailable",
        "Authenticated own home/cases and cross-resident isolation",
        "Authenticated synthetic gauges/history, desktop and320px",
        "Authenticated advisory assistant answers and cross-resident denial",
        "Actual top-right account sign-out and revoked-session replay",
        "Genuine1800-second live session expiry"
    ]
    report = {"url": BASE, "recorded_at": datetime.now(UTC).isoformat(),
              "results": results, "failure": failure,
              "owner_run": [{"check": name, "status": "Blocked"} for name in blocked],
              "ingress_mutations": 0, "credential_reads": 0,
              "limitations": "Anonymous browser proof only; fixture expiry tests are separate."}
    (args.out / "live-result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"passed": sum(r["status"] == "Passed" for r in results),
                      "failed": failure, "blocked": len(blocked)}))
    if failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
