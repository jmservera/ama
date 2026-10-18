"""External Docker controls, ACA-compatible image startup and CI scan contracts."""

import errno
import importlib.util
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("check_container", ROOT / "src/check-container.py")
assert SPEC is not None and SPEC.loader is not None
HARNESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)
STATUS = "\n".join(
    [
        "CapInh:\t0000000000000000",
        "CapPrm:\t0000000000000000",
        "CapEff:\t0000000000000000",
        "CapBnd:\t0000000000000000",
        "CapAmb:\t0000000000000000",
        "NoNewPrivs:\t1",
    ]
)


class ContainerContractTests(unittest.TestCase):
    def verify(self, *, uid=10001, gid=10001, flags=os.ST_RDONLY, status=STATUS):
        def write(path, text):
            if str(path) == "/app/security-probe":
                raise OSError(errno.EROFS, "read-only filesystem")
            self.assertEqual(str(path), "/state/security-probe")

        with (
            patch.object(os, "getuid", return_value=uid),
            patch.object(os, "getgid", return_value=gid),
            patch.object(os, "statvfs", return_value=SimpleNamespace(f_flag=flags)),
            patch.object(Path, "read_text", return_value=status),
            patch.object(Path, "write_text", autospec=True, side_effect=write),
            patch.object(Path, "exists", return_value=False),
        ):
            exec(HARNESS.PROBE, {})

    def test_hardened_runtime_probe_passes(self):
        self.verify()

    def test_probe_rejects_each_missing_control(self):
        for arguments in ({"uid": 0}, {"gid": 0}, {"flags": 0}):
            with self.subTest(arguments=arguments), self.assertRaises(AssertionError):
                self.verify(**arguments)
        for name in ("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb", "NoNewPrivs"):
            value = "0" if name == "NoNewPrivs" else "0000000000000001"
            status = "\n".join(
                f"{name}:\t{value}" if line.startswith(f"{name}:") else line
                for line in STATUS.splitlines()
            )
            with self.subTest(field=name), self.assertRaises(AssertionError):
                self.verify(status=status)

    def test_unknown_runtime_status_is_not_accepted(self):
        for status in ("", STATUS.replace("CapBnd:\t0000000000000000", "CapBnd:\tinvalid")):
            with self.subTest(status=status), self.assertRaises((KeyError, ValueError)):
                self.verify(status=status)

    def test_probe_checks_actual_root_write_rejection(self):
        probe = HARNESS.PROBE.split("try:\n", 1)[1]
        probe = "try:\n" + probe
        with (
            patch.object(Path, "write_text", return_value=9),
            self.assertRaisesRegex(AssertionError, "root filesystem accepted a write"),
        ):
            exec(probe, {"Path": Path, "errno": errno})

    def test_every_src_image_is_nonroot_without_startup_guard(self):
        paths = sorted((ROOT / "src").glob("*/Dockerfile"))
        self.assertEqual(len(paths), 4)
        for path in paths:
            text = path.read_text()
            with self.subTest(image=path.parent.name):
                self.assertIn("USER 10001:10001", text)
                self.assertIn('CMD ["python", "-m", "zava_forward.', text)
                self.assertNotIn("container-entrypoint", text)
                self.assertNotIn("ENTRYPOINT", text)
                self.assertIn("apt-get upgrade -y --no-install-recommends", text)
                for line in text.splitlines():
                    if line.startswith("FROM "):
                        self.assertRegex(line, r"^FROM python@sha256:[a-f0-9]{64}( AS build)?$")
        self.assertFalse((ROOT / "src/container-entrypoint.py").exists())

    def test_runtime_controls_are_external_and_application_is_tested_both_ways(self):
        self.assertEqual(
            HARNESS.CONTROLS,
            ["--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges"],
        )
        text = (ROOT / "src/check-container.py").read_text()
        self.assertIn("for flags in (CONTROLS, []):", text)
        self.assertIn("check_api(image, flags, writable, seed)", text)
        self.assertNotIn("--entrypoint", (ROOT / "src/acr-cutover.yaml").read_text())
        recipe = (ROOT / "src/acr-cutover.yaml").read_text()
        self.assertEqual(recipe.count("--read-only --cap-drop ALL"), 4)
        self.assertEqual(recipe.count("--security-opt no-new-privileges"), 4)

    def test_existing_workflows_gate_fixable_and_report_unfixed_without_lists(self):
        for name in ("src-ci.yml",):
            text = (ROOT / ".github/workflows" / name).read_text()
            with self.subTest(workflow=name):
                self.assertEqual(text.count("trivy-config: src/trivy.yaml"), 3)
                self.assertEqual(text.count("ignore-unfixed: true"), 1)
                self.assertEqual(text.count("ignore-unfixed: false"), 1)
                self.assertIn('exit-code: "1"', text)
                self.assertIn('exit-code: "0"', text)
                self.assertIn("-all.json", text)
                self.assertIn("actions/upload-artifact@", text)
                self.assertNotIn("trivyignores:", text)
                self.assertNotIn("continue-on-error:", text)
                self.assertIn("version: v0.76.0", text)
                self.assertIn("format: spdx-json", text)
                self.assertIn("zava-forward-${{ matrix.project }}.spdx.json", text)
                self.assertIn("name: Retain SPDX evidence", text)
        text = (ROOT / ".github/workflows/src-ci.yml").read_text()
        self.assertIn("python src/check-container.py", text)
        self.assertNotIn('pythonpath: "${{ github.workspace }}', text)
        self.assertIn("format('{0}/src/core/tests:{0}/src/agents/tests', github.workspace)", text)
        config = (ROOT / "src/trivy.yaml").read_text()
        self.assertIn("ignore-unfixed: false", config)
        self.assertIn("ignorefile: /dev/null", config)
        self.assertFalse(list((ROOT / "src").rglob(".trivyignore*")))


if __name__ == "__main__":
    unittest.main()
