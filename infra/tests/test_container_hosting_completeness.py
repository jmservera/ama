"""Container hosting completeness: scale, probes, limits and rollback contracts (issue 144).

Reads the Bicep sources as text, so it needs no Azure access and no change to the templates.
It is a source contract, not evidence of a deployed scale rule, probe or revision rollback.
"""

import importlib.util
import json
import re
import unittest
from pathlib import Path
from typing import ClassVar

ROOT = Path(__file__).resolve().parents[2]
INFRA = ROOT / "infra"
RESOURCE = re.compile(
    r"^resource (\w+) 'Microsoft\.App/(containerApps|jobs)@[\w-]+' = ", re.MULTILINE
)
LIMITS = re.compile(r"resources: \{ cpu: json\('([\d.]+)'\), memory: '([\d.]+)Gi' \}")


def workloads() -> dict[str, tuple[str, str]]:
    """Every declared (not `existing`) Container App or job, keyed by file and symbol."""
    found: dict[str, tuple[str, str]] = {}
    for path in sorted([*INFRA.glob("*.bicep"), *INFRA.glob("modules/*.bicep")]):
        text = path.read_text()
        matches = list(RESOURCE.finditer(text))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            found[f"{path.relative_to(INFRA)}:{match.group(1)}"] = (
                match.group(2),
                text[match.start() : end],
            )
    return found


class WorkloadContracts(unittest.TestCase):
    def test_inventory_covers_api_worker_jobs_and_demo(self) -> None:
        names = set(workloads())
        for expected in (
            "modules/containerapps.bicep:api",
            "modules/containerapps.bicep:agents",
            "modules/containerapps.bicep:orchestrator",
            "modules/containerapps.bicep:tokenRenewal",
            "modules/containerapps.bicep:ledgerVerify",
            "modules/containerapps.bicep:rankingPublish",
            "modules/containerapps.bicep:importJob",
            "resident-demo.bicep:app",
            "live-receiver-job.bicep:job",
            "live-simulator-job.bicep:job",
        ):
            self.assertIn(expected, names)

    def test_every_container_declares_bounded_cpu_and_memory(self) -> None:
        for name, (_, text) in workloads().items():
            with self.subTest(workload=name):
                limits = LIMITS.findall(text)
                self.assertTrue(limits, "no resource limits")
                for cpu, memory in limits:
                    self.assertLessEqual(float(cpu), 0.5)
                    self.assertLessEqual(float(memory), 1.0)

    def test_every_app_bounds_replicas_with_a_scale_rule_where_it_scales(self) -> None:
        for name, (kind, text) in workloads().items():
            if kind != "containerApps":
                continue
            with self.subTest(workload=name):
                self.assertRegex(text, r"minReplicas: [\w]+")
                maximum = re.search(r"maxReplicas: ([^\n},]+)", text)
                self.assertIsNotNone(maximum)
                assert maximum is not None
                bound = maximum.group(1).strip()
                self.assertTrue(
                    re.fullmatch(r"\d+", bound) or "? 1 :" in bound,
                    f"unbounded max: {bound}",
                )
                if bound != "1" and not bound.startswith("enable"):
                    self.assertIn("rules: [", text)

    def test_every_job_bounds_runtime_and_retries(self) -> None:
        for name, (kind, text) in workloads().items():
            if kind != "jobs":
                continue
            with self.subTest(workload=name):
                self.assertRegex(text, r"replicaTimeout: [\w +]+")
                self.assertRegex(text, r"replicaRetryLimit: \d+")

    def test_apps_with_ingress_declare_all_three_probes_on_the_listening_port(
        self,
    ) -> None:
        checked = 0
        for name, (kind, text) in workloads().items():
            if kind != "containerApps" or "ingress:" not in text:
                continue
            checked += 1
            with self.subTest(workload=name):
                for probe in ("Startup", "Readiness", "Liveness"):
                    self.assertRegex(text, rf"type: '{probe}', httpGet:")
                ports = set(re.findall(r"httpGet: \{ path: '[^']+', port: (\d+)", text))
                self.assertEqual(len(ports), 1)
                self.assertIn(f"targetPort: {ports.pop()}", text)
        self.assertGreaterEqual(checked, 1)

    def test_every_app_runs_a_single_active_revision(self) -> None:
        for name, (kind, text) in workloads().items():
            if kind != "containerApps":
                continue
            with self.subTest(workload=name):
                self.assertRegex(text, r"activeRevisionsMode: '?Single'?")


class CrossChecks(unittest.TestCase):
    def test_api_limits_and_scale_match_the_load_run_assumptions(self) -> None:
        text = (INFRA / "modules/containerapps.bicep").read_text()
        api = text.split("resource api ", 1)[1].split("resource apiAuth ", 1)[0]
        self.assertEqual(LIMITS.findall(api), [("0.5", "1")])
        self.assertIn("concurrentRequests: '50'", api)
        harness = (ROOT / "src/api/tests/scale_load.py").read_text()
        self.assertIn('API_LIMITS = {"vcpu": 0.5, "memory_gib": 1.0, "max_replicas": 4}', harness)
        self.assertIn("maxReplicas: enablePublicSimulationLane ? 1 : 4", api)

    def test_probe_path_is_the_store_readiness_handler(self) -> None:
        server = (ROOT / "src/api/src/zava_forward/api/server.py").read_text()
        handler = server.split('if url.path == "/healthz":', 1)[1].split("\n            if not", 1)[
            0
        ]
        self.assertIn("app.store.ready()", handler)
        self.assertIn("503", handler)
        self.assertIn("200", handler)

    def test_worker_has_no_listener_so_no_hosted_probe(self) -> None:
        text = (INFRA / "modules/containerapps.bicep").read_text()
        agents = text.split("resource agents ", 1)[1].split("resource orchestrator ", 1)[0]
        self.assertNotIn("probes:", agents)
        self.assertNotIn("ingress:", agents)

    def test_rollback_path_is_revert_and_redeploy_not_an_untested_digest_swap(
        self,
    ) -> None:
        readme = (INFRA / "README.md").read_text()
        section = readme.split("Revision rollback:", 1)[1].split("Load run, from", 1)[0]
        flat = " ".join(section.split())
        for phrase in (
            "activeRevisionsMode: Single",
            "no historical digest redeploy path",
            "revert the change",
            "src-deploy.yml",
            "No traffic splitting",
        ):
            self.assertIn(phrase, flat)
        pipeline = (INFRA / "scripts/pipeline.py").read_text()
        self.assertIn("RELEASE_SHA", pipeline)

    def test_declared_scale_fixture_is_the_documented_one_and_not_a_production_claim(
        self,
    ) -> None:
        harness = (ROOT / "src/api/tests/scale_load.py").read_text()
        self.assertIn('"homes": 60000', harness)
        self.assertIn('"events": 600000', harness)
        self.assertIn('"inference_per_home": False', harness)
        readme = " ".join((INFRA / "README.md").read_text().split())
        self.assertIn("not at declared scale", readme)
        self.assertIn("makes no production", readme)

    def test_recorded_reports_disclaim_declared_scale_and_production_claims(self) -> None:
        readme = (INFRA / "README.md").read_text()
        for name in ("scale-load-2026-11-01.json", "scale-restart-2026-11-13.json"):
            self.assertIn(name, readme)
            report = json.loads((ROOT / "docs/architecture" / name).read_text())
            self.assertFalse(report["executed_workload"]["meets_declared_workload"], name)
            self.assertIn("Not production scale", report["scope"], name)
            self.assertIn("Azure", report["scope"], name)


class DeployedImageAndProbeInvariants(unittest.TestCase):
    PLACEHOLDER = "mcr.microsoft.com/k8se/quickstart:latest"

    def test_every_deployed_container_image_is_a_parameter_never_a_literal(self) -> None:
        for name, (_, text) in workloads().items():
            with self.subTest(workload=name):
                images = re.findall(r"^\s+image: (.+)$", text, re.MULTILINE)
                self.assertTrue(images, "no container image")
                for image in images:
                    self.assertRegex(image.strip(), r"^[A-Za-z]\w*$")

    def test_module_never_embeds_the_placeholder_image(self) -> None:
        module = (INFRA / "modules/containerapps.bicep").read_text()
        self.assertNotIn("quickstart", module)
        self.assertNotRegex(module, r"image: '")

    def test_main_passes_all_four_images_and_only_bootstraps_with_the_placeholder(
        self,
    ) -> None:
        main = (INFRA / "main.bicep").read_text()
        for wired in (
            "apiImage: apiImage",
            "agentImage: agentImage",
            "importImage: importImage",
            "orchestratorImage: empty(orchestratorImage) ? '"
            + self.PLACEHOLDER
            + "' : orchestratorImage",
        ):
            self.assertIn(wired, main)
        self.assertEqual(main.count(self.PLACEHOLDER), 4)
        self.assertIn("publicSimulationRequiresRealApiImage", main)

    def test_probe_timings_are_bounded_and_startup_budget_covers_slow_starts(self) -> None:
        text = (INFRA / "modules/containerapps.bicep").read_text()
        api = text.split("resource api ", 1)[1].split("resource apiAuth ", 1)[0]
        probes = {
            m.group(1): {k: int(v) for k, v in re.findall(r"(\w+): (\d+)", m.group(2))}
            for m in re.finditer(r"type: '(\w+)', httpGet: \{[^}]*\}, ([^}\n]+) \}", api)
        }
        self.assertEqual(set(probes), {"Startup", "Readiness", "Liveness"})
        for kind, values in probes.items():
            with self.subTest(probe=kind):
                self.assertGreaterEqual(values["periodSeconds"], 1)
                self.assertLessEqual(values["timeoutSeconds"], values["periodSeconds"] + 2)
                self.assertGreaterEqual(values["failureThreshold"], 1)
        startup = probes["Startup"]
        budget = (
            startup["initialDelaySeconds"] + startup["periodSeconds"] * startup["failureThreshold"]
        )
        self.assertGreaterEqual(budget, 60)
        self.assertLessEqual(budget, 300)

    def test_startup_window_outlasts_the_sql_lock_retry_budget(self) -> None:
        store = (ROOT / "src/core/src/zava_forward/core/mssqlstore.py").read_text()

        def constant(name: str) -> float:
            return float(re.search(rf"^{name} = ([\d.]+)", store, re.MULTILINE).group(1))

        attempts = int(constant("LOCK_RETRY_ATTEMPTS"))
        lock_timeout = int(re.search(r"@LockTimeout = (\d+)", store).group(1)) / 1000
        sleeps = sum(
            min(constant("LOCK_RETRY_CAP"), constant("LOCK_RETRY_BASE") * 2**i)
            for i in range(attempts - 1)
        )
        worst_case = attempts * lock_timeout + sleeps
        text = (INFRA / "modules/containerapps.bicep").read_text()
        api = text.split("resource api ", 1)[1].split("resource apiAuth ", 1)[0]
        startup = re.search(r"type: 'Startup', httpGet: \{[^}]*\}, ([^}\n]+) \}", api).group(1)
        values = {k: int(v) for k, v in re.findall(r"(\w+): (\d+)", startup)}
        window = (
            values["initialDelaySeconds"] + values["periodSeconds"] * values["failureThreshold"]
        )
        self.assertGreater(window, worst_case)

    def test_queue_workers_scale_from_zero_with_a_finite_cap(self) -> None:
        text = (INFRA / "modules/containerapps.bicep").read_text()
        agents = text.split("resource agents ", 1)[1].split("resource orchestrator ", 1)[0]
        self.assertIn("minReplicas: 0", agents)
        self.assertRegex(agents, r"maxReplicas: [1-9]\d?\n")
        self.assertIn("type: 'azure-queue'", agents)
        importer = text.split("resource importJob ", 1)[1]
        self.assertRegex(importer, r"maxExecutions: [1-9]\d?\n")
        self.assertIn("type: 'azure-queue'", importer)


class WorkerImageMapping(unittest.TestCase):
    """Each worker receives the image of the project that ships its module (issue 144)."""

    SYMBOLS: ClassVar[dict[str, str]] = {
        "api": "api",
        "agents": "agents",
        "orchestrator": "orchestrator",
        "tokenRenewal": "auth-renewal",
        "ledgerVerify": "ledger-verify",
        "rankingPublish": "rank-publish",
        "importJob": "import",
    }
    OWNER: ClassVar[dict[str, str]] = {
        "apiImage": "api",
        "agentImage": "agents",
        "orchestratorImage": "orchestrator",
        "importImage": "importer",
    }

    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location(
            "pipeline_for_mapping", INFRA / "scripts/pipeline.py"
        )
        assert spec and spec.loader
        cls.pipeline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.pipeline)
        text = (INFRA / "modules/containerapps.bicep").read_text()
        matches = list(RESOURCE.finditer(text))
        cls.blocks = {
            m.group(1): text[
                m.start() : matches[i + 1].start() if i + 1 < len(matches) else len(text)
            ]
            for i, m in enumerate(matches)
        }

    def test_every_bicep_workload_has_a_pipeline_image_mapping(self) -> None:
        self.assertEqual(set(self.blocks), set(self.SYMBOLS))
        self.assertEqual(set(self.SYMBOLS.values()), set(self.pipeline.WORKLOAD_IMAGE_PARAMETERS))

    def test_bicep_image_parameter_matches_the_pipeline_deployed_digest(self) -> None:
        for symbol, key in self.SYMBOLS.items():
            with self.subTest(workload=symbol):
                images = re.findall(r"^\s+image: (\w+)$", self.blocks[symbol], re.MULTILINE)
                self.assertEqual(images, [self.pipeline.WORKLOAD_IMAGE_PARAMETERS[key]])

    def test_worker_command_module_ships_in_the_image_project(self) -> None:
        checked = 0
        for symbol in self.SYMBOLS:
            block = self.blocks[symbol]
            command = re.search(r"command: \['python', '-m', '([\w.]+)'", block)
            if not command:
                continue
            image = re.search(r"^\s+image: (\w+)$", block, re.MULTILINE).group(1)
            module = Path(command.group(1).replace(".", "/"))
            base = ROOT / "src" / self.OWNER[image] / "src" / module
            with self.subTest(workload=symbol, module=command.group(1)):
                self.assertTrue(
                    base.with_suffix(".py").is_file() or (base / "__main__.py").is_file(),
                    f"{command.group(1)} is not shipped by the {self.OWNER[image]} image",
                )
            checked += 1
        self.assertEqual(checked, 6)


if __name__ == "__main__":
    unittest.main()
