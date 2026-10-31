"""Content-versioned packaged assets shared by the employee and resident sites."""

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs

_ATTRIBUTE = re.compile(rb'(?P<prefix>\b(?:src|href)=["\'])(?P<url>/[^"\']+)(?P<quote>["\'])')


@dataclass(frozen=True)
class Asset:
    body: bytes
    content_type: str
    etag: str
    version: str

    def headers(self, query: str = "") -> dict[str, str]:
        if self.content_type.startswith("text/html"):
            return {"Cache-Control": "no-store"}
        versioned = parse_qs(query, keep_blank_values=True).get("v") == [self.version]
        return {
            "Cache-Control": (
                "public, max-age=31536000, immutable" if versioned else "no-cache, must-revalidate"
            ),
            "ETag": self.etag,
        }

    def not_modified(self, validator: str | None) -> bool:
        if not validator or self.content_type.startswith("text/html"):
            return False
        return any(
            tag.strip().removeprefix("W/") in ("*", self.etag) for tag in validator.split(",")
        )


class StaticAssets:
    """Snapshot one release so HTML versions and served bytes cannot drift apart."""

    def __init__(self, files: Mapping[str, tuple[Path, str]]) -> None:
        contents = {url: (path.read_bytes(), ctype) for url, (path, ctype) in files.items()}
        digest = hashlib.sha256()
        for url, (body, _) in sorted(contents.items()):
            digest.update(url.encode() + b"\0" + hashlib.sha256(body).digest())
        self.version = digest.hexdigest()
        self._assets: dict[str, Asset] = {}
        for url, (body, ctype) in contents.items():
            if ctype.startswith("text/html"):
                body = _ATTRIBUTE.sub(
                    lambda match: (
                        match["prefix"] + self.url(match["url"].decode()).encode() + match["quote"]
                        if match["url"].decode() in contents
                        and not contents[match["url"].decode()][1].startswith("text/html")
                        else match[0]
                    ),
                    body,
                )
            self._assets[url] = Asset(
                body, ctype, f'"{hashlib.sha256(body).hexdigest()}"', self.version
            )

    def url(self, path: str) -> str:
        return f"{path}?v={self.version}"

    def get(self, path: str) -> Asset | None:
        return self._assets.get(path)
