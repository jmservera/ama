"""Offline fake-az lifecycle and real shared-SQL worker regressions."""

from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

import test_initialize_workbench_staff as sql_fixture
import test_setup_entra as setup_fixture

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import credential_arm as CREDENTIAL
import staff_azure as JOB

SETUP = setup_fixture.SETUP
ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "staff_worker", ROOT / "infra/scripts/staff-azure-worker.py"
)
assert SPEC and SPEC.loader
WORKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKER)

ROOT_ID = setup_fixture.APP_ID.split("/providers/")[0]
IDENTITY = (
    ROOT_ID + "/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-cutover-test-init"
)
SOURCE = ROOT_ID + "/providers/Microsoft.App/jobs/job-cutover-test-init"
SQL = ROOT_ID + "/providers/Microsoft.Sql/servers/fictional-sql"
MI = setup_fixture.uid("init-client")
PRINCIPAL = setup_fixture.uid("init-principal")
PERSON = "Private Candidate"
EMAIL = "private-candidate@example.invalid"


class FakeJobs(setup_fixture.FakeAzure):
    def __init__(self):
        super().__init__()
        self.app["properties"]["managedEnvironmentId"] = setup_fixture.ENV_ID
        self.app["properties"]["template"]["containers"][0]["env"] += [
            {"name": "ZF_SQL_SERVER", "value": "fictional-sql.database.windows.net"},
            {"name": "ZF_SQL_DATABASE", "value": "fixture"},
        ]
        self.environment["id"] = setup_fixture.ENV_ID
        self.environment["properties"]["vnetConfiguration"]["infrastructureSubnetId"] = (
            ROOT_ID + "/providers/Microsoft.Network/virtualNetworks/fictional/subnets/apps"
        )
        self.resources = {
            IDENTITY: {
                "id": IDENTITY,
                "properties": {
                    "clientId": MI,
                    "principalId": PRINCIPAL,
                    "tenantId": setup_fixture.TENANT,
                },
            },
            SOURCE: {
                "id": SOURCE,
                "name": "job-cutover-test-init",
                "location": "fictional",
                "identity": {"type": "UserAssigned", "userAssignedIdentities": {IDENTITY: {}}},
                "properties": {
                    "environmentId": setup_fixture.ENV_ID,
                    "configuration": {
                        "registries": [{"server": "fixture.azurecr.io", "identity": IDENTITY}]
                    },
                    "template": {
                        "containers": [
                            {
                                "name": "proof",
                                "image": "fixture.azurecr.io/zava-forward-cutover-proof@sha256:"
                                + "a" * 64,
                            }
                        ]
                    },
                },
            },
            SQL: {
                "properties": {
                    "fullyQualifiedDomainName": "fictional-sql.database.windows.net",
                    "publicNetworkAccess": "Disabled",
                }
            },
            SQL + "/databases/fixture": {"id": SQL + "/databases/fixture"},
            SQL + "/administrators/ActiveDirectory": {
                "properties": {
                    "sid": PRINCIPAL,
                    "tenantId": setup_fixture.TENANT,
                    "principalType": "Application",
                }
            },
            SQL + "/azureADOnlyAuthentications/Default": {
                "properties": {"azureADOnlyAuthentication": True}
            },
        }
        self.jobs = {}
        self.requests = []
        self.deleted = []
        self.stopped = []
        self.status = "Succeeded"
        self.fail_at = None
        self.polls = 0
        self.log_mutation = lambda value: value
        self.collision = False
        self.relay_tags = {"preserved": "original"}
        self.published = False
        self.credential_template = None
        self.whatif_mutation = lambda value: value
        self.metadata_mutation = lambda value: value
        self.deployment_state = "Succeeded"

    def run(self, command, **kwargs):
        if command[:4] == ["az", "deployment", "group", "what-if"]:
            self.calls.append((command, kwargs["env"]))
            template = Path(command[command.index("--template-file") + 1])
            parameters = Path(command[command.index("--parameters") + 1][1:])
            assert template.stat().st_mode & 0o077 == parameters.stat().st_mode & 0o077 == 0
            self.credential_template = json.loads(template.read_text())
            assert json.loads(parameters.read_text())["credential"]["value"] == setup_fixture.SECRET
            intended = self.credential_template["resources"][0]
            planned = {
                "status": "Succeeded",
                "changes": [
                    {
                        "resourceId": ROOT_ID
                        + "/providers/Microsoft.KeyVault/vaults/"
                        + intended["name"].replace("/", "/secrets/", 1),
                        "changeType": "Create",
                    }
                ],
            }
            return subprocess.CompletedProcess(
                command, 0, json.dumps(self.whatif_mutation(planned)), ""
            )
        if command[:4] == ["az", "containerapp", "job", "logs"]:
            raise AssertionError("The laptop path must never require console logs.")
        if command[:3] == ["az", "containerapp", "job"]:
            self.calls.append((command, kwargs["env"]))
            name = command[command.index("-n") + 1]
            operation = command[3]
            if operation == "start":
                self.polls = 0
                if self.fail_at == "start":
                    raise SETUP.AzureError("network")
                value = {"name": name + "-execution"}
            elif operation == "stop":
                self.stopped.append(name)
                if self.fail_at == "stop":
                    raise SETUP.AzureError("permission")
                value = {}
            elif operation == "replica":
                value = [{"name": name + "-replica"}]
            else:
                raise AssertionError(operation)
            return subprocess.CompletedProcess(command, 0, json.dumps(value), "")
        return super().run(command, **kwargs)

    def rest(self, method, url, body):
        resource = url.removeprefix(SETUP.ARM).split("?")[0]
        vault = ROOT_ID + "/providers/Microsoft.KeyVault/vaults/fictional-vault"
        if resource == vault:
            return {
                "id": vault,
                "properties": {"publicNetworkAccess": "Disabled", "enableRbacAuthorization": True},
            }
        if resource == vault + "/secrets":
            return {"value": []}
        if resource.startswith(ROOT_ID + "/providers/Microsoft.Resources/deployments/entra-"):
            if method == "PUT":
                assert body["properties"]["template"] == self.credential_template
                assert (
                    body["properties"]["parameters"]["credential"]["value"] == setup_fixture.SECRET
                )
            return {"properties": {"provisioningState": self.deployment_state}}
        if resource.startswith(vault + "/secrets/"):
            intended = self.credential_template["resources"][0]
            return self.metadata_mutation(
                {
                    "id": resource,
                    "properties": {
                        "secretUri": "https://fictional-vault.vault.azure.net/secrets/"
                        + intended["name"].split("/")[1],
                        "attributes": intended["properties"]["attributes"],
                    },
                }
            )
        if url == JOB.tags_url(SOURCE):
            if method == "PATCH":
                self.assert_tag_delete(body)
                return {"properties": {"tags": self.relay_tags}}
            if self.requests and self.polls and not self.published:
                if self.fail_at == "logs":
                    raise SETUP.AzureError("permission")
                request = self.requests[-1]
                summary = (
                    {"candidates": self.candidates}
                    if request["operation"] == "candidates"
                    else {
                        "positions": len(request["payload"].get("wanted", [])),
                        "staff_changes": 0,
                        "owner_labels": 0,
                        "sql_verified": True,
                        "restart_required": request["operation"] != "apply",
                    }
                )
                result = {
                    "version": 1,
                    "run": request["run"],
                    "operation": request["operation"],
                    "ok": True,
                    **summary,
                }
                frames = self.log_mutation(
                    "\n".join(
                        json.dumps({"Log": frame}) for frame in JOB.encode_result(request, result)
                    )
                )
                self.relay_tags.update(
                    {
                        JOB.result_prefix(request) + str(i): json.loads(frame)["Log"]
                        for i, frame in enumerate(frames.splitlines())
                    }
                )
                self.published = True
            return {"properties": {"tags": copy.deepcopy(self.relay_tags)}}
        if "/jobs/job-staff-" in resource:
            if "/executions/" in resource:
                self.polls += 1
                return {"properties": {"status": "Running" if self.polls == 1 else self.status}}
            if method == "PUT":
                self.published = False
                self.polls = 0
                self.jobs[resource] = copy.deepcopy(body)
                self.jobs[resource]["properties"]["provisioningState"] = "Succeeded"
                request = json.loads(body["properties"]["configuration"]["secrets"][0]["value"])
                self.requests.append(request)
                if self.fail_at == "create":
                    raise SETUP.AzureError("network")
                return self.jobs[resource]
            if method == "DELETE":
                if self.fail_at == "delete":
                    raise SETUP.AzureError("permission")
                self.deleted.append(resource)
                self.jobs.pop(resource, None)
                return {}
            if self.collision:
                return {"tags": {"zava-forward-staff-run": "another-owner"}}
            if resource not in self.jobs:
                raise SETUP.AzureError("not-found")
            return self.jobs[resource]
        if resource in self.resources:
            assert method == "GET"
            return self.resources[resource]
        if "/providers/Microsoft.App/jobs/" in resource:
            raise SETUP.AzureError("not-found")
        if url.startswith(SETUP.GRAPH + f"users/{setup_fixture.USER}?"):
            return {
                "id": setup_fixture.USER,
                "displayName": PERSON,
                "userPrincipalName": EMAIL,
                "accountEnabled": True,
                "userType": "Member",
            }
        return super().rest(method, url, body)

    def assert_tag_delete(self, body):
        assert body["operation"] == "Delete"
        for key, value in body["properties"]["tags"].items():
            assert key.startswith(JOB.result_prefix(self.requests[-1]))
            assert self.relay_tags[key] == value
            del self.relay_tags[key]


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.home = Path(self.directory.name)
        self.profile = self.home / "profile"
        self.profile.mkdir(mode=0o700)
        self.fake = FakeJobs()
        self.cli = SETUP.Azure(self.profile, body_directory=self.profile)
        self.cli.subscription = setup_fixture.SUB
        self.output = io.StringIO()
        self.addCleanup(patch.stopall)
        patch.object(SETUP.subprocess, "run", side_effect=self.fake.run).start()
        patch.object(JOB.time, "sleep").start()

    def execute(self, operation="candidates", payload=None, **kwargs):
        with redirect_stdout(self.output), redirect_stderr(self.output):
            return JOB.execute(self.cli, self.fake.app, operation, payload or {}, **kwargs)

    def assert_private(self):
        output = self.output.getvalue()
        argv = json.dumps([c for c, _ in self.fake.calls])
        for private in (PERSON, EMAIL, setup_fixture.USER, setup_fixture.SECRET):
            self.assertNotIn(private, output)
            self.assertNotIn(private, argv)
        for request in self.fake.requests:
            self.assertNotIn(request["key"], output + argv)
        self.assertEqual(list(self.profile.glob("request-*.json")), [])
        self.assertIn(SOURCE, self.fake.resources)
        self.assertFalse(self.fake.jobs)
        self.assertEqual(self.fake.relay_tags, {"preserved": "original"})
        self.assertFalse(
            any(c[:4] == ["az", "containerapp", "job", "logs"] for c, _ in self.fake.calls)
        )

    def test_success_uses_private_secret_existing_identity_no_network_mutation(self):
        self.fake.resources[SOURCE]["properties"]["configuration"]["registries"][0].update(
            username=None, passwordSecretRef=None
        )
        result = self.execute()
        self.assertEqual(result["candidates"], self.fake.candidates)
        self.assertEqual(len(self.fake.deleted), 1)
        put = next(
            body
            for method, url, body in self.fake.writes
            if method == "PUT" and "/jobs/job-staff-" in url
        )
        config = put["properties"]["configuration"]
        self.assertEqual(config["replicaRetryLimit"], 0)
        self.assertEqual(
            config["manualTriggerConfig"], {"parallelism": 1, "replicaCompletionCount": 1}
        )
        self.assertEqual(set(put["identity"]["userAssignedIdentities"]), {IDENTITY})
        self.assertEqual(put["properties"]["environmentId"], setup_fixture.ENV_ID)
        worker = put["properties"]["template"]["containers"][0]
        self.assertIn({"name": "ZF_STAFF_REQUEST", "secretRef": "request"}, worker["env"])
        self.assertTrue(
            all(
                (method in {"PUT", "DELETE"} and "/jobs/job-staff-" in url)
                or (method == "PATCH" and url == JOB.tags_url(SOURCE))
                for method, url, _ in self.fake.writes
            )
        )
        self.assert_private()

    def test_failure_start_loss_logs_and_interrupt_always_stop_delete(self):
        for failure in ("create", "start", "logs", "worker", "stop"):
            with self.subTest(failure=failure):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.fake.fail_at = failure
                if failure in ("worker", "stop"):
                    self.fake.status = "Failed"
                with self.assertRaises((JOB.StaffJobError, SETUP.AzureError)):
                    self.execute()
                self.assertEqual(len(self.fake.deleted), 1)
                self.assertEqual(len(self.fake.stopped), 1)
                self.assert_private()
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        with (
            patch.object(JOB, "read_result", side_effect=KeyboardInterrupt),
            self.assertRaises(KeyboardInterrupt),
        ):
            self.execute()
        self.assert_private()

    def test_timeout_is_incomplete_and_cleanup_is_verified(self):
        self.fake.status = "Running"
        ticks = iter([0, 0, 0, 0, 700])
        with (
            patch.object(JOB.time, "monotonic", side_effect=lambda: next(ticks, 700)),
            self.assertRaisesRegex(JOB.StaffJobError, "timed out"),
        ):
            self.execute()
        self.assert_private()

    def test_timeout_with_decoded_result_never_returns_success(self):
        self.fake.status = "Running"
        clock = [0.0]

        def sleep(_seconds):
            if self.fake.polls:
                clock[0] += 400

        with (
            patch.object(JOB.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(JOB.time, "sleep", side_effect=sleep),
            self.assertRaisesRegex(JOB.StaffJobError, "timed out"),
        ):
            self.execute()
        self.assertGreater(self.fake.polls, 1)
        self.assertEqual(len(self.fake.deleted), 1)
        self.assert_private()

    def test_cleanup_failure_never_returns_success_and_has_owned_recovery_name(self):
        self.fake.fail_at = "delete"
        with self.assertRaisesRegex(JOB.StaffJobError, "cleanup NOT confirmed.*job-staff-"):
            self.execute()
        self.assertEqual(len(self.fake.jobs), 1)
        self.assertIn(SOURCE, self.fake.resources)

    def test_collision_refused_without_deleting_or_transferring_roster(self):
        self.fake.collision = True
        with self.assertRaisesRegex(JOB.StaffJobError, "collision"):
            self.execute()
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.deleted)

    def test_resource_guards_fail_before_secret_transfer(self):
        changes = [
            (IDENTITY, lambda r: r["properties"].update(tenantId=setup_fixture.uid("wrong"))),
            (IDENTITY, lambda r: r["properties"].update(principalId=MI)),
            (SOURCE, lambda r: r["properties"].update(environmentId="/wrong")),
            (SOURCE, lambda r: r["identity"]["userAssignedIdentities"].update({"/extra": {}})),
            (
                SOURCE,
                lambda r: r["properties"]["template"]["containers"].append({"image": "wrong"}),
            ),
            (
                SOURCE,
                lambda r: r["properties"]["configuration"]["registries"][0].update(
                    passwordSecretRef="bad"
                ),
            ),
            (
                SOURCE,
                lambda r: r["properties"]["template"]["containers"][0].update(
                    image="untrusted:latest"
                ),
            ),
            (SQL, lambda r: r["properties"].update(publicNetworkAccess="Enabled")),
            (
                SQL + "/administrators/ActiveDirectory",
                lambda r: r["properties"].update(principalType="Group"),
            ),
            (
                SQL + "/azureADOnlyAuthentications/Default",
                lambda r: r["properties"].update(azureADOnlyAuthentication=False),
            ),
            (SQL + "/databases/fixture", lambda r: r.update(id="/wrong")),
        ]
        for key, mutate in changes:
            with self.subTest(key=key):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                mutate(self.fake.resources[key])
                with self.assertRaises(JOB.StaffJobError):
                    self.execute()
                self.assertFalse(self.fake.requests)
                self.assertFalse(self.fake.deleted)
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        self.fake.environment["properties"]["vnetConfiguration"]["infrastructureSubnetId"] = (
            "/outside"
        )
        with self.assertRaises(JOB.StaffJobError):
            self.execute()

    def test_same_vnet_parent_environment_allowed_but_other_vnet_and_tag_exhaustion_block(self):
        other = setup_fixture.ENV_ID + "-parent"
        self.fake.resources[SOURCE]["properties"]["environmentId"] = other
        environment = copy.deepcopy(self.fake.environment)
        environment["id"] = other
        environment["properties"]["vnetConfiguration"]["infrastructureSubnetId"] = (
            ROOT_ID + "/providers/Microsoft.Network/virtualNetworks/fictional/subnets/parent"
        )
        self.fake.resources[other] = environment
        self.assertTrue(self.execute()["ok"])
        environment["properties"]["vnetConfiguration"]["infrastructureSubnetId"] = (
            ROOT_ID + "/providers/Microsoft.Network/virtualNetworks/other/subnets/parent"
        )
        with self.assertRaises(JOB.StaffJobError):
            self.execute()
        self.fake.resources[SOURCE]["properties"]["environmentId"] = setup_fixture.ENV_ID
        self.fake.relay_tags.update({f"other-{i}": "preserved" for i in range(10)})
        with self.assertRaisesRegex(JOB.StaffJobError, "tag capacity"):
            self.execute()

    def test_direct_demo_automatically_discovers_only_its_verified_parent_initializer(self):
        self.fake.app["id"] = setup_fixture.APP_ID.replace("-test-api", "-test-demo-api")
        self.fake.app["name"] = "ca-cutover-test-demo-api"
        result = self.execute()
        self.assertTrue(result["ok"])
        self.assertEqual(self.fake.requests[-1]["payload"]["target"], self.fake.app["id"])
        self.assertEqual(self.fake.requests[-1]["payload"]["relay"], SOURCE)

    def test_tag_tamper_oversize_and_failed_cleanup_block_success(self):
        for mutation in (
            lambda text: text.replace("ZFSTAFF:", "ZFSTAFF:wrong"),
            lambda text: json.dumps({"Log": "x" * 257}),
            lambda text: "",
        ):
            self.fake = FakeJobs()
            SETUP.subprocess.run.side_effect = self.fake.run
            self.fake.log_mutation = mutation
            # A missing result is bounded by the execution deadline, even at Succeeded.
            clock = [0]
            with (
                patch.object(JOB.time, "monotonic", side_effect=lambda clock=clock: clock[0]),
                patch.object(
                    JOB.time,
                    "sleep",
                    side_effect=lambda _, clock=clock: clock.__setitem__(0, clock[0] + 250),
                ),
                self.assertRaises(JOB.StaffJobError),
            ):
                self.execute()
            self.assertFalse(self.fake.jobs)
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        with (
            patch.object(JOB, "clear_result", side_effect=SETUP.AzureError("permission")),
            self.assertRaisesRegex(JOB.StaffJobError, "cleanup NOT confirmed"),
        ):
            self.execute()

    def test_secret_person_data_never_in_command_line_logs_or_leftover_body_files(self):
        payload = {
            "wanted": [{"code": "private-code", "userId": setup_fixture.USER}],
            "people": {setup_fixture.USER: {"displayName": PERSON, "userPrincipalName": EMAIL}},
        }
        self.execute("apply", payload)
        self.assertEqual(self.fake.requests[-1]["payload"]["people"], payload["people"])
        self.assert_private()

    def test_wire_authentication_framing_and_total_limits(self):
        request = {
            "version": 1,
            "run": "fictional-run",
            "operation": "check",
            "digest": "digest",
            "key": base64.b64encode(b"a" * 32).decode(),
        }
        result = {
            "version": 1,
            "run": request["run"],
            "operation": "check",
            "ok": True,
            "padding": "x" * 3000,
        }
        frames = JOB.encode_result(request, result)
        output = "\n".join(json.dumps({"Log": line}) for line in frames)
        self.assertEqual(JOB.decode_result(request, output), result)
        self.assertIsNone(JOB.decode_result(request, "\n".join(output.splitlines()[:-1])))
        for bad in (
            output + "\n" + output,
            output.replace("fictional-run", "wrong"),
            output.replace(frames[0][-8:], "aaaaaaaa"),
        ):
            with self.subTest(bad=bad[:30]), self.assertRaises(JOB.StaffJobError):
                JOB.decode_result(request, bad)
        with self.assertRaises(JOB.StaffJobError):
            JOB.decode_result(dict(request, operation="apply"), output)
        with self.assertRaises(JOB.StaffJobError):
            JOB.decode_result(dict(request, key=base64.b64encode(b"b" * 32).decode()), output)
        with self.assertRaises(JOB.StaffJobError):
            self.execute(payload={"oversize": "x" * JOB.MAX_INPUT})
        self.assertFalse(self.fake.requests)


class SetupAzureTests(unittest.TestCase):
    """Exercise real setup with fake az; existing local regressions run separately."""

    write_roster = setup_fixture.SetupTests.write_roster
    invoke = setup_fixture.SetupTests.invoke
    demo_roster = setup_fixture.SetupTests.demo_roster
    demo_person = staticmethod(setup_fixture.SetupTests.demo_person)

    def setUp(self):
        setup_fixture.SetupTests.setUp(self)
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run

    def test_explicit_azure_and_automatic_sql_preflight_fallback_finish_restart(self):
        for explicit in (True, False):
            with self.subTest(explicit=explicit):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.fake.sql_code = 1
                flags = ["--run-in-azure"] if explicit else []
                self.assertEqual(self.invoke(*flags), 0, self.output.getvalue())
                self.assertEqual([r["operation"] for r in self.fake.requests], ["check", "apply"])
                self.assertEqual(len(self.fake.sql_calls), 0 if explicit else 1)
                self.assertFalse(self.fake.jobs)
                self.assertIn("replica restart: verified", self.output.getvalue())
                self.assertNotIn(PERSON, self.output.getvalue())
                self.assertNotIn(EMAIL, self.output.getvalue())

    def test_azure_candidates_are_count_only_and_cleaned_up(self):
        self.roster.unlink()
        self.assertEqual(self.invoke("--run-in-azure", "--list-staff"), 0, self.output.getvalue())
        self.assertNotIn("fictional-coordinator", self.output.getvalue())
        self.assertEqual([r["operation"] for r in self.fake.requests], ["candidates"])
        self.assertFalse(self.fake.jobs)

    def test_azure_generated_roster_retains_admin_seed_and_never_prints_codes(self):
        self.demo_roster()
        self.assertEqual(self.invoke("--run-in-azure", "--seed", "41"), 0, self.output.getvalue())
        data = json.loads(self.roster.read_text())
        self.assertEqual(data["seed"], 41)
        self.assertEqual(
            next(r for r in data["staff"] if r["code"] == "PM-01")["userId"],
            setup_fixture.uid("administrator"),
        )
        self.assertEqual(len({r["userId"] for r in data["staff"]}), len(data["staff"]))
        for row in data["staff"]:
            self.assertNotIn(row["code"], self.output.getvalue())
            self.assertNotIn(row["userId"], self.output.getvalue())
        for user in self.fake.users:
            self.assertNotIn(user["displayName"], self.output.getvalue())
            self.assertNotIn(user["userPrincipalName"], self.output.getvalue())
        self.assertEqual(
            [r["operation"] for r in self.fake.requests], ["candidates", "check", "apply"]
        )
        self.assertFalse(self.fake.jobs)

    def test_unknown_local_apply_result_never_falls_back_or_reapplies(self):
        original = self.fake.run

        def run(command, **kwargs):
            if command[0] != "az" and "--apply" in command:
                self.fake.sql_calls.append(command)
                raise subprocess.TimeoutExpired(command, 600)
            return original(command, **kwargs)

        SETUP.subprocess.run.side_effect = run
        self.assertEqual(self.invoke(), 2, self.output.getvalue())
        self.assertFalse(self.fake.requests)
        self.assertEqual(sum("--apply" in command for command in self.fake.sql_calls), 1)

    def test_azure_dry_run_never_creates_jobs(self):
        self.assertEqual(self.invoke("--run-in-azure", "--dry-run"), 2, self.output.getvalue())
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.sql_calls)
        self.assertIn("--dry-run never creates", self.output.getvalue())

    def test_candidate_auto_fallback_and_missing_image_exact_private_host_fallback(self):
        self.fake.candidate_code = 1
        self.roster.unlink()
        self.assertEqual(self.invoke("--list-staff"), 0, self.output.getvalue())
        self.assertEqual(len(self.fake.sql_calls), 1)
        self.assertEqual([r["operation"] for r in self.fake.requests], ["candidates"])
        self.fake.resources[SOURCE]["properties"]["template"]["containers"][0]["image"] = (
            "old:latest"
        )
        self.assertEqual(self.invoke("--run-in-azure", "--list-staff"), 1)
        self.assertIn("authorized private-connected host", self.output.getvalue())

    def test_azure_store_guard_blocks_app_state_before_graph_writes(self):
        for case in ("explicit", "recorded", "reference"):
            with self.subTest(case=case):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                flags = ["--secret-store", "app"] if case == "explicit" else []
                if case == "recorded":
                    self.fake.app["tags"][SETUP.STORE_TAG] = "app"
                if case == "reference":
                    self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"][
                        "clientSecretSettingName"
                    ] = "preserved"
                self.assertEqual(self.invoke("--run-in-azure", *flags), 1)
                self.assertFalse(self.fake.writes)
                self.assertIsNone(self.fake.reg)

    def test_azure_vault_preflight_failure_never_creates_password_or_falls_back(self):
        self.fake.app["tags"]["zava-forward-ingress"] = "direct"
        self.fake.app["properties"]["configuration"]["ingress"]["external"] = True
        with patch.object(CREDENTIAL, "preflight", side_effect=SETUP.AzureError("permission")):
            self.assertEqual(self.invoke("--run-in-azure"), 1)
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertNotEqual(self.fake.app["tags"].get(SETUP.STORE_TAG), "app")

    def test_azure_vault_write_failure_preserves_auth_and_never_uses_app_storage(self):
        secrets = json.loads(json.dumps(self.fake.app["properties"]["configuration"]["secrets"]))
        auth = json.loads(json.dumps(self.fake.auth))
        with patch.object(CREDENTIAL, "store", side_effect=CREDENTIAL.CredentialError("failed")):
            self.assertEqual(self.invoke("--run-in-azure", "--secret-store", "keyvault"), 1)
        self.assertEqual(self.fake.app["properties"]["configuration"]["secrets"], secrets)
        self.assertEqual(self.fake.auth, auth)
        self.assertNotEqual(self.fake.app["tags"].get(SETUP.STORE_TAG), "app")
        self.assertNotIn(setup_fixture.SECRET, self.output.getvalue())

    def test_existing_valid_keyvault_reference_is_reused_without_another_password(self):
        self.assertEqual(self.invoke("--run-in-azure", "--secret-store", "keyvault"), 0)
        count = len(self.fake.reg["passwordCredentials"])
        with patch.object(CREDENTIAL, "store", side_effect=AssertionError("unexpected rotation")):
            self.assertEqual(self.invoke("--run-in-azure", "--secret-store", "keyvault"), 0)
        self.assertEqual(len(self.fake.reg["passwordCredentials"]), count)


class CredentialArmTests(unittest.TestCase):
    setUp = TransportTests.setUp

    def credential(self):
        return CREDENTIAL.store(
            self.cli,
            self.fake.app,
            "fictional-vault",
            "entra-" + "a" * 32 + "-" + "b" * 12,
            setup_fixture.SECRET,
            "2027-04-01T00:00:00Z",
            seconds=10,
        )

    def test_secure_single_secret_deployment_no_data_plane_or_argument_leak(self):
        self.fake.whatif_mutation = lambda result: {
            **result,
            "changes": [*result["changes"], {"changeType": "Ignore", "resourceId": SOURCE}],
        }
        CREDENTIAL.preflight(self.cli, self.fake.app, "fictional-vault")
        self.assertIn("/secrets/entra-", self.credential())
        self.assertEqual(
            self.fake.credential_template["parameters"]["credential"]["type"], "secureString"
        )
        self.assertNotIn("outputs", self.fake.credential_template)
        self.assertEqual(len(self.fake.credential_template["resources"]), 1)
        argv = json.dumps([c for c, _ in self.fake.calls])
        self.assertNotIn(setup_fixture.SECRET, argv)
        self.assertNotIn("keyvault", [c[1] for c, _ in self.fake.calls])
        self.assertEqual(list(self.profile.iterdir()), [])
        self.assertIsNone(self.cli.deadline)

    def test_unreviewed_scope_or_incomplete_whatif_never_applies(self):
        for mutate in (
            lambda result: {**result, "status": "Running"},
            lambda result: {**result, "changes": []},
            lambda result: {**result, "changes": result["changes"] * 2},
            lambda result: {
                **result,
                "changes": [{"resourceId": "/wrong", "changeType": "Create"}],
            },
            lambda result: {
                **result,
                "changes": [{**result["changes"][0], "changeType": "Modify"}],
            },
        ):
            self.fake.whatif_mutation = mutate
            with self.assertRaises(CREDENTIAL.CredentialError):
                self.credential()
            self.assertFalse(self.fake.writes)
            self.assertEqual(list(self.profile.iterdir()), [])

    def test_failed_timeout_and_unverified_metadata_never_return_reference(self):
        self.fake.deployment_state = "Failed"
        with self.assertRaises(CREDENTIAL.CredentialError):
            self.credential()
        self.fake.deployment_state = "Running"
        clock = [0]
        with (
            patch.object(CREDENTIAL.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(
                CREDENTIAL.time, "sleep", side_effect=lambda _: clock.__setitem__(0, clock[0] + 20)
            ),
            self.assertRaises(CREDENTIAL.CredentialError),
        ):
            self.credential()
        self.fake.deployment_state = "Succeeded"
        for field in ("enabled", "exp"):

            def mutate(value, field=field):
                value["properties"]["attributes"] = {
                    **value["properties"]["attributes"],
                    field: False,
                }
                return value

            self.fake.metadata_mutation = mutate
            with self.assertRaises(CREDENTIAL.CredentialError):
                self.credential()

    def test_invalid_scope_and_vault_fail_before_writes(self):
        self.cli.subscription = setup_fixture.uid("wrong-subscription")
        with self.assertRaises(CREDENTIAL.CredentialError):
            self.credential()
        self.assertFalse(self.fake.writes)


class WorkerTests(unittest.TestCase):
    def setUp(self):
        fixture = sql_fixture.StaffInitializationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.db = fixture.db
        self.db.execute("ALTER TABLE cases ADD contractor TEXT")
        self.db.execute("UPDATE cases SET contractor='Example Supplier'")
        person = {
            "id": sql_fixture.ONE,
            "displayName": "Tenant Coordinator",
            "userPrincipalName": "coordinator@example.invalid",
            "accountEnabled": True,
            "userType": "Member",
        }
        self.request = {
            "operation": "apply",
            "payload": {
                "target": setup_fixture.APP_ID,
                "relay": SOURCE,
                "wanted": [{"code": "RC-01", "role": "Coordinator", "userId": sql_fixture.ONE}],
                "people": {sql_fixture.ONE: person},
            },
        }
        self.management = Mock()

    def test_apply_checks_persisted_sql_then_restarts_even_on_noop(self):
        with patch.object(WORKER.STAFF, "restart_api") as restart:
            result = WORKER.run_sql(self.request, self.db, self.management)
            self.assertTrue(result["sql_verified"])
            self.assertFalse(result["restart_required"])
            self.assertEqual(result["staff_changes"], 1)
            restart.assert_called_once_with("ama", "ca-cutover-test-api", call=self.management.call)
            result = WORKER.run_sql(self.request, self.db, self.management)
            self.assertEqual(result["staff_changes"], 0)
            self.assertEqual(restart.call_count, 2)
        self.assertEqual(self.db.execute("SELECT count FROM audit_head").fetchone()[0], 1)

    def test_check_and_candidates_have_no_sql_writes_or_restart(self):
        with patch.object(WORKER.STAFF, "restart_api") as restart:
            result = WORKER.run_sql(dict(self.request, operation="check"), self.db)
            self.assertEqual(result["staff_changes"], 1)
            self.assertFalse(result["sql_verified"])
            candidates = WORKER.run_sql(dict(self.request, operation="candidates"), self.db)
            self.assertEqual(candidates["candidates"][0]["code"], "RC-01")
            restart.assert_not_called()
        self.assertEqual(self.db.execute("SELECT count FROM audit_head").fetchone()[0], 0)

    def test_postcommit_drift_and_restart_failure_never_report_success(self):
        with (
            patch.object(
                WORKER.STAFF,
                "install_roster",
                side_effect=[
                    {"staff_changes": 1, "owner_labels": 1},
                    {"staff_changes": 1, "owner_labels": 0},
                ],
            ),
            patch.object(WORKER.STAFF, "restart_api") as restart,
            self.assertRaises(ValueError),
        ):
            WORKER.run_sql(self.request, self.db, self.management)
        restart.assert_not_called()
        with (
            patch.object(WORKER.STAFF, "restart_api", side_effect=RuntimeError("private")),
            self.assertRaises(RuntimeError),
        ):
            WORKER.run_sql(self.request, self.db, self.management)

    def test_worker_failure_never_prints_private_exception_or_payload(self):
        from zava_forward.core import mssqlstore

        payload = json.dumps(self.request["payload"], sort_keys=True)
        request = {
            **self.request,
            "version": 1,
            "run": "fixture-run",
            "digest": hashlib.sha256(payload.encode()).hexdigest(),
            "key": base64.b64encode(b"a" * 32).decode(),
        }
        output = io.StringIO()
        env = {
            "ZF_STAFF_REQUEST": json.dumps(request),
            "ZF_STAFF_TARGET": setup_fixture.APP_ID,
            "ZF_STAFF_RELAY": SOURCE,
            "ZF_SQL_AUTH": "msi",
            "ZF_SQL_CLIENT_ID": MI,
            "AZURE_CLIENT_ID": MI,
        }
        with (
            patch.dict(os.environ, env),
            patch.object(
                mssqlstore, "_Conn", side_effect=RuntimeError(PERSON + EMAIL + sql_fixture.ONE)
            ),
            patch.object(mssqlstore, "connection_string", return_value="fixture"),
            patch.object(WORKER, "publish_result") as publish,
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            self.assertEqual(WORKER.main(), 1)
            self.assertFalse(publish.call_args.args[1]["ok"])
        for private in (PERSON, EMAIL, sql_fixture.ONE, request["key"]):
            self.assertNotIn(private, output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn("GRAPH", Path(WORKER.__file__).read_text())

    def test_image_and_rbac_contract_are_narrow(self):
        image = (ROOT / "infra/cutover-proof.Dockerfile").read_text()
        for asset in (
            "staff-azure-worker.py",
            "staff_azure.py",
            "staff_roster.py",
            "initialize-workbench-staff.py",
            "entra/app-registration.json",
        ):
            self.assertIn(asset, image)
        role = (ROOT / "infra/staff-initializer-rbac.bicep").read_text()
        self.assertIn("scope: api", role)
        self.assertIn("initializer.properties.principalId", role)
        self.assertNotIn("'*'", role)
        self.assertNotIn("Contributor", role)
        self.assertIn("Microsoft.App/containerApps/revisions/restart/action", role)

    def test_worker_publishes_only_bounded_ciphertext_and_preserves_other_tags(self):
        request = {
            "payload": {"relay": SOURCE},
            "run": "a" * 32,
            "operation": "candidates",
            "digest": "digest",
            "key": base64.b64encode(b"a" * 32).decode(),
        }
        management = Mock()
        management.request.return_value = {"properties": {"tags": {"preserved": "tag"}}}
        with (
            patch.dict(os.environ, {"ZF_STAFF_RELAY": SOURCE}),
            patch.object(WORKER, "Management", return_value=management),
        ):
            WORKER.publish_result(request, {"private": PERSON})
        body = management.request.call_args.kwargs["body"]
        self.assertEqual(body["operation"], "Merge")
        self.assertNotIn(PERSON, json.dumps(body))
        self.assertNotIn(request["key"], json.dumps(body))
        self.assertTrue(all(len(v) <= 256 for v in body["properties"]["tags"].values()))
        self.assertNotIn("preserved", body["properties"]["tags"])
        management.credential.close.assert_called_once()


class BuildContextTests(unittest.TestCase):
    def test_every_dockerfile_copy_source_survives_dockerignore(self):
        import fnmatch
        import re

        infra = ROOT / "infra"
        rules = [
            line.strip()
            for line in (infra / ".dockerignore").read_text().splitlines()
            if line.strip() and not line.startswith("#")
        ]

        def ignored(path):
            result = False
            for rule in rules:
                negate = rule.startswith("!")
                pattern = rule.lstrip("!").rstrip("/")
                parts = path.split("/")
                prefixes = ["/".join(parts[: i + 1]) for i in range(len(parts))]
                if pattern == "**":
                    hit = True
                else:
                    hit = any(fnmatch.fnmatchcase(prefix, pattern) for prefix in prefixes)
                if hit:
                    result = not negate
            return result

        sources = []
        for line in (infra / "cutover-proof.Dockerfile").read_text().splitlines():
            if line.startswith("COPY "):
                words = [w for w in line.split()[1:] if not w.startswith("--")]
                sources += words[:-1]
        self.assertTrue(sources)
        for source in sources:
            self.assertTrue((infra / source).is_file(), source)
            self.assertFalse(ignored(source), source)
        self.assertTrue(re.search(r"entra/app-registration.json", " ".join(sources)))


if __name__ == "__main__":
    unittest.main()
