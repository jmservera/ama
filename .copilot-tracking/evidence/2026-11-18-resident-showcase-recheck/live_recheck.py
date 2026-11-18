"""Live desktop check of the synthetic resident showcase (issue #462, demo recheck).

Credentials come from ~/.ama-resident-test-user (line 1 email, line 2 password) and are never printed.
"""

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
res: dict = {"url": URL, "checks": {}}


def rec(name, value):
    res["checks"][name] = value


def wait_ready(page):
    for _ in range(8):
        try:
            if page.request.get(URL + "/demo/session", timeout=60000).status == 200:
                return
        except Exception:
            time.sleep(5)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()
    t0 = time.time()
    wait_ready(page)
    rec("cold_start_seconds", round(time.time() - t0, 1))
    r = page.request.get(URL.replace("https", "http") + "/", max_redirects=0)
    rec("http_to_https", [r.status, r.headers.get("location", "")[:5]])

    page.goto(URL + "/", wait_until="networkidle", timeout=90000)
    rec("title", page.title())
    rec("banner_mentions_synthetic", "synthetic" in page.inner_text("body").lower())
    page.screenshot(path=str(OUT / "01-signin-desktop.png"))
    resp = page.request.get(URL + "/demo/session")
    sess = resp.json()
    rec("session_signed_out", sess.get("signed_in"))
    rec("hsts_header_present", "strict-transport-security" in resp.headers)
    rec("security_headers", sorted(k for k in resp.headers if k in {
        "content-security-policy", "x-content-type-options", "x-frame-options",
        "referrer-policy", "cache-control", "strict-transport-security"}))
    csrf = sess.get("csrf")
    origin = {"Origin": URL, "Content-Type": "application/json"}

    def login(body, headers=None, token=csrf, ctxreq=None):
        h = dict(origin)
        if token:
            h["X-CSRF-Token"] = token
        h.update(headers or {})
        return (ctxreq or ctx.request).post(URL + "/demo/login", data=json.dumps(body), headers=h)

    rec("login_no_csrf", login({"email": EMAIL, "password": "x"}, token=None).status)
    rec("login_foreign_origin", login({"email": EMAIL, "password": "x"},
                                      {"Origin": "https://evil.example"}).status)
    w = login({"email": EMAIL, "password": "not-the-password-1"})
    u = login({"email": "nobody.synthetic@example.invalid", "password": "not-the-password-1"})
    rec("wrong_password", [w.status, w.text()])
    rec("unknown_email", [u.status, u.text()])
    rec("denial_bodies_identical", w.text() == u.text())
    rec("denial_sets_cookie", ["set-cookie" in w.headers, "set-cookie" in u.headers])

    probes = ["/api/cases", "/workbench", "/api/staff", "/admin", "/demo/staff", "/.env"]
    rec("staff_probes", {pth: ctx.request.get(URL + pth).status for pth in probes})
    rec("unsigned_view", ctx.request.get(URL + "/demo/view").status)
    forged = b.new_context()
    forged.add_cookies([{"name": "__Host-zfdemo", "value": "forged.value.sig", "url": URL,
                         "secure": True, "httpOnly": True, "sameSite": "Strict"}])
    rec("forged_cookie_view", forged.request.get(URL + "/demo/view",
                                                  headers={"X-Resident-Session": "x"}).status)
    rec("forged_cookie_session", forged.request.get(URL + "/demo/session").json().get("signed_in"))
    forged.close()

    # Correct sign in through the real UI
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    page.evaluate("""() => document.querySelectorAll('input').forEach(
        i => { if (i.type === 'email' || i.type === 'password') i.type = 'password'; })""")
    page.screenshot(path=str(OUT / "02-signin-filled-masked.png"))
    page.evaluate("""() => document.querySelectorAll('input').forEach(
        i => { if (i.name === 'email' || i.id === 'email') i.type = 'email'; })""")
    with page.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        page.keyboard.press("Enter")
    rec("ui_login_status", ri.value.status)
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT / "03-signed-in-desktop.png"), full_page=True)
    text = page.inner_text("body")
    rec("signed_in_text_has_password", PASSWORD in text)
    rec("signed_in_sections", {k: (k in text.lower()) for k in
                               ["timeline", "documents", "sensor", "not available in this showcase"]})

    cookies = {c["name"]: c for c in ctx.cookies()}
    sc, cc = cookies.get("__Host-zfdemo"), cookies.get("__Host-zfdemo-csrf")
    rec("session_cookie", sc and {k: sc[k] for k in ("secure", "httpOnly", "sameSite", "path")} | {
        "lifetime_seconds": round(sc["expires"] - time.time())})
    rec("csrf_cookie", cc and {k: cc[k] for k in ("secure", "httpOnly", "sameSite", "path")})

    sid = ctx.request.get(URL + "/demo/session").json()
    rec("session_signed_in", sid.get("signed_in"))
    sh = {"X-Resident-Session": sid.get("session_id", "")}
    v = ctx.request.get(URL + "/demo/view", headers=sh)
    rec("view_status", v.status)
    view = v.json()
    rec("view_top_level_keys", sorted(view))
    rec("view_no_session_header", ctx.request.get(URL + "/demo/view").status)
    rec("view_wrong_session_header", ctx.request.get(
        URL + "/demo/view", headers={"X-Resident-Session": "wrong"}).status)
    base = json.dumps(view, sort_keys=True)
    overrides = {}
    for q in ("case=OTHER", "case_id=OTHER", "email=other@example.invalid"):
        r2 = ctx.request.get(URL + "/demo/view?" + q, headers=sh)
        overrides["?" + q.split("=")[0]] = [r2.status, json.dumps(r2.json(), sort_keys=True) == base]
    for hn in ("X-Case-Id", "X-Forwarded-User"):
        r2 = ctx.request.get(URL + "/demo/view", headers=sh | {hn: "OTHER"})
        overrides[hn] = [r2.status, json.dumps(r2.json(), sort_keys=True) == base]
    rec("identity_overrides_ignored", overrides)

    terms = ["safeguard", "vulnerab", "invoice", "salary", "iban", "token", "internal note",
             "date_of_birth", "dob", "phone", "password", "secret", "staff"]
    low = base.lower()
    hits = {t: len(re.findall(re.escape(t), low)) for t in terms if t in low}
    rec("projection_canary_term_counts", hits)
    ctxs = {}
    for t in hits:
        i = low.index(t)
        ctxs[t] = base[max(0, i - 40): i + 60].replace(EMAIL, "<own-email>")
    rec("projection_canary_context", ctxs)
    emails = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", base))
    rec("projection_email_count_all_own", [len(emails), emails <= {EMAIL}])
    rec("password_in_view", PASSWORD in base)
    rec("write_routes_405_on_get", {pth: ctx.request.get(URL + pth).status for pth in
                                    ("/demo/logout", "/demo/assistant", "/demo/agenda")})

    # Sign out through the UI
    page.click("#account summary")
    page.screenshot(path=str(OUT / "03b-account-menu-desktop.png"))
    page.click("#signout")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(OUT / "04-signed-out-desktop.png"))
    rec("after_logout_signed_in", ctx.request.get(URL + "/demo/session").json().get("signed_in"))
    rec("after_logout_view", ctx.request.get(URL + "/demo/view", headers=sh).status)

    # Rate limit last; fresh context
    c3 = b.new_context()
    tok = c3.request.get(URL + "/demo/session").json()["csrf"]
    codes = [login({"email": EMAIL, "password": "bad-%d" % i}, token=tok, ctxreq=c3.request).status
             for i in range(8)]
    rec("rate_limit_sequence", codes)
    c3.close()
    b.close()

blob = json.dumps(res)
assert PASSWORD not in blob and EMAIL not in blob.replace("<own-email>", ""), "credential leaked"
(OUT / "live-checks.json").write_text(json.dumps(res, indent=1, sort_keys=True))
print("ok", len(res["checks"]), "checks")
sys.exit(0)
