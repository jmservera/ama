"""Epic #149: heading hierarchy, table headers and control names on every role workbench view.

The workbench views are drawn in the browser by the shipped scripts, and the API is a
standard-library server (there is no TestClient), so each role signs in over a real local HTTP
server on constructed data and the rendered DOM of every primary view is read in headless
Chromium. This is engineering evidence of document structure. It is not WCAG conformance,
screen-reader or assistive-technology acceptance, which stay with human testers.
"""

import importlib.util
import unittest
from typing import Any, ClassVar

from role_matrix_fixture import MatrixServer, build

HAS_PLAYWRIGHT = importlib.util.find_spec("playwright") is not None

CASE = "ZF-1"
EXTRA_VIEWS = ("#/screens", "#/handoff-waiting", "#/simulator", "#/import", "#/coordinator")
# Recorded gaps, shrink-only: the staff case lists render their filter and briefing headings
# before the page h1 (the contractor list is correct). A fix must remove the view here so the
# check then enforces it.
H1_NOT_FIRST = {"#/", "#/all"}
LISTS = ("#/", "#/all")

COLLECT = """() => {
  const shown = (e) => !e.closest('[hidden],[inert]')
    && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden';
  const text = (e) => (e.textContent || '').trim();
  const named = (e) => {
    const label = e.getAttribute('aria-label');
    if (label && label.trim()) return true;
    const by = e.getAttribute('aria-labelledby');
    if (by && by.split(/\\s+/).some((id) => {
      const t = document.getElementById(id);
      return t && text(t);
    })) return true;
    if (text(e)) return true;
    return [...e.querySelectorAll('img[alt]')].some((i) => i.alt.trim());
  };
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(shown)
    .map((e) => ({level: Number(e.tagName[1]), text: text(e)}));
  const tables = [...document.querySelectorAll('table')].filter(shown).map((t) => ({
    named: Boolean(t.querySelector('caption') || t.getAttribute('aria-label')
      || t.getAttribute('aria-labelledby')),
    unscoped: [...t.querySelectorAll('th')].filter(
      (th) => !['col', 'row', 'colgroup', 'rowgroup'].includes(th.getAttribute('scope') || '')
    ).length,
  }));
  const controls = [...document.querySelectorAll('a[href],button,[role=button],[role=link]')]
    .filter(shown).filter((e) => !named(e)).map((e) => e.outerHTML.slice(0, 120));
  return {headings, tables, controls};
}"""


class RoleWorkbenchStructure(MatrixServer):
    audit: ClassVar[dict[tuple[str, str], dict[str, Any]]]
    roles: ClassVar[dict[str, list[str]]]

    @classmethod
    def setUpClass(cls) -> None:
        if not HAS_PLAYWRIGHT:
            raise unittest.SkipTest("needs the playwright dev dependency")
        from playwright.sync_api import sync_playwright

        super().setUpClass()
        cls.audit = {}
        cls.roles = {}
        try:
            with sync_playwright() as pw:
                try:
                    browser = pw.chromium.launch()
                except Exception as error:  # pragma: no cover - browser not installed
                    raise unittest.SkipTest(f"needs a Chromium for Playwright: {error}") from error
                try:
                    cls.crawl(browser)
                finally:
                    browser.close()
        except BaseException:
            super().tearDownClass()
            raise

    @classmethod
    def crawl(cls, browser: Any) -> None:
        for user in build()["staff"][:-1]:
            context = browser.new_context()
            login = context.request.post(
                cls.base + "/api/login", data={"email": user["email"], "password": "zf-test"}
            )
            assert login.ok, user["role"]
            navigation = context.request.get(cls.base + "/api/me").json()["navigation"]
            page = context.new_page()

            role = user["role"]
            views = [item["href"] for item in navigation] + [f"#/case/{CASE}", *EXTRA_VIEWS]
            for view in views:
                cls.render(page, role, view)
            screens = page.eval_on_selector_all(
                "nav[aria-label='Specialist screens'] a",
                "(a) => a.map((x) => x.getAttribute('href'))",
            )
            for screen in screens:
                cls.render(page, role, screen)
                cls.render(page, role, f"{screen}&case={CASE}")
            cls.roles[user["role"]] = [v for (r, v) in cls.audit if r == user["role"]]
            context.close()

    @classmethod
    def render(cls, page: Any, role: str, view: str) -> None:
        page.goto(cls.base + "/app" + view)
        page.wait_for_selector("#app h1")
        page.wait_for_load_state("networkidle")
        cls.audit[(role, view)] = page.evaluate(COLLECT)

    def each(self) -> list[tuple[str, str, dict[str, Any]]]:
        return [(role, view, found) for (role, view), found in sorted(self.audit.items())]

    def test_every_role_and_primary_view_was_rendered(self) -> None:
        self.assertEqual(len(self.roles), 8, sorted(self.roles))
        self.assertIn("Contractor", self.roles)
        for role, views in self.roles.items():
            self.assertIn("#/screens", views, role)
            self.assertIn(f"#/case/{CASE}", views, role)
        for role in self.roles:
            if role != "Contractor":
                for view in LISTS:
                    self.assertIn(view, self.roles[role], role)
        self.assertGreater(len(self.audit), 100)

    def test_each_view_has_exactly_one_h1_with_text(self) -> None:
        for role, view, found in self.each():
            with self.subTest(role=role, view=view):
                h1 = [h for h in found["headings"] if h["level"] == 1]
                self.assertEqual(len(h1), 1, found["headings"])
                self.assertTrue(h1[0]["text"])

    def test_heading_levels_never_skip_and_are_never_empty(self) -> None:
        for role, view, found in self.each():
            with self.subTest(role=role, view=view):
                levels = [h["level"] for h in found["headings"]]
                for before, after in zip(levels, levels[1:], strict=False):
                    self.assertLessEqual(after, before + 1, found["headings"])
                self.assertTrue(all(h["text"] for h in found["headings"]), found["headings"])

    def test_h1_comes_first_except_for_the_recorded_list_gap(self) -> None:
        for role, view, found in self.each():
            with self.subTest(role=role, view=view):
                first_is_h1 = found["headings"][0]["level"] == 1
                gap = view in H1_NOT_FIRST and role != "Contractor"
                self.assertEqual(first_is_h1, not gap, f"{view}: update H1_NOT_FIRST")

    def test_data_tables_are_named_and_every_th_has_a_scope(self) -> None:
        seen = 0
        for role, view, found in self.each():
            for table in found["tables"]:
                seen += 1
                with self.subTest(role=role, view=view):
                    self.assertTrue(table["named"], "table needs a caption or aria-label")
                    self.assertEqual(table["unscoped"], 0, "every th needs scope")
        self.assertGreater(seen, 20, "the crawl should reach data tables")

    def test_links_and_buttons_have_accessible_text(self) -> None:
        for role, view, found in self.each():
            with self.subTest(role=role, view=view):
                self.assertEqual(found["controls"], [])


if __name__ == "__main__":
    unittest.main()
