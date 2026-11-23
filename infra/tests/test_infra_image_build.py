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


PLAN_PATH = ROOT / ".github/workflows/infra-plan.yml"


def plan_contract_errors(document):
    errors = []
    jobs = document["jobs"]
    job = jobs["what-if"]
    if job.get("needs") != "changes" or "infra == 'true'" not in job.get("if", ""):
        errors.append("what-if must be gated on the infra path check")
    uploads = [s for s in job["steps"] if s.get("uses", "").startswith("actions/upload-artifact@")]
    if len(uploads) != 1:
        errors.append("what-if must upload exactly one result artifact")
    for step in uploads:
        if not re.fullmatch(r"[\w./-]+@[0-9a-f]{40}( # .*)?", step["uses"]):
            errors.append("upload-artifact must be pinned to a SHA")
        if step["with"].get("if-no-files-found") != "error":
            errors.append("a missing what-if summary must fail the job")
        if not step["with"]["path"].endswith("what-if-summary.json"):
            errors.append("upload must carry the what-if summary")
        if step.get("if") != "${{ !cancelled() }}":
            errors.append("upload must run after a failed what-if")
    for name, other in jobs.items():
        if name != "what-if" and "id-token" in other.get("permissions", {}):
            errors.append(f"{name} must not request id-token")
    text = "\n".join(s.get("run", "") for s in job["steps"])
    for forbidden in ("apply", "deployment group create", "docker push", "secrets."):
        if forbidden in text or forbidden in PLAN_PATH.read_text():
            errors.append(f"read-only workflow must not contain {forbidden}")
    return errors


class InfraPlanWorkflowContractTests(unittest.TestCase):
    def test_what_if_uploads_result_and_stays_read_only(self):
        document = yaml.load(PLAN_PATH.read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(plan_contract_errors(document), [])

    def test_contract_rejects_missing_upload_and_extra_id_token(self):
        document = yaml.load(PLAN_PATH.read_text(), Loader=yaml.BaseLoader)
        steps = document["jobs"]["what-if"]["steps"]
        document["jobs"]["what-if"]["steps"] = [
            s for s in steps if "upload-artifact" not in s.get("uses", "")
        ]
        document["jobs"]["changes"]["permissions"] = {"id-token": "write"}
        errors = plan_contract_errors(document)
        self.assertIn("what-if must upload exactly one result artifact", errors)
        self.assertIn("changes must not request id-token", errors)


if __name__ == "__main__":
    unittest.main()
