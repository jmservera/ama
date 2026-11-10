"""Derive the workspace script-retry contract from app.js so browser checks cannot drift from it.

The loader (`retryWorkspaceScript` in app.js) makes one request per declared retry delay after
the initial document-driven load, stops on any outcome other than a script error, and memoises
one attempt sequence per path. The expected totals below come from that declaration, never from
observed requests. The transformations let a check prove that its oracle fails on a changed
loader; they only alter the text served to the page, never the repository file.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from playwright.sync_api import Page, Route

from checks.asset_urls import asset_url

APP_JS = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/app.js"
DECLARATION = re.compile(r"^const SCRIPT_RETRY_DELAYS = \[([^\]]*)\];$", re.MULTILINE)
MEMO_RETURN = "return workspaceScriptLoads.get(path);"
STOP_ON_NON_ERROR = 'if (outcome !== "error") break;'

# The initial load plus the single retry that evaluates without the readiness global and stops.
MISSING_GLOBAL_REQUESTS = 2

EXTRA_DELAY_MS = 250
EXPECT_TIMEOUT_MS = 5000
TIMEOUT_MARGIN_MS = 1000

Mutation = Literal["extra", "early", "reset", "continue"]


def parse_retry_delays(source: str) -> tuple[int, ...]:
    found = DECLARATION.findall(source)
    if len(found) != 1:
        raise ValueError(
            f"expected exactly one SCRIPT_RETRY_DELAYS declaration in app.js, found {len(found)}"
        )
    items = [item.strip() for item in found[0].split(",")]
    if not all(re.fullmatch(r"[1-9][0-9]*", item) for item in items):
        raise ValueError(
            f"malformed SCRIPT_RETRY_DELAYS in app.js: expected positive integers, got [{found[0]}]"
        )
    return tuple(int(item) for item in items)


def retry_delays() -> tuple[int, ...]:
    return parse_retry_delays(APP_JS.read_text(encoding="utf-8"))


def exhausted_requests() -> int:
    """One initial load plus one request for every declared retry delay."""
    return 1 + len(retry_delays())


def declare(source: str, delays: tuple[int, ...]) -> str:
    declaration = f"const SCRIPT_RETRY_DELAYS = [{', '.join(str(delay) for delay in delays)}];"
    return DECLARATION.sub(lambda _: declaration, source, count=1)


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise ValueError(f"expected exactly one occurrence of {old!r}, found {source.count(old)}")
    return source.replace(old, new)


def mutate_app(source: str, kind: Mutation) -> str:
    delays = parse_retry_delays(source)
    if kind == "extra":
        if sum(delays) + EXTRA_DELAY_MS > EXPECT_TIMEOUT_MS - TIMEOUT_MARGIN_MS:
            raise ValueError("the controlled schedule would leave too little expect-timeout margin")
        return declare(source, (*delays, EXTRA_DELAY_MS))
    if kind == "early":
        return declare(source, delays[:-1])
    if kind == "reset":
        return replace_once(
            source,
            MEMO_RETURN,
            "const load = workspaceScriptLoads.get(path);"
            " load.then(() => workspaceScriptLoads.delete(path)); return load;",
        )
    if len(delays) < 2:
        raise ValueError("the continue control needs at least two declared delays")
    return replace_once(source, STOP_ON_NON_ERROR, "")


def serve_mutated_app(page: Page, base: str, kind: Mutation) -> None:
    # Validate eagerly so an unmatched transformation fails loudly, not inside a route callback.
    mutate_app(APP_JS.read_text(encoding="utf-8"), kind)

    def handler(route: Route) -> None:
        response = route.fetch()
        route.fulfill(
            status=response.status,
            headers={"cache-control": "no-store"},
            content_type="text/javascript; charset=utf-8",
            body=mutate_app(response.text(), kind),
        )

    page.route(asset_url("/app.js", base), handler)


def assert_requests(observed: int, expected: int, message: str) -> None:
    if observed != expected:
        raise AssertionError(f"{message}: expected {expected}, observed {observed}")


def expect_detected(
    run: Callable[[], None], message: str, expected: int, observed: int, label: str
) -> None:
    """Pass only when the oracle fails with exactly the counts a changed loader must produce."""
    if expected == observed:
        raise ValueError(f"negative control {label} cannot be told apart from the contract")
    detected = f"{message}: expected {expected}, observed {observed}"
    try:
        run()
    except AssertionError as error:
        if str(error) != detected:
            raise AssertionError(
                f"negative control {label} failed on the wrong assertion: {error}"
            ) from error
        print(f"PASS negative control {label} detected: {detected}", flush=True)
        return
    raise AssertionError(f"negative control {label} was not detected")
