from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "deployed_images.py"
spec = importlib.util.spec_from_file_location("deployed_images", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

REGISTRY = "crx.azurecr.io"
DIGEST = "sha256:" + "a" * 64


def resource(name: str, image: str) -> dict[str, object]:
    return {"name": name, "properties": {"template": {"containers": [{"image": image}]}}}


class DeployedImageAuditTests(unittest.TestCase):
    def kinds(self, *images: str) -> list[str]:
        report = module.audit([resource(f"r{i}", img) for i, img in enumerate(images)], REGISTRY)
        return [row["kind"] for row in report["containers"]]

    def test_classifies_each_reference_shape(self) -> None:
        self.assertEqual(
            self.kinds(
                f"{REGISTRY}/zava-forward-api@{DIGEST}",
                f"{REGISTRY}/zava-forward-api:release-1",
                f"{REGISTRY}/zava-forward-api:latest",
                f"{REGISTRY}/zava-forward-api",
                "mcr.microsoft.com/k8se/quickstart:latest",
                f"docker.io/library/python@{DIGEST}",
            ),
            [
                "digest-pinned",
                "tag-only",
                "latest",
                "latest",
                "placeholder",
                "foreign-registry",
            ],
        )

    def test_only_all_digest_pinned_passes_and_provenance_stays_unproven(self) -> None:
        good = module.audit([resource("a", f"{REGISTRY}/zava-forward-agents@{DIGEST}")], REGISTRY)
        self.assertTrue(good["all_real_and_immutable"])
        self.assertEqual(good["containers"][0]["repository"], "zava-forward-agents")
        self.assertIn("unproven", good["provenance"])
        bad = module.audit(
            [
                resource("a", f"{REGISTRY}/zava-forward-agents@{DIGEST}"),
                resource("b", "mcr.microsoft.com/k8se/quickstart:latest"),
            ],
            REGISTRY,
        )
        self.assertFalse(bad["all_real_and_immutable"])
        self.assertFalse(module.audit([], REGISTRY)["all_real_and_immutable"])

    def test_cli_exit_codes(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "apps.json"
            path.write_text(json.dumps([resource("a", f"{REGISTRY}/x@{DIGEST}")]))
            self.assertEqual(module.main([str(path), "--registry", REGISTRY]), 0)
            self.assertEqual(module.main([str(path), "--registry", "other.azurecr.io"]), 1)


if __name__ == "__main__":
    unittest.main()
