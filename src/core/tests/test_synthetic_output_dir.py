import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from zava_forward.core import factory
from zava_forward.core.data_paths import data_file
from zava_forward.core.synthetic import output_dir


class OutputDirTests(unittest.TestCase):
    def test_runtime_and_generator_use_the_same_data_folder(self) -> None:
        for env in ({}, {"ZF_DATA": "/var/zf/dataset"}, {"ZF_DATA": "~/fixture/custom.json"}):
            with self.subTest(env=env), patch.object(factory, "Store") as store:
                factory.open_store(env)  # type: ignore[no-untyped-call]
                path = data_file(env)
                store.assert_called_once_with(str(path), None, None)
                self.assertEqual(output_dir("fixture", env), path.parent / "fixture")
        self.assertEqual(data_file({}), Path.home() / ".zava-forward/data/zavaforward.json")
        self.assertEqual(
            data_file({"ZF_DATA": "/var/zf/dataset"}), Path("/var/zf/dataset/zavaforward.json")
        )
        self.assertEqual(
            data_file({"ZF_DATA": "~/fixture/custom.json"}), Path.home() / "fixture/custom.json"
        )

    def test_default_is_per_user_folder_outside_the_repository(self) -> None:
        out = output_dir("scale-fixture", {})
        self.assertEqual(out, Path.home() / ".zava-forward" / "data" / "scale-fixture")

    def test_zf_data_folder_is_used_as_the_root(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(
                output_dir("chat-fixture", {"ZF_DATA": folder}), Path(folder) / "chat-fixture"
            )

    def test_zf_data_file_means_its_folder(self) -> None:
        out = output_dir("sensor-backfill", {"ZF_DATA": "/var/zf/zavaforward.json"})
        self.assertEqual(out, Path("/var/zf/sensor-backfill"))


if __name__ == "__main__":
    unittest.main()
