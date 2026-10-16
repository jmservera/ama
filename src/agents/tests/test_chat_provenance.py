"""Exercise all generated chat payloads through the shared offline privacy checker."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import privacy

import chat_fixture


class ChatProvenanceTests(unittest.TestCase):
    def test_all_nine_payloads_reject_unlabelled_rows_and_person_patterns(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as tmp:
            root = Path(tmp)
            chat_fixture.write(root)  # type: ignore[no-untyped-call]
            self.assertEqual(privacy.snapshot_issues(root, "chat"), [])
            for name in privacy.CHAT_FILES:
                path = root / f"{name}.jsonl"
                original = path.read_text()
                for field, value, diagnostic in (
                    ("is_synthetic", False, "missing_synthetic_label"),
                    ("test_probe", "jo.smith@example.com", "email"),
                ):
                    with self.subTest(payload=name, mutation=field):
                        rows = [json.loads(line) for line in original.splitlines()]
                        self.assertTrue(rows)
                        rows[0][field] = value
                        path.write_text("".join(json.dumps(row) + "\n" for row in rows))
                        manifest = json.loads((root / "manifest.json").read_text())
                        manifest["sha256"] = hashlib.sha256(
                            b"".join(
                                (root / f"{stem}.jsonl").read_bytes() for stem in privacy.CHAT_FILES
                            )
                        ).hexdigest()
                        (root / "manifest.json").write_text(json.dumps(manifest))
                        issues = privacy.snapshot_issues(root, "chat")
                        self.assertIn(f"{name}.jsonl:row-1:{diagnostic}", issues)
                        self.assertNotIn("manifest:hash_mismatch", issues)
                        path.write_text(original)


if __name__ == "__main__":
    unittest.main()
