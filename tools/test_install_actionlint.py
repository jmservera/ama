"""Unit tests for tools/install-actionlint.py."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import tarfile
import tempfile
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "install_actionlint", Path(__file__).parent / "install-actionlint.py"
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def make_archive(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def asset_for(name: str, asset_id: int, body: bytes) -> Any:
    return mod.Asset(name, asset_id, len(body), hashlib.sha256(body).hexdigest())


class Response(io.BytesIO):
    def __enter__(self) -> Response:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class Network:
    """Scripted opener: each call pops the next outcome for its URL host."""

    def __init__(self, script: dict[str, list[Any]]) -> None:
        self.script = script
        self.requests: list[urllib.request.Request] = []

    def __call__(self, request: urllib.request.Request, timeout: float) -> Response:
        self.requests.append(request)
        host = urllib.parse.urlparse(request.full_url).hostname
        outcome = self.script[str(host)].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return Response(outcome)


def http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://x", code, "err", {}, None)  # type: ignore[arg-type]


class FetchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.body = b"payload-bytes"
        self.asset = asset_for("a.tar.gz", 7, self.body)
        self.sleeps: list[float] = []

    def run_fetch(self, script: dict[str, list[Any]], token: str | None = None) -> Any:
        network = Network(script)
        result = mod.fetch(
            self.asset, token, opener=network, sleep=self.sleeps.append, log=lambda _: None
        )
        return result, network

    def test_504_then_recovery_on_same_source(self) -> None:
        result, network = self.run_fetch(
            {"github.com": [http_error(504), http_error(504), self.body]}
        )
        self.assertEqual(result, self.body)
        self.assertEqual(len(network.requests), 3)
        self.assertEqual(self.sleeps, [2.0, 5.0])

    def test_browser_exhaustion_falls_back_to_official_api(self) -> None:
        result, network = self.run_fetch(
            {"github.com": [http_error(504)] * 3, "api.github.com": [self.body]}
        )
        self.assertEqual(result, self.body)
        self.assertTrue(network.requests[-1].full_url.endswith("/releases/assets/7"))

    def test_truncated_body_is_retried_and_never_returned(self) -> None:
        result, _ = self.run_fetch({"github.com": [self.body[:4], self.body]})
        self.assertEqual(result, self.body)

    def test_wrong_checksum_on_every_source_exhausts(self) -> None:
        wrong = b"x" * len(self.body)
        with self.assertRaisesRegex(mod.InstallError, "exhausted"):
            self.run_fetch({"github.com": [wrong] * 3, "api.github.com": [wrong] * 3})

    def test_all_504_exhausts_with_bounded_attempts(self) -> None:
        network = Network(
            {"github.com": [http_error(504)] * 3, "api.github.com": [http_error(504)] * 3}
        )
        with self.assertRaisesRegex(mod.InstallError, "exhausted"):
            mod.fetch(
                self.asset, None, opener=network, sleep=self.sleeps.append, log=lambda _: None
            )
        self.assertEqual(len(network.requests), 6)

    def test_client_error_skips_to_next_source_without_retry(self) -> None:
        result, network = self.run_fetch(
            {"github.com": [http_error(404)], "api.github.com": [self.body]}
        )
        self.assertEqual(result, self.body)
        self.assertEqual(len(network.requests), 2)

    def test_token_only_on_api_host_and_dropped_on_foreign_redirect(self) -> None:
        _, network = self.run_fetch(
            {"github.com": [http_error(404)], "api.github.com": [self.body]}, token="secret"
        )
        self.assertNotIn("Authorization", network.requests[0].headers)
        self.assertEqual(network.requests[1].get_header("Authorization"), "Bearer secret")
        handler = mod._DropAuthOnRedirect()
        original = urllib.request.Request(
            "https://api.github.com/x", headers={"Authorization": "Bearer secret"}
        )
        moved = handler.redirect_request(
            original, io.BytesIO(), 302, "Found", {}, "https://objects.example.com/y"
        )
        self.assertIsNotNone(moved)
        self.assertNotIn("Authorization", moved.headers)

    def test_oversized_response_is_rejected(self) -> None:
        with mock.patch.object(mod, "MAX_BYTES", 4):
            with self.assertRaisesRegex(mod.InstallError, "exhausted"):
                self.run_fetch({"github.com": [self.body] * 3, "api.github.com": [self.body] * 3})


class InstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.binary = b"#!/bin/sh\necho actionlint\n"
        self.archive = make_archive({"actionlint": self.binary, "README.md": b"x"})
        self.archive_asset = asset_for("actionlint_1.7.7_linux_amd64.tar.gz", 1, self.archive)
        self.sums = f"{self.archive_asset.sha256}  {self.archive_asset.name}\n".encode()
        self.sums_asset = asset_for("actionlint_1.7.7_checksums.txt", 2, self.sums)

    def patched(self) -> Any:
        stack = mock.patch.multiple(mod, ARCHIVE=self.archive_asset, CHECKSUMS=self.sums_asset)
        return stack

    def test_installs_verified_binary_with_execute_bit(self) -> None:
        network = Network({"github.com": [http_error(504), self.sums, self.archive]})
        with self.patched(), tempfile.TemporaryDirectory() as tmp:
            path = mod.install(
                Path(tmp) / "bin", opener=network, sleep=lambda _: None, log=lambda _: None
            )
            self.assertEqual(path.read_bytes(), self.binary)
            self.assertTrue(path.stat().st_mode & 0o111)
            self.assertEqual([p.name for p in path.parent.iterdir()], ["actionlint"])

    def test_checksums_file_not_listing_pinned_archive_fails_closed(self) -> None:
        other = b"0" * 64 + b"  " + self.archive_asset.name.encode() + b"\n"
        self.sums_asset = asset_for(self.sums_asset.name, 2, other)
        network = Network({"github.com": [other]})
        with self.patched(), tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(mod.InstallError, "pinned archive digest"):
                mod.install(Path(tmp), opener=network, sleep=lambda _: None, log=lambda _: None)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_archive_without_binary_or_invalid_archive_installs_nothing(self) -> None:
        for body in (make_archive({"README.md": b"x"}), b"not a tarball at all"):
            archive_asset = asset_for(self.archive_asset.name, 1, body)
            sums = f"{archive_asset.sha256}  {archive_asset.name}\n".encode()
            sums_asset = asset_for(self.sums_asset.name, 2, sums)
            network = Network({"github.com": [sums, body]})
            with (
                mock.patch.multiple(mod, ARCHIVE=archive_asset, CHECKSUMS=sums_asset),
                tempfile.TemporaryDirectory() as tmp,
            ):
                with self.assertRaises((mod.InstallError, tarfile.TarError)):
                    mod.install(Path(tmp), opener=network, sleep=lambda _: None, log=lambda _: None)
                self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_main_exit_codes(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with mock.patch.object(mod, "install", side_effect=mod.InstallError("exhausted")):
                self.assertEqual(mod.main(["x", "/nonexistent-never-created"]), 1)
            self.assertEqual(mod.main(["x"]), 2)


if __name__ == "__main__":
    unittest.main()
