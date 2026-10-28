"""Source contracts complement the real-server map interaction browser check."""

import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
APP = (WEB / "app.js").read_text(encoding="utf-8")
CSS = (WEB / "style.css").read_text(encoding="utf-8")
MAP = APP.split("function mapPanel(coordinator = null) {", 1)[1].split(
    "\nasync function coordinatorView()", 1
)[0]


class MapFullscreen(unittest.TestCase):
    def test_native_dialog_and_named_summary(self) -> None:
        for expected in (
            'h("dialog", { class: "map-dialog", "aria-labelledby": "map-title"',
            "dialog.showModal()",
            '"aria-expanded": "false"',
            '"aria-labelledby": "map-home-title"',
            '"aria-label": "Close home summary"',
            'h("span", { "aria-hidden": "true" }, "\\u00d7")',
        ):
            self.assertIn(expected, MAP)

    def test_summary_uses_only_permitted_map_fields_and_native_link(self) -> None:
        self.assertIn('h("a", { class: "btn" }, "Open home")', MAP)
        for field in ("name", "address", "id", "stage", "kind"):
            self.assertIn(f"point.{field}", MAP)
        self.assertIn("Address not included in this map", MAP)
        self.assertIn('stage.textContent = point.stage || "Unknown"', MAP)
        self.assertNotIn("innerHTML", MAP)
        self.assertNotIn("api(`/api/cases/", MAP)
        self.assertNotIn("bindTooltip", MAP)
        self.assertIn("mapAction(m, () => showHome(p))", MAP)

    def test_dismissal_and_stable_focus_contract(self) -> None:
        for expected in (
            'event.key === "Escape" && selectedId !== null',
            "event.stopPropagation()",
            'map.on("click", () => closeHome())',
            "markers.get(id)?.getElement()",
            "target?.isConnected ? target : el",
            "title.focus()",
            "toggle.focus({ preventScroll: true })",
            "else if (focusedMarker) restoreMarker(focusedMarker)",
        ):
            self.assertIn(expected, MAP)

    def test_route_cleanup_and_stale_response_protection(self) -> None:
        for expected in (
            'signal.addEventListener("abort", dispose, { once: true })',
            'signal.removeEventListener("abort", dispose)',
            "map?.remove()",
            "dialog.remove()",
            "signal.aborted || my !== seq",
            "point.id === previousSelection",
            "else closeHome(false)",
        ):
            self.assertIn(expected, MAP)
        self.assertIn("function login(msg) {\n  disposeMapPanel?.();", APP)

    def test_no_map_animation_and_bounded_native_layout(self) -> None:
        for expected in (
            "zoomAnimation: false",
            "fadeAnimation: false",
            "markerZoomAnimation: false",
            "keyboard: false, inertia: false",
            "autoPanOnFocus: false",
            "map.panBy(offsets[event.key], { animate: false })",
            "invalidateSize({ pan: false, animate: false })",
        ):
            self.assertIn(expected, MAP)
        for expected in (
            "grid-template-columns:19rem minmax(0,1fr)",
            "height:calc(100dvh",
            "overscroll-behavior:contain",
            "env(safe-area-inset-top)",
            ".map-home-close",
        ):
            self.assertIn(expected, CSS)

    def test_manual_links_and_coordinator_exit_remain_available(self) -> None:
        self.assertIn('href: "#/all"', MAP)
        self.assertIn('h("a", { href: `#/case/${encodeURIComponent(p.id)}` }', MAP)
        self.assertIn('document.getElementById("coordinator-records").focus()', MAP)
        self.assertIn("collapse(false);", MAP)
        self.assertIn("Show the map areas as a list", MAP)


if __name__ == "__main__":
    unittest.main()
