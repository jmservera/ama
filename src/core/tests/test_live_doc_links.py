"""Relative Markdown links in live documentation must resolve (Refs #203).

Append-only history (the knowledge-base log and the capstone record) is excluded
because it legitimately cites paths retired at the 2026-10-27 cut-over.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HISTORY = ("docs/capstone/", "docs/reference/log.md")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)")
FENCE = re.compile(r"```.*?```", re.S)
EXTERNAL = re.compile(r"(https?:|mailto:|#)")
SKIP_DIRS = {".git", ".copilot-tracking", "node_modules", ".venv", "support"}


def live_markdown(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if SKIP_DIRS.intersection(rel.parts):
            continue
        if rel.as_posix().startswith(HISTORY):
            continue
        found.append(path)
    return sorted(found)


def unresolved(path: Path, root: Path) -> list[str]:
    text = FENCE.sub("", path.read_text(encoding="utf-8", errors="ignore"))
    missing: list[str] = []
    for match in LINK.finditer(text):
        target = match.group(1)
        if EXTERNAL.match(target) or "{" in target or "<" in target:
            continue
        relative = target.split("#", 1)[0]
        if relative and not (path.parent / relative).resolve().exists():
            missing.append(f"{path.relative_to(root).as_posix()} -> {target}")
    return missing


class LiveDocLinkTests(unittest.TestCase):
    def test_helper_flags_a_missing_target(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "ok.md").write_text("x", encoding="utf-8")
            page = base / "page.md"
            page.write_text("[a](ok.md#s) [b](gone.md) [c](https://x.test)", encoding="utf-8")
            self.assertEqual(unresolved(page, base), ["page.md -> gone.md"])

    def test_live_docs_have_no_unresolved_relative_links(self) -> None:
        if not (ROOT / "docs").is_dir():
            self.skipTest("repository docs are not in this image")
        problems = [item for path in live_markdown(ROOT) for item in unresolved(path, ROOT)]
        self.assertEqual(problems, [], "\n".join(problems[:20]))


if __name__ == "__main__":
    unittest.main()
