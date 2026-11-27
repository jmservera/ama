"""Public welcome page: the resident site link, pictures and favicon.

The platform sign-in bypass serves only a short list of paths, so the page cannot
link to extra image files. Its pictures and favicon are packaged beside it and inlined as data
URIs when the page is served instead.

The resident site is a different host, so its address is configuration, never
hard-coded. The page carries two marked blocks: a link and a plain-words fallback.
Exactly one of them is served.
"""

import base64
import functools
import html
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import ParseResult, urlparse, urlunparse

WEB = Path(__file__).resolve().parent / "web"
LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
MARKER = b"__RESIDENT_SITE_URL__"
LINK_BLOCK = b"resident-site"
FALLBACK_BLOCK = b"no-resident-site"
PHOTOS = {
    b"__WELCOME_STREET__": "welcome-street.webp",
    b"__WELCOME_ESTATE__": "welcome-estate.webp",
    b"__WELCOME_DUSK__": "welcome-dusk.webp",
    b"__WELCOME_SHIELD__": "welcome-shield.webp",
}
ICONS_MARKER = b"__WELCOME_ICONS__"
ICONS_FILE = "welcome-icons.svg"
FAVICON_MARKER = b"__WELCOME_FAVICON__"
FAVICON_FILE = "favicon-employee.png"
SPRITE = re.compile(rb"<svg[^>]*>(.*)</svg>", re.S)


def _parse(raw: str) -> ParseResult | None:
    try:
        parts = urlparse(raw)
        _ = parts.port  # raises ValueError for a malformed port
    except ValueError:
        return None
    return parts


def resident_site_url(env: Mapping[str, str] | None = None) -> str:
    """Return the address in ZF_RESIDENT_SITE_URL, or "" when it is not set.

    Only a plain https address is accepted (http only for a loopback development
    site). A value that could carry credentials, a query or a script stops start-up.
    """
    source = os.environ if env is None else env
    raw = (source.get("ZF_RESIDENT_SITE_URL") or "").strip()
    if not raw:
        return ""
    parts = _parse(raw)
    if parts is not None and parts.hostname:
        loopback_http = parts.scheme == "http" and parts.hostname in LOOPBACK
        carries_more = parts.username or parts.password or parts.params
        if (parts.scheme == "https" or loopback_http) and not (
            carries_more or parts.query or parts.fragment
        ):
            return urlunparse((parts.scheme, parts.netloc, parts.path or "/", "", "", ""))
    sys.exit(
        "ZF_RESIDENT_SITE_URL must be an https address such as https://residents.example.org/ "
        "with no credentials, query or fragment (http only for 127.0.0.1 or localhost)."
    )


def _block(name: bytes) -> re.Pattern[bytes]:
    return re.compile(b"<!--" + name + b"-->.*?<!--/" + name + b"-->", re.S)


@functools.cache
def media() -> tuple[tuple[bytes, bytes], ...]:
    """Marker and replacement pairs for the page's media, read once per process."""
    pairs = [
        (marker, b"data:image/webp;base64," + base64.b64encode((WEB / name).read_bytes()))
        for marker, name in PHOTOS.items()
    ]
    sprite = SPRITE.search((WEB / ICONS_FILE).read_bytes())
    if sprite is None:
        raise ValueError(f"{ICONS_FILE} is not an SVG file")
    favicon = b"data:image/png;base64," + base64.b64encode((WEB / FAVICON_FILE).read_bytes())
    return (*pairs, (ICONS_MARKER, sprite.group(1)), (FAVICON_MARKER, favicon))


def render(body: bytes, resident_url: str) -> bytes:
    """Serve the resident link when a site is configured, otherwise its fallback text."""
    keep, drop = (LINK_BLOCK, FALLBACK_BLOCK) if resident_url else (FALLBACK_BLOCK, LINK_BLOCK)
    body = _block(drop).sub(b"", body)
    body = body.replace(b"<!--" + keep + b"-->", b"").replace(b"<!--/" + keep + b"-->", b"")
    body = body.replace(MARKER, html.escape(resident_url, quote=True).encode())
    for marker, replacement in media():
        body = body.replace(marker, replacement)
    return body
