"""Offline workflow contracts, fake-command orchestration and real local HTTP denials."""

import importlib.util
import json
import os
import re
import secrets
import socket
import subprocess
import sys
import threading
import unittest
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import UUID

import yaml

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("pipeline", ROOT / "infra/scripts/pipeline.py")
assert SPEC is not None and SPEC.loader is not None
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)
SHA = "a" * 40
SUBSCRIPTION = str(UUID(int=1))  # Constructed fixture, not a tenant/subscription identifier.
ENV = {
    "RELEASE_SHA": SHA,
    "AZURE_SUBSCRIPTION_ID": SUBSCRIPTION,
    "GITHUB_RUN_ID": "123",
    "GITHUB_RUN_ATTEMPT": "1",
    "AZURE_REGISTRY_NAME": "example",
}
OVERRIDES = {
    key: (
        True
        if key == "entraBearerOnly"
        else str(UUID(int=2))
        if key in {"entraClientId", "sqlAdminGroupObjectId"}
        else "operator@example.test"
        if key == "alertEmail"
        else "uksouth"
        if key in {"location", "sqlLocation"}
        else "synthetic-reviewed-reference"
    )
    for key in pipeline.OVERRIDES
}
ENV["DEPLOY_PARAMETERS"] = json.dumps(OVERRIDES)
RESOURCE = (
    f"/subscriptions/{SUBSCRIPTION}/resourceGroups/ama/providers/Microsoft.App/containerApps/api"
)


def workflow(name):
    # BaseLoader retains the YAML 'on' key instead of YAML 1.1 boolean coercion.
    return yaml.load((ROOT / ".github/workflows" / name).read_text(), Loader=yaml.BaseLoader)


def workflow_errors(document):
    errors = []
    if document.get("permissions") != {"contents": "read"}:
        errors.append("top-level permissions")
    for job in document["jobs"].values():
        permissions = job.get("permissions", {"contents": "read"})
        if set(permissions) - {"contents", "actions", "id-token"}:
            errors.append("excess permissions")
        if permissions.get("contents") != "read" or permissions.get("actions", "read") != "read":
            errors.append("write permissions")
        privileged = permissions.get("id-token") == "write"
        steps = job["steps"]
        if privileged:
            if "environment" not in job or "self-hosted" not in job["runs-on"]:
                errors.append("privileged runner/environment")
            approvals = [
                index
                for index, step in enumerate(steps)
                if "verify-environment" in step.get("run", "")
            ]
            logins = [
                index
                for index, step in enumerate(steps)
                if step.get("uses", "").startswith("azure/")
            ]
            if not approvals or not logins or approvals[0] >= logins[0]:
                errors.append("approval order")
        for step in steps:
            uses = step.get("uses", "")
            if uses and not re.fullmatch(r"[\w./-]+@[0-9a-f]{40}", uses):
                errors.append("unpinned action")
            if uses.startswith("actions/checkout@"):
                if step["with"].get("persist-credentials") != "false":
                    errors.append("checkout credentials")
            script = step.get("run", "")
            if "${{" in script:
                errors.append("expression injection")
            if re.search(
                r"(?m)(set -x|printenv|env\s*$|echo.*(?:TOKEN|SECRET|PARAMETERS))", script
            ):
                errors.append("credential echo")
            if "secrets." in json.dumps(step):
                errors.append("stored secret reference")
    return errors


def infra_test_dependency_errors(document):
    errors = []
    discovery = "python -m unittest discover -s infra/tests"
    scripts = [
        step["run"]
        for job in document["jobs"].values()
        for step in job["steps"]
        if discovery in step.get("run", "")
    ]
    if not scripts:
        errors.append("missing infra discovery")
    for script in scripts:
        if "pip install 'PyYAML==6.0.3'" not in script.partition(discovery)[0]:
            errors.append("missing pinned PyYAML before infra discovery")
    return errors


class WorkflowTests(unittest.TestCase):
    def test_each_infra_ci_step_installs_pinned_test_dependency_before_discovery(self):
        for name in ("src-ci.yml", "mvp-validation.yml"):
            with self.subTest(name=name):
                self.assertEqual(infra_test_dependency_errors(workflow(name)), [])

    def test_reject_missing_or_late_infra_test_dependency(self):
        install = "pip install 'PyYAML==6.0.3'"
        for name in ("src-ci.yml", "mvp-validation.yml"):
            for replacement in ("", "pip install PyYAML"):
                with self.subTest(name=name, replacement=replacement):
                    document = deepcopy(workflow(name))
                    for job in document["jobs"].values():
                        for step in job["steps"]:
                            if "unittest discover -s infra/tests" in step.get("run", ""):
                                step["run"] = step["run"].replace(install, replacement)
                    self.assertTrue(infra_test_dependency_errors(document))
            with self.subTest(name=name, ordering="late"):
                document = deepcopy(workflow(name))
                for job in document["jobs"].values():
                    for step in job["steps"]:
                        if "unittest discover -s infra/tests" in step.get("run", ""):
                            step["run"] = step["run"].replace(install, "") + f"\n{install}\n"
                self.assertTrue(infra_test_dependency_errors(document))

    def test_structure_permissions_pinning_and_no_secret_echo(self):
        for name in ("src-deploy.yml", "infra-plan.yml"):
            with self.subTest(name=name):
                self.assertEqual(workflow_errors(workflow(name)), [])

    def test_reject_unsafe_workflow_mutations(self):
        original = workflow("src-deploy.yml")
        mutations = [
            lambda doc: doc.update(permissions={"contents": "write"}),
            lambda doc: doc["jobs"]["deploy"].pop("environment"),
            lambda doc: doc["jobs"]["deploy"].update(**{"runs-on": "ubuntu-latest"}),
            lambda doc: doc["jobs"]["deploy"]["permissions"].update(packages="write"),
            lambda doc: doc["jobs"]["build"]["steps"][0].update(uses="actions/checkout@v4"),
            lambda doc: doc["jobs"]["build"]["steps"].append({"run": "echo $SECRET"}),
            lambda doc: doc["jobs"]["build"]["steps"].append({"run": "echo ${{ inputs.foo }}"}),
        ]
        for mutate in mutations:
            document = deepcopy(original)
            mutate(document)
            self.assertTrue(workflow_errors(document))

    def test_privileged_pr_workflow_is_default_branch_workflow_run_only(self):
        document = workflow("infra-plan.yml")
        self.assertEqual(set(document["on"]), {"workflow_run"})
        condition = document["jobs"]["changes"]["if"]
        for predicate in (
            "'pull_request'",
            "'success'",
            "head_repository.full_name",
            "number != null",
        ):
            self.assertIn(predicate, condition)
        steps = document["jobs"]["what-if"]["steps"]
        checkouts = [step for step in steps if step.get("uses", "").startswith("actions/checkout@")]
        self.assertEqual(checkouts[0]["with"]["ref"], "${{ github.sha }}")
        self.assertEqual(checkouts[1]["with"]["path"], "candidate")
        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertNotIn("python3 candidate", commands)
        self.assertIn("--infra candidate/infra", commands)

    def test_release_is_main_only_serialized_and_gates_exact_image(self):
        document = workflow("src-deploy.yml")
        self.assertEqual(set(document["on"]), {"workflow_dispatch"})
        self.assertEqual(
            document["concurrency"], {"group": "ama-release", "cancel-in-progress": "false"}
        )
        self.assertEqual(document["jobs"]["build"]["if"], "github.ref == 'refs/heads/main'")
        self.assertNotIn("id-token", document["jobs"]["build"].get("permissions", {}))
        self.assertEqual(document["jobs"]["publish"]["needs"], "build")
        self.assertEqual(document["jobs"]["deploy"]["needs"], "publish")
        build = document["jobs"]["build"]
        self.assertEqual(build["strategy"]["matrix"]["project"], list(pipeline.PROJECTS))
        scans = [
            step for step in build["steps"] if step.get("uses", "").startswith("aquasecurity/")
        ]
        self.assertEqual(len(scans), 2)
        self.assertEqual(scans[0]["with"]["trivy-config"], "src/trivy.yaml")
        self.assertEqual(scans[0]["with"]["ignore-unfixed"], "true")
        self.assertEqual(scans[0]["with"]["exit-code"], "1")
        self.assertIn("steps.build.outcome == 'success'", scans[0]["if"])
        self.assertEqual(scans[1]["with"]["ignore-unfixed"], "false")
        commands = "\n".join(step.get("run", "") for step in build["steps"])
        self.assertIn('"src/$PROJECT/Dockerfile"', commands)
        self.assertIn("src/check-container.py", commands)
        self.assertIn("docker save", commands)

    def test_tests_and_filters_are_wired_into_source_ci(self):
        document = workflow("src-ci.yml")
        commands = "\n".join(
            step.get("run", "") for job in document["jobs"].values() for step in job["steps"]
        )
        self.assertIn("unittest discover -s infra/tests", commands)
        self.assertIn("PyYAML==6.0.3", commands)
        build = next(
            step for step in document["jobs"]["project"]["steps"] if step.get("id") == "build"
        )
        self.assertIn("image-paths.outputs.images", build["if"])


class PipelineTests(unittest.TestCase):
    def test_plan_cannot_select_apply_via_release_metadata(self):
        with (
            patch.object(sys, "argv", ["pipeline.py", "plan", "--images", "ignored"]),
            patch.object(pipeline, "deployment") as deployment,
            patch("sys.stderr"),
        ):
            self.assertEqual(pipeline.main(), 1)
            deployment.assert_not_called()

    def test_path_filters_include_transitive_dependencies(self):
        expected = {
            "src/api/src/file.py": ["api"],
            "src/agents/requirements.txt": ["api", "agents"],
            "src/core/src/file.py": list(pipeline.PROJECTS),
            "src/importer/Dockerfile": ["importer"],
            "src/build-requirements.txt": list(pipeline.PROJECTS),
            "infra/main.bicep": list(pipeline.PROJECTS),
            "docs/unrelated.md": [],
        }
        for path, projects in expected.items():
            self.assertEqual(pipeline.changed_images([path]), projects)

    def test_compile_committed_parameters_and_typed_overrides(self):
        for environment, filename in pipeline.PARAMETER_FILES.items():
            with (
                patch.dict(os.environ, ENV),
                patch.object(
                    pipeline, "az", return_value={"parametersJson": '{"parameters":{}}'}
                ) as az,
            ):
                result = pipeline.parameters(ROOT / "infra", environment)["parameters"]
            self.assertEqual(result["environmentName"], {"value": environment})
            self.assertEqual(result["allowPublicNetworkAccess"], {"value": False})
            self.assertEqual(result["entraBearerOnly"], {"value": True})
            self.assertIn(filename, az.call_args.args[3])
            self.assertNotIn("sqlPublicNetworkAccess", result)

    def test_override_contract_fails_closed(self):
        for overrides in (
            {},
            {**OVERRIDES, "allowPublicNetworkAccess": True},
            {**OVERRIDES, "entraClientId": str(UUID(int=0))},
            {**OVERRIDES, "location": ""},
            {**OVERRIDES, "alertEmail": "alerts@example.invalid"},
            {**OVERRIDES, "location": True},
            {**OVERRIDES, "entraBearerOnly": "false"},
        ):
            with patch.dict(os.environ, {**ENV, "DEPLOY_PARAMETERS": json.dumps(overrides)}):
                with patch.object(
                    pipeline, "az", return_value={"parametersJson": '{"parameters":{}}'}
                ):
                    with self.assertRaises((pipeline.PipelineError, ValueError)):
                        pipeline.parameters(ROOT / "infra", "pilot")

    def test_approval_configuration_is_fail_closed(self):
        good = {
            "protection_rules": [
                {"type": "required_reviewers", "reviewers": [{}], "prevent_self_review": True}
            ],
            "can_admins_bypass": False,
            "deployment_branch_policy": {"protected_branches": True},
        }
        records = [
            {**good, "protection_rules": []},
            {**good, "can_admins_bypass": True},
            {**good, "deployment_branch_policy": None},
            {
                **good,
                "protection_rules": [
                    {"type": "required_reviewers", "reviewers": [{}], "prevent_self_review": False}
                ],
            },
        ]
        with patch.dict(os.environ, GITHUB_REPOSITORY="example/example"):
            with patch.object(pipeline, "run", return_value=json.dumps(good)):
                pipeline.verify_environment("test")
            for record in records:
                with patch.object(pipeline, "run", return_value=json.dumps(record)):
                    with self.assertRaises(pipeline.PipelineError):
                        pipeline.verify_environment("test")

    def test_sanitized_summary_contains_no_identifiers_or_deltas(self):
        plan = {
            "status": "Succeeded",
            "changes": [
                {"resourceId": RESOURCE, "changeType": "Modify", "delta": ["CANARY_PRIVATE_VALUE"]}
            ],
        }
        result = pipeline.summarize_plan(plan, SUBSCRIPTION, SHA)
        self.assertEqual(result["change_counts"], {"Modify": 1})
        self.assertNotIn(SUBSCRIPTION, json.dumps(result))
        self.assertNotIn("CANARY_PRIVATE_VALUE", json.dumps(result))

    def test_plan_rejects_delete_unknown_out_of_scope_and_public_sql(self):
        for plan in (
            {"status": "Failed", "changes": []},
            {"status": "Succeeded"},
            *[
                {"status": "Succeeded", "changes": [{"resourceId": RESOURCE, "changeType": kind}]}
                for kind in ("Delete", "Ignore", "Unsupported", "Unknown", "Deploy", None)
            ],
            {
                "status": "Succeeded",
                "changes": [
                    {"resourceId": RESOURCE.replace("/ama/", "/other/"), "changeType": "Create"}
                ],
            },
            {
                "status": "Succeeded",
                "changes": [
                    {
                        "resourceId": RESOURCE,
                        "changeType": "Modify",
                        "after": {
                            "type": "Microsoft.Sql/servers",
                            "properties": {"publicNetworkAccess": "Enabled"},
                        },
                    }
                ],
            },
        ):
            with self.assertRaises(pipeline.PipelineError):
                pipeline.summarize_plan(plan, SUBSCRIPTION, SHA)

    def test_sql_precondition_is_not_vacuous(self):
        for servers in ([], [{}], [{"publicNetworkAccess": "Enabled"}], None):
            with patch.object(pipeline, "az", return_value=servers):
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.check_sql()
        with patch.object(pipeline, "az", return_value=[{"publicNetworkAccess": "Disabled"}]) as az:
            pipeline.check_sql()
            self.assertEqual(
                az.call_args.args, ("sql", "server", "list", "--resource-group", "ama")
            )

    def test_run_does_not_expose_command_error_output(self):
        completed = subprocess.CompletedProcess(
            ["az"], 1, "CANARY_PRIVATE_VALUE", "CANARY_PRIVATE_VALUE"
        )
        with patch.object(subprocess, "run", return_value=completed):
            with self.assertRaises(pipeline.PipelineError) as error:
                pipeline.run("az", "anything")
        self.assertNotIn("CANARY", str(error.exception))

    def write_images(self, directory):
        for project in pipeline.PROJECTS:
            (directory / f"{project}.json").write_text(
                json.dumps(
                    {
                        "project": project,
                        "source_sha": SHA,
                        "tag": f"sha-{SHA}-r123-a1",
                        "image": f"example.azurecr.io/zava-forward-{project}@sha256:" + "b" * 64,
                    }
                )
            )

    def test_release_metadata_binding_and_quarantine_pull_admission(self):
        with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV):
            directory = Path(temporary)
            self.write_images(directory)
            with patch.object(pipeline, "run") as run:
                images = pipeline.release_images(directory, "example.azurecr.io")
            self.assertEqual(set(images), set(pipeline.IMAGE_PARAMETERS.values()))
            self.assertEqual(run.call_count, 4)
            self.assertTrue(all(call.args[:2] == ("docker", "pull") for call in run.call_args_list))
            for field, value in (
                ("source_sha", "c" * 40),
                ("tag", "latest"),
                ("project", "agents"),
                ("image", "attacker.invalid/api@sha256:" + "b" * 64),
            ):
                self.write_images(directory)
                path = directory / "api.json"
                record = json.loads(path.read_text())
                record[field] = value
                path.write_text(json.dumps(record))
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.release_images(directory, "example.azurecr.io")
            self.write_images(directory)
            with patch.object(pipeline, "run", side_effect=pipeline.PipelineError("pull denied")):
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.release_images(directory, "example.azurecr.io")

    def test_publish_records_the_pushed_digest_without_running_the_image(self):
        with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV):
            directory = Path(temporary)
            digest = "example.azurecr.io/zava-forward-api@sha256:" + "b" * 64
            with (
                patch.object(pipeline, "registry", return_value="example.azurecr.io"),
                patch.object(
                    pipeline, "run", side_effect=["", "", "", json.dumps([digest])]
                ) as run,
            ):
                pipeline.publish("api", directory)
            self.assertEqual(
                [call.args[:2] for call in run.call_args_list],
                [("docker", "load"), ("docker", "tag"), ("docker", "push"), ("docker", "inspect")],
            )
            record = json.loads((directory / "api.json").read_text())
            self.assertEqual(record["image"], digest)
            self.assertEqual(record["source_sha"], SHA)
            self.assertEqual(record["tag"], f"sha-{SHA}-r123-a1")
            self.assertNotIn("latest", json.dumps(record))

    def test_deploy_uses_same_parameters_for_what_if_and_apply(self):
        with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV):
            directory = Path(temporary)
            calls = []

            def fake_az(*args):
                if args[:2] == ("containerapp", "list"):
                    return []
                calls.append(args)
                if args[:3] == ("deployment", "group", "what-if"):
                    parameter_path = Path(args[args.index("--parameters") + 1][1:])
                    self.assertEqual(
                        json.loads(parameter_path.read_text())["parameters"]["apiImage"]["value"],
                        "pinned",
                    )
                    return {"status": "Succeeded", "changes": []}
                return {
                    "properties": {
                        "provisioningState": "Succeeded",
                        "outputs": {
                            "apiInternalFqdn": {"value": "api.example.azurecontainerapps.io"}
                        },
                    }
                }

            with (
                patch.object(
                    pipeline,
                    "parameters",
                    return_value={"parameters": {"entraBearerOnly": {"value": True}}},
                ),
                patch.object(pipeline, "release_images", return_value={"apiImage": "pinned"}),
                patch.object(pipeline, "registry", return_value="example.azurecr.io"),
                patch.object(pipeline, "check_sql") as sql,
                patch.object(pipeline, "az", side_effect=fake_az),
                patch.object(pipeline, "smoke") as smoke,
            ):
                pipeline.deployment(ROOT / "infra", "test", directory / "summary.json", directory)
            self.assertEqual(calls[0][:3], ("deployment", "group", "what-if"))
            self.assertEqual(calls[1][:3], ("deployment", "group", "create"))
            self.assertEqual(calls[0][3:-1], calls[1][3:-2])
            self.assertEqual(sql.call_count, 2)
            smoke.assert_called_once_with(
                "https://api.example.azurecontainerapps.io", browser=False
            )
            self.assertFalse(parameter_path_exists(calls[0]))

    def test_pr_plan_preserves_existing_images_and_never_applies(self):
        def resource(name, project):
            return {
                "name": name,
                "properties": {
                    "template": {
                        "containers": [
                            {"image": f"example.azurecr.io/{project}@sha256:" + "b" * 64}
                        ]
                    }
                },
            }

        apps = [resource(f"ca-forward-test-{name}", name) for name in ("api", "agents")]
        jobs = [
            resource("job-forward-test-orchestrator", "orchestrator"),
            resource("job-forward-test-auth-renewal", "orchestrator"),
            resource("job-forward-test-ledger-verify", "orchestrator"),
            resource("job-forward-test-import", "importer"),
        ]
        with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV):
            directory = Path(temporary)
            with (
                patch.object(pipeline, "parameters", return_value={"parameters": {}}),
                patch.object(pipeline, "check_sql"),
                patch.object(
                    pipeline,
                    "az",
                    side_effect=[apps, jobs, {"status": "Succeeded", "changes": []}],
                ) as az,
            ):
                pipeline.deployment(ROOT / "infra", "test", directory / "summary.json", None)
            self.assertEqual(az.call_count, 3)
            self.assertEqual(az.call_args.args[:3], ("deployment", "group", "what-if"))
            self.assertNotIn("create", json.dumps(az.call_args_list, default=str))
            for invalid_jobs in (
                jobs[:-1],
                [*jobs[:1], resource("job-forward-test-auth-renewal", "other"), *jobs[2:]],
            ):
                with (
                    patch.object(pipeline, "parameters", return_value={"parameters": {}}),
                    patch.object(pipeline, "az", side_effect=[apps, invalid_jobs]) as az,
                ):
                    with self.assertRaises(pipeline.PipelineError):
                        pipeline.deployment(
                            ROOT / "infra", "test", directory / "summary.json", None
                        )
                self.assertEqual(az.call_count, 2)

    def test_failed_what_if_never_applies(self):
        with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV):
            directory = Path(temporary)
            with (
                patch.object(pipeline, "parameters", return_value={"parameters": {}}),
                patch.object(pipeline, "release_images", return_value={}),
                patch.object(pipeline, "registry", return_value="example.azurecr.io"),
                patch.object(pipeline, "check_sql"),
                patch.object(
                    pipeline, "az", side_effect=[[], {"status": "Failed", "changes": []}]
                ) as az,
            ):
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.deployment(
                        ROOT / "infra", "dev", directory / "summary.json", directory
                    )
            self.assertEqual(az.call_count, 2)
            self.assertEqual(
                json.loads((directory / "summary.json").read_text())["status"], "Failed"
            )

    def test_auth_lock_or_app_local_store_blocks_pipeline_before_plan_or_apply(self):
        for tags in ({"zava-forward-auth-lock": "other-session"},
                     {"zava-forward-credential-store": "app"}):
            with TemporaryDirectory() as temporary, patch.dict(os.environ, ENV), \
                    patch.object(pipeline, "parameters", return_value={"parameters": {}}), \
                    patch.object(pipeline, "az", return_value=[{"tags": tags}]) as az, \
                    patch.object(pipeline, "release_images") as images:
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.deployment(ROOT / "infra", "test",
                                        Path(temporary) / "summary.json", Path(temporary))
                images.assert_not_called()
                self.assertEqual(az.call_count, 1)

    def test_real_cli_with_failing_fake_az_never_leaks_output(self):
        with TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fake = directory / "az"
            fake.write_text(
                f"#!{sys.executable}\nprint('CANARY_PRIVATE_VALUE')\nraise SystemExit(1)\n"
            )
            fake.chmod(0o700)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "infra/scripts/pipeline.py"),
                    "plan",
                    "--output",
                    str(directory / "summary.json"),
                ],
                env={**ENV, "PATH": str(directory)},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("CANARY", result.stdout + result.stderr)


def parameter_path_exists(command):
    return Path(command[command.index("--parameters") + 1][1:]).exists()


class SmokeTests(unittest.TestCase):
    def probe(self, health=200, protected=401, bearer=401, forged=401, browser=None):
        statuses = iter((health, protected, bearer, forged, browser))

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(next(statuses))
                self.send_header("Location", "/healthz")
                self.end_headers()

            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            pipeline.smoke(
                f"http://127.0.0.1:{server.server_port}",
                attempts=1,
                delay=0,
                browser=browser is not None,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_exact_success(self):
        self.probe()
        self.probe(browser=302)

    def test_wrong_health_and_any_unauthenticated_success_or_redirect_fail(self):
        for options in (
            {"health": 204},
            {"health": 503},
            {"protected": 200},
            {"protected": 302},
            {"protected": 403},
            {"bearer": 200},
            {"forged": 200},
            {"browser": 200},
        ):
            with self.subTest(options=options):
                with self.assertRaises(pipeline.PipelineError):
                    self.probe(**options)

    def test_network_error_fails(self):
        with patch.object(
            pipeline.urllib.request.OpenerDirector, "open", side_effect=urllib_error()
        ):
            with self.assertRaises(pipeline.PipelineError):
                pipeline.smoke("http://127.0.0.1:1", attempts=1, delay=0)

    def test_installed_local_api_denies_unauthenticated_requests(self):
        with TemporaryDirectory(prefix="ama-local-api-") as temporary:
            directory = Path(temporary)
            seed = directory / "synthetic.json"
            seed.write_text('{"cases":[],"staff":[]}')
            with socket.socket() as listener:
                listener.bind(("127.0.0.1", 0))
                port = listener.getsockname()[1]
            env = {key: value for key, value in os.environ.items() if not key.startswith("ZF_")}
            env.update(
                ZF_DATA=str(seed),
                ZF_STATE=str(directory),
                ZF_STORE="json",
                ZF_AI="off",
                ZF_PASSWORD=secrets.token_hex(16),
                ZF_BIND="127.0.0.1",
                PORT=str(port),
            )
            process = subprocess.Popen(
                [sys.executable, "-m", "zava_forward.api"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                pipeline.smoke(f"http://127.0.0.1:{port}", attempts=40, delay=0.1)
                self.assertIsNone(process.poll())
            finally:
                process.terminate()
                try:
                    process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate(timeout=5)


def urllib_error():
    return pipeline.urllib.error.URLError("constructed network failure")


if __name__ == "__main__":
    unittest.main()
