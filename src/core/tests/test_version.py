import importlib.metadata
import importlib.util
import unittest

from zava_forward.core import version

DISTRIBUTION = "zava-forward-core"


class VersionTests(unittest.TestCase):
    def test_version_matches_distribution_metadata(self) -> None:
        self.assertEqual(version.__version__, importlib.metadata.version(DISTRIBUTION))

    def test_namespace_has_no_init_module(self) -> None:
        spec = importlib.util.find_spec("zava_forward")
        self.assertIsNotNone(spec)
        assert spec is not None
        self.assertIsNone(spec.origin)
        self.assertIsNotNone(spec.submodule_search_locations)

    def test_declares_sql_and_blob_extras(self) -> None:
        extras = importlib.metadata.metadata(DISTRIBUTION).get_all("Provides-Extra") or []
        self.assertIn("sql", extras)
        self.assertIn("blob", extras)


if __name__ == "__main__":
    unittest.main()
