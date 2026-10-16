"""Offline deployment CLI regressions with a real subprocess and a fake az."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "deploy.py"
PLACEHOLDER = "mcr.microsoft.com/k8se/quickstart:latest"
CURRENT = "example.azurecr.io/zava-forward-orchestrator@sha256:abc123"
REGISTRY = [{"name": "example", "loginServer": "example.azurecr.io"}]
REPOSITORIES = ["zava-forward-orchestrator"]

FAKE_AZ = """
import json
import os
import sys
from pathlib import Path

root = Path(os.environ["FAKE_AZ_ROOT"])
calls_path = root / "calls.json"
calls = json.loads(calls_path.read_text())
responses = json.loads((root / "responses.json").read_text())
index = len(calls)
calls.append(sys.argv[1:])
calls_path.write_text(json.dumps(calls))
if index >= len(responses):
    sys.exit("Unexpected az call")
response = responses[index]
if sys.argv[1:1 + len(response["command"])] != response["command"]:
    sys.exit("Unexpected command: " + repr(sys.argv[1:]))
print(response.get("raw", json.dumps(response.get("value"))))
print(response.get("error", ""), file=sys.stderr)
sys.exit(response.get("code", 0))
"""


def reply(command: str, value=None, *, error: str = "", code: int = 0) -> dict:
    return {"command": command.split(), "value": value, "error": error, "code": code}


def job(suffix: str, image: str, prefix: str = "forward-test") -> dict:
    return {
        "name": f"job-{prefix}-{suffix}",
        "properties": {"template": {"containers": [{"name": suffix, "image": image}]}},
    }


class DeployTests(unittest.TestCase):
    def run_deploy(self, responses: list[dict], *options: str, script: Path = SCRIPT):
        with TemporaryDirectory(prefix="ama-fake-az-") as directory:
            root = Path(directory)
            az = root / "az"
            az.write_text(f"#!{sys.executable}\n{FAKE_AZ}", encoding="utf-8")
            az.chmod(0o755)
            (root / "calls.json").write_text("[]", encoding="utf-8")
            (root / "responses.json").write_text(json.dumps(responses), encoding="utf-8")
            env = {**os.environ, "PATH": str(root), "FAKE_AZ_ROOT": str(root)}
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--resource-group",
                    "ama",
                    "--registry",
                    "example",
                    "--parameters",
                    "private.bicepparam",
                    "--environment",
                    "test",
                    *options,
                ],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            calls = json.loads((root / "calls.json").read_text(encoding="utf-8"))
        return result, calls

    def assert_selection(self, responses: list[dict], image: str, *options: str, **kwargs):
        result, calls = self.run_deploy(
            [*responses, reply("deployment group what-if")], *options, **kwargs
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"orchestratorImage={image} (source:", result.stdout)
        self.assertEqual(calls[-1][-2:], ["--parameters", f"orchestratorImage={image}"])
        self.assertIn("workload=forward", calls[-1])
        self.assertIn("environmentName=test", calls[-1])
        self.assertEqual(calls[-1][3:5], ["--resource-group", "ama"])
        self.assertIn("private.bicepparam", calls[-1])
        self.assertIn("--template-file", calls[-1])
        for call in calls[:-1]:
            if call[:3] == ["acr", "repository", "list"]:
                self.assertEqual(call[3:], ["--name", "example", "--output", "json"])
            elif call[:3] == ["acr", "repository", "show-tags"]:
                self.assertEqual(
                    call[3:],
                    [
                        "--name",
                        "example",
                        "--repository",
                        "zava-forward-orchestrator",
                        "--orderby",
                        "time_desc",
                        "--top",
                        "1",
                        "--output",
                        "json",
                    ],
                )
            else:
                self.assertIn("--resource-group", call)
                self.assertIn("ama", call)
        if image == PLACEHOLDER:
            self.assertIn("WARNING: placeholder image selected", result.stderr)
        else:
            self.assertNotIn("WARNING:", result.stderr)
        return result, calls

    def test_each_existing_job_preserves_its_image_without_querying_registry(self):
        for suffix in ("orchestrator", "auth-renewal", "ledger-verify"):
            with self.subTest(suffix=suffix):
                result, calls = self.assert_selection(
                    [reply("containerapp job list", [job(suffix, CURRENT)])], CURRENT
                )
                self.assertIn("source: existing job", result.stdout)
                self.assertEqual(len(calls), 2)

    def test_real_job_wins_over_placeholder_and_unrelated_jobs(self):
        jobs = [
            job("orchestrator", PLACEHOLDER),
            job("auth-renewal", CURRENT),
            job("ledger-verify", CURRENT),
            job("orchestrator", "other:image", prefix="other-test"),
            job("import", "import:image"),
        ]
        self.assert_selection([reply("containerapp job list", jobs)], CURRENT)

    def test_newest_registry_tag_not_lexicographic_or_latest(self):
        responses = [
            reply("containerapp job list", []),
            reply("acr list", REGISTRY),
            reply("acr repository list", REPOSITORIES),
            reply("acr repository show-tags", ["build-2"]),
        ]
        result, _ = self.assert_selection(
            responses, "example.azurecr.io/zava-forward-orchestrator:build-2"
        )
        self.assertIn("source: newest registry tag (time_desc)", result.stdout)

    def test_placeholder_job_does_not_hide_registry_image(self):
        self.assert_selection(
            [
                reply("containerapp job list", [job("orchestrator", PLACEHOLDER)]),
                reply("acr list", REGISTRY),
                reply("acr repository list", REPOSITORIES),
                reply("acr repository show-tags", ["release"]),
            ],
            "example.azurecr.io/zava-forward-orchestrator:release",
        )

    def test_no_registry_in_group_uses_warned_placeholder(self):
        self.assert_selection(
            [
                reply("containerapp job list", []),
                reply("acr list", [{"name": "unrelated", "loginServer": "other.azurecr.io"}]),
            ],
            PLACEHOLDER,
        )

    def test_empty_or_missing_repository_uses_warned_placeholder(self):
        for responses in (
            [reply("acr repository list", [])],
            [reply("acr repository list", ["unrelated"])],
            [
                reply("acr repository list", REPOSITORIES),
                reply("acr repository show-tags", []),
            ],
        ):
            with self.subTest(responses=responses):
                self.assert_selection(
                    [reply("containerapp job list", []), reply("acr list", REGISTRY), *responses],
                    PLACEHOLDER,
                )

    def test_explicit_tag_digest_and_placeholder_skip_discovery(self):
        for image in ("registry/image:release", CURRENT, PLACEHOLDER):
            with self.subTest(image=image):
                result, calls = self.assert_selection([], image, "--orchestrator-image", image)
                self.assertEqual(len(calls), 1)
                self.assertIn("source: explicit --orchestrator-image", result.stdout)

    def test_empty_explicit_image_resolves_normally(self):
        self.assert_selection(
            [reply("containerapp job list", [job("orchestrator", CURRENT)])],
            CURRENT,
            "--orchestrator-image",
            "",
        )

    def test_conflicting_job_images_stop_deployment(self):
        result, calls = self.run_deploy(
            [
                reply(
                    "containerapp job list",
                    [job("orchestrator", CURRENT), job("ledger-verify", "registry/image:other")],
                )
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflicting real images", result.stderr)
        self.assertEqual(len(calls), 1)

    def test_discovery_errors_stop_instead_of_falling_back(self):
        stages = [
            [],
            [reply("containerapp job list", [])],
            [reply("containerapp job list", []), reply("acr list", REGISTRY)],
            [
                reply("containerapp job list", []),
                reply("acr list", REGISTRY),
                reply("acr repository list", REPOSITORIES),
            ],
        ]
        commands = [
            "containerapp job list",
            "acr list",
            "acr repository list",
            "acr repository show-tags",
        ]
        for prefix, command in zip(stages, commands, strict=True):
            for error in ("AuthorizationFailed", "network unavailable", "(ResourceNotFound)"):
                with self.subTest(command=command, error=error):
                    result, calls = self.run_deploy([*prefix, reply(command, error=error, code=1)])
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(error, result.stderr)
                    self.assertNotIn("orchestratorImage=", result.stdout)
                    self.assertEqual(len(calls), len(prefix) + 1)

    def test_invalid_discovery_data_stops_deployment(self):
        scenarios = [
            [reply("containerapp job list", {})],
            [reply("containerapp job list", [{"name": "job-forward-test-orchestrator"}])],
            [reply("containerapp job list", [job("orchestrator", "")])],
            [reply("containerapp job list", []), reply("acr list", {})],
            [reply("containerapp job list", []), reply("acr list", [{"name": "example"}])],
            [
                reply("containerapp job list", []),
                reply("acr list", REGISTRY),
                reply("acr repository list", REPOSITORIES),
                reply("acr repository show-tags", [""]),
            ],
            [{"command": ["containerapp", "job", "list"], "raw": "not json"}],
        ]
        for responses in scenarios:
            with self.subTest(responses=responses):
                result, calls = self.run_deploy(responses)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Deployment stopped:", result.stderr)
                self.assertEqual(len(calls), len(responses))

    def test_apply_and_extra_parameters_and_exit_status(self):
        result, calls = self.run_deploy(
            [reply("deployment group create", error="deployment failed", code=7)],
            "--apply",
            "--orchestrator-image",
            CURRENT,
            "--parameter",
            "apiImage=registry/api:release",
        )
        self.assertEqual(result.returncode, 7)
        self.assertIn("apiImage=registry/api:release", calls[-1])
        self.assertIn(CURRENT, result.stdout)

    def test_lookup_identity_and_deployed_identity_match(self):
        result, calls = self.run_deploy(
            [
                reply(
                    "containerapp job list", [job("orchestrator", CURRENT, prefix="custom-pilot")]
                ),
                reply("deployment group what-if"),
            ],
            "--workload",
            "custom",
            "--environment",
            "pilot",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("workload=custom", calls[-1])
        self.assertIn("environmentName=pilot", calls[-1])
        self.assertIn(f"orchestratorImage={CURRENT}", calls[-1])

    def test_inline_overrides_cannot_bypass_resolver_identity(self):
        for value in (
            "orchestratorImage=",
            "workload=other",
            "environmentName=pilot",
            "invalid",
            "=value",
        ):
            with self.subTest(value=value):
                result, calls = self.run_deploy([], "--parameter", value)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(calls, [])

    def test_mutations_break_precedence_forwarding_and_warning_assertions(self):
        source = SCRIPT.read_text(encoding="utf-8")
        mutations = [
            (
                'return next(iter(images)), "existing job"',
                'return PLACEHOLDER, "existing job"',
                [reply("containerapp job list", [job("orchestrator", CURRENT)])],
                CURRENT,
            ),
            (
                'f"orchestratorImage={image}",',
                'f"orchestratorImage={PLACEHOLDER}",',
                [],
                CURRENT,
            ),
            (
                "if image == PLACEHOLDER:",
                "if False:",
                [reply("containerapp job list", []), reply("acr list", [])],
                PLACEHOLDER,
            ),
            (
                '"time_desc",',
                '"time_asc",',
                [
                    reply("containerapp job list", []),
                    reply("acr list", REGISTRY),
                    reply("acr repository list", REPOSITORIES),
                    reply("acr repository show-tags", ["release"]),
                ],
                "example.azurecr.io/zava-forward-orchestrator:release",
            ),
        ]
        with TemporaryDirectory(prefix="ama-resolver-mutations-") as directory:
            mutant = Path(directory) / "deploy.py"
            for old, new, responses, image in mutations:
                with self.subTest(mutation=old):
                    self.assertEqual(source.count(old), 1)
                    mutant.write_text(source.replace(old, new), encoding="utf-8")
                    options = ("--orchestrator-image", CURRENT) if not responses else ()
                    with self.assertRaises(AssertionError):
                        self.assert_selection(responses, image, *options, script=mutant)


if __name__ == "__main__":
    unittest.main()
