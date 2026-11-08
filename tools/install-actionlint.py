#!/usr/bin/env python3
"""Install the pinned actionlint release with bounded, fail-closed retrieval.

Both release assets are fetched from official GitHub endpoints only (the browser
download URL, then the release asset API) and must match pinned SHA-256 digests
before anything is extracted. Any exhausted, truncated or mismatched result
exits non-zero and leaves no binary behind.
"""

from __future__ import annotations

import hashlib
import io
import os
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

VERSION = "1.7.7"
REPO = "rhysd/actionlint"
ATTEMPTS = 3
DELAYS = (2.0, 5.0)
TIMEOUT = 30
MAX_BYTES = 8 * 1024 * 1024


class Asset(NamedTuple):
    name: str
    asset_id: int
    size: int
    sha256: str


ARCHIVE = Asset(
    f"actionlint_{VERSION}_linux_amd64.tar.gz",
    221573254,
    2080472,
    "023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757",
)
CHECKSUMS = Asset(
    f"actionlint_{VERSION}_checksums.txt",
    221573261,
    1119,
    "ac22e6577b8d133c7cd779682e65712ef722e719a297633699a4da05e9f351e0",
)
API_HOST = "api.github.com"


class InstallError(Exception):
    pass


class _DropAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: Any, msg: Any, headers: Any, newurl: str
    ) -> urllib.request.Request | None:
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlparse(newurl).hostname != API_HOST:
            new.remove_header("Authorization")
        return new


def _open(request: urllib.request.Request, timeout: float) -> Any:
    return urllib.request.build_opener(_DropAuthOnRedirect).open(request, timeout=timeout)


def sources(asset: Asset, token: str | None) -> list[tuple[str, dict[str, str]]]:
    browser = f"https://github.com/{REPO}/releases/download/v{VERSION}/{asset.name}"
    api_headers = {"Accept": "application/octet-stream", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        api_headers["Authorization"] = f"Bearer {token}"
    api = f"https://{API_HOST}/repos/{REPO}/releases/assets/{asset.asset_id}"
    return [(browser, {"Accept": "application/octet-stream"}), (api, api_headers)]


def _read(response: Any) -> bytes:
    body = response.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise InstallError("response exceeds the size limit")
    return bytes(body)


def fetch(
    asset: Asset,
    token: str | None = None,
    opener: Callable[[urllib.request.Request, float], Any] = _open,
    sleep: Callable[[float], None] = time.sleep,
    log: Callable[[str], None] = lambda message: print(message, file=sys.stderr),
) -> bytes:
    """Return verified bytes for the asset or raise InstallError when every source is exhausted."""
    failures: list[str] = []
    for url, headers in sources(asset, token):
        host = urllib.parse.urlparse(url).hostname
        for attempt in range(1, ATTEMPTS + 1):
            try:
                request = urllib.request.Request(url, headers=headers)
                with opener(request, TIMEOUT) as response:
                    body = _read(response)
                if len(body) != asset.size or hashlib.sha256(body).hexdigest() != asset.sha256:
                    raise InstallError("size or SHA-256 mismatch")
                log(f"{asset.name}: verified from {host} on attempt {attempt}")
                return body
            except urllib.error.HTTPError as error:
                failures.append(f"{host} HTTP {error.code}")
                if error.code < 500 and error.code != 429:
                    break
            except (OSError, InstallError) as error:
                failures.append(f"{host} {type(error).__name__}: {error}")
            if attempt < ATTEMPTS:
                sleep(DELAYS[min(attempt - 1, len(DELAYS) - 1)])
    raise InstallError(f"{asset.name}: all official sources exhausted ({'; '.join(failures)})")


def check_checksums(text: bytes) -> None:
    expected = f"{ARCHIVE.sha256}  {ARCHIVE.name}"
    if expected not in text.decode("utf-8", "replace").splitlines():
        raise InstallError("checksums file does not list the pinned archive digest")


def extract(archive: bytes, dest: Path) -> Path:
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        try:
            member = tar.getmember("actionlint")
        except KeyError:
            raise InstallError("archive has no actionlint member") from None
        source = tar.extractfile(member) if member.isreg() else None
        if source is None:
            raise InstallError("actionlint member is not a regular file")
        data = source.read()
    dest.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=dest, prefix=".actionlint-")
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(data)
        os.chmod(temporary, 0o755)
        target = dest / "actionlint"
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return target


def install(dest: Path, token: str | None = None, **kwargs: Any) -> Path:
    check_checksums(fetch(CHECKSUMS, token, **kwargs))
    return extract(fetch(ARCHIVE, token, **kwargs), dest)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: install-actionlint.py <destination-directory>", file=sys.stderr)
        return 2
    try:
        print(install(Path(argv[1]), os.environ.get("GITHUB_TOKEN") or None))
    except (InstallError, tarfile.TarError, OSError) as error:
        print(f"actionlint {VERSION} was not installed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
