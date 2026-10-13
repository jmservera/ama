import io
import unittest
from email.message import Message
from urllib.error import HTTPError, URLError
from unittest.mock import MagicMock

from zavaforward_mvp import profile


class PhotoTests(unittest.TestCase):
    def opener(self, data=b"\x89PNG\r\n\x1a\nphoto", kind="image/png"):
        opener = MagicMock()
        response = opener.open.return_value.__enter__.return_value
        response.headers = Message()
        response.headers["Content-Type"] = kind
        response.read.return_value = data
        return opener

    def test_own_photo_has_fixed_url_timeout_and_no_redirects(self):
        opener = self.opener()
        raw, kind = profile.own_photo("fake-token", opener)
        self.assertEqual((raw, kind), (b"\x89PNG\r\n\x1a\nphoto", "image/png"))
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, profile.PHOTO_URL)
        self.assertEqual(opener.open.call_args.kwargs["timeout"], 10)
        self.assertIsNone(profile.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.example.test"))

    def test_jpeg_and_png_only_with_valid_magic_and_size(self):
        self.assertEqual(profile.own_photo("t", self.opener(b"\xff\xd8\xffphoto", "image/jpeg"))[1], "image/jpeg")
        for data, kind in ((b"html", "image/png"), (b"\x89PNG\r\n\x1a\n", "text/html"), (b"\x89PNG\r\n\x1a\n" + b"x" * profile.MAX_PHOTO, "image/png")):
            with self.subTest(kind=kind), self.assertRaises(profile.PhotoError) as error:
                profile.own_photo("t", self.opener(data, kind))
            self.assertEqual(error.exception.status, 502)

    def test_expected_errors_are_explicit_and_never_include_upstream_body(self):
        for code in (404, 401, 403, 302, 500):
            opener = self.opener()
            opener.open.side_effect = HTTPError(profile.PHOTO_URL, code, "secret-upstream-body", {}, io.BytesIO(b"private"))
            with self.subTest(code=code), self.assertRaises(profile.PhotoError) as error:
                profile.own_photo("secret-token", opener)
            self.assertEqual(error.exception.status, code if code in (404, 401, 403) else 502)
            self.assertNotIn("secret", str(error.exception))
            self.assertNotIn("private", str(error.exception))

    def test_missing_token_network_and_timeout(self):
        with self.assertRaises(profile.PhotoError) as error:
            profile.own_photo(None)
        self.assertEqual(error.exception.status, 503)
        for failure in (URLError("private details"), TimeoutError()):
            opener = self.opener()
            opener.open.side_effect = failure
            with self.assertRaises(profile.PhotoError) as error:
                profile.own_photo("t", opener)
            self.assertEqual(error.exception.status, 502)
