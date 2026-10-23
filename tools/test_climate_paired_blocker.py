import json
import re
import unittest
from pathlib import Path

ARTIFACT = Path(__file__).resolve().parents[1] / "docs/reference/research/climate-paired-source-blocker-178.json"
BOUND_KEY = re.compile(r"min|max|bound|threshold|percentile", re.I)


def numeric_bound_keys(node, path=""):
    found = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}/{key}"
            if BOUND_KEY.search(key) and isinstance(value, (int, float)) and not isinstance(value, bool):
                found.append(here)
            found.extend(numeric_bound_keys(value, here))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(numeric_bound_keys(value, f"{path}[{index}]"))
    return found


class PairedBlockerEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(ARTIFACT.read_text())

    def test_blocked_without_bounds_or_approval(self):
        self.assertEqual(self.data["status"], "blocked")
        self.assertEqual(self.data["paired_observed_bounds"]["status"], "unavailable")
        self.assertEqual(self.data["humidity"]["status"], "unavailable")
        self.assertEqual(self.data["owner_reuse_approval"], "UNMET")

    def test_no_synthetic_substitution_or_numeric_bounds(self):
        self.assertIs(self.data["synthetic_substitution"]["applied"], False)
        self.assertEqual(numeric_bound_keys(self.data), [])

    def test_probes_yield_no_observations_and_name_owner_action(self):
        self.assertTrue(self.data["probes"])
        self.assertTrue(all(p["yields_observations"] is False for p in self.data["probes"]))
        self.assertIn("own existing CEDA account", self.data["owner_action"])


if __name__ == "__main__":
    unittest.main()
