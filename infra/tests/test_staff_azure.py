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
import threading
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import test_initialize_workbench_staff as sql_fixture
import test_setup_entra as setup_fixture

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import credential_arm as CREDENTIAL
import staff_azure as JOB
import staff_blob as BLOB

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


BLOB_URL = "https://fictionalstaff.blob.core.windows.net"
STORAGE = ROOT_ID + "/providers/Microsoft.Storage/storageAccounts/fictionalstaff"


class FakeContainer:
    """In-memory stand-in for a private ContainerClient; no network or tenant is touched."""

    def __init__(self):
        self.blobs = {}
        self.unreachable = False
        self.uploads = []
        self.stall_list = None
        self.stall_download = None
        self.timeouts = []
        self.downloads = []
        self.read_sizes = []

    def list_blobs(self, name_starts_with="", timeout=None):
        self.timeouts.append(timeout)
        if self.stall_list is not None:
            self.stall_list.wait(10)
        if self.unreachable:
            raise OSError("unreachable")
        return [
            {"name": name, "size": len(body)}
            for name, body in sorted(self.blobs.items())
            if name.startswith(name_starts_with)
        ]

    def download_blob(self, name, timeout=None, *, offset=0, length=None):
        self.timeouts.append(timeout)
        self.downloads.append((name, offset, length))
        if self.stall_download is not None:
            self.stall_download.wait(10)
        if self.unreachable:
            raise OSError("unreachable")

        def readall():
            end = None if length is None else offset + length
            data = self.blobs[name][offset:end]
            self.read_sizes.append(len(data))
            return data

        return Mock(readall=readall)

    def upload_blob(self, name, body, overwrite=False, length=None):
        if self.unreachable:
            raise OSError("unreachable")
        assert overwrite is False and length == len(body)
        if name in self.blobs:
            raise FileExistsError(name)
        self.blobs[name] = body
        self.uploads.append(name)


class FakeJobs(setup_fixture.FakeAzure):
    def __init__(self):
        super().__init__()
        self.app["properties"]["managedEnvironmentId"] = setup_fixture.ENV_ID
        self.app["properties"]["template"]["containers"][0]["env"] += [
            {"name": "ZF_SQL_SERVER", "value": "fictional-sql.database.windows.net"},
            {"name": "ZF_SQL_DATABASE", "value": "fixture"},
            {"name": "ZF_BLOB_ACCOUNT_URL", "value": BLOB_URL},
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
            STORAGE: {
                "id": STORAGE,
                "properties": {
                    "publicNetworkAccess": "Disabled",
                    "allowSharedKeyAccess": False,
                    "allowBlobPublicAccess": False,
                },
            },
            STORAGE + "/blobServices/default/containers/staff-results": {
                "properties": {"publicAccess": "None"}
            },
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
        self.container = FakeContainer()
        self.mutate_blob = None
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
        if "/jobs/job-staff-" in resource:
            if "/executions/" in resource:
                self.polls += 1
                if self.polls > 1 and not self.published and self.requests:
                    self.publish()
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

    def publish(self):
        request = self.requests[-1]
        if self.fail_at == "logs":
            self.container.unreachable = True
            return
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
        BLOB.write_result(self.container, request, result)
        if self.mutate_blob:
            self.mutate_blob(self.container, request)
        self.published = True


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
            kwargs.setdefault("container", self.fake.container)
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
        self.assertFalse(any("tags" in url for _, url, _ in self.fake.writes))
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
                method in {"PUT", "DELETE"} and "/jobs/job-staff-" in url
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
            patch.object(BLOB, "read_result", side_effect=KeyboardInterrupt),
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

    def test_same_vnet_parent_environment_allowed_but_other_vnet_blocks(self):
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

    def test_direct_demo_automatically_discovers_only_its_verified_parent_initializer(self):
        self.fake.app["id"] = setup_fixture.APP_ID.replace("-test-api", "-test-demo-api")
        self.fake.app["name"] = "ca-cutover-test-demo-api"
        result = self.execute()
        self.assertTrue(result["ok"])
        self.assertEqual(self.fake.requests[-1]["payload"]["target"], self.fake.app["id"])
        self.assertEqual(self.fake.requests[-1]["payload"]["blob"], BLOB_URL)

    def run_with_clock(self):
        clock = [0]
        with (
            patch.object(JOB.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(
                JOB.time, "sleep", side_effect=lambda _: clock.__setitem__(0, clock[0] + 250)
            ),
        ):
            return self.execute()

    def test_blob_corruption_missing_extra_and_unreachable_block_success(self):
        def tamper(container, request):
            name = BLOB.blob_name(request["run"], 0)
            record = json.loads(container.blobs[name])
            record["ct"] = record["ct"][:-4] + "AAAA"
            container.blobs[name] = json.dumps(record).encode()

        def extra(container, request):
            container.blobs[request["run"] + "/page-009.json"] = b"{}"

        def stray(container, request):
            container.blobs[request["run"] + "/other.json"] = b"{}"

        def vanish(container, request):
            container.blobs.clear()

        for mutation in (tamper, extra, stray, vanish):
            with self.subTest(mutation=mutation.__name__):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.fake.mutate_blob = mutation
                with self.assertRaises(JOB.StaffJobError):
                    self.run_with_clock()
                self.assertFalse(self.fake.jobs)
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        self.fake.fail_at = "logs"
        with self.assertRaises(JOB.StaffJobError):
            self.run_with_clock()
        self.assertFalse(self.fake.jobs)

    def test_preflight_refuses_unreachable_or_dirty_prefix_before_any_job(self):
        self.fake.container.unreachable = True
        with self.assertRaisesRegex(JOB.StaffJobError, "no job was created"):
            self.execute()
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.writes)
        self.fake.container.unreachable = False
        self.fake.container.blobs["f" * 32 + "/page-000.json"] = b"{}"
        with (
            patch.object(JOB.uuid, "uuid4", return_value=Mock(hex="f" * 32)),
            self.assertRaisesRegex(JOB.StaffJobError, "not empty"),
        ):
            self.execute()
        self.assertFalse(self.fake.requests)

    def test_failed_job_never_reads_blob_and_image_drift_is_refused(self):
        self.fake.status = "Failed"
        with patch.object(BLOB, "read_result") as read, self.assertRaises(JOB.StaffJobError):
            self.execute()
        read.assert_not_called()
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        original = self.fake.rest

        def drift(method, url, body):
            value = original(method, url, body)
            if method == "GET" and "/jobs/job-staff-" in url and "/executions/" not in url:
                value = copy.deepcopy(value)
                value["properties"]["template"]["containers"][0]["image"] += "x"
            return value

        self.fake.rest = drift
        with self.assertRaises(JOB.StaffJobError):
            self.execute()

    def test_storage_must_be_private_keyless_and_account_url_exact(self):
        for key, value in (
            ("publicNetworkAccess", "Enabled"),
            ("allowSharedKeyAccess", True),
            ("allowBlobPublicAccess", True),
        ):
            with self.subTest(key=key):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.fake.resources[STORAGE]["properties"][key] = value
                with self.assertRaises(JOB.StaffJobError):
                    self.execute()
                self.assertFalse(self.fake.requests)
        for url in ("http://fictionalstaff.blob.core.windows.net", BLOB_URL + ".evil.example"):
            with self.subTest(url=url):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                env = self.fake.app["properties"]["template"]["containers"][0]["env"]
                next(i for i in env if i["name"] == "ZF_BLOB_ACCOUNT_URL")["value"] = url
                with self.assertRaises(JOB.StaffJobError):
                    self.execute()
                self.assertFalse(self.fake.requests)

    def test_secret_person_data_never_in_command_line_logs_or_leftover_body_files(self):
        payload = {
            "wanted": [{"code": "private-code", "userId": setup_fixture.USER}],
            "people": {setup_fixture.USER: {"displayName": PERSON, "userPrincipalName": EMAIL}},
        }
        self.execute("apply", payload)
        self.assertEqual(self.fake.requests[-1]["payload"]["people"], payload["people"])
        self.assert_private()

    def test_oversize_payload_is_refused_before_any_job(self):
        with self.assertRaises(JOB.StaffJobError):
            self.execute(payload={"oversize": "x" * JOB.MAX_INPUT})
        self.assertFalse(self.fake.requests)

    def release(self):
        for event in (self.fake.container.stall_list, self.fake.container.stall_download):
            if event is not None:
                event.set()

    def test_stalled_preflight_list_stops_before_any_job(self):
        self.fake.container.stall_list = threading.Event()
        self.addCleanup(self.release)
        started = time.monotonic()
        with (
            patch.object(BLOB, "PREFLIGHT_BUDGET", 0.2),
            self.assertRaisesRegex(JOB.StaffJobError, "no job was created"),
        ):
            self.execute()
        self.assertLess(time.monotonic() - started, 5)
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.jobs)

    def test_stalled_download_is_unverified_and_job_secret_is_cleaned_up(self):
        self.fake.container.stall_download = threading.Event()
        self.addCleanup(self.release)
        started = time.monotonic()
        with (
            patch.object(BLOB, "READ_BUDGET", 0.2),
            self.assertRaisesRegex(JOB.StaffJobError, "unverified"),
        ):
            self.execute()
        self.assertLess(time.monotonic() - started, 30)
        self.assertFalse(self.fake.jobs)

    def test_stalled_list_during_read_is_unverified_and_cleaned_up(self):
        self.addCleanup(self.release)
        original = self.fake.container.list_blobs
        calls = []

        def list_blobs(name_starts_with="", timeout=None):
            calls.append(1)
            if len(calls) > 1:
                self.fake.container.stall_list = threading.Event()
            return original(name_starts_with, timeout)

        self.fake.container.list_blobs = list_blobs
        with (
            patch.object(BLOB, "READ_BUDGET", 0.2),
            self.assertRaisesRegex(JOB.StaffJobError, "unverified"),
        ):
            self.execute()
        self.assertFalse(self.fake.jobs)

    def test_failing_download_is_unverified_and_cleaned_up(self):
        original = self.fake.container.download_blob

        def failing(name, timeout=None, *, offset=0, length=None):
            raise OSError("reset")

        self.fake.container.download_blob = failing
        with self.assertRaisesRegex(JOB.StaffJobError, "unverified"):
            self.execute()
        self.fake.container.download_blob = original
        self.assertFalse(self.fake.jobs)

    def test_replaced_oversized_download_is_bounded_and_job_secret_is_cleaned_up(self):
        original = self.fake.container.download_blob

        def replaced(name, timeout=None, *, offset=0, length=None):
            self.fake.container.blobs[name] = b"x" * (BLOB.MAX_BLOB + 1024)
            return original(name, timeout, offset=offset, length=length)

        self.fake.container.download_blob = replaced
        with self.assertRaises(JOB.StaffJobError):
            self.execute()
        self.assertEqual(self.fake.container.downloads[0][1:], (0, BLOB.MAX_BLOB + 1))
        self.assertEqual(self.fake.container.read_sizes, [BLOB.MAX_BLOB + 1])
        self.assertEqual(len(self.fake.deleted), 1)
        self.assert_private()

    def test_exhausted_deadline_refuses_without_calling_the_sdk(self):
        self.fake.container.blobs.clear()
        request = {"run": "a" * 32}
        with self.assertRaisesRegex(JOB.StaffJobError, "time budget"):
            BLOB.read_result(self.fake.container, request, deadline=time.monotonic() - 1)
        self.assertEqual(self.fake.container.timeouts, [])

    def test_sdk_calls_carry_explicit_server_timeouts(self):
        self.execute()
        self.assertTrue(self.fake.container.timeouts)
        self.assertTrue(all(isinstance(t, int) and t > 0 for t in self.fake.container.timeouts))

    def test_execute_binds_blob_client_to_the_transport(self):
        with patch.object(JOB, "default_container", return_value=self.fake.container) as make:
            JOB.execute(self.cli, self.fake.app, "candidates", {})
        self.assertIs(make.call_args.args[1], self.cli)


class BlobCodecTests(unittest.TestCase):
    def request(self):
        return {
            "version": 1,
            "run": "a" * 32,
            "operation": "candidates",
            "digest": "d" * 64,
            "image": "b" * 64,
            "key": base64.b64encode(b"k" * 32).decode(),
        }

    def result(self, count):
        return {
            "version": 1,
            "run": "a" * 32,
            "operation": "candidates",
            "ok": True,
            "candidates": [{"n": i, "pad": "x" * 200} for i in range(count)],
        }

    def written(self, count):
        request, container = self.request(), FakeContainer()
        BLOB.write_result(container, request, self.result(count))
        return container, request

    def test_round_trip_pages_a_large_complete_result_without_truncation(self):
        container, request = self.written(1000)
        self.assertGreater(len(container.blobs), 1)
        self.assertTrue(all(len(b) <= BLOB.MAX_BLOB for b in container.blobs.values()))
        self.assertEqual(BLOB.read_result(container, request), self.result(1000))
        self.assertTrue(all(offset == 0 for _, offset, _ in container.downloads))
        self.assertTrue(all(length == BLOB.MAX_BLOB + 1 for _, _, length in container.downloads))

    def test_oversized_intermediate_page_includes_wrapper_in_bound(self):
        with self.assertRaises(JOB.StaffJobError):
            BLOB.split_pages({"candidates": ["x" * (BLOB.PAGE_BYTES - 3), "y"]})

    def test_oversized_initial_head_is_refused_even_when_final_page_fits(self):
        for candidates in ([], ["y"]):
            with self.subTest(candidates=candidates), self.assertRaises(JOB.StaffJobError):
                BLOB.split_pages({"metadata": "x" * BLOB.PAGE_BYTES, "candidates": candidates})

    def test_exact_page_limit_and_near_boundary_multiple_pages(self):
        head = {"metadata": "h" * 100}
        first_overhead = len(BLOB._compact({"head": head, "items": [""]}))
        later_overhead = len(BLOB._compact({"items": [""]}))
        items = [
            "x" * (BLOB.PAGE_BYTES - first_overhead),
            "y" * (BLOB.PAGE_BYTES - later_overhead),
            "z",
        ]
        pages, count, size = BLOB.split_pages({**head, "candidates": items})
        sizes = [len(BLOB._compact(page)) for page in pages]
        self.assertEqual(sizes[:2], [BLOB.PAGE_BYTES, BLOB.PAGE_BYTES])
        self.assertTrue(all(length <= BLOB.PAGE_BYTES for length in sizes))
        self.assertEqual(pages[0]["head"], head)
        self.assertEqual([item for page in pages for item in page["items"]], items)
        self.assertEqual(count, len(items))
        self.assertEqual(size, sum(sizes))

    def test_one_byte_over_complete_item_wrapper_is_refused_before_upload(self):
        container = FakeContainer()
        overhead = len(BLOB._compact({"items": [""]}))
        result = dict(self.result(0), candidates=["x" * (BLOB.PAGE_BYTES - overhead + 1)])
        with self.assertRaises(JOB.StaffJobError):
            BLOB.write_result(container, self.request(), result)
        self.assertFalse(container.uploads)

    def test_escaped_unicode_items_preserve_exact_serialized_byte_totals(self):
        items = ['"\\\n\u00e9' * 1000 for _ in range(20)]
        pages, count, size = BLOB.split_pages({"candidates": items})
        self.assertGreater(len(pages), 1)
        self.assertTrue(all(len(BLOB._compact(page)) <= BLOB.PAGE_BYTES for page in pages))
        self.assertEqual(count, len(items))
        self.assertEqual(size, sum(len(BLOB._compact(page)) for page in pages))
        self.assertEqual([item for page in pages for item in page["items"]], items)

    def test_exact_max_page_count_and_one_more_page_refusal(self):
        overhead = len(BLOB._compact({"items": [""]}))
        item = "x" * (BLOB.PAGE_BYTES - overhead)
        pages, count, _ = BLOB.split_pages({"candidates": [item] * (BLOB.MAX_PAGES - 1)})
        self.assertEqual(len(pages), BLOB.MAX_PAGES)
        self.assertEqual(count, BLOB.MAX_PAGES - 1)
        with self.assertRaisesRegex(JOB.StaffJobError, "bounded page set"):
            BLOB.split_pages({"candidates": [item] * BLOB.MAX_PAGES})

    def test_empty_prefix_reads_none_and_unpageable_results_are_refused(self):
        self.assertIsNone(BLOB.read_result(FakeContainer(), self.request()))
        with self.assertRaisesRegex(JOB.StaffJobError, "bounded page set"):
            BLOB.split_pages(self.result(BLOB.MAX_PAGES * 300))
        with self.assertRaisesRegex(JOB.StaffJobError, "exceeds one page"):
            BLOB.split_pages({"candidates": ["x" * BLOB.PAGE_BYTES]})

    def test_binding_failures_are_refused(self):
        container, request = self.written(300)
        for field, value in (
            ("operation", "apply"),
            ("digest", "e" * 64),
            ("image", "f" * 64),
            ("key", base64.b64encode(b"z" * 32).decode()),
        ):
            with self.subTest(field=field), self.assertRaises(JOB.StaffJobError):
                BLOB.read_result(container, dict(request, **{field: value}))
        other = dict(request, run="c" * 32)
        moved = FakeContainer()
        moved.blobs = {
            n.replace(request["run"], other["run"]): b for n, b in container.blobs.items()
        }
        with self.assertRaises(JOB.StaffJobError):
            BLOB.read_result(moved, other)

    def test_expiry_future_gap_swap_and_overwrite_are_refused(self):
        container, request = self.written(600)
        names = sorted(container.blobs)
        self.assertGreater(len(names), 2)
        now = BLOB.time.time()
        with self.assertRaisesRegex(JOB.StaffJobError, "expired"):
            BLOB.read_result(container, request, now=now + BLOB.TTL + 5)
        with self.assertRaises(JOB.StaffJobError):
            BLOB.read_result(container, request, now=now - 10 * BLOB.SKEW)
        gap = FakeContainer()
        gap.blobs = {n: b for n, b in container.blobs.items() if n != names[1]}
        with self.assertRaisesRegex(JOB.StaffJobError, "incomplete"):
            BLOB.read_result(gap, request)
        swapped = FakeContainer()
        swapped.blobs = dict(container.blobs)
        swapped.blobs[names[0]] = container.blobs[names[1]]
        swapped.blobs[names[1]] = container.blobs[names[0]]
        with self.assertRaises(JOB.StaffJobError):
            BLOB.read_result(swapped, request)
        with self.assertRaises(FileExistsError):
            BLOB.write_result(container, request, self.result(1))

    def test_account_url_grammar_and_import_graph(self):
        self.assertEqual(BLOB.account_url(BLOB_URL + "/"), BLOB_URL)
        for bad in (
            None,
            "http://fictionalstaff.blob.core.windows.net",
            BLOB_URL + "/x",
            BLOB_URL + "@evil.example",
            "https://fictionalstaff.blob.core.windows.net.evil.example",
        ):
            with self.subTest(bad=bad), self.assertRaises(JOB.StaffJobError):
                BLOB.account_url(bad)
        self.assertIs(JOB.StaffJobError, BLOB.StaffJobError)
        self.assertIs(WORKER.write_result, BLOB.write_result)

    def test_worker_publishes_without_overwrite_and_rejects_foreign_account(self):
        request = dict(self.request(), payload={"blob": BLOB_URL})
        container = FakeContainer()
        with patch.dict(os.environ, {"ZF_STAFF_BLOB": BLOB_URL}):
            WORKER.publish_result(request, self.result(5), container)
            self.assertEqual(BLOB.read_result(container, request), self.result(5))
            with self.assertRaises(FileExistsError):
                WORKER.publish_result(request, self.result(5), container)
        with patch.dict(os.environ, {"ZF_STAFF_BLOB": "https://other.blob.core.windows.net"}):
            with self.assertRaises(ValueError):
                WORKER.publish_result(request, self.result(5), FakeContainer())


class SetupAzureTests(unittest.TestCase):
    """Exercise real setup with fake az; existing local regressions run separately."""

    write_roster = setup_fixture.SetupTests.write_roster
    invoke = setup_fixture.SetupTests.invoke
    demo_roster = setup_fixture.SetupTests.demo_roster
    demo_person = staticmethod(setup_fixture.SetupTests.demo_person)
    mixed_secret_inventory = setup_fixture.SetupTests.mixed_secret_inventory
    secret_response = setup_fixture.SetupTests.secret_response

    def setUp(self):
        setup_fixture.SetupTests.setUp(self)
        self.fake = FakeJobs()
        SETUP.subprocess.run.side_effect = self.fake.run
        patch.object(
            JOB, "default_container", side_effect=lambda url, cli: self.fake.container
        ).start()

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
        self.assertEqual(self.invoke("--run-in-azure", "--list-staff"), 1, self.output.getvalue())
        self.assertNotIn("fictional-coordinator", self.output.getvalue())
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)
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
        self.assertEqual(self.invoke("--list-staff"), 1, self.output.getvalue())
        self.assertEqual(len(self.fake.sql_calls), 1)
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)
        self.fake.resources[SOURCE]["properties"]["template"]["containers"][0]["image"] = (
            "old:latest"
        )
        self.assertEqual(self.invoke("--run-in-azure", "--list-staff"), 1)

    def test_readonly_transport_guard_precedes_payload_and_execute(self):
        cli = SETUP.Azure(self.profile)
        for flag in ("--check", "--dry-run", "--list-staff"):
            args = SETUP.parser().parse_args([flag, "--roster", str(self.roster)])
            for operation in ("candidates", "check", "apply"):
                with (
                    self.subTest(flag=flag, operation=operation),
                    patch.object(SETUP, "read_roster", side_effect=AssertionError("payload")),
                    patch.object(SETUP.staff_azure, "execute", side_effect=AssertionError("write")),
                ):
                    with self.assertRaises(SETUP.staff_azure.StaffJobError):
                        SETUP.azure_staff(args, self.fake.app, operation, cli)
        self.assertFalse(self.fake.calls)
        self.assertFalse(self.fake.requests)
        self.assertFalse(self.fake.writes)

    def test_check_explicit_and_failed_local_fallback_make_no_cloud_writes(self):
        for explicit in (True, False):
            for failure in ("code", "timeout"):
                with self.subTest(explicit=explicit, failure=failure):
                    self.fake = FakeJobs()
                    original = self.fake.run

                    def run(command, failure=failure, original=original, **kwargs):
                        if command[0] != "az" and failure == "timeout":
                            self.fake.sql_calls.append(command)
                            raise subprocess.TimeoutExpired(command, 600)
                        return original(command, **kwargs)

                    SETUP.subprocess.run.side_effect = run
                    self.fake.sql_code = 1
                    flags = ["--run-in-azure"] if explicit else []
                    self.assertEqual(self.invoke("--check", *flags), 2, self.output.getvalue())
                    self.assertFalse(self.fake.requests)
                    self.assertFalse(self.fake.writes)
                    self.assertFalse(self.fake.tag_writes)
                    self.assertFalse(self.fake.jobs)
                    self.assertTrue(all("--check" in command for command in self.fake.sql_calls))
                    self.assertIsNone(self.fake.credential_template)
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

    def unreferenced_reuse_candidate(self, *, keyvault=False):
        self.assertEqual(self.invoke("--run-in-azure", "--secret-store", "keyvault"), 0)
        secrets = self.fake.app["properties"]["configuration"]["secrets"]
        candidate = secrets[-1]
        if not keyvault:
            candidate.pop("keyVaultUrl")
            candidate.pop("identity")
            candidate["value"] = setup_fixture.SECRET
        for name in (SETUP.STORE_TAG, "zava-forward-credential-name"):
            self.fake.app["tags"].pop(name, None)
        SETUP.aad_registration(self.fake.auth).pop("clientSecretSettingName", None)
        self.fake.writes.clear()
        self.fake.tag_writes.clear()
        return candidate

    def test_unreferenced_app_candidate_is_rejected_at_actual_azure_reuse_boundary(self):
        for readonly in (False, True):
            with self.subTest(readonly=readonly):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.unreferenced_reuse_candidate()
                before_app, before_reg = copy.deepcopy(self.fake.app), copy.deepcopy(self.fake.reg)
                args = SETUP.parser().parse_args(["--run-in-azure", "--secret-store", "keyvault"])
                cli = SETUP.Azure(self.profile, body_directory=self.profile)
                with self.assertRaisesRegex(SETUP.SetupError, "requires Key Vault"):
                    SETUP.secret_reference(
                        cli, cli, self.fake.app, self.fake.reg, self.fake.auth, args, readonly
                    )
                self.assertEqual(self.fake.app, before_app)
                self.assertEqual(self.fake.reg, before_reg)
                self.assertFalse(self.fake.writes)
                self.assertFalse(self.fake.tag_writes)

    def test_unreferenced_app_candidate_blocks_before_directory_reconciliation(self):
        for lookup in ("configured", "sentinel", "explicit"):
            for mode in ((), ("--check",), ("--dry-run",)):
                with self.subTest(lookup=lookup, mode=mode):
                    self.fake = FakeJobs()
                    SETUP.subprocess.run.side_effect = self.fake.run
                    self.unreferenced_reuse_candidate()
                    self.fake.reg["web"]["redirectUris"] = []
                    if lookup == "sentinel":
                        SETUP.aad_registration(self.fake.auth)["clientId"] = (
                            "systemAssignedIdentity"
                        )
                    flags = ["--client-id", setup_fixture.CLIENT] if lookup == "explicit" else []
                    before_app = copy.deepcopy(self.fake.app)
                    before_reg, before_auth = (
                        copy.deepcopy(self.fake.reg),
                        copy.deepcopy(self.fake.auth),
                    )
                    self.assertEqual(
                        self.invoke("--run-in-azure", "--secret-store", "keyvault", *flags, *mode),
                        1,
                        self.output.getvalue(),
                    )
                    self.assertEqual(self.fake.reg, before_reg)
                    self.assertEqual(self.fake.app, before_app)
                    self.assertEqual(self.fake.auth, before_auth)
                    self.assertFalse(self.fake.writes)
                    self.assertFalse(self.fake.tag_writes)

    def test_azure_reuse_guard_respects_actual_candidate_precedence_and_expiry(self):
        for case in ("unrelated", "expired", "missing-expiry", "preferred-kv", "last-app"):
            with self.subTest(case=case):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                candidate = self.unreferenced_reuse_candidate(keyvault=True)
                other = {"name": candidate["name"] + "-other", "value": setup_fixture.SECRET}
                self.fake.app["properties"]["configuration"]["secrets"].append(other)
                credential = copy.deepcopy(self.fake.reg["passwordCredentials"][0])
                credential["displayName"] = other["name"]
                if case == "unrelated":
                    credential["displayName"] = "unrelated-password"
                elif case == "expired":
                    credential["endDateTime"] = "2000-01-01T00:00:00Z"
                elif case == "missing-expiry":
                    credential.pop("endDateTime")
                elif case == "preferred-kv":
                    SETUP.aad_registration(self.fake.auth)["clientSecretSettingName"] = candidate[
                        "name"
                    ]
                self.fake.reg["passwordCredentials"].append(credential)
                before = copy.deepcopy(self.fake.app["properties"]["configuration"]["secrets"])
                self.fake.reg["web"]["redirectUris"] = []
                count = len(self.fake.reg["passwordCredentials"])
                expected = 1 if case == "last-app" else 0
                self.assertEqual(self.invoke("--run-in-azure"), expected, self.output.getvalue())
                self.assertEqual(self.fake.app["properties"]["configuration"]["secrets"], before)
                self.assertEqual(len(self.fake.reg["passwordCredentials"]), count)
                if case == "last-app":
                    self.assertFalse(self.fake.writes)
                    self.assertFalse(self.fake.tag_writes)
                else:
                    self.assertEqual(self.fake.app["tags"][SETUP.STORE_TAG], "keyvault")

    def test_reuse_preflight_verifies_pending_handoff_without_writes_or_storage(self):
        candidate = self.unreferenced_reuse_candidate(keyvault=True)
        self.fake.app["tags"][SETUP.HANDOFF_TAG] = SETUP.secret_reference_digest(
            self.fake.app["properties"]["configuration"]["secrets"]
        )
        before = copy.deepcopy(self.fake.app)
        args = SETUP.parser().parse_args(["--run-in-azure", "--secret-store", "keyvault"])
        cli = SETUP.Azure(self.profile, body_directory=self.profile)
        with patch.object(CREDENTIAL, "store", side_effect=AssertionError("unexpected storage")):
            result = SETUP.secret_reference(
                cli, cli, self.fake.app, self.fake.reg, self.fake.auth, args, True, reuse_only=True
            )
            self.assertEqual(result[0], candidate["name"])
            self.assertEqual(self.fake.app, before)
            self.assertFalse(self.fake.writes)
            self.assertFalse(self.fake.tag_writes)
            with self.assertRaisesRegex(SETUP.SetupError, "must be read-only"):
                SETUP.secret_reference(
                    cli,
                    cli,
                    self.fake.app,
                    self.fake.reg,
                    self.fake.auth,
                    args,
                    False,
                    reuse_only=True,
                )
        self.assertEqual(self.fake.app, before)

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

    def test_arm_handoff_preserves_mixed_inventory_across_provider_response_shapes(self):
        for shape in ("full", "names-only", "resolved-values", "omitted-kv", "config-names-only"):
            with self.subTest(shape=shape):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                references, listed = self.mixed_secret_inventory()
                if shape == "names-only":
                    listed[:2] = [{"name": row["name"]} for row in references]
                elif shape == "resolved-values":
                    listed[:2] = [
                        {"name": row["name"], "value": "FICTIONAL-RESOLVED-KV"}
                        for row in references
                    ]
                elif shape == "omitted-kv":
                    del listed[:2]
                elif shape == "config-names-only":
                    self.fake.app["properties"]["configuration"]["secrets"][:2] = [
                        {"name": row["name"]} for row in references
                    ]
                token_store = copy.deepcopy(self.fake.auth["login"]["tokenStore"])

                def metadata_only(app):
                    for secret in app["properties"]["configuration"]["secrets"]:
                        secret.pop("value", None)
                    return app

                with self.secret_response({"value": listed}, project=metadata_only):
                    self.assertEqual(self.invoke("--run-in-azure"), 0, self.output.getvalue())
                    count = len(self.fake.reg["passwordCredentials"])
                    with patch.object(CREDENTIAL, "store", side_effect=AssertionError("rotation")):
                        self.assertEqual(self.invoke("--run-in-azure"), 0, self.output.getvalue())
                    self.assertEqual(len(self.fake.reg["passwordCredentials"]), count)
                patches = [
                    body
                    for method, url, body in self.fake.writes
                    if method == "PATCH"
                    and url == setup_fixture.ARM_APP
                    and "configuration" in body.get("properties", {})
                ]
                self.assertEqual(len(patches), 1)
                payload = patches[0]["properties"]["configuration"]["secrets"]
                for reference in references:
                    self.assertIn(reference, payload)
                self.assertIn({"name": "preserved", "value": "preserved-private-value"}, payload)
                self.assertIn({"name": "empty", "value": ""}, payload)
                self.assertEqual(len(payload), 5)
                self.assertEqual(
                    patches[0]["tags"][SETUP.HANDOFF_TAG], SETUP.secret_reference_digest(payload)
                )
                self.assertNotIn(SETUP.HANDOFF_TAG, self.fake.app["tags"])
                self.assertEqual(self.fake.auth["login"]["tokenStore"], token_store)
                self.assertFalse(
                    any(
                        command[:3] == ["az", "keyvault", "secret"]
                        for command, _ in self.fake.calls
                    )
                )
                for private in (
                    "FICTIONAL-RESOLVED-KV",
                    "preserved-private-value",
                    setup_fixture.SECRET,
                ):
                    self.assertNotIn(private, self.output.getvalue())

    def test_arm_handoff_corruption_blocks_auth_and_rerun_without_another_credential(self):
        for corruption in ("missing-name", "keyVaultUrl", "identity", "transport"):
            with self.subTest(corruption=corruption):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                _, listed = self.mixed_secret_inventory()
                original = self.fake.rest
                transport_failed = []

                def corrupt(
                    method,
                    url,
                    body,
                    *,
                    listed=listed,
                    original=original,
                    corruption=corruption,
                    transport_failed=transport_failed,
                ):
                    if "/listSecrets?" in url:
                        return copy.deepcopy({"value": listed})
                    result = original(method, url, body)
                    if (
                        url == setup_fixture.ARM_APP
                        and method == "PATCH"
                        and "configuration" in body.get("properties", {})
                    ):
                        secrets = self.fake.app["properties"]["configuration"]["secrets"]
                        if corruption == "missing-name":
                            del secrets[0]
                        elif corruption != "transport":
                            secrets[0][corruption] = "FICTIONAL-WRONG-REFERENCE"
                    if (
                        url == setup_fixture.ARM_APP
                        and method == "GET"
                        and corruption == "transport"
                        and not transport_failed
                        and len(self.fake.app["properties"]["configuration"]["secrets"]) == 5
                    ):
                        transport_failed.append(True)
                        raise SETUP.AzureError("network")
                    return result

                auth_before = copy.deepcopy(self.fake.auth)
                with patch.object(self.fake, "rest", side_effect=corrupt):
                    self.assertEqual(self.invoke("--run-in-azure"), 1)
                self.assertEqual(self.fake.auth, auth_before)
                self.assertIn(SETUP.HANDOFF_TAG, self.fake.app["tags"])
                with patch.object(CREDENTIAL, "store", side_effect=AssertionError("rotation")):
                    if corruption == "transport":
                        self.assertEqual(self.invoke("--run-in-azure"), 0, self.output.getvalue())
                        self.assertNotIn(SETUP.HANDOFF_TAG, self.fake.app["tags"])
                    else:
                        self.assertEqual(self.invoke("--run-in-azure", "--check"), 1)
                        self.assertEqual(self.invoke("--run-in-azure"), 1)
                        self.assertEqual(self.fake.auth, auth_before)
                        self.assertFalse(
                            any(url == setup_fixture.AUTH_URL for _, url, _ in self.fake.writes)
                        )
                self.assertEqual(len(self.fake.reg["passwordCredentials"]), 1)

    def test_arm_inventory_rejection_precedes_password_and_vault_deployment(self):
        for shape in ("missing-app", "conflicting-kv", "duplicate"):
            with self.subTest(shape=shape):
                self.fake = FakeJobs()
                SETUP.subprocess.run.side_effect = self.fake.run
                _, listed = self.mixed_secret_inventory()
                if shape == "missing-app":
                    del listed[2]
                elif shape == "conflicting-kv":
                    listed[0]["identity"] = "different-identity"
                else:
                    listed.append(copy.deepcopy(listed[-1]))
                auth_before = copy.deepcopy(self.fake.auth)
                with (
                    self.secret_response({"value": listed}),
                    patch.object(CREDENTIAL, "store", side_effect=AssertionError("unsafe write")),
                ):
                    self.assertEqual(self.invoke("--run-in-azure"), 1)
                self.assertFalse(self.fake.reg["passwordCredentials"])
                self.assertEqual(self.fake.auth, auth_before)
                self.assertIsNone(self.fake.credential_template)

    def test_arm_generated_and_legacy_kv_reuse_retains_upstream_expiry_boundaries(self):
        now = datetime(2030, 1, 1, tzinfo=UTC)
        for legacy in (False, True):
            for expiry in (
                None,
                "2029-12-31T23:59:59Z",
                "2030-01-01T00:00:00Z",
                "2030-01-01T00:00:01+00:00",
            ):
                with self.subTest(legacy=legacy, expiry=expiry):
                    self.fake = FakeJobs()
                    SETUP.subprocess.run.side_effect = self.fake.run
                    self.assertEqual(self.invoke("--run-in-azure"), 0)
                    old = self.fake.reg["passwordCredentials"][0]
                    if legacy:
                        old["displayName"] = "legacy-browser-secret"
                        self.fake.app["properties"]["configuration"]["secrets"][-1]["name"] = old[
                            "displayName"
                        ]
                        SETUP.aad_registration(self.fake.auth)["clientSecretSettingName"] = old[
                            "displayName"
                        ]
                        self.fake.app["tags"]["zava-forward-credential-name"] = old["displayName"]
                    old["endDateTime"] = expiry
                    before = copy.deepcopy(old)
                    reusable = expiry == "2030-01-01T00:00:01+00:00"
                    with patch.object(SETUP, "datetime", wraps=datetime) as clock:
                        clock.now.return_value = now
                        for flag in ("--check", "--dry-run"):
                            writes = copy.deepcopy(self.fake.writes)
                            tags = copy.deepcopy(self.fake.tag_writes)
                            requests = copy.deepcopy(self.fake.requests)
                            self.assertEqual(self.invoke("--run-in-azure", flag), 2)
                            self.assertEqual(len(self.fake.reg["passwordCredentials"]), 1)
                            self.assertEqual(self.fake.reg["passwordCredentials"][0], before)
                            self.assertEqual(self.fake.writes, writes)
                            self.assertEqual(self.fake.tag_writes, tags)
                            self.assertEqual(self.fake.requests, requests)
                        self.assertEqual(self.invoke("--run-in-azure"), 0, self.output.getvalue())
                    self.assertEqual(self.fake.reg["passwordCredentials"][0], before)
                    self.assertEqual(
                        len(self.fake.reg["passwordCredentials"]), 1 if reusable else 2
                    )
                    self.assertNotIn(SETUP.HANDOFF_TAG, self.fake.app["tags"])


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
                "blob": BLOB_URL,
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
            "ZF_STAFF_BLOB": BLOB_URL,
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
            "staff_blob.py",
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


class ProfileCredentialTests(unittest.TestCase):
    URL = "https://zavastorage.blob.core.windows.net"

    def cli(self, stdout, code=0):
        self.profile = Path(tempfile.mkdtemp()) / "fallback-profile"
        self.addCleanup(lambda: __import__("shutil").rmtree(self.profile.parent, True))
        run = patch.object(
            SETUP.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], code, stdout, "AADSTS tok-secret"),
        )
        self.run = run.start()
        self.addCleanup(run.stop)
        return SETUP.Azure(self.profile)

    def token_json(self, **extra):
        return json.dumps(
            {"accessToken": "tok-secret", "expires_on": int(time.time()) + 3600, **extra}
        )

    def test_real_client_uses_selected_fallback_profile_not_ambient_chain(self):
        cli = self.cli(self.token_json())
        with patch("azure.identity.DefaultAzureCredential", side_effect=AssertionError("ambient")):
            client = JOB.default_container(self.URL, cli)
        self.assertIsInstance(client.credential, JOB.ProfileCredential)
        args, kwargs = next(c for c in self.run.call_args_list if "get-access-token" in c.args[0])
        self.assertEqual(
            args[0][:5], ["az", "account", "get-access-token", "--resource", JOB.STORAGE_RESOURCE]
        )
        self.assertEqual(kwargs["env"]["AZURE_CONFIG_DIR"], str(self.profile))
        token = client.credential.get_token(JOB.STORAGE_RESOURCE + ".default")
        self.assertEqual(token.token, "tok-secret")
        self.assertEqual(self.run.call_count, 1)

    def test_client_has_explicit_socket_and_retry_limits(self):
        cli = self.cli(self.token_json())
        with patch("azure.storage.blob.ContainerClient") as client:
            JOB.default_container(self.URL, cli)
        limits = client.call_args.kwargs
        self.assertEqual(
            (limits["connection_timeout"], limits["read_timeout"], limits["retry_total"]),
            (5, 15, 2),
        )

    def test_token_failures_fail_closed_without_leaking_detail(self):
        for stdout, code in (
            ("", 1),
            ("not json", 0),
            (json.dumps({"accessToken": "", "expires_on": int(time.time()) + 99}), 0),
            (json.dumps({"accessToken": "tok-secret", "expires_on": 1}), 0),
            (json.dumps({"accessToken": "tok-secret", "expiresOn": "garbage"}), 0),
            (json.dumps({"accessToken": "tok-secret"}), 0),
        ):
            with self.subTest(stdout=stdout[:20], code=code):
                cli = self.cli(stdout, code)
                with self.assertRaises(JOB.StaffJobError) as raised:
                    JOB.ProfileCredential(cli).get_token(JOB.STORAGE_RESOURCE + ".default")
                self.assertNotIn("tok-secret", str(raised.exception))
                self.assertNotIn("AADSTS", str(raised.exception))
                self.assertIsNone(raised.exception.__cause__)

    def test_naive_local_expires_on_and_unexpected_scope(self):
        later = datetime.now() + timedelta(hours=1)
        cli = self.cli(json.dumps({"accessToken": "tok-secret", "expiresOn": later.isoformat()}))
        credential = JOB.ProfileCredential(cli)
        self.assertAlmostEqual(
            credential.get_token(JOB.STORAGE_RESOURCE + ".default").expires_on,
            later.timestamp(),
            delta=2,
        )
        with self.assertRaises(JOB.StaffJobError):
            credential.get_token("https://management.azure.com/.default")

    def test_priming_is_bounded_and_restores_the_shared_deadline(self):
        cli = self.cli(self.token_json())
        cli.deadline = None
        JOB.default_container(self.URL, cli)
        self.assertIsNone(cli.deadline)
        token_call = next(c for c in self.run.call_args_list if "get-access-token" in c.args[0])
        timeout = token_call.kwargs["timeout"]
        self.assertLessEqual(timeout, BLOB.PREFLIGHT_BUDGET)


class StorageContractTests(unittest.TestCase):
    def test_staff_results_container_is_last_private_and_expires(self):
        text = (ROOT / "infra/modules/storage.bicep").read_text()
        self.assertIn("'ledger-digests', 'staff-results']", text)
        self.assertIn("parent: blobContainers[4]", text)
        self.assertIn("parent: blobContainers[5]", text)
        self.assertIn("publicAccess: 'None'", text)
        lifecycle = text[text.index("staffResultsLifecycle") :]
        self.assertIn("prefixMatch: ['staff-results/']", lifecycle)
        self.assertIn("version: { delete:", lifecycle)
        self.assertIn("allowSharedKeyAccess: false", text)

    def test_retired_tag_relay_is_absent_from_scripts_and_bicep(self):
        import re

        pattern = re.compile(
            "tags_url|result_tags|ZFSTAFF|ZF_STAFF_" + "RELAY|TAG_VERSION|Microsoft.Resources/tags"
        )
        files = [*(ROOT / "infra/scripts").glob("staff*"), *ROOT.glob("infra/**/*.bicep")]
        self.assertTrue(files)
        for file in files:
            self.assertIsNone(pattern.search(file.read_text()), str(file))


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
        for excluded in (
            "scripts/setup-entra.py",
            "scripts/.env",
            "scripts/__pycache__/staff_roster.cpython-312.pyc",
            "entra/private-profile.json",
            "private-data.json",
        ):
            self.assertTrue(ignored(excluded), excluded)


if __name__ == "__main__":
    unittest.main()
