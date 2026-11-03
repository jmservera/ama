"""Unit tests for tools/ci-affected.py."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "ci_affected", Path(__file__).parent / "ci-affected.py"
)
assert SPEC and SPEC.loader
ci = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci)

ALL = set(ci.PROJECTS)


class SelectTests(unittest.TestCase):
    def test_core_change_selects_all_dependents(self) -> None:
        s = ci.select(["src/core/src/zava_forward/core/x.py"])
        self.assertEqual(s["projects"], ALL)
        self.assertTrue(s["mssql"])

    def test_core_tests_change_selects_dependents(self) -> None:
        self.assertEqual(ci.select(["src/core/tests/helper.py"])["projects"], ALL)

    def test_api_only(self) -> None:
        s = ci.select(["src/api/src/zava_forward/api/web/app.js"])
        self.assertEqual(s["projects"], {"api"})
        self.assertTrue(s["namespace"])
        self.assertTrue(s["mssql"])

    def test_agents_selects_api(self) -> None:
        self.assertEqual(ci.select(["src/agents/src/a.py"])["projects"], {"agents", "api"})

    def test_importer_only_skips_mssql(self) -> None:
        s = ci.select(["src/importer/tests/test_a.py"])
        self.assertEqual(s["projects"], {"importer"})
        self.assertFalse(s["mssql"])

    def test_project_docs_only_selects_nothing(self) -> None:
        s = ci.select(["src/api/README.md", "src/README.md", "src/core/docs/a.md"])
        self.assertEqual(s["projects"], set())
        self.assertFalse(s["namespace"])
        self.assertFalse(s["mssql"])

    def test_infra_workflow_and_top_level_src_select_all(self) -> None:
        for path in [
            "infra/main.bicep",
            ".github/workflows/src-ci.yml",
            "src/trivy.yaml",
            "src/new/x.py",
        ]:
            with self.subTest(path=path):
                s = ci.select(["src/api/README.md", path])
                self.assertEqual(s["projects"], ALL)
                self.assertTrue(s["namespace"] and s["mssql"])

    def test_gate_tooling_selects_namespace_only(self) -> None:
        s = ci.select(["tools/rpi-checks.py"])
        self.assertEqual(s["projects"], set())
        self.assertTrue(s["namespace"])
        self.assertFalse(s["mssql"])

    def test_unknown_path_selects_all(self) -> None:
        self.assertEqual(ci.select(["support/synthetic-data/a.json"])["projects"], ALL)

    def test_none_selects_all(self) -> None:
        s = ci.select(None)
        self.assertEqual(s["projects"], ALL)
        self.assertTrue(s["namespace"] and s["mssql"])


class MainTests(unittest.TestCase):
    def run_main(self, env: dict[str, str], files: list[str] | None) -> dict[str, str]:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            full = {**env, "GITHUB_OUTPUT": str(out)}
            with (
                mock.patch.dict(os.environ, full, clear=True),
                mock.patch.object(ci, "changed_files", return_value=files),
            ):
                self.assertEqual(ci.main(), 0)
            return dict(line.split("=", 1) for line in out.read_text().splitlines())

    def test_dispatch_and_push_run_everything(self) -> None:
        for event in ["workflow_dispatch", "push"]:
            with self.subTest(event=event):
                out = self.run_main({"EVENT_NAME": event}, ["src/api/README.md"])
                matrix = json.loads(out["matrix"])
                self.assertTrue(all(e["run"] for e in matrix["include"]))
                self.assertEqual((out["namespace"], out["mssql"]), ("true", "true"))

    def test_pull_request_filters_matrix(self) -> None:
        out = self.run_main(
            {"EVENT_NAME": "pull_request", "BASE_SHA": "a", "HEAD_SHA": "b"},
            ["src/api/src/x.py"],
        )
        runs = {e["project"]: e["run"] for e in json.loads(out["matrix"])["include"]}
        self.assertEqual(
            runs,
            {
                "core": False,
                "api": True,
                "agents": False,
                "orchestrator": False,
                "importer": False,
            },
        )

    def test_matrix_keeps_every_project_entry(self) -> None:
        out = self.run_main({"EVENT_NAME": "pull_request"}, [])
        names = [e["project"] for e in json.loads(out["matrix"])["include"]]
        self.assertEqual(names, list(ci.PROJECTS))


class RiskTests(unittest.TestCase):
    def test_txt_is_not_documentation(self) -> None:
        for path in [
            "src/api/requirements.txt",
            "src/core/notes.txt",
            "src/build-requirements.txt",
        ]:
            with self.subTest(path=path):
                sel = ci.select([path])
                self.assertTrue(sel["namespace"])
                self.assertTrue(sel["projects"])

    def test_markdown_under_src_is_still_skipped(self) -> None:
        sel = ci.select(["src/api/README.md", "src/README.md"])
        self.assertEqual(sel["projects"], set())
        self.assertFalse(sel["namespace"])

    def test_dependency_manifests_run_everything(self) -> None:
        for path in [
            "src/core/pyproject.toml",
            "src/importer/pyproject.toml",
            "src/api/requirements.txt",
            "src/api/requirements-dev.txt",
            "src/agents/build-requirements.txt",
        ]:
            with self.subTest(path=path):
                sel = ci.select([path])
                self.assertEqual(sel["projects"], set(ci.PROJECTS))
                self.assertTrue(sel["namespace"])
                self.assertTrue(sel["mssql"])


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        import pathlib

        import yaml

        path = pathlib.Path(__file__).resolve().parents[1] / ".github/workflows/src-ci.yml"
        self.jobs = yaml.safe_load(path.read_text(encoding="utf-8"))["jobs"]

    def test_dependents_run_when_changes_job_fails(self) -> None:
        for name in ["image-paths", "project", "namespace", "mssql"]:
            with self.subTest(job=name):
                condition = str(self.jobs[name]["if"])
                self.assertIn("!cancelled()", condition)
        for name in ["namespace", "mssql"]:
            self.assertIn("needs.changes.result != 'success'", self.jobs[name]["if"])

    def test_fallback_matrix_runs_everything(self) -> None:
        expression = self.jobs["project"]["strategy"]["matrix"]
        literal = expression.split("|| '", 1)[1].rsplit("') }}", 1)[0]
        matrix = json.loads(literal)
        self.assertEqual([e["project"] for e in matrix["include"]], list(ci.PROJECTS))
        self.assertTrue(all(e["run"] for e in matrix["include"]))

    def test_required_job_names_unchanged(self) -> None:
        self.assertEqual(self.jobs["namespace"]["name"], "src-namespace")
        self.assertEqual(self.jobs["no-working-data"]["name"], "src-no-working-data")
        self.assertEqual(self.jobs["project"]["name"], "src-${{ matrix.project }}")


if __name__ == "__main__":
    unittest.main()
