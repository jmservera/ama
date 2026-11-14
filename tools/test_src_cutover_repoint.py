"""Local contract proof that build, CI and infra paths use src/ (Refs #201, criterion 5).

This proves the repository half only. A deployed and healthy build from src/ in
Azure is the separate Azure-only half of criterion 5 and is not proven here.
"""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ("api", "agents", "orchestrator", "importer")
DISTRIBUTIONS = ("core", "agents", "api", "orchestrator", "importer")
RETIRED_PATH = re.compile(r"(?<![\w./-])(?:mvp|prototype)/")
RETIRED_PYTHONPATH = re.compile(r"PYTHONPATH=\S*\b(?:mvp|prototype)\b")
# Negative guards that assert retired data stays absent are not job targets.
ALLOWED_GUARD = re.compile(r"git ls-files\b.*\bmvp/data\b")
# Documented historical or cutover proof material, excluded from runtime paths.
HISTORICAL_FILES = {
    "infra/scripts/private-cutover-proof.py",
    "infra/cutover-proof.Dockerfile",
}


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def tracked(*patterns: str) -> list[Path]:
    found: set[Path] = set()
    for pattern in patterns:
        found.update(p for p in ROOT.glob(pattern) if p.is_file())
    return sorted(found)


def retired_hits(text: str) -> list[str]:
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        if ALLOWED_GUARD.search(line):
            continue
        if RETIRED_PATH.search(line) or RETIRED_PYTHONPATH.search(line):
            hits.append(f"{number}: {line.strip()}")
    return hits


def workflow_steps(workflow: dict) -> list[dict]:
    return [
        step
        for job in workflow.get("jobs", {}).values()
        for step in job.get("steps", [])
        if isinstance(step, dict)
    ]


class WorkflowContract(unittest.TestCase):
    def test_workflows_parse_and_have_no_retired_targets(self):
        for path in tracked(".github/workflows/*.yml"):
            with self.subTest(workflow=path.name):
                yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertEqual(retired_hits(path.read_text(encoding="utf-8")), [])

    def test_jobs_do_not_work_in_retired_directories(self):
        for path in tracked(".github/workflows/*.yml"):
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            for name, job in workflow.get("jobs", {}).items():
                defaults = (
                    job.get("defaults", {}).get("run", {}).get("working-directory", "")
                )
                with self.subTest(workflow=path.name, job=name):
                    self.assertIsNone(RETIRED_PATH.search(str(defaults)))
                    for step in job.get("steps", []):
                        self.assertIsNone(
                            RETIRED_PATH.search(str(step.get("working-directory", "")))
                        )

    def test_source_ci_lints_type_checks_tests_and_builds_from_src(self):
        workflow = yaml.safe_load(read(".github/workflows/src-ci.yml"))
        project = workflow["jobs"]["project"]
        self.assertEqual(
            project["defaults"]["run"]["working-directory"], "src/${{ matrix.project }}"
        )
        runs = "\n".join(str(step.get("run", "")) for step in project["steps"])
        self.assertIn("ruff check .", runs)
        self.assertIn("ruff format --check .", runs)
        self.assertIn("mypy", runs)
        self.assertIn("unittest", runs)
        self.assertIn(
            "docker build -f src/${{ matrix.project }}/Dockerfile -t zava-forward-${{ matrix.project }}:ci src",
            runs,
        )
        matrix = re.findall(r'\{"project":"(\w+)"', str(project["strategy"]["matrix"]))
        self.assertEqual(sorted(matrix), sorted(DISTRIBUTIONS))

    def test_namespace_job_installs_all_distributions_from_src(self):
        workflow = yaml.safe_load(read(".github/workflows/src-ci.yml"))
        runs = "\n".join(
            str(step.get("run", "")) for step in workflow["jobs"]["namespace"]["steps"]
        )
        for dist in DISTRIBUTIONS:
            self.assertIn(f"src/{dist}", runs)

    def test_source_ci_workflow_triggers_cover_src(self):
        triggers = workflow_on(yaml.safe_load(read(".github/workflows/src-ci.yml")))
        self.assertIn("src/**", triggers["pull_request"]["paths"])

    def test_deploy_workflow_builds_every_image_with_src_context(self):
        workflow = yaml.safe_load(read(".github/workflows/src-deploy.yml"))
        build = [
            s
            for s in workflow_steps(workflow)
            if "docker build" in str(s.get("run", ""))
        ]
        self.assertTrue(build)
        for step in build:
            self.assertIn('-f "src/$PROJECT/Dockerfile"', step["run"])
            self.assertTrue(step["run"].rstrip().endswith(" src"))
        matrix = [j for j in workflow["jobs"].values() if "strategy" in j]
        projects = {
            p for job in matrix for p in job["strategy"]["matrix"].get("project", [])
        }
        self.assertEqual(projects, set(PROJECTS))

    def test_legacy_named_ci_builds_from_src_context(self):
        workflow = yaml.safe_load(read(".github/workflows/mvp-ci.yml"))
        builds = [
            s["run"]
            for s in workflow_steps(workflow)
            if "docker build" in str(s.get("run", ""))
        ]
        self.assertTrue(builds)
        for run in builds:
            self.assertIn("-f src/api/Dockerfile", run)
            self.assertTrue(run.rstrip().endswith(" src"))


def workflow_on(workflow: dict) -> dict:
    # PyYAML parses the bare key "on" as boolean True.
    return workflow.get("on", workflow.get(True, {}))


class DockerfileContract(unittest.TestCase):
    def test_every_project_has_a_dockerfile(self):
        for project in PROJECTS:
            self.assertTrue((ROOT / "src" / project / "Dockerfile").is_file(), project)

    def test_dockerfiles_copy_distributions_from_src_context(self):
        for project in PROJECTS:
            text = read(f"src/{project}/Dockerfile")
            copies = re.findall(r"^COPY\s+(?:--\S+\s+)*(\S+)\s", text, re.MULTILINE)
            with self.subTest(project=project):
                self.assertEqual(retired_hits(text), [])
                self.assertIn("core/pyproject.toml", copies)
                self.assertIn("core/src", copies)
                self.assertIn(f"{project}/pyproject.toml", copies)
                self.assertIn(f"{project}/src", copies)
                for source in copies:
                    if source in {"build-requirements.txt"}:
                        continue
                    self.assertIn(source.split("/")[0], DISTRIBUTIONS, source)
                self.assertTrue((ROOT / "src" / "build-requirements.txt").is_file())
                for source in copies:
                    self.assertTrue((ROOT / "src" / source).exists(), source)

    def test_dockerfiles_build_wheels_not_pythonpath(self):
        for project in PROJECTS:
            text = read(f"src/{project}/Dockerfile")
            with self.subTest(project=project):
                self.assertIn("pip wheel", text)
                self.assertNotIn("PYTHONPATH", text)


class InfraContract(unittest.TestCase):
    def test_infra_runtime_files_have_no_retired_paths(self):
        files = tracked(
            "infra/*.bicep",
            "infra/*.bicepparam",
            "infra/modules/*.bicep",
            "infra/*.py",
            "infra/*.sh",
            "infra/*Dockerfile",
            "infra/scripts/*.py",
            "infra/scripts/*.sh",
            "tools/test_src_cutover_repoint.py",
        )
        self.assertTrue(files)
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            if (
                relative in HISTORICAL_FILES
                or relative == "tools/test_src_cutover_repoint.py"
            ):
                continue
            with self.subTest(file=relative):
                self.assertEqual(retired_hits(path.read_text(encoding="utf-8")), [])

    def test_historical_proof_files_are_documented_exceptions(self):
        for relative in sorted(HISTORICAL_FILES):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_bicep_loads_src_contract_files_that_exist(self):
        for path in tracked("infra/*.bicep", "infra/modules/*.bicep"):
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"loadJsonContent\('([^']+)'\)", text):
                resolved = (path.parent / target).resolve()
                with self.subTest(file=path.name, target=target):
                    self.assertTrue(resolved.is_file())
                    if "/src/" in resolved.as_posix() or target.startswith("../src/"):
                        self.assertTrue(resolved.is_relative_to(ROOT / "src"))

    def test_bicep_image_guidance_names_src_dockerfiles(self):
        guard = read("infra/modules/guard.bicep")
        self.assertIn("src/api/Dockerfile", guard)
        for name in ("live-receiver-job.bicep", "live-simulator-job.bicep"):
            text = read(f"infra/{name}")
            self.assertIn("src/api/live-simulator.Dockerfile", text)
        self.assertTrue((ROOT / "src/api/live-simulator.Dockerfile").is_file())

    def test_deploy_script_targets_src_orchestrator_image(self):
        self.assertIn('"zava-forward-orchestrator"', read("infra/scripts/deploy.py"))

    def test_infra_readme_builds_with_src_context(self):
        text = read("infra/README.md")
        self.assertIn("az acr build -r <registry> -f src/api/Dockerfile", text)
        self.assertIn("-f src/api/Dockerfile src", text)


if __name__ == "__main__":
    unittest.main()
