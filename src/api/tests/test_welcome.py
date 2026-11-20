"""Public welcome page: resident link, inlined pictures and anonymous-visitor paths."""

import http.client
import re
import unittest
from html.parser import HTMLParser

from test_accessibility_baseline import ROOT, WEB, ratio, token
from test_ui_support import Base
from zava_forward.api import welcome

PAGE = (WEB / "welcome.html").read_bytes()
LINK = b'<!--resident-site--><a href="__RESIDENT_SITE_URL__">Open</a><!--/resident-site-->'
FALLBACK = b"<!--no-resident-site-->Ask your housing officer.<!--/no-resident-site-->"
# Foreground and background colour tokens the page pairs, as written in style.css.
PALETTE_PAIRS = (
    ("lp-ink", "lp-paper"),
    ("lp-ink", "lp-sage"),
    ("lp-paper", "lp-forest"),
    ("lp-paper", "lp-moss"),
    ("lp-paper", "lp-green"),
    ("lp-sage", "lp-forest"),
    ("lp-amber", "lp-forest"),
    ("lp-forest", "lp-amber"),
    ("lp-forest", "lp-sage"),
    ("lp-forest", "lp-paper"),
    ("lp-amber-ink", "lp-amber-tint"),
)


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.uses: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "img":
            self.images.append(values)
        if tag == "use":
            self.uses.append(values["href"] or "")
        for name in ("src", "href"):
            if values.get(name) and tag != "use":
                self.urls.append(values[name] or "")


def references(body: bytes) -> References:
    found = References()
    found.feed(body.decode())
    return found


class ResidentSiteUrl(unittest.TestCase):
    def test_unset_means_no_link(self) -> None:
        self.assertEqual(welcome.resident_site_url({}), "")
        self.assertEqual(welcome.resident_site_url({"ZF_RESIDENT_SITE_URL": "  "}), "")

    def test_https_and_loopback_http_are_accepted(self) -> None:
        for raw, expected in (
            ("https://residents.example.org", "https://residents.example.org/"),
            ("https://residents.example.org:8443/home", "https://residents.example.org:8443/home"),
            ("http://127.0.0.1:8090/", "http://127.0.0.1:8090/"),
            ("http://localhost/", "http://localhost/"),
        ):
            with self.subTest(raw=raw):
                self.assertEqual(welcome.resident_site_url({"ZF_RESIDENT_SITE_URL": raw}), expected)

    def test_anything_that_could_misdirect_a_visitor_stops_start_up(self) -> None:
        for raw in (
            "http://residents.example.org/",
            "https://user:secret@residents.example.org/",
            "https://residents.example.org/?next=//evil.example",
            "https://residents.example.org/#top",
            "javascript:alert(1)",
            "//residents.example.org/",
            "https://residents.example.org:notaport/",
            "residents.example.org",
        ):
            with self.subTest(raw=raw), self.assertRaises(SystemExit):
                welcome.resident_site_url({"ZF_RESIDENT_SITE_URL": raw})


class Render(unittest.TestCase):
    def test_exactly_one_resident_block_is_served_and_the_address_is_escaped(self) -> None:
        linked = welcome.render(LINK + FALLBACK, "https://r.example/a&b/")
        self.assertEqual(linked, b'<a href="https://r.example/a&amp;b/">Open</a>')
        self.assertEqual(welcome.render(LINK + FALLBACK, ""), b"Ask your housing officer.")

    def test_served_page_has_no_template_marker_and_carries_its_pictures(self) -> None:
        for resident in ("", "https://residents.example.org/"):
            with self.subTest(resident=resident):
                body = welcome.render(PAGE, resident)
                self.assertNotRegex(body.decode(), r"__[A-Z_]+__|<!--")
                self.assertEqual(body.count(b'src="data:image/webp;base64,'), 4)
                self.assertEqual(b"https://residents.example.org/" in body, bool(resident))


class PublicSurface(unittest.TestCase):
    """Anonymous visitors can fetch only a short list of paths, so the page may use no others."""

    def test_page_uses_only_paths_that_skip_sign_in(self) -> None:
        bicep = (ROOT / "infra" / "modules" / "containerapps.bicep").read_text()
        listed = re.search(r"excludedPaths: \[(.*?)\]", bicep)
        self.assertIsNotNone(listed)
        public = set(re.findall(r"'(/[^']*)'", listed.group(1) if listed else ""))
        urls = references(welcome.render(PAGE, "https://residents.example.org/")).urls
        paths = {u.partition("?")[0] for u in urls if u.startswith("/")}
        self.assertLessEqual(paths, public)
        self.assertTrue({"/sign-in", "/style.css", "/zava-logo.png"} <= paths)
        for url in urls:
            self.assertTrue(
                url.startswith(("/", "#", "data:", "https://residents.example.org/")), url
            )

    def test_every_picture_has_dimensions_and_alternative_text(self) -> None:
        found = references(PAGE)
        self.assertGreaterEqual(len(found.images), 5)
        for image in found.images:
            with self.subTest(src=(image.get("src") or "")[:40]):
                self.assertTrue(image.get("width") and image.get("height"))
                self.assertIn("alt", image)

    def test_every_icon_used_exists_in_the_sprite(self) -> None:
        sprite = (WEB / "welcome-icons.svg").read_text()
        for ref in set(references(PAGE).uses):
            self.assertIn(f'<symbol id="{ref.lstrip("#")}"', sprite, ref)

    def test_sign_in_options_cover_employees_contractors_and_residents(self) -> None:
        text = PAGE.decode()
        self.assertIn('href="/sign-in?switch=1"', text)
        self.assertEqual(text.count('class="btn" href="/sign-in"'), 2)
        self.assertIn('href="__RESIDENT_SITE_URL__"', text)


class Palette(unittest.TestCase):
    def test_text_pairs_meet_the_workbench_contrast_floor(self) -> None:
        for foreground, background in PALETTE_PAIRS:
            self.assertGreaterEqual(
                ratio(token(foreground), token(background)), 4.5, f"{foreground} on {background}"
            )


def fetch(server: Base, path: str) -> tuple[http.client.HTTPResponse, str]:
    connection = http.client.HTTPConnection("127.0.0.1", server.httpd.server_port, timeout=5)
    connection.request("GET", path)
    response = connection.getresponse()
    return response, response.read().decode()


class ServedPage(Base):
    ENV = {"ZF_RESIDENT_SITE_URL": "https://residents.example.org/"}

    def test_both_entry_paths_serve_the_rendered_page(self) -> None:
        for path in ("/", "/welcome.html"):
            with self.subTest(path=path):
                response, body = fetch(self, path)
                self.assertEqual(response.getheader("Cache-Control"), "no-store")
                self.assertIn('href="https://residents.example.org/"', body)
                self.assertNotIn("__RESIDENT_SITE_URL__", body)
                self.assertNotIn("no-resident-site", body)


class ServedPageWithoutResidentSite(Base):
    ENV = {"ZF_RESIDENT_SITE_URL": ""}

    def test_page_explains_where_to_ask_for_the_resident_site(self) -> None:
        _, body = fetch(self, "/")
        self.assertIn("Ask your housing officer for the address of the resident site.", body)
        self.assertNotIn("Open the resident site", body)


if __name__ == "__main__":
    unittest.main()
