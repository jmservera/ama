"""Issue #144 container hosting completeness verification suite.

Covers all four Issue #144 acceptance areas without fabricating live Azure claims:
1. Real, versioned worker and job images wired through Dockerfiles, src-deploy.yml,
   pipeline.py / deploy.py digest checks (including rank-publish), and compiled Bicep.
2. Container hardening enforced in the deployed app specifications (ZF_CONTAINER_HARDENING,
   PYTHONDONTWRITEBYTECODE, EmptyDir scratch mounts) and inside workload startup entrypoints
   (non-root 10001:10001, NoNewPrivs=1, zero active capabilities, immutable / and /app).
3. Declared 60,000-home scale fixture load test recorded and bounded honestly without
   claiming production scale or Azure SLA validation.
4. Single-replica / single-revision contracts, separate-process API SIGKILL restart with
   intact /api/audit-check SHA-256 chain persistence, and worker crash redelivery.
"""

from __future__ import annotations

import contextlib
import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
for _extra_path in (
    ROOT / "infra/tests",
    ROOT / "src/core/src",
    ROOT / "src/agents/src",
    ROOT / "src/api/src",
    ROOT / "src/orchestrator/src",
    ROOT / "src/importer/src",
    ROOT / "src/core/tests",
    ROOT / "src/agents/tests",
    ROOT / "src/api/tests",
):
    _text = str(_extra_path)
    if _text not in sys.path:
        sys.path.append(_text)
importlib.invalidate_caches()


def _load_infra_script(name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "infra/scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


deploy = _load_infra_script("deploy")
pipeline = _load_infra_script("pipeline")
scale_load = importlib.import_module("scale_load")
scale_restart = importlib.import_module("test_scale_fixture_load_and_restart")
_bicep_policy = importlib.import_module("test_bicep_policy")
compile_bicep = _bicep_policy.compile_bicep
module_template = _bicep_policy.module_template
render_api_container = _bicep_policy.render_api_container
resources = _bicep_policy.resources
_test_dispatch = importlib.import_module("test_dispatch")
Sink = _test_dispatch.Sink
good_text = _test_dispatch.good_text
limits = _test_dispatch.limits
message = _test_dispatch.message
returned = _test_dispatch.returned
_agents_dispatch = importlib.import_module("zava_forward.agents.dispatch")
AgentWorker = _agents_dispatch.AgentWorker
InMemoryQueue = _agents_dispatch.InMemoryQueue
serve = importlib.import_module("zava_forward.agents.worker").serve
_hardening = importlib.import_module("zava_forward.core.container_hardening")
EXPECTED_GID = _hardening.EXPECTED_GID
EXPECTED_UID = _hardening.EXPECTED_UID
ContainerHardeningError = _hardening.ContainerHardeningError
enforce_container_hardening = _hardening.enforce_container_hardening
enforce_from_env = _hardening.enforce_from_env
FORBIDDEN_ENV_PREFIXES = importlib.import_module(
    "zava_forward.core.resident_showcase"
).FORBIDDEN_ENV_PREFIXES

SAMPLE_DIGEST = "sha256:" + ("a" * 64)
ALT_DIGEST = "sha256:" + ("b" * 64)
CLEAN_PROC_STATUS = (
    "Name:\tpython3\n"
    "Uid:\t10001\t10001\t10001\t10001\n"
    "Gid:\t10001\t10001\t10001\t10001\n"
    "NoNewPrivs:\t1\n"
    "CapInh:\t0000000000000000\n"
    "CapPrm:\t0000000000000000\n"
    "CapEff:\t0000000000000000\n"
    "CapBnd:\t0000000000000000\n"
    "CapAmb:\t0000000000000000\n"
)


def _child_env(**overrides: str) -> dict[str, str]:
    env = dict(os.environ)
    env.pop("ZF_CONTAINER_HARDENING", None)
    python_paths = [
        str(ROOT / "src/core/src"),
        str(ROOT / "src/agents/src"),
        str(ROOT / "src/api/src"),
        str(ROOT / "src/orchestrator/src"),
        str(ROOT / "src/importer/src"),
    ]
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = ":".join(python_paths + ([existing] if existing else []))
    env.update(overrides)
    return env


@lru_cache(maxsize=8)
def _compiled(template_rel: str) -> dict[str, Any]:
    return compile_bicep(template_rel)


def _requires_az_bicep() -> Any:
    return unittest.skipUnless(
        shutil.which("az") or os.environ.get("REQUIRE_AZ_BICEP") == "1",
        "Azure CLI with Bicep is needed to compile templates",
    )


class WorkerAndJobPipelineTests(unittest.TestCase):
    """Criterion 1: Worker and job images are real, versioned and deployed through the pipeline."""

    def test_all_four_service_dockerfiles_are_pinned_non_root_and_real(self) -> None:
        expected_cmds = {
            "api": 'CMD ["python", "-m", "zava_forward.api"]',
            "agents": 'CMD ["python", "-m", "zava_forward.agents"]',
            "orchestrator": 'CMD ["python", "-m", "zava_forward.orchestrator"]',
            "importer": 'CMD ["python", "-m", "zava_forward.importer"]',
        }
        base_digests: set[str] = set()
        for service, cmd_line in expected_cmds.items():
            dockerfile = (ROOT / "src" / service / "Dockerfile").read_text(encoding="utf-8")
            with self.subTest(service=service):
                self.assertIn("FROM python@sha256:", dockerfile)
                from_lines = [
                    line.split(" AS ", 1)[0].strip()
                    for line in dockerfile.splitlines()
                    if line.startswith("FROM ")
                ]
                self.assertGreaterEqual(len(from_lines), 2)
                base_digests.update(from_lines)
                self.assertIn("PYTHONDONTWRITEBYTECODE=1", dockerfile)
                self.assertIn("USER 10001:10001", dockerfile)
                self.assertIn("/app /data /state", dockerfile)
                self.assertIn(cmd_line, dockerfile)
                self.assertNotIn("quickstart", dockerfile.lower())
        self.assertEqual(len(base_digests), 1, "All four Dockerfiles must share one pinned base")

    def test_orchestrator_supports_bare_version_check_and_bounded_run_mode(self) -> None:
        bare = subprocess.run(
            [sys.executable, "-m", "zava_forward.orchestrator"],
            env=_child_env(),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(bare.returncode, 0, bare.stderr)
        self.assertIn("zava-forward-orchestrator", bare.stdout)

        missing_cfg = subprocess.run(
            [sys.executable, "-m", "zava_forward.orchestrator", "run"],
            env=_child_env(QUEUE_ENDPOINT="", TASK_QUEUE="", API_BASE_URL=""),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(missing_cfg.returncode, 2)
        self.assertIn("TASK_QUEUE", missing_cfg.stderr)

        standby = subprocess.run(
            [sys.executable, "-m", "zava_forward.orchestrator", "run"],
            env=_child_env(
                QUEUE_ENDPOINT="https://stforwarddev.queue.core.windows.net",
                TASK_QUEUE="agent-tasks",
                API_BASE_URL="https://ca-forward-dev-api.internal.example",
            ),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(standby.returncode, 0, standby.stderr)
        payload = json.loads(standby.stdout.strip())
        self.assertEqual(payload["job"], "orchestrator")
        self.assertEqual(payload["mode"], "standby")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["taskQueue"], "agent-tasks")

    def test_src_deploy_workflow_builds_scans_and_promotes_all_four_immutable_digests(self) -> None:
        workflow = (ROOT / ".github/workflows/src-deploy.yml").read_text(encoding="utf-8")
        for service in ("api", "agents", "orchestrator", "importer"):
            self.assertIn(service, workflow)
        self.assertIn("release-image-${{ matrix.project }}", workflow)
        self.assertIn("release-digest-${{ matrix.project }}", workflow)
        self.assertIn("python3 infra/scripts/pipeline.py publish --project", workflow)
        self.assertIn("python3 infra/scripts/pipeline.py deploy --environment", workflow)
        self.assertIn("pattern: release-digest-*", workflow)

    def test_pipeline_and_deploy_enforce_immutable_digests_across_all_orchestrator_jobs(
        self,
    ) -> None:
        sha = "c" * 40
        server = "acr.azurecr.io"
        with tempfile.TemporaryDirectory(prefix="zf-pipe-144-") as tmp:
            digest_dir = Path(tmp)
            for project in ("api", "agents", "orchestrator", "importer"):
                (digest_dir / f"{project}.json").write_text(
                    json.dumps(
                        {
                            "project": project,
                            "image": f"{server}/zava-forward-{project}@{SAMPLE_DIGEST}",
                            "source_sha": sha,
                            "tag": f"sha-{sha}",
                        }
                    ),
                    encoding="utf-8",
                )
            pulled: list[tuple[str, ...]] = []
            orig_run = pipeline.run
            orig_sha = pipeline.source_sha
            orig_tag = pipeline.release_tag
            try:
                pipeline.run = lambda *args, **_: pulled.append(args) or ""
                pipeline.source_sha = lambda: sha
                pipeline.release_tag = lambda: f"sha-{sha}"
                resolved = pipeline.release_images(digest_dir, server)
                self.assertEqual(
                    set(resolved),
                    {"apiImage", "agentImage", "orchestratorImage", "importImage"},
                )
                self.assertEqual(len(pulled), 4)

                # Mutable tag (non-digest) must fail closed.
                (digest_dir / "agents.json").write_text(
                    json.dumps(
                        {
                            "project": "agents",
                            "image": f"{server}/zava-forward-agents:latest",
                            "source_sha": sha,
                            "tag": f"sha-{sha}",
                        }
                    ),
                    encoding="utf-8",
                )
                with self.assertRaises(pipeline.PipelineError):
                    pipeline.release_images(digest_dir, server)
            finally:
                pipeline.run = orig_run
                pipeline.source_sha = orig_sha
                pipeline.release_tag = orig_tag

        # PR planning what-if must reject drifted rank-publish orchestratorImage.
        existing_apps = [
            {
                "name": "ca-forward-dev-api",
                "tags": {},
                "properties": {
                    "template": {
                        "containers": [{"image": f"{server}/zava-forward-api@{SAMPLE_DIGEST}"}]
                    }
                },
            },
            {
                "name": "ca-forward-dev-agents",
                "tags": {},
                "properties": {
                    "template": {
                        "containers": [{"image": f"{server}/zava-forward-agents@{SAMPLE_DIGEST}"}]
                    }
                },
            },
        ]
        drifted_jobs = [
            {
                "name": "job-forward-dev-orchestrator",
                "properties": {
                    "template": {
                        "containers": [
                            {"image": f"{server}/zava-forward-orchestrator@{SAMPLE_DIGEST}"}
                        ]
                    }
                },
            },
            {
                "name": "job-forward-dev-import",
                "properties": {
                    "template": {
                        "containers": [{"image": f"{server}/zava-forward-importer@{SAMPLE_DIGEST}"}]
                    }
                },
            },
            {
                "name": "job-forward-dev-auth-renewal",
                "properties": {
                    "template": {
                        "containers": [
                            {"image": f"{server}/zava-forward-orchestrator@{SAMPLE_DIGEST}"}
                        ]
                    }
                },
            },
            {
                "name": "job-forward-dev-ledger-verify",
                "properties": {
                    "template": {
                        "containers": [
                            {"image": f"{server}/zava-forward-orchestrator@{SAMPLE_DIGEST}"}
                        ]
                    }
                },
            },
            {
                "name": "job-forward-dev-rank-publish",
                "properties": {
                    "template": {
                        "containers": [
                            {"image": f"{server}/zava-forward-orchestrator@{ALT_DIGEST}"}
                        ]
                    }
                },
            },
        ]
        orig_params = pipeline.parameters
        orig_az = pipeline.az
        orig_sha = pipeline.source_sha
        orig_req = pipeline.required
        try:
            pipeline.parameters = lambda *_: {"parameters": {}}
            pipeline.az = lambda *args: (
                existing_apps if args[:2] == ("containerapp", "list") else drifted_jobs
            )
            pipeline.source_sha = lambda: sha
            pipeline.required = lambda *_: "00000000-0000-0000-0000-000000000001"
            with (
                tempfile.TemporaryDirectory() as out_tmp,
                self.assertRaisesRegex(pipeline.PipelineError, "conflicting orchestrator images"),
            ):
                pipeline.deployment(Path(out_tmp), "dev", Path(out_tmp) / "summary.json", None)
        finally:
            pipeline.parameters = orig_params
            pipeline.az = orig_az
            pipeline.source_sha = orig_sha
            pipeline.required = orig_req

        # deploy.resolve_image must also detect conflict on job-forward-dev-rank-publish.
        orig_deploy_az = deploy.az_json
        try:
            deploy.az_json = lambda *_: [drifted_jobs[0], drifted_jobs[-1]]
            with self.assertRaisesRegex(deploy.DeploymentError, "conflicting real images"):
                deploy.resolve_image("ama", "forward-dev", server)
        finally:
            deploy.az_json = orig_deploy_az

    @_requires_az_bicep()
    def test_compiled_bicep_wires_real_versioned_parameters_to_all_workers_and_jobs(self) -> None:
        main = _compiled("main.bicep")
        apps = module_template(main, "containerapps")
        for param_name in ("apiImage", "agentImage", "orchestratorImage", "importImage"):
            self.assertIn(param_name, apps["parameters"])
            self.assertEqual(apps["parameters"][param_name]["type"], "string")

        expected = {
            "api": ("[parameters('apiImage')]", None, None),
            "agents": (
                "[parameters('agentImage')]",
                ["python", "-m", "zava_forward.agents"],
                ["serve"],
            ),
            "orchestrator": (
                "[parameters('orchestratorImage')]",
                ["python", "-m", "zava_forward.orchestrator"],
                ["run"],
            ),
            "auth-renewal": (
                "[parameters('orchestratorImage')]",
                ["python", "-m", "zava_forward.orchestrator.token_store"],
                None,
            ),
            "ledger-verify": (
                "[parameters('orchestratorImage')]",
                ["python", "-m", "zava_forward.orchestrator.digest_blob", "--publish"],
                None,
            ),
            "ranking-publish": (
                "[parameters('orchestratorImage')]",
                ["python", "-m", "zava_forward.orchestrator.ranking_publish"],
                None,
            ),
            "import": ("[parameters('importImage')]", None, None),
        }
        seen: set[str] = set()
        for res in resources(apps):
            if res["type"] not in ("Microsoft.App/containerApps", "Microsoft.App/jobs"):
                continue
            container = res["properties"]["template"]["containers"][0]
            cname = container["name"]
            seen.add(cname)
            self.assertIn(cname, expected)
            exp_image, exp_cmd, exp_args = expected[cname]
            self.assertEqual(container["image"], exp_image)
            self.assertNotIn("quickstart", str(container["image"]).lower())
            if exp_cmd is not None:
                self.assertEqual(container.get("command"), exp_cmd)
            if exp_args is not None:
                self.assertEqual(container.get("args"), exp_args)
        self.assertEqual(seen, set(expected))


class DeployedContainerHardeningTests(unittest.TestCase):
    """Criterion 2: Container hardening is enforced in the deployed app, not only in CI."""

    @_requires_az_bicep()
    def test_compiled_bicep_enforces_runtime_hardening_and_scratch_mounts_on_all_workloads(
        self,
    ) -> None:
        main = _compiled("main.bicep")
        for sim_flag in (False, True):
            rendered_api = render_api_container(main, enablePublicSimulationLane=sim_flag)
            api_container = rendered_api["containers"][0]
            api_env = {item["name"]: item["value"] for item in api_container["env"]}
            self.assertEqual(api_env.get("ZF_CONTAINER_HARDENING"), "enforced")
            self.assertEqual(api_env.get("PYTHONDONTWRITEBYTECODE"), "1")
            self.assertEqual(api_env.get("TMPDIR"), "/tmp")
            self.assertEqual(api_env.get("ZF_STATE"), "/state")
            mounts = {m["volumeName"]: m["mountPath"] for m in api_container["volumeMounts"]}
            self.assertEqual(mounts, {"tmp": "/tmp", "state": "/state"})
            vols = {v["name"]: v["storageType"] for v in rendered_api["volumes"]}
            self.assertEqual(vols, {"tmp": "EmptyDir", "state": "EmptyDir"})
            if sim_flag:
                recipe = api_container["command"][2]
                self.assertLess(
                    recipe.index("enforce_from_env()"),
                    recipe.index("/state/public-simulation"),
                )

        apps = module_template(main, "containerapps")
        variables = apps.get("variables", {})
        hardening_vars = {item["name"]: item["value"] for item in variables.get("hardeningEnv", [])}
        self.assertEqual(
            hardening_vars,
            {
                "ZF_CONTAINER_HARDENING": "enforced",
                "PYTHONDONTWRITEBYTECODE": "1",
                "TMPDIR": "/tmp",
                "ZF_STATE": "/state",
            },
        )
        for res in resources(apps):
            if res["type"] not in ("Microsoft.App/containerApps", "Microsoft.App/jobs"):
                continue
            template = res["properties"]["template"]
            container = template["containers"][0]
            with self.subTest(container=container["name"]):
                self.assertEqual(
                    container.get("volumeMounts"), "[variables('scratchVolumeMounts')]"
                )
                self.assertEqual(template.get("volumes"), "[variables('scratchVolumes')]")
                env_expr = str(container.get("env"))
                self.assertTrue(
                    "commonEnv" in env_expr or "hardeningEnv" in env_expr,
                    f"{container['name']} must inherit hardeningEnv",
                )

        resident = _compiled("resident-demo.bicep")
        res_app = next(r for r in resources(resident) if r["type"] == "Microsoft.App/containerApps")
        res_template = res_app["properties"]["template"]
        res_container = res_template["containers"][0]
        res_env = {item["name"]: item.get("value", "") for item in res_container["env"]}
        self.assertEqual(res_env.get("ZF_CONTAINER_HARDENING"), "enforced")
        self.assertEqual(res_env.get("PYTHONDONTWRITEBYTECODE"), "1")
        self.assertEqual(res_env.get("TMPDIR"), "/tmp")
        for env_name in res_env:
            self.assertFalse(
                env_name.startswith(FORBIDDEN_ENV_PREFIXES),
                f"resident-demo env {env_name} violates FORBIDDEN_ENV_PREFIXES",
            )
        self.assertEqual(
            res_container["volumeMounts"], [{"volumeName": "tmp", "mountPath": "/tmp"}]
        )
        self.assertEqual(res_template["volumes"], [{"name": "tmp", "storageType": "EmptyDir"}])

        for job_template_name in ("live-receiver-job.bicep", "live-simulator-job.bicep"):
            compiled_job = _compiled(job_template_name)
            job_res = next(r for r in resources(compiled_job) if r["type"] == "Microsoft.App/jobs")
            j_template = job_res["properties"]["template"]
            j_container = j_template["containers"][0]
            j_env = {item["name"]: item.get("value", "") for item in j_container["env"]}
            with self.subTest(template=job_template_name):
                self.assertEqual(j_env.get("ZF_CONTAINER_HARDENING"), "enforced")
                self.assertEqual(j_env.get("PYTHONDONTWRITEBYTECODE"), "1")
                self.assertEqual(j_env.get("TMPDIR"), "/tmp")
                self.assertEqual(j_env.get("ZF_STATE"), "/state")
                mount_map = {m["volumeName"]: m["mountPath"] for m in j_container["volumeMounts"]}
                self.assertEqual(
                    mount_map, {"device-certs": "/certs", "tmp": "/tmp", "state": "/state"}
                )
                vol_map = {v["name"]: v for v in j_template["volumes"]}
                self.assertEqual(vol_map["device-certs"].get("mountOptions"), "ro")
                self.assertEqual(vol_map["tmp"].get("storageType"), "EmptyDir")
                self.assertEqual(vol_map["state"].get("storageType"), "EmptyDir")

    def test_runtime_guard_accepts_hardened_posture_and_rejects_every_violation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="zf-hardening-") as tmp:
            base = Path(tmp)
            ro_root = base / "ro_root"
            ro_app = base / "ro_app"
            rw_tmp = base / "rw_tmp"
            rw_state = base / "rw_state"
            unwritable_scratch = base / "ro_scratch"
            for directory in (ro_root, ro_app, rw_tmp, rw_state, unwritable_scratch):
                directory.mkdir()
            ro_root.chmod(0o555)
            ro_app.chmod(0o555)
            rw_tmp.chmod(0o700)
            rw_state.chmod(0o700)
            unwritable_scratch.chmod(0o555)
            try:
                umask_calls: list[int] = []
                prctl_calls: list[int] = []
                common_ids = {
                    "uid_getter": lambda: EXPECTED_UID,
                    "euid_getter": lambda: EXPECTED_UID,
                    "gid_getter": lambda: EXPECTED_GID,
                    "egid_getter": lambda: EXPECTED_GID,
                    "dont_write_bytecode": True,
                    "platform": "linux",
                }
                report = enforce_container_hardening(
                    immutable_paths=(ro_root, ro_app),
                    writable_paths=(rw_tmp, rw_state),
                    proc_status_text=CLEAN_PROC_STATUS,
                    prctl_fn=lambda: (prctl_calls.append(1), 0)[1],
                    umask_fn=lambda mask: (umask_calls.append(mask), 0o022)[1],
                    **common_ids,  # type: ignore[arg-type]
                )
                self.assertTrue(report.enforced)
                self.assertEqual((report.uid, report.gid), (10001, 10001))
                self.assertEqual(report.no_new_privs, 1)
                self.assertEqual(umask_calls, [0o077])
                self.assertEqual(prctl_calls, [1])

                # Violation 1: root / wrong UID or GID
                with self.assertRaisesRegex(ContainerHardeningError, "non-root"):
                    enforce_container_hardening(
                        immutable_paths=(ro_root,),
                        writable_paths=(rw_tmp,),
                        proc_status_text=CLEAN_PROC_STATUS,
                        uid_getter=lambda: 0,
                        euid_getter=lambda: 0,
                        gid_getter=lambda: 0,
                        egid_getter=lambda: 0,
                        dont_write_bytecode=True,
                        platform="linux",
                        prctl_fn=lambda: 0,
                        umask_fn=lambda _: 0o022,
                    )

                # Violation 2: writable root / app filesystem
                with self.assertRaisesRegex(ContainerHardeningError, "accepted writes"):
                    enforce_container_hardening(
                        immutable_paths=(rw_tmp,),
                        writable_paths=(rw_state,),
                        proc_status_text=CLEAN_PROC_STATUS,
                        prctl_fn=lambda: 0,
                        umask_fn=lambda _: 0o022,
                        **common_ids,  # type: ignore[arg-type]
                    )

                # Violation 3: non-zero Linux capability mask
                cap_status = CLEAN_PROC_STATUS.replace(
                    "CapEff:\t0000000000000000", "CapEff:\t00000000a80425fb"
                )
                with self.assertRaisesRegex(ContainerHardeningError, "capability mask CapEff"):
                    enforce_container_hardening(
                        immutable_paths=(ro_root,),
                        writable_paths=(rw_tmp,),
                        proc_status_text=cap_status,
                        prctl_fn=lambda: 0,
                        umask_fn=lambda _: 0o022,
                        **common_ids,  # type: ignore[arg-type]
                    )

                # Violation 4: NoNewPrivs remains 0
                no_nnp_status = CLEAN_PROC_STATUS.replace("NoNewPrivs:\t1", "NoNewPrivs:\t0")
                with self.assertRaisesRegex(ContainerHardeningError, "NoNewPrivs"):
                    enforce_container_hardening(
                        immutable_paths=(ro_root,),
                        writable_paths=(rw_tmp,),
                        proc_status_text=no_nnp_status,
                        prctl_fn=lambda: 0,
                        umask_fn=lambda _: 0o022,
                        **common_ids,  # type: ignore[arg-type]
                    )

                # Violation 5: missing/unwritable EmptyDir scratch mount
                with self.assertRaisesRegex(ContainerHardeningError, "not writable"):
                    enforce_container_hardening(
                        immutable_paths=(ro_root,),
                        writable_paths=(unwritable_scratch,),
                        proc_status_text=CLEAN_PROC_STATUS,
                        prctl_fn=lambda: 0,
                        umask_fn=lambda _: 0o022,
                        **common_ids,  # type: ignore[arg-type]
                    )

                # Violation 6: unknown ZF_CONTAINER_HARDENING mode fails closed
                off_report = enforce_from_env({})
                self.assertFalse(off_report.enforced)
                with self.assertRaisesRegex(
                    ContainerHardeningError, "Invalid ZF_CONTAINER_HARDENING"
                ):
                    enforce_from_env({"ZF_CONTAINER_HARDENING": "permissive"})
            finally:
                for directory in (ro_root, ro_app, unwritable_scratch):
                    directory.chmod(0o700)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux kernel prctl check")
    def test_child_process_applies_real_linux_prctl_no_new_privs_and_umask(self) -> None:
        probe_code = """
import json, os, sys, tempfile
from pathlib import Path
from zava_forward.core.container_hardening import enforce_container_hardening

with tempfile.TemporaryDirectory() as tmp:
    ro = Path(tmp) / "ro"
    rw = Path(tmp) / "rw"
    ro.mkdir()
    rw.mkdir()
    ro.chmod(0o555)
    rw.chmod(0o700)
    try:
        report = enforce_container_hardening(
            expected_uid=os.getuid(),
            expected_gid=os.getgid(),
            bytecode_env="1",
            immutable_paths=(ro,),
            writable_paths=(rw,),
        )
        probe_file = rw / "umask-check"
        probe_file.write_text("ok", encoding="utf-8")
        mode = probe_file.stat().st_mode & 0o777
        status_text = Path("/proc/self/status").read_text(encoding="utf-8")
        nnp = [
            line.split(":", 1)[1].strip()
            for line in status_text.splitlines()
            if line.startswith("NoNewPrivs:")
        ][0]
        print(json.dumps({
            "enforced": report.enforced,
            "no_new_privs": report.no_new_privs,
            "kernel_nnp": nnp,
            "file_mode": mode,
            "dont_write_bytecode": sys.dont_write_bytecode,
        }))
    finally:
        ro.chmod(0o700)
"""
        proc = subprocess.run(
            [sys.executable, "-B", "-c", probe_code],
            env=_child_env(PYTHONDONTWRITEBYTECODE="1"),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout.strip())
        self.assertTrue(data["enforced"])
        self.assertEqual(data["no_new_privs"], 1)
        self.assertEqual(data["kernel_nnp"], "1")
        self.assertEqual(data["file_mode"], 0o600)
        self.assertTrue(data["dont_write_bytecode"])

    def test_all_deployed_entrypoints_fail_closed_under_enforced_hardening_violation(self) -> None:
        commands = (
            ("api", [sys.executable, "-m", "zava_forward.api"]),
            ("resident_demo", [sys.executable, "-m", "zava_forward.api.resident_demo"]),
            ("live_receiver", [sys.executable, "-m", "zava_forward.api.live_receiver"]),
            ("live_simulator", [sys.executable, "-m", "zava_forward.api.live_simulator"]),
            ("agents", [sys.executable, "-m", "zava_forward.agents", "serve"]),
            ("orchestrator", [sys.executable, "-m", "zava_forward.orchestrator", "run"]),
            ("token_store", [sys.executable, "-m", "zava_forward.orchestrator.token_store"]),
            ("digest_blob", [sys.executable, "-m", "zava_forward.orchestrator.digest_blob"]),
            (
                "ranking_publish",
                [sys.executable, "-m", "zava_forward.orchestrator.ranking_publish"],
            ),
            ("importer", [sys.executable, "-m", "zava_forward.importer"]),
        )
        for label, cmd in commands:
            with self.subTest(entrypoint=label):
                proc = subprocess.run(
                    cmd,
                    env=_child_env(ZF_CONTAINER_HARDENING="enforced"),
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=15,
                )
                self.assertEqual(proc.returncode, 2, f"{label} stderr: {proc.stderr}")
                self.assertIn("Refusing to start:", proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)


class DeclaredScaleLoadFixtureTests(unittest.TestCase):
    """Criterion 3: Load test against the declared scale fixture is run and recorded honestly."""

    def test_recorded_60000_home_load_and_restart_reports_preserve_non_production_bounds(
        self,
    ) -> None:
        load_path = ROOT / "docs/architecture/scale-load-2026-11-15.json"
        restart_path = ROOT / "docs/architecture/scale-restart-2026-11-15.json"
        self.assertTrue(load_path.is_file(), f"Missing {load_path}")
        self.assertTrue(restart_path.is_file(), f"Missing {restart_path}")

        load_report = json.loads(load_path.read_text(encoding="utf-8"))
        restart_report = json.loads(restart_path.read_text(encoding="utf-8"))

        expected_declared = {
            "homes": 60000,
            "events": 600000,
            "sessions": 20,
            "requests_per_second": 5.0,
            "duration_seconds": 1800,
            "inference_per_home": False,
        }
        self.assertEqual(load_report["declared_workload"], expected_declared)
        self.assertEqual(restart_report["declared_workload"], expected_declared)

        self.assertEqual(load_report["executed_workload"]["homes"], 60000)
        self.assertGreater(load_report["executed_workload"]["events_in_fixture"], 50000)
        self.assertEqual(load_report["executed_workload"]["sessions"], 20)
        self.assertFalse(load_report["executed_workload"]["meets_declared_workload"])
        self.assertIn("Not production scale", load_report["scope"])
        self.assertIn("not an Azure measurement", load_report["scope"])

        for route_name in ("list", "detail", "dashboard"):
            route = load_report["routes"][route_name]
            self.assertGreater(route["requests"], 0)
            self.assertEqual(route["errors"], 0)
            self.assertGreater(route["p95_ms"], 0.0)
        self.assertGreater(load_report["cost_drivers"]["sql_statements"], 0)

        self.assertEqual(restart_report["executed_workload"]["homes"], 60000)
        self.assertFalse(restart_report["executed_workload"]["meets_declared_workload"])
        self.assertIn("Not production scale", restart_report["scope"])
        self.assertEqual(restart_report["load"]["errors"], 0)
        self.assertGreater(restart_report["load"]["requests"], 100)
        self.assertLess(restart_report["server_rss"]["high_water_mib"], 1024.0)

        readme = " ".join((ROOT / "infra/README.md").read_text(encoding="utf-8").split())
        self.assertIn("scale-load-2026-11-15.json", readme)
        self.assertIn("scale-restart-2026-11-15.json", readme)
        self.assertIn("not at declared scale", readme)
        self.assertIn("makes no production", readme)

    def test_live_bounded_scale_fixture_load_harness_executes_cleanly(self) -> None:
        report = scale_load.run(homes=150, sessions=4, rate=8.0, duration=1.5)
        self.assertEqual(report["declared_workload"]["homes"], 60000)
        self.assertEqual(report["executed_workload"]["homes"], 150)
        self.assertFalse(report["executed_workload"]["meets_declared_workload"])
        self.assertIn("Not production scale", report["scope"])
        total_requests = 0
        for route_name in ("list", "detail", "dashboard"):
            route = report["routes"][route_name]
            self.assertEqual(route["errors"], 0)
            total_requests += route["requests"]
        self.assertGreaterEqual(total_requests, 6)
        self.assertGreater(report["cost_drivers"]["sql_statements"], 0)


class SingleReplicaRestartAndAuditPersistenceTests(unittest.TestCase):
    """Criterion 4: Single-replica and restart behaviour is verified with audit persistence."""

    @_requires_az_bicep()
    def test_compiled_bicep_enforces_single_active_revision_and_bounded_replicas(self) -> None:
        apps = module_template(_compiled("main.bicep"), "containerapps")
        by_container = {
            res["properties"]["template"]["containers"][0]["name"]: res
            for res in resources(apps)
            if res["type"] == "Microsoft.App/containerApps"
        }
        api_res = by_container["api"]
        self.assertEqual(api_res["properties"]["configuration"]["activeRevisionsMode"], "Single")
        api_scale = api_res["properties"]["template"]["scale"]
        self.assertEqual(api_scale["rules"][0]["http"]["metadata"]["concurrentRequests"], "50")

        agents_res = by_container["agents"]
        self.assertEqual(agents_res["properties"]["configuration"]["activeRevisionsMode"], "Single")
        agents_scale = agents_res["properties"]["template"]["scale"]
        self.assertEqual(agents_scale["minReplicas"], 0)
        self.assertEqual(agents_scale["maxReplicas"], 5)
        queue_rule = agents_scale["rules"][0]["custom"]
        self.assertEqual(queue_rule["type"], "azure-queue")
        self.assertEqual(queue_rule["metadata"]["queueName"], "agent-tasks")
        self.assertEqual(queue_rule["metadata"]["queueLength"], "5")
        self.assertTrue(queue_rule["identity"], "agents queue scale rule must bind identity")

        resident = _compiled("resident-demo.bicep")
        res_app = next(r for r in resources(resident) if r["type"] == "Microsoft.App/containerApps")
        self.assertEqual(res_app["properties"]["configuration"]["activeRevisionsMode"], "Single")
        self.assertEqual(
            res_app["properties"]["template"]["scale"], {"minReplicas": 0, "maxReplicas": 1}
        )

    def test_recorded_60000_home_sigkill_restart_preserves_audit_hash_chain(self) -> None:
        restart_report = json.loads(
            (ROOT / "docs/architecture/scale-restart-2026-11-15.json").read_text(encoding="utf-8")
        )
        restart = restart_report["restart"]
        self.assertEqual(restart["kill"], "SIGKILL, no graceful shutdown")
        self.assertEqual(restart["acknowledged_calls_before_kill"], 3)
        self.assertEqual(restart["entries_before_kill"], 3)
        self.assertEqual(restart["entries_after_restart"], 3)
        self.assertTrue(restart["chain_intact_after_restart"])
        self.assertEqual(restart["acknowledged_call_after_restart"], 1)
        self.assertEqual(restart["entries_after_new_write"], 4)
        self.assertTrue(restart["chain_intact_after_new_write"])

    def test_live_separate_process_sigkill_restart_preserves_sqlite_audit_chain(self) -> None:
        saved_hardening = os.environ.pop("ZF_CONTAINER_HARDENING", None)
        saved_pythonpath = os.environ.get("PYTHONPATH")
        child_paths = [
            str(ROOT / "src/core/src"),
            str(ROOT / "src/agents/src"),
            str(ROOT / "src/api/src"),
        ]
        if saved_pythonpath:
            child_paths.append(saved_pythonpath)
        os.environ["PYTHONPATH"] = os.pathsep.join(child_paths)
        try:
            report = scale_restart.run(homes=120, concurrency=4, seconds=1.5)
        finally:
            if saved_pythonpath is None:
                os.environ.pop("PYTHONPATH", None)
            else:
                os.environ["PYTHONPATH"] = saved_pythonpath
            if saved_hardening is not None:
                os.environ["ZF_CONTAINER_HARDENING"] = saved_hardening
        self.assertEqual(report["load"]["errors"], 0)
        restart = report["restart"]
        self.assertEqual(restart["kill"], "SIGKILL, no graceful shutdown")
        self.assertEqual(restart["acknowledged_calls_before_kill"], 3)
        self.assertEqual(restart["entries_before_kill"], 3)
        self.assertEqual(restart["entries_after_restart"], 3)
        self.assertTrue(restart["chain_intact_after_restart"])
        self.assertEqual(restart["acknowledged_call_after_restart"], 1)
        self.assertEqual(restart["entries_after_new_write"], 4)
        self.assertTrue(restart["chain_intact_after_new_write"])

    def test_worker_replica_crash_before_ack_redelivers_without_losing_task(self) -> None:
        class SimulatedReplicaCrash(BaseException):
            pass

        class CrashingSink(Sink):
            def post(self, result: Any) -> None:
                raise SimulatedReplicaCrash

        def _provider(*_: Any) -> dict[str, Any]:
            return returned(good_text())

        queue = InMemoryQueue([message()])
        dying_sink = CrashingSink()
        with contextlib.suppress(SimulatedReplicaCrash):
            serve(
                queue,
                AgentWorker(_provider),
                dying_sink,
                limits(),
                threading.Event(),
                idle=0.01,
            )
        self.assertEqual(dying_sink.results, [])
        self.assertEqual(queue.acked, [])
        self.assertEqual(len(queue.leased), 1)

        # Simulate queue visibility-timeout lease expiry and replacement single-replica startup.
        for receipt in list(queue.leased):
            queue.release(receipt)
        stop = threading.Event()
        replacement_sink = Sink()
        original_ack = queue.ack

        def _ack_and_stop(receipt: str) -> None:
            original_ack(receipt)
            stop.set()

        queue.ack = _ack_and_stop  # type: ignore[method-assign]
        completed = serve(
            queue,
            AgentWorker(_provider),
            replacement_sink,
            limits(),
            stop,
            idle=0.01,
        )
        self.assertEqual(completed, 1)
        self.assertEqual(len(replacement_sink.results), 1)
        self.assertEqual(queue.acked, ["0"])
        self.assertEqual((queue.pending, queue.leased), ([], {}))


if __name__ == "__main__":
    unittest.main()
