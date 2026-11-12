"""Browser evidence for the Held draft download on the Funding screen (#96, demo only).

Run from src/api with the src packages and Playwright/Chromium installed:
PYTHONDONTWRITEBYTECODE=1 python -m checks.held_form_download_browser_check

Real server authorization throughout: the only page-level interception is the injected failure
and held-response cases of the saved copy checker, which are labelled in the check output. The owned loopback server is started
with the default-OFF synthetic-demo switch set only here. The schema, source document, staged
candidate and working review are made through the real APIs as the Retrofit Programme Manager
before the observation window, so no page request after sign-in may write, except exactly one
read-only freshness POST per press of the saved copy checker. The numeric fidelity cases use
genuinely downloaded synthetic copies. Engineering evidence only: the axe scan of the checker
group runs only when ZF_AXE_JS names the pinned 4.10.3 file; no assistive-technology or WCAG
acceptance.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
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
GROUP = '[role="group"][aria-label="Check a saved Held copy"]'
FILE_LABEL = "Saved Held draft file"
BUTTON = "Check saved Held copy (read-only)"
RESULT = '[data-held-check="result"]'
FRESH_SUFFIX = "/held-export/freshness"
CURRENT_TEXT = "The details checked in this file match the working review now."
NOT_RUN_TEXT = "The check could not run, so nothing is judged about your file."
RESULT_WORDS = ("Invalid", "Stale", "Current", "Unavailable")
SOURCE_TEXT = b"EPC D\nEPC E\n12.0\n9007199254740993\n"
BIG_INTEGER = 9007199254740993
AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
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


def area_batch(document_id: str, raw: str, start: int) -> dict[str, Any]:
    body = staging_batch(document_id)
    body["candidates"] = [
        dict(field_id="area", raw_value=raw, locator=dict(start=start, end=start + len(raw)))
    ]
    return body


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
            data=base64.b64encode(SOURCE_TEXT).decode(),
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


def read_download(page: Page, tmp: Path, name: str = "held.json") -> tuple[Any, dict[str, Any]]:
    with page.expect_download() as pending:
        page.keyboard.press("Enter")
    download = pending.value
    saved = tmp / name
    download.save_as(saved)
    return download, json.loads(saved.read_text(encoding="utf-8"))


def field_row(body: dict[str, Any], field_id: str) -> dict[str, Any]:
    row: dict[str, Any] = next(r for r in body["fields"] if r["field_id"] == field_id)
    return row


def write_copy(tmp: Path, name: str, body: dict[str, Any]) -> Path:
    path = tmp / name
    path.write_text(json.dumps(body), encoding="utf-8")
    return path


def reseal(body: dict[str, Any]) -> dict[str, Any]:
    sealed = dict(body)
    sealed["content_sha256"] = hashlib.sha256(
        json.dumps(
            {k: sealed[k] for k in BODY_KEYS}, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    return sealed


class Checker:
    """Drives the saved Held copy control on the Funding screen and counts its requests."""

    def __init__(self, page: Page, fresh: list[str], tmp: Path) -> None:
        self.page = page
        self.fresh = fresh
        self.tmp = tmp
        self.group = page.locator(GROUP)
        self.file_input = self.group.get_by_label(FILE_LABEL)
        self.button = self.group.get_by_role("button", name=BUTTON, exact=True)
        self.result = self.group.locator(RESULT)

    def settle(self) -> str:
        self.page.wait_for_function(
            "(sel) => { const e = document.querySelector(sel);"
            " return !!e && e.textContent.trim() !== '' && !e.textContent.startsWith('Checking'); }",
            arg=GROUP + " " + RESULT,
        )
        self.button.and_(self.page.locator(":enabled")).wait_for()
        return self.result.inner_text()

    def press(self, path: Path) -> tuple[str, int]:
        self.file_input.set_input_files(str(path))
        before = len(self.fresh)
        self.button.click()
        text = self.settle()
        return text, len(self.fresh) - before

    def active(self) -> str:
        return str(
            self.page.evaluate(
                "() => document.activeElement.tagName + ':' + (document.activeElement.type || '')"
            )
        )

    def storage(self) -> str:
        return str(
            self.page.evaluate(
                "() => JSON.stringify([Object.entries(localStorage), Object.entries(sessionStorage)])"
            )
        )

    def stringified(self, path: Path, draft_id: str) -> str:
        """The shared-helper behaviour: parse then JSON.stringify, to prove the fidelity test bites."""
        return str(
            self.page.evaluate(
                """async ([url, text]) => {
                    const res = await fetch(url, { method: "POST",
                        headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" },
                        body: JSON.stringify(JSON.parse(text)) });
                    return (await res.json()).status;
                }""",
                [
                    CASE_PATH + f"/form-review/{draft_id}/held-export/freshness",
                    path.read_text(encoding="utf-8"),
                ],
            )
        )


def answer(status: int, body: str) -> Any:
    def handler(route: Any) -> None:
        route.fulfill(status=status, content_type="application/json", body=body)

    return handler


def axe_scan(page: Page, story: str) -> None:
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        print(f"SKIP {story} axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate(
        """async (sel) => await axe.run(document.querySelector(sel), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""",
        GROUP,
    )
    check(
        f"{story} axe 4.10.3 (checker group with a result, 1280px) finds no violations: "
        f"{[v['id'] for v in result['violations']]}",
        not result["violations"],
    )


def failure_story(story: str, checker: Checker, copy_path: Path) -> None:
    page = checker.page
    cases = [
        (
            503,
            '{"error":"Form storage failed. Reload before retrying; no approval or submission occurred."}',
            "503",
        ),
        (502, '{"error":"The document store is unavailable."}', "502"),
        (409, '{"error":"The form or source changed. Reload before retrying."}', "409"),
        (404, '{"error":"Not found."}', "404"),
        (403, '{"error":"Your role does not include this."}', "403"),
        (400, '{"error":"Could not read that."}', "400"),
        (200, "not json", "unparseable 200"),
        (200, '{"status":"Maybe","reviewed":false}', "unknown status"),
        (500, "<html>boom</html>", "5xx without JSON"),
    ]
    for status, body, label in cases:
        page.route("**" + FRESH_SUFFIX, answer(status, body))
        text, sent = checker.press(copy_path)
        page.unroute("**" + FRESH_SUFFIX)
        check(
            f"{story} {label} sends one request and names a next action: {text}",
            sent == 1 and "Next action" in text,
        )
        check(
            f"{story} {label} is never shown as a result word, an approval or a write: {text}",
            not any(word in text for word in RESULT_WORDS),
        )
    page.route("**" + FRESH_SUFFIX, lambda route: route.abort())
    text, _ = checker.press(copy_path)
    page.unroute("**" + FRESH_SUFFIX)
    check(f"{story} network failure says the check could not run: {text}", NOT_RUN_TEXT in text)


def lifecycle_story(story: str, checker: Checker, first: Path, second: Path) -> None:
    page = checker.page
    held: list[Any] = []
    page.route("**" + FRESH_SUFFIX, lambda route: held.append(route))
    checker.file_input.set_input_files(str(first))
    checker.button.click()
    for _ in range(100):
        if held:
            break
        page.wait_for_timeout(50)
    check(f"{story} press sends the request", len(held) == 1)
    checker.button.press("Enter", no_wait_after=True)
    page.wait_for_timeout(300)
    check(f"{story} second press while pending sends no second request", len(held) == 1)
    checker.file_input.focus()
    checker.file_input.set_input_files(str(second))
    check(
        f"{story} changing the file clears the pending status",
        checker.result.inner_text().strip() == "",
    )
    held[0].fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(
            dict(
                status="Stale",
                stale_fields=["epc"],
                unaffected_fields=[],
                reasons=["x"],
                action="y",
                reviewed=False,
            )
        ),
    )
    checker.button.and_(page.locator(":enabled")).wait_for()
    page.wait_for_timeout(200)
    check(f"{story} an obsolete response is ignored", checker.result.inner_text().strip() == "")
    check(f"{story} focus the person moved is not taken", checker.active() == "INPUT:file")
    page.unroute("**" + FRESH_SUFFIX)


def numeric_story(
    story: str, checker: Checker, page: Page, base: str, tmp: Path, draft_id: str, doc_id: str
) -> None:
    for label, raw, start, value, name in (
        ("float 12.0", "12.0", 12, 12.0, "area-float.json"),
        ("integer above 2^53", str(BIG_INTEGER), 17, BIG_INTEGER, "area-big.json"),
    ):
        staged = post(
            page, base, CASE_PATH + "/form-candidates", area_batch(doc_id, raw, start), 201
        )
        view = page.request.get(base + CASE_PATH + "/form-review").json()["drafts"][0]
        post(
            page,
            base,
            CASE_PATH + "/form-review",
            dict(
                action="review",
                draft_id=draft_id,
                expected_version=view["input_version"],
                field_id="area",
                decision="correct",
                batch_id=staged["id"],
                candidate_id=staged["candidates"][0]["id"],
                value=value,
                reason="SYN numeric correction",
            ),
            201,
        )
        page.locator(LINK).focus()
        read_download(page, tmp, name)
        raw_text = (tmp / name).read_text(encoding="utf-8")
        check(f"{story} downloaded copy keeps {label} as written", f'"value": {raw}' in raw_text)
        text, sent = checker.press(tmp / name)
        check(
            f"{story} genuine unedited copy with {label} is Current: {text}",
            sent == 1 and CURRENT_TEXT in text,
        )
        check(
            f"{story} the shared stringify path would wrongly say Invalid for {label}",
            checker.stringified(tmp / name, draft_id) == "Invalid",
        )


def saved_copy_checks(
    page: Page, base: str, tmp: Path, shown: dict[str, Any], fresh: list[str]
) -> None:
    story = "pam saved copy check"
    checker = Checker(page, fresh, tmp)
    draft_id = shown["draft_id"]
    check(
        f"{story} shows one labelled file input and one button",
        (checker.group.count(), checker.file_input.count(), checker.button.count()) == (1, 1, 1),
    )
    check(f"{story} no freshness request on load: {fresh}", not fresh)
    original, newer = tmp / "original.json", tmp / "newer.json"
    checker.file_input.set_input_files(str(newer))
    page.wait_for_timeout(200)
    check(f"{story} choosing a file sends no request", not fresh)
    checker.file_input.set_input_files([])
    checker.button.click()
    page.wait_for_timeout(200)
    check(
        f"{story} pressing with no file sends no request and flags the input",
        not fresh and checker.file_input.get_attribute("aria-invalid") == "true",
    )
    check(
        f"{story} no-file error is next to the input",
        "Choose" in checker.group.locator(".field-error").inner_text(),
    )

    before = checker.storage()
    checker.file_input.set_input_files(str(newer))
    checker.file_input.focus()
    page.keyboard.press("Tab")
    check(
        f"{story} Tab from the file input reaches the button", checker.active() == "BUTTON:button"
    )
    page.keyboard.press("Enter")
    text = checker.settle()
    check(f"{story} Enter runs exactly one POST: {len(fresh)}", len(fresh) == 1)
    check(
        f"{story} Current wording is bounded: {text}",
        text.startswith("Current.")
        and CURRENT_TEXT in text
        and "not an approval" in text.lower()
        and "genuine" in text,
    )
    check(
        f"{story} result shows no field values",
        "9007199254740993" not in text and "SYN" not in text,
    )
    check(f"{story} nothing is stored in the browser", checker.storage() == before)
    check(
        f"{story} focus stays on the button after the result: {checker.active()}",
        checker.active() == "BUTTON:button",
    )

    axe_scan(page, story)
    text, sent = checker.press(original)
    check(
        f"{story} an older copy is Stale with a next action: {text}",
        sent == 1 and text.startswith("Stale.") and "Next action" in text,
    )

    edited = json.loads(newer.read_text(encoding="utf-8"))
    field_row(edited, "epc")["value"] = "G"
    text, _ = checker.press(write_copy(tmp, "edited.json", edited))
    check(
        f"{story} an edited copy is Invalid and names no field: {text}",
        text.startswith("Invalid.") and "epc" not in text,
    )

    forged = json.loads(newer.read_text(encoding="utf-8"))
    field_row(forged, "epc")["field_id"] = "<b>x</b>"
    text, _ = checker.press(write_copy(tmp, "forged.json", reseal(forged)))
    check(
        f"{story} a forged field id is shown as text: {text}",
        "<b>x</b>" in text and checker.result.locator("b").count() == 0,
    )

    other = json.loads(newer.read_text(encoding="utf-8"))
    other["draft_id"] = "OTHER-DRAFT"
    text, _ = checker.press(write_copy(tmp, "other.json", other))
    check(
        f"{story} another draft's file is refused in plain words: {text}",
        "Choose the saved Held file for this draft" in text,
    )

    notes = tmp / "notes.txt"
    notes.write_text("not json", encoding="utf-8")
    before_sent = len(fresh)
    text, _ = checker.press(notes)
    check(
        f"{story} a non-JSON file is refused locally: {text}",
        len(fresh) == before_sent and "could not read" in text.lower(),
    )

    failure_story(story, checker, newer)
    lifecycle_story(story, checker, newer, original)
    numeric_story(story, checker, page, base, tmp, draft_id, document_id_of(page, base))

    page.set_viewport_size({"width": 360, "height": 800})
    checker.group.scroll_into_view_if_needed()
    boxes = [checker.file_input.bounding_box(), checker.button.bounding_box()]
    check(
        f"{story} control fits a 360px viewport",
        all(b is not None and b["x"] >= 0 and b["x"] + b["width"] <= 361 for b in boxes)
        and page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1"),
    )
    page.set_viewport_size({"width": 1280, "height": 900})


def document_id_of(page: Page, base: str) -> str:
    case = page.request.get(base + CASE_PATH).json()
    return str(next(d for d in case["documents"] if d["name"] == "synthetic.txt")["id"])


def session_end_check(page: Page, checker: Checker, newer: Path) -> None:
    story = "pam saved copy check"
    page.route(
        "**" + FRESH_SUFFIX,
        lambda route: route.fulfill(
            status=401, content_type="application/json", body='{"error":"Please sign in."}'
        ),
    )
    checker.file_input.set_input_files(str(newer))
    checker.button.click()
    page.get_by_text("Your session has ended. Sign in again.").first.wait_for()
    page.unroute("**" + FRESH_SUFFIX)
    check(f"{story} a 401 returns the person to sign in", page.locator("#email").count() == 1)


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
        fresh: list[str] = []

        def observe(request: Any) -> None:
            urls.append(request.url)
            if request.method == "POST" and request.url.endswith(FRESH_SUFFIX):
                fresh.append(request.url)
            elif request.method not in SAFE_METHODS:
                writes.append(f"{request.method} {request.url}")

        page.on("request", observe)
        page.reload()
        page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
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
        download, body = read_download(page, tmp, "original.json")
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
        check(f"{story} no freshness POST before any press: {fresh}", not fresh)

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
        _, newer = read_download(page, tmp, "newer.json")
        check(
            f"{story} later download is the current review, not the screen version: "
            f"{newer['input_version']} > {shown['input_version']}",
            newer["input_version"] > shown["input_version"],
        )

        saved_copy_checks(page, base, tmp, shown, fresh)
        page.set_viewport_size({"width": 360, "height": 800})
        page.locator(LINK).scroll_into_view_if_needed()
        box = page.locator(LINK).bounding_box()
        check(
            f"{story} link fits a 360px viewport",
            box is not None and box["x"] >= 0 and box["x"] + box["width"] <= 360 + 1,
        )
        session_end_check(page, Checker(page, fresh, tmp), tmp / "newer.json")
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
        check(f"{story} shows no saved copy checker", page.locator(GROUP).count() == 0)
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
        "COMPLETE: Held draft download, saved copy checker (authorized, keyboard, numeric fidelity, "
        "failures) and denials checked; axe scan of the checker group only when ZF_AXE_JS is set; "
        "no assistive-technology acceptance"
    )


if __name__ == "__main__":
    main(run_browser, synthetic_data, env_overrides=ENV)
