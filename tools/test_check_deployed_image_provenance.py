"""Behaviour tests for tools/check-deployed-image-provenance.py (Issue #203)."""

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest import mock


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "check_deployed_image_provenance",
        Path(__file__).with_name("check-deployed-image-provenance.py"),
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = load_tool()

DOCKERFILE = "src/api/Dockerfile"


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def commit(root: Path, files: dict[str, str]) -> str:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "c")
    return git(root, "rev-parse", "--short=10", "HEAD")


class ProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        git(self.root, "init", "-q")

    def check(self, image: str) -> str:
        return tool.check_image(self.root, image, "HEAD", DOCKERFILE)[0]

    def test_src_built_ancestor_is_verified(self) -> None:
        sha = commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        commit(self.root, {"README.md": "later\n"})
        self.assertEqual(self.check(f"r.azurecr.io/zava-forward-api:demo-{sha}"), "verified")

    def test_retired_tree_or_missing_dockerfile_fails(self) -> None:
        old = commit(self.root, {f"{tool.RETIRED_TREES[0]}/Dockerfile": "FROM scratch\n"})
        self.assertEqual(self.check(f"r/x:demo-{old}"), "failed")
        both = commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        self.assertEqual(self.check(f"r/x:demo-{both}"), "failed")

    def test_unknown_commit_and_digest_pin_are_not_verified(self) -> None:
        commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        self.assertEqual(self.check("r/x:demo-deadbeef12"), "failed")
        self.assertEqual(self.check("r/x@sha256:" + "a" * 64), "unverifiable")

    def test_non_ancestor_commit_fails(self) -> None:
        commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        git(self.root, "checkout", "-q", "-b", "side")
        side = commit(self.root, {DOCKERFILE: "FROM busybox\n"})
        git(self.root, "checkout", "-q", "-")
        self.assertEqual(self.check(f"r/x:demo-{side}"), "failed")

    def run_main(self, *argv: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return int(tool.main(["--root", str(self.root), *argv]))

    def test_tag_needs_at_least_seven_hex_digits(self) -> None:
        sha = commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        self.assertEqual(self.check(f"r/x:demo-{sha[:6]}"), "unverifiable")
        self.assertEqual(self.check(f"r/x:demo-{sha[:7]}"), "verified")

    def test_app_image_is_read_from_azure_and_checked(self) -> None:
        sha = commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        with mock.patch.object(tool, "image_from_azure", return_value=f"r/x:demo-{sha}") as az:
            self.assertEqual(self.run_main("--app", "ca-demo", "--resource-group", "rg"), 0)
        az.assert_called_once_with("rg", "ca-demo")

    def test_ref_selects_the_ancestry_reference(self) -> None:
        commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        base = git(self.root, "branch", "--show-current")
        git(self.root, "checkout", "-q", "-b", "side")
        side = commit(self.root, {DOCKERFILE: "FROM busybox\n"})
        git(self.root, "checkout", "-q", base)
        self.assertEqual(self.run_main("--image", f"r/x:demo-{side}"), 1)
        self.assertEqual(self.run_main("--image", f"r/x:demo-{side}", "--ref", "side"), 0)

    def test_main_exit_codes(self) -> None:
        sha = commit(self.root, {DOCKERFILE: "FROM scratch\n"})
        good = f"r/x:demo-{sha}"
        pin = "r/x@sha256:" + "a" * 64

        def run(*images: str) -> int:
            argv = ["--root", str(self.root)]
            for image in images:
                argv += ["--image", image]
            with contextlib.redirect_stdout(io.StringIO()):
                return tool.main(argv)

        self.assertEqual(run(good), 0)
        self.assertEqual(run(good, pin), 2)
        self.assertEqual(run(good, "r/x:demo-deadbeef12"), 1)
        self.assertEqual(run(pin, "r/x:demo-deadbeef12"), 1)


if __name__ == "__main__":
    unittest.main()
