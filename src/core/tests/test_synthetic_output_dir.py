import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import output_dir


class OutputDirTests(unittest.TestCase):
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
