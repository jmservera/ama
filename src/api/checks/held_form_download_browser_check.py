"""Browser evidence for the Held draft download on the Funding screen (#96, demo only).

Run from src/api with the src packages and Playwright/Chromium installed:
PYTHONDONTWRITEBYTECODE=1 python -m checks.held_form_download_browser_check

Real server authorization throughout: no route is mocked. The owned loopback server is started
with the default-OFF synthetic-demo switch set only here. The schema, source document, staged
candidate and working review are made through the real APIs as the Retrofit Programme Manager
before the observation window, so no page request after sign-in may write. Engineering evidence
only: no axe scan, no assistive-technology or WCAG acceptance.
"""

from __future__ import annotations

import base64
import hashlib
import json
import runpy
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.role_screens_fixtures import synthetic_data
from checks.schema_download_browser_check import (
    DENIED,
    SAFE_METHODS,
    open_funding_screen,
    schema_body,
)

CASE_PATH = "/api/cases/ZF-1"
LINK = 'a[download="held-form-draft-export.json"]'
LABEL = "Download Held draft (unreviewed)"
ENV = {"ZF_FORM_HELD_DOWNLOAD": "synthetic-demo-only", "ZF_DEPLOYMENT_PROFILE": "demo"}
BODY_KEYS = (
    "draft_id",
    "input_version",
    "schema_id",
    "schema_version",
    "schema_digest",
    "template",
    "rule_refs",
    "fields",
    "history",
    "attachments",
    "stale_fields",
    "open_issues",
)


def staging_batch(document_id: str) -> dict[str, Any]:
    tests = str(ROOT / "src/core/tests/test_form_staging.py")
    batch: dict[str, Any] = runpy.run_path(tests)["batch"](document_id)
    return batch


def post(page: Page, base: str, path: str, body: dict[str, Any], status: int) -> Any:
    response = page.request.post(base + path, data=body)
    check(f"setup {path} returned {status}: {response.status}", response.status == status)
    return response.json()


def prepare_review(page: Page, base: str) -> dict[str, Any]:
    post(page, base, "/api/form-schemas", schema_body(), 201)
    post(
        page,
        base,
        CASE_PATH + "/upload",
        dict(
            name="synthetic.txt",
            kind="EPC",
            data=base64.b64encode(b"EPC D\nEPC E").decode(),
            source="SYN fixture supplied register",
            source_version="fixture-1",
            reason="Synthetic browser operation",
            handoff_version=0,
        ),
        200,
    )
    case = page.request.get(base + CASE_PATH).json()
    doc = next(d for d in case["documents"] if d["name"] == "synthetic.txt")
    staged = post(page, base, CASE_PATH + "/form-candidates", staging_batch(doc["id"]), 201)
    draft = post(
        page,
        base,
        CASE_PATH + "/form-review",
        dict(action="open", schema_id="SYN-TECH", schema_version=1),
        201,
    )
    post(
        page,
        base,
        CASE_PATH + "/form-review",
        dict(
            action="review",
            draft_id=draft["draft_id"],
            expected_version=draft["input_version"],
            field_id="epc",
            decision="accept",
            batch_id=staged["id"],
            candidate_id=staged["candidates"][0]["id"],
            value=None,
            reason="SYN field review reason",
        ),
        201,
    )
    review = page.request.get(base + CASE_PATH + "/form-review").json()
    check("review view reports the download switch on", review.get("held_download_enabled") is True)
    shown: dict[str, Any] = review["drafts"][0]
    return shown


def tab_to_link(page: Page) -> bool:
    for _ in range(200):
        page.keyboard.press("Tab")
        if page.evaluate("(sel) => document.activeElement.matches(sel)", LINK):
            return True
    return False


def read_download(page: Page, tmp: Path) -> tuple[Any, dict[str, Any]]:
    with page.expect_download() as pending:
        page.keyboard.press("Enter")
    download = pending.value
    saved = tmp / "held.json"
    download.save_as(saved)
    return download, json.loads(saved.read_text(encoding="utf-8"))


def authorized_story(browser: Any, base: str, tmp: Path) -> None:
    story = "pam held download"
    context = browser.new_context(viewport={"width": 1280, "height": 900}, accept_downloads=True)
    try:
        page = context.new_page()
        errors: list[str] = []
        writes: list[str] = []
        urls: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        open_funding_screen(page, base, "pam@example.test")
        shown = prepare_review(page, base)
        page.reload()
        page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
        page.on(
            "request",
            lambda r: (
                writes.append(f"{r.method} {r.url}") if r.method not in SAFE_METHODS else None
            ),
        )
        page.on("request", lambda r: urls.append(r.url))
        link = page.locator(LINK)
        link.wait_for()
        check(f"{story} one link only", link.count() == 1)
        check(f"{story} link text", link.inner_text() == LABEL)
        check(
            f"{story} no automatic download or export request on load",
            not any("held-export" in u for u in urls),
        )
        text = page.locator("main, body").first.inner_text()
        check(
            f"{story} states Not submitted and eligibility Not assessed",
            "Not submitted; eligibility Not assessed." in text,
        )
        check(
            f"{story} states the version on screen may be older",
            f"may be newer than input version {shown['input_version']}" in text,
        )
        check(f"{story} reaches the link by keyboard Tab", tab_to_link(page))
        download, body = read_download(page, tmp)
        check(
            f"{story} suggests the fixed filename",
            download.suggested_filename == "held-form-draft-export.json",
        )
        check(
            f"{story} status Held, unreviewed, not submitted, not assessed",
            (body["status"], body["reviewed"], body["submission"], body["eligibility"])
            == ("Held", False, "Not submitted", "Not assessed"),
        )
        check(f"{story} names this draft", body["draft_id"] == shown["draft_id"])
        check(
            f"{story} history carries the reviewer",
            body["history"] and body["history"][0]["reviewer"] == "pam@example.test",
        )
        digest = hashlib.sha256(
            json.dumps(
                {k: body[k] for k in BODY_KEYS}, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        check(f"{story} integrity hash matches the body", digest == body["content_sha256"])
        check(f"{story} carries both notices", body["notice"] and body["working_notice"])
        check(f"{story} made no non-GET/HEAD/OPTIONS page requests: {writes}", not writes)

        diagnosed = page.request.post(
            base + CASE_PATH + "/form-review",
            data=dict(
                action="diagnose",
                draft_id=shown["draft_id"],
                expected_version=shown["input_version"],
            ),
        )
        check(f"{story} setup bump returned 201: {diagnosed.status}", diagnosed.status == 201)
        check(
            f"{story} on-screen version stays as loaded",
            f"input version {shown['input_version']} " in page.locator("body").inner_text(),
        )
        page.locator(LINK).focus()
        _, newer = read_download(page, tmp)
        check(
            f"{story} later download is the current review, not the screen version: "
            f"{newer['input_version']} > {shown['input_version']}",
            newer["input_version"] > shown["input_version"],
        )

        page.set_viewport_size({"width": 360, "height": 800})
        page.locator(LINK).scroll_into_view_if_needed()
        box = page.locator(LINK).bounding_box()
        check(
            f"{story} link fits a 360px viewport",
            box is not None and box["x"] >= 0 and box["x"] + box["width"] <= 360 + 1,
        )
        check(f"{story} has no JavaScript errors: {errors}", not errors)
    finally:
        context.close()


def denied_story(browser: Any, base: str, email: str) -> None:
    story = f"{email.split('@')[0]} held download denied"
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        page = context.new_page()
        open_funding_screen(page, base, email)
        check(f"{story} shows no download link", page.locator(LINK).count() == 0)
        direct = page.request.get(base + CASE_PATH + "/form-review/UNKNOWN/held-export")
        check(f"{story} direct URL is refused: {direct.status}", direct.status == 403)
        check(
            f"{story} refusal is not an attachment",
            "attachment" not in direct.headers.get("content-disposition", ""),
        )
    finally:
        context.close()


def run_browser(base: str) -> None:
    import tempfile

    with sync_playwright() as playwright, tempfile.TemporaryDirectory(prefix="zf-held-") as scratch:
        browser = playwright.chromium.launch()
        try:
            authorized_story(browser, base, Path(scratch))
            for email in DENIED:
                denied_story(browser, base, email)
        finally:
            browser.close()
    print(
        "COMPLETE: Held draft download (authorized, keyboard, snapshot) and denials checked; "
        "no axe scan here"
    )


if __name__ == "__main__":
    main(run_browser, synthetic_data, env_overrides=ENV)
