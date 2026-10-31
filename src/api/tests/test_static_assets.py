"""Release identity and conditional HTTP on the actual employee/resident handlers."""

import hashlib
import http.client
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from test_resident_demo_api import DemoTestCase
from test_ui_support import Base
from zava_forward.api.resident_preview.app import ResidentPreview, serve
from zava_forward.api.server import WEB as SHARED_WEB
from zava_forward.api.static_assets import StaticAssets

IMMUTABLE = "public, max-age=31536000, immutable"
REVALIDATE = "no-cache, must-revalidate"


class AssetLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        url = values.get("src" if tag == "script" else "href")
        if tag in ("script", "link") and url:
            self.urls.append(url)


def request(
    port: int, path: str, method: str = "GET", headers: dict[str, str] | None = None
) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request(method, path, headers=headers or {})
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read()
    finally:
        connection.close()


class CacheContract(unittest.TestCase):
    def check_cache(self, port: int, entry: str, headers: dict[str, str] | None = None) -> None:
        status, response, body = request(port, entry, headers=headers)
        self.assertEqual(status, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertNotIn("ETag", response)
        links = AssetLinks()
        links.feed(body.decode())
        self.assertTrue(links.urls)
        versions = {urlsplit(url).query for url in links.urls}
        self.assertEqual(len(versions), 1)
        self.assertRegex(next(iter(versions)), r"^v=[0-9a-f]{64}$")
        query = next(iter(versions))
        for method in ("GET", "HEAD"):
            status, response, content = request(
                port, entry + "?" + query, method, {**(headers or {}), "If-None-Match": "*"}
            )
            self.assertEqual(status, 200)
            self.assertEqual(response["Cache-Control"], "no-store")
            self.assertNotIn("ETag", response)
            self.assertEqual(content, body if method == "GET" else b"")
        for url in links.urls:
            status, response, body = request(port, url, headers=headers)
            self.assertEqual(status, 200, url)
            if urlsplit(url).path in ("/chat-widget.js", "/chat-widget.css"):
                self.assertEqual(body, (SHARED_WEB / urlsplit(url).path.lstrip("/")).read_bytes())
            self.assertEqual(response["Cache-Control"], IMMUTABLE)
            etag = f'"{hashlib.sha256(body).hexdigest()}"'
            self.assertEqual(response["ETag"], etag)
            for validator in (etag, f"W/{etag}", f'"unrelated", W/{etag}', "*"):
                status, cached, content = request(
                    port, url, headers={**(headers or {}), "If-None-Match": validator}
                )
                self.assertEqual((status, content), (304, b""), url)
                self.assertNotIn("Content-Length", cached)
                self.assertEqual(cached["ETag"], etag)
                self.assertEqual(cached["Cache-Control"], IMMUTABLE)
            status, _, content = request(
                port, url, headers={**(headers or {}), "If-None-Match": '"old-release"'}
            )
            self.assertEqual((status, content), (200, body))
            bare = urlsplit(url).path
            for path, policy in (
                (url, IMMUTABLE),
                (url + "&other=1", IMMUTABLE),
                (bare, REVALIDATE),
                (bare + "?v=old", REVALIDATE),
                (bare + "?v=", REVALIDATE),
                (bare + "?other=1", REVALIDATE),
                (url + "&" + query, REVALIDATE),
                (url + "&v=old", REVALIDATE),
                (url + "&v=", REVALIDATE),
            ):
                for method in ("GET", "HEAD"):
                    status, response, content = request(port, path, method, headers)
                    self.assertEqual((status, content), (200, body if method == "GET" else b""))
                    self.assertEqual(int(response["Content-Length"]), len(body))
                    self.assertEqual(response["ETag"], etag)
                    self.assertEqual(response["Cache-Control"], policy, path)
                    status, cached, content = request(
                        port, path, method, {**(headers or {}), "If-None-Match": etag}
                    )
                    self.assertEqual((status, content), (304, b""), path)
                    self.assertNotIn("Content-Length", cached)
                    self.assertEqual(cached["ETag"], etag)
                    self.assertEqual(cached["Cache-Control"], policy, path)


class EmployeeAssets(Base, CacheContract):
    def test_static_contract_and_all_html_entries(self) -> None:
        port = self.httpd.server_port
        for entry in ("/", "/welcome.html", "/app", "/index.html", "/law.html"):
            self.check_cache(port, entry)
        for path in ("/api/me", "/missing.js"):
            status, headers, _ = request(port, path, headers={"If-None-Match": "*"})
            self.assertIn(status, (401, 404))
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertNotIn("ETag", headers)


class ResidentAssets(DemoTestCase, CacheContract):
    def test_static_contract_and_no_store_denials(self) -> None:
        for entry in ("/", "/index.html"):
            self.check_cache(self.app.port, entry, {"Host": "demo.test.invalid"})
        for path, headers in (
            ("/demo/view", {"Host": "demo.test.invalid"}),
            ("/chat-widget.js?v=old", {"Host": "wrong.invalid", "If-None-Match": "*"}),
        ):
            status, response, _ = request(self.app.port, path, headers=headers)
            self.assertIn(status, (401, 403))
            self.assertEqual(response["Cache-Control"], "no-store")
            self.assertNotIn("ETag", response)


class PreviewAssets(CacheContract):
    def test_static_cache_contract(self) -> None:
        import threading

        app = ResidentPreview(None, Path("unused-synthetic-fixture"), "synthetic", "127.0.0.1", 0)
        server = serve(app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for entry in ("/", "/index.html"):
                self.check_cache(app.port, entry)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(5)


class ReleaseIdentity(unittest.TestCase):
    def test_headers_require_single_current_snapshot_version_and_html_never_caches(self) -> None:
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            script = root / "app.js"
            html = root / "index.html"
            script.write_bytes(b"release A")
            html.write_text('<script src="/app.js"></script>')
            files = {"/app.js": (script, "text/javascript"), "/index.html": (html, "text/html")}
            original = StaticAssets(files)
            current = "v=" + original.version
            asset = original.get("/app.js")
            page = original.get("/index.html")
            assert asset is not None and page is not None
            for query in (
                current,
                current + "&other=1",
                "other=1&" + current,
                f"v=%{ord(original.version[0]):02X}{original.version[1:]}",
            ):
                self.assertEqual(
                    asset.headers(query), {"Cache-Control": IMMUTABLE, "ETag": asset.etag}
                )
                self.assertEqual(page.headers(query), {"Cache-Control": "no-store"})
                self.assertFalse(page.not_modified("*"))
            for query in (
                "",
                "v",
                "v=",
                "v=old",
                "version=" + original.version,
                current + "&v=",
                current + "&v=old",
                current + "&" + current,
            ):
                self.assertEqual(
                    asset.headers(query), {"Cache-Control": REVALIDATE, "ETag": asset.etag}
                )
            script.write_bytes(b"release B")
            changed = StaticAssets(files).get("/app.js")
            assert changed is not None
            self.assertEqual(changed.headers(current)["Cache-Control"], REVALIDATE)
            self.assertEqual(asset.headers(current)["Cache-Control"], IMMUTABLE)
            self.assertEqual((asset.body, changed.body), (b"release A", b"release B"))

    def test_changes_names_shared_and_vendor_bytes_change_release_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            html = root / "index.html"
            html.write_text(
                '<script src="/vendor/leaflet.js"></script><script src="/chat-widget.js"></script>'
                '<link href="/style.css" rel="stylesheet"><a href="/app">Work</a>'
            )
            files = {"/index.html": (html, "text/html")}
            for name in ("vendor/leaflet.js", "chat-widget.js", "style.css"):
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"release A")
                files["/" + name] = (
                    path,
                    "text/css" if name.endswith(".css") else "text/javascript",
                )
            original = StaticAssets(files)
            self.assertEqual(
                original.version, StaticAssets(dict(reversed(list(files.items())))).version
            )
            for name in ("/vendor/leaflet.js", "/chat-widget.js", "/style.css"):
                path, _ = files[name]
                path.write_bytes(b"release B")
                changed = StaticAssets(files)
                self.assertNotEqual(original.version, changed.version)
                asset = changed.get("/index.html")
                assert asset is not None
                self.assertIn(changed.url(name).encode(), asset.body)
                self.assertIn(b'<a href="/app">', asset.body)
                old = original.get(name)
                assert old is not None
                self.assertEqual(old.body, b"release A")
                path.write_bytes(b"release A")
            renamed = dict(files)
            renamed["/renamed.js"] = renamed.pop("/chat-widget.js")
            self.assertNotEqual(original.version, StaticAssets(renamed).version)
