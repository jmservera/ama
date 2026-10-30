"""Source contracts complement the real-server map interaction browser check."""

import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
APP = (WEB / "app.js").read_text(encoding="utf-8")
CSS = (WEB / "style.css").read_text(encoding="utf-8")
MAP = APP.split("function mapPanel(coordinator = null, filters = null) {", 1)[1].split(
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
        dispose = MAP.split("const dispose = () => {", 1)[1].split("\n  };", 1)[0]
        steps = (
            "slot.inert = true;",
            "toggle.disabled = true;",
            "collapse(false);",
            "seq++;",
            "dialog.remove();",
            "slot.remove();",
            "map?.remove();",
            "map = null;",
        )
        positions = [dispose.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("function expand() {\n    if (slot.inert) return;", MAP)

    def test_no_map_animation_and_bounded_native_layout(self) -> None:
        for expected in (
            "zoomAnimation: false",
            "fadeAnimation: false",
            "markerZoomAnimation: false",
            "keyboard: false, inertia: false",
            "autoPanOnFocus: false",
            "map.panBy(offsets[event.key], { animate: false })",
            "invalidateSize({ pan: true, animate: false })",
        ):
            self.assertIn(expected, MAP)
        for expected in (
            "grid-template-columns:min(19rem,45%) minmax(0,1fr)",
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

    def test_expanded_filters_reuse_and_restore_original_controls(self) -> None:
        self.assertIn('h("div", { class: "map-filter-slot" }, filters)', MAP)
        self.assertIn("if (filters) box.insertBefore(filters, workspace)", MAP)
        self.assertIn("if (filters) filterSlot.append(filters)", MAP)
        self.assertIn("filters: filterSlot", MAP)
        overview = APP.split("async function overviewView() {", 1)[1].split(
            "\nasync function visitsView()", 1
        )[0]
        self.assertIn("mapPanel(null, filters)", overview)
        self.assertIn('button.setAttribute("aria-pressed", String(selected))', overview)
        self.assertIn('button.querySelector(".tile-selection").textContent', overview)
        self.assertIn("if (ovState.flag === f) return", overview)
        self.assertNotIn("replaceChildren", overview)
        self.assertNotIn("return mp.draw", overview)
        self.assertIn('id: "mapArea", name: "area", autocomplete: "off"', overview)

    def test_compact_filters_wrap_scroll_and_preserve_map_space(self) -> None:
        for expected in (
            ".map-dialog .overview-map-filters",
            "minmax(min(100%,8rem),1fr)",
            "max-height:45%;overflow:auto;overscroll-behavior:contain",
            ".overview-map-filters .tile.static{display:none}",
            ".overview-map-filters .tile strong{font-size:var(--fs-base)}",
            ".overview-map-filters+.map-workspace",
            "flex-basis:14rem;flex-shrink:0;min-height:14rem",
        ):
            self.assertIn(expected, CSS)


if __name__ == "__main__":
    unittest.main()
