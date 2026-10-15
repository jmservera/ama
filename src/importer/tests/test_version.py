import importlib.metadata
import importlib.util
import unittest

from zava_forward.importer import version

DISTRIBUTION = "zava-forward-import"


class VersionTests(unittest.TestCase):
    def test_version_matches_distribution_metadata(self) -> None:
        self.assertEqual(version.__version__, importlib.metadata.version(DISTRIBUTION))

    def test_namespace_has_no_init_module(self) -> None:
        spec = importlib.util.find_spec("zava_forward")
        self.assertIsNotNone(spec)
        assert spec is not None
        self.assertIsNone(spec.origin)
        self.assertIsNotNone(spec.submodule_search_locations)


if __name__ == "__main__":
    unittest.main()
