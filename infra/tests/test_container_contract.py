"""Source-image startup, CI scan and build-context regression contracts."""

import importlib.util
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "container_entrypoint", ROOT / "src/container-entrypoint.py"
)
assert SPEC is not None and SPEC.loader is not None
ENTRYPOINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ENTRYPOINT)
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
        with (
            patch.object(ENTRYPOINT.os, "getuid", return_value=uid),
            patch.object(ENTRYPOINT.os, "getgid", return_value=gid),
            patch.object(ENTRYPOINT.os, "statvfs", return_value=SimpleNamespace(f_flag=flags)),
            patch.object(ENTRYPOINT.Path, "read_text", return_value=status),
        ):
            ENTRYPOINT.verify_runtime()

    def test_hardened_runtime_is_accepted(self):
        self.verify()

    def test_each_missing_control_is_rejected(self):
        for arguments in ({"uid": 0}, {"gid": 0}, {"flags": 0}):
            with self.subTest(arguments=arguments), self.assertRaises(RuntimeError):
                self.verify(**arguments)
        for name in ("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb", "NoNewPrivs"):
            value = "0" if name == "NoNewPrivs" else "0000000000000001"
            status = "\n".join(
                f"{name}:\t{value}" if line.startswith(f"{name}:") else line
                for line in STATUS.splitlines()
            )
            with self.subTest(field=name), self.assertRaises(RuntimeError):
                self.verify(status=status)

    def test_unknown_runtime_status_fails_closed_with_diagnostic(self):
        for error in (
            OSError("proc unavailable"),
            KeyError("CapBnd"),
            ValueError("invalid status"),
        ):
            with (
                self.subTest(error=error),
                patch.object(ENTRYPOINT, "verify_runtime", side_effect=error),
                patch("sys.stderr") as stderr,
                patch.object(ENTRYPOINT.os, "execvp") as execute,
            ):
                self.assertEqual(ENTRYPOINT.main(), 78)
                execute.assert_not_called()
                self.assertIn(
                    "Container security contract failed", str(stderr.write.call_args_list)
                )

    def test_exec_preserves_command_arguments(self):
        with (
            patch.object(ENTRYPOINT, "verify_runtime"),
            patch.object(ENTRYPOINT.sys, "argv", ["guard", "python", "-m", "job", "--publish"]),
            patch.object(ENTRYPOINT.os, "execvp", side_effect=OSError("test exec")) as execute,
            patch("sys.stderr"),
        ):
            self.assertEqual(ENTRYPOINT.main(), 78)
            execute.assert_called_once_with("python", ["python", "-m", "job", "--publish"])

    def test_missing_command_is_rejected(self):
        with (
            patch.object(ENTRYPOINT, "verify_runtime"),
            patch.object(ENTRYPOINT.sys, "argv", ["guard"]),
            patch.object(ENTRYPOINT.os, "execvp") as execute,
            patch("sys.stderr"),
        ):
            self.assertEqual(ENTRYPOINT.main(), 78)
            execute.assert_not_called()

    def test_every_src_image_uses_the_same_guard(self):
        paths = sorted((ROOT / "src").glob("*/Dockerfile"))
        self.assertEqual(len(paths), 4)
        for path in paths:
            text = path.read_text()
            with self.subTest(image=path.parent.name):
                self.assertIn(
                    "COPY container-entrypoint.py /usr/local/bin/container-entrypoint.py", text
                )
                self.assertIn("USER 10001:10001", text)
                self.assertIn(
                    'ENTRYPOINT ["python", "/usr/local/bin/container-entrypoint.py"]', text
                )
                self.assertIn('CMD ["python", "-m", "zava_forward.', text)
        self.assertIn(
            "!container-entrypoint.py",
            (ROOT / "src/api/Dockerfile.dockerignore").read_text().splitlines(),
        )
        self.assertNotIn("--entrypoint", (ROOT / "src/acr-cutover.yaml").read_text())

    def test_existing_workflows_scan_without_suppression(self):
        for name in ("src-ci.yml", "mvp-ci.yml"):
            text = (ROOT / ".github/workflows" / name).read_text()
            with self.subTest(workflow=name):
                self.assertIn("trivy-config: src/trivy.yaml", text)
                self.assertIn("ignore-unfixed: false", text)
                self.assertNotIn("ignore-unfixed: true", text)
                self.assertNotIn("trivyignores:", text)
        text = (ROOT / ".github/workflows/src-ci.yml").read_text()
        self.assertIn("python src/check-container.py", text)
        config = (ROOT / "src/trivy.yaml").read_text()
        self.assertIn("ignore-unfixed: false", config)
        self.assertIn("ignorefile: /dev/null", config)


if __name__ == "__main__":
    unittest.main()
