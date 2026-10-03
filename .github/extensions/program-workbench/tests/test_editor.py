import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from playwright.sync_api import sync_playwright, expect


EXTENSION = Path(__file__).resolve().parents[1]
DOCUMENT = """---
title: Editor fixture
ms.date: 2026-10-03
---

## Original heading

Text with **bold**, `code` and [relative link](./other.md).

* First item
* Second item

| Name | Value |
| --- | --- |
| One | Two |
"""


class EditorIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.root = Path(cls.directory.name)
        (cls.root / "docs").mkdir()
        (cls.root / "README.md").write_text("# Test workspace\n", encoding="utf-8")
        (cls.root / "docs" / "fixture.md").write_text(DOCUMENT, encoding="utf-8")
        (cls.root / "docs" / "other.md").write_text("# Other document\n", encoding="utf-8")
        (cls.root / "docs" / "callout.md").write_text(
            "---\ntitle: Callout fixture\n---\n\n> [!IMPORTANT]\n> Preserve this.\n",
            encoding="utf-8",
        )
        (cls.root / "docs" / "case_study_48_original.md").write_text(
            "# Protected fixture\n", encoding="utf-8"
        )
        script = (
            f"import {{ startProgramWorkbenchServer }} from {json.dumps((EXTENSION / 'server.mjs').as_uri())};"
            f"const entry = await startProgramWorkbenchServer({{repositoryRoot: {json.dumps(str(cls.root))}, initialPath: 'docs/fixture.md'}});"
            "console.log(entry.url);"
        )
        cls.server = subprocess.Popen(
            ["node", "--input-type=module", "-e", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        cls.url = cls.server.stdout.readline().strip()
        if not cls.url:
            raise RuntimeError(cls.server.stderr.read())
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.terminate()
        cls.server.wait(timeout=10)
        cls.server.stdout.close()
        cls.server.stderr.close()
        cls.directory.cleanup()

    def setUp(self):
        (self.root / "docs" / "fixture.md").write_text(DOCUMENT, encoding="utf-8")
        self.page = self.browser.new_page(viewport={"width": 1600, "height": 1000})
        self.errors = []
        self.external = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.on("console", lambda message: self.errors.append(message.text)
                     if message.type == "error" and "Content Security Policy" in message.text else None)
        self.page.on("request", lambda request: self.external.append(request.url)
                     if not request.url.startswith(self.url) else None)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
        self.page.locator('[data-mode="edit"]').click()

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.assertEqual(self.external, [])
        self.page.close()

    def test_visual_source_toggle_and_save(self):
        self.assertEqual(self.page.locator("#save-button").is_disabled(), True)
        self.page.locator(".toastui-editor-mode-switch").get_by_text("WYSIWYG", exact=True).click()
        self.page.wait_for_timeout(100)
        self.assertTrue(self.page.locator("#save-button").is_disabled())
        visual = self.page.locator(".toastui-editor-ww-container .ProseMirror")
        self.assertIn("Original heading", visual.inner_text())
        self.assertEqual(visual.locator("table").count(), 1)
        visual.locator("h2").click()
        self.page.keyboard.press("End")
        self.page.keyboard.type(" changed")
        self.page.locator(".toastui-editor-mode-switch").get_by_text("Markdown", exact=True).click()
        self.assertIn("Original heading changed", self.page.locator(".toastui-editor-md-container").inner_text())
        self.page.locator("#save-button").click()
        expect(self.page.locator("#save-button")).to_be_disabled()
        saved = (self.root / "docs" / "fixture.md").read_text(encoding="utf-8")
        self.assertTrue(saved.startswith(DOCUMENT.split("##")[0]))
        self.assertIn("Original heading changed", saved)
        self.assertIn("./other.md", saved)
        self.assertIn("|", saved)

    def test_metadata_and_source_fallback(self):
        self.page.locator('[data-mode="preview"]').click()
        self.page.locator('.library-document[data-path="docs/callout.md"]').click()
        expect(self.page.locator("#meta-path")).to_have_text("docs/callout.md")
        self.page.locator('[data-mode="edit"]').click()
        self.assertTrue(self.page.locator("#visual-editor").is_visible())
        self.assertIn("TOAST Markdown mode protects", self.page.locator("#editor-note").inner_text())
        source = self.page.locator(".toastui-editor-md-container .ProseMirror")
        source.click()
        self.page.keyboard.press("Control+End")
        self.page.keyboard.press("Enter")
        self.page.keyboard.type("New source text.")
        self.page.locator("#save-button").click()
        expect(self.page.locator("#save-button")).to_be_disabled()
        saved = (self.root / "docs" / "callout.md").read_text()
        self.assertIn("> [!IMPORTANT]", saved)
        self.assertIn("New source text.", saved)
        self.page.locator('.library-document[data-path="docs/case_study_48_original.md"]').click()
        expect(self.page.locator("#document-title")).to_have_text("Protected fixture")
        self.assertTrue(self.page.locator('[data-mode="edit"]').is_disabled())
        self.assertFalse(self.page.locator("#conversation-button").is_disabled())

    def test_refresh_preserves_dirty_edits_and_reloads_saved_changes(self):
        metadata = self.page.locator("#frontmatter-editor")
        self.page.locator("#frontmatter-wrap summary").click()
        metadata.fill(metadata.input_value().replace("Editor fixture", "Unsaved title"))
        self.page.locator("#refresh-button").click()
        self.page.wait_for_load_state("networkidle")
        self.assertIn("Unsaved title", metadata.input_value())
        self.page.locator("#save-button").click()
        expect(self.page.locator("#save-button")).to_be_disabled()
        (self.root / "docs" / "fixture.md").write_text(
            DOCUMENT.replace("Editor fixture", "External update"), encoding="utf-8"
        )
        self.page.evaluate("window.dispatchEvent(new Event('focus'))")
        expect(self.page.locator("#document-title")).to_have_text("External update")
        self.assertTrue(self.page.locator("#editor-wrap").is_visible())

    def test_actual_repository_documents_open_without_rewriting(self):
        repo = EXTENSION.parents[2]
        for relative in [
            "docs/ideas/idea-register.md",
            "docs/brds/agentic-retrofit-programme-brd.md",
            "docs/reference/research/sector/housing-association-primer.md",
        ]:
            source = repo / relative
            target = self.root / "docs" / source.name
            original = source.read_bytes()
            target.write_bytes(original)
            self.page.locator("#refresh-button").click()
            self.page.wait_for_load_state("networkidle")
            self.page.locator(f'.library-document[data-path="docs/{source.name}"]').click()
            expect(self.page.locator("#meta-path")).to_have_text(f"docs/{source.name}")
            self.page.locator('[data-mode="edit"]').click()
            expect(self.page.locator("#save-button")).to_be_disabled()
            if self.page.locator("#visual-editor").is_visible():
                self.page.locator(".toastui-editor-mode-switch").get_by_text("WYSIWYG", exact=True).click()
                self.page.locator(".toastui-editor-mode-switch").get_by_text("Markdown", exact=True).click()
                expect(self.page.locator("#save-button")).to_be_disabled()
            self.assertEqual(target.read_bytes(), original)

    def test_raw_edit_and_new_callout_blocks_visual_conversion(self):
        raw = self.page.locator(".toastui-editor-md-container .ProseMirror")
        raw.click()
        self.page.keyboard.press("Control+End")
        self.page.keyboard.press("Enter")
        self.page.keyboard.type("> [!IMPORTANT]")
        self.page.locator(".toastui-editor-mode-switch").get_by_text("WYSIWYG", exact=True).click()
        expect(self.page.locator("#editor-note")).to_contain_text("Keep editing in Markdown mode")
        self.assertTrue(raw.is_visible())
        self.page.locator("#save-button").click()
        expect(self.page.locator("#save-button")).to_be_disabled()
        self.assertIn("> [!IMPORTANT]", (self.root / "docs" / "fixture.md").read_text())
        sanitized = self.page.evaluate("""() => workbenchSanitize('<img src="x" onerror="alert(1)" style="display:none"><script>alert(1)</script>')""")
        self.assertNotIn("onerror", sanitized)
        self.assertNotIn("<script", sanitized)
        self.assertNotIn("style=", sanitized)

    def test_editor_fills_visible_height_with_internal_scroll(self):
        long_document = DOCUMENT + "\n".join(f"Paragraph {index}.\n" for index in range(300))
        (self.root / "docs" / "fixture.md").write_text(long_document, encoding="utf-8")
        self.page.locator("#refresh-button").click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator(".toastui-editor-md-container")).to_contain_text("Paragraph 299.")
        for width, height in [(1600, 1000), (1600, 700), (900, 800)]:
            self.page.set_viewport_size({"width": width, "height": height})
            self.page.wait_for_timeout(150)
            dimensions = self.page.evaluate("""() => {
              const main = document.querySelector('#main');
              const host = document.querySelector('#visual-editor').getBoundingClientRect();
              const editor = document.querySelector('.toastui-editor-defaultUI').getBoundingClientRect();
              const scroller = document.querySelector('.toastui-editor-md-container .ProseMirror');
              return {
                viewport: innerHeight, hostBottom: host.bottom,
                editorBottom: editor.bottom, mainHeight: main.clientHeight,
                mainScrollHeight: main.scrollHeight, scrollHeight: scroller.scrollHeight,
                clientHeight: scroller.clientHeight
              };
            }""")
            self.assertLessEqual(abs(dimensions["hostBottom"] - (height - 16)), 2)
            self.assertLessEqual(abs(dimensions["editorBottom"] - dimensions["hostBottom"]), 2)
            self.assertLessEqual(dimensions["mainScrollHeight"], dimensions["mainHeight"] + 1)
            self.assertGreater(dimensions["scrollHeight"], dimensions["clientHeight"])
        self.page.locator("#frontmatter-wrap summary").click()
        self.page.wait_for_timeout(100)
        expect(self.page.locator(".toastui-editor-mode-switch")).to_be_in_viewport()


if __name__ == "__main__":
    unittest.main()
