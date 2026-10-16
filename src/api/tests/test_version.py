import importlib.metadata
import importlib.util
import runpy
import unittest
from unittest.mock import patch

from zava_forward.api import version

DISTRIBUTION = "zava-forward-api"


class VersionTests(unittest.TestCase):
    def test_module_entry_point_starts_the_existing_server(self) -> None:
        with patch("zava_forward.api.server.main") as main:
            runpy.run_module("zava_forward.api", run_name="__main__")
        main.assert_called_once_with()

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
