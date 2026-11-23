"""Contract for the credential-free pull request image build workflow (#2313)."""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / ".github/workflows/infra-image-build.yml"


def load():
    # BaseLoader keeps the 'on' key instead of coercing it to a boolean.
    return yaml.load(PATH.read_text(), Loader=yaml.BaseLoader)


class InfraImageBuildTests(unittest.TestCase):
    def test_only_pull_requests_touching_infra_or_src(self):
        document = load()
        self.assertEqual(set(document["on"]), {"pull_request"})
        self.assertIn("infra/**", document["on"]["pull_request"]["paths"])

    def test_least_permissions_and_pinned_actions(self):
        document = load()
        self.assertEqual(document["permissions"], {"contents": "read"})
        job = document["jobs"]["build"]
        self.assertEqual(job.get("permissions", {"contents": "read"}), {"contents": "read"})
        self.assertNotIn("environment", job)
        for step in job["steps"]:
            uses = step.get("uses", "")
            if uses:
                self.assertRegex(uses, r"[\w./-]+@[0-9a-f]{40}")
            if uses.startswith("actions/checkout@"):
                self.assertEqual(step["with"]["persist-credentials"], "false")
            self.assertNotIn("${{", step.get("run", ""))

    def test_builds_versioned_tag_without_login_push_or_deploy(self):
        text = PATH.read_text()
        document = load()
        commands = "\n".join(step.get("run", "") for step in document["jobs"]["build"]["steps"])
        for forbidden in ("docker push", "docker login", "az ", "azure/", "secrets.", "id-token"):
            self.assertNotIn(forbidden, text)
        self.assertRegex(
            commands, r'tag="sha-\$\{GITHUB_SHA\}-r\$\{GITHUB_RUN_ID\}-a\$\{GITHUB_RUN_ATTEMPT\}"'
        )
        self.assertIn("docker build", commands)
        self.assertEqual(
            document["jobs"]["build"]["strategy"]["matrix"]["project"],
            ["api", "agents", "orchestrator", "importer"],
        )
        self.assertIsNone(re.search(r"(?m)^\s+(deploy|publish):", text))


if __name__ == "__main__":
    unittest.main()
