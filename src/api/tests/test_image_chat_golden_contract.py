"""Dockerfile contract for #2303: the image ships the chat golden file and sets ZF_CHAT_GOLDEN."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCKERFILE = ROOT / "src" / "api" / "Dockerfile"
GOLDEN = "chat_golden.json"


class ImageChatGoldenContract(unittest.TestCase):
    def test_golden_source_exists(self) -> None:
        self.assertTrue((ROOT / "src" / "agents" / "evals" / GOLDEN).is_file())

    def test_image_copies_golden_and_sets_variable(self) -> None:
        text = DOCKERFILE.read_text(encoding="utf-8")
        copy = re.search(rf"^COPY\s+agents/evals/{GOLDEN}\s+(\S+)\s*$", text, re.M)
        self.assertIsNotNone(copy, "Dockerfile must COPY agents/evals/chat_golden.json")
        env = re.search(r"\bZF_CHAT_GOLDEN=(\S+)", text)
        self.assertIsNotNone(env, "Dockerfile must set ZF_CHAT_GOLDEN")
        assert copy and env
        dest = copy.group(1)
        copied = dest if dest.endswith(".json") else dest.rstrip("/") + "/" + GOLDEN
        self.assertEqual(env.group(1), "/app/" + copied.removeprefix("./"))

    def test_build_context_does_not_exclude_golden(self) -> None:
        lines = (ROOT / "src" / ".dockerignore").read_text(encoding="utf-8").splitlines()
        self.assertIn(f"!agents/evals/{GOLDEN}", lines)


if __name__ == "__main__":
    unittest.main()
