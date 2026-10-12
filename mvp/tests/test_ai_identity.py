"""Managed identity selection for real MVP model calls."""
from io import BytesIO
import json
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from zavaforward_mvp.ai import Ai, SCOPE


class AiIdentityTests(unittest.TestCase):
    def test_container_app_selects_its_user_assigned_identity_and_caches_token(self):
        environment = {
            "IDENTITY_ENDPOINT": "http://localhost/identity",
            "IDENTITY_HEADER": "test-header",
            "AZURE_CLIENT_ID": "test-client",
        }
        with patch.dict("os.environ", environment, clear=True), patch(
            "urllib.request.urlopen",
            return_value=BytesIO(json.dumps({"access_token": "test-token", "expires_on": 9999999999}).encode()),
        ) as send:
            ai = Ai()
            self.assertEqual(ai._token(), "test-token")
            self.assertEqual(ai._token(), "test-token")
            self.assertEqual(send.call_count, 1)
            request = send.call_args.args[0]
            self.assertEqual(parse_qs(urlsplit(request.full_url).query), {
                "resource": [SCOPE], "api-version": ["2019-08-01"], "client_id": ["test-client"],
            })
            self.assertEqual(request.get_header("X-identity-header"), "test-header")

    def test_system_identity_keeps_the_imds_path_without_a_client_selector(self):
        with patch.dict("os.environ", {}, clear=True), patch(
            "urllib.request.urlopen",
            return_value=BytesIO(json.dumps({"access_token": "test-token"}).encode()),
        ) as send:
            self.assertEqual(Ai()._token(), "test-token")
            request = send.call_args.args[0]
            self.assertEqual(urlsplit(request.full_url).hostname, "169.254.169.254")
            self.assertNotIn("client_id", parse_qs(urlsplit(request.full_url).query))
            self.assertEqual(request.get_header("Metadata"), "true")
