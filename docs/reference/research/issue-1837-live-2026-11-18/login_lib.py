"""Shared sign-in for the issue 1837 live probes. Reads credentials at run time; never prints them."""
import os, re

APP = os.environ["DEMO_API_URL"]
home = os.path.expanduser("~")


def _rd(name):
    return open(os.path.join(home, name)).read().split("\n")[0].strip()


def sign_in(page):
    user, pw = _rd(".ama-test-user-id"), _rd(".ama-test-user")
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", user)
    page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw)
    page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
