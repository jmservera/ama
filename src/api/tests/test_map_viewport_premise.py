"""The viewport premise check must attribute its map read to the viewport change (issue 1828)."""

import contextlib
import unittest
from collections.abc import Callable, Iterator
from typing import Any
from unittest.mock import patch

from checks import map_fullscreen_browser_check as check_module

ZOOM = 15
OLD_WIDTH = 1200
NEW_WIDTH = 1160


class Request:
    def __init__(self, url: str) -> None:
        self.url = url


def read_url(width_px: float) -> str:
    degrees = width_px * 360 / (256 * 2**ZOOM)
    return f"/api/map?area=Point%20examples&zoom={ZOOM}&bbox=51.0,-1.0,51.1,{-1.0 + degrees}"


class FakePage:
    """Virtual-clock stand-in for the Playwright calls the premise check makes."""

    def __init__(self, resize_reads: list[tuple[int, int]], stale_reads: list[int]) -> None:
        self.now = 0
        self.width = OLD_WIDTH
        self.container_follows_viewport = True
        self.viewport = {"width": 1280, "height": 900}
        self.listeners: list[Callable[[Request], None]] = []
        self.events: list[tuple[int, str]] = [(at, read_url(OLD_WIDTH)) for at in stale_reads]
        self.resize_reads = resize_reads
        self.log: list[str] = []

    @property
    def viewport_size(self) -> dict[str, int]:
        return dict(self.viewport)

    def set_viewport_size(self, size: dict[str, int]) -> None:
        shrunk = size["width"] < self.viewport["width"]
        self.viewport = dict(size)
        if self.container_follows_viewport:
            self.width = NEW_WIDTH if shrunk else OLD_WIDTH
        if shrunk:
            self.events += [
                (self.now + after, read_url(width)) for after, width in self.resize_reads
            ]

    def on(self, name: str, listener: Callable[[Request], None]) -> None:
        self.listeners.append(listener)

    def remove_listener(self, name: str, listener: Callable[[Request], None]) -> None:
        self.listeners.remove(listener)

    def wait_for_timeout(self, ms: int) -> None:
        self.now += ms
        for event in [item for item in self.events if item[0] <= self.now]:
            self.events.remove(event)
            self.log.append(event[1])
            for listener in list(self.listeners):
                listener(Request(event[1]))

    def locator(self, selector: str) -> "FakePage":
        return self

    def get_attribute(self, name: str) -> None:
        return None

    def evaluate(self, script: str, *args: Any) -> int:
        return self.width

    @contextlib.contextmanager
    def expect_request(
        self, predicate: Callable[[Request], bool], timeout: int = 30000
    ) -> Iterator[None]:
        seen: list[Request] = []
        self.on("request", seen.append)
        yield
        waited = 0
        while not any(predicate(request) for request in seen) and waited < timeout:
            self.wait_for_timeout(50)
            waited += 50
        self.remove_listener("request", seen.append)
        if not any(predicate(request) for request in seen):
            raise TimeoutError("no matching request")


class ViewportPremiseTests(unittest.TestCase):
    def run_check(self, page: FakePage) -> None:
        def monotonic() -> float:
            return page.now / 1000

        with patch.object(check_module.time, "monotonic", monotonic):
            check_module.check_viewport_change_requests_map(page)  # type: ignore[arg-type]

    def test_read_pending_from_the_previous_step_does_not_satisfy_the_premise(self) -> None:
        page = FakePage(resize_reads=[], stale_reads=[150])
        with self.assertRaises(AssertionError):
            self.run_check(page)
        self.assertEqual(page.viewport["width"], 1280)

    def test_read_for_the_resized_viewport_satisfies_the_premise(self) -> None:
        page = FakePage(resize_reads=[(200, NEW_WIDTH)], stale_reads=[150])
        self.run_check(page)
        self.assertEqual(page.viewport["width"], 1280)

    def test_read_with_the_old_viewport_width_after_the_resize_is_not_attributed(self) -> None:
        page = FakePage(resize_reads=[(200, OLD_WIDTH)], stale_reads=[])
        with self.assertRaises(AssertionError):
            self.run_check(page)

    def test_premise_is_unprovable_when_the_container_does_not_change_width(self) -> None:
        page = FakePage(resize_reads=[(200, NEW_WIDTH)], stale_reads=[])
        page.container_follows_viewport = False
        with self.assertRaises(AssertionError):
            self.run_check(page)


if __name__ == "__main__":
    unittest.main()
