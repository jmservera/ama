import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from zava_forward.orchestrator import token_store


class RenewalTests(unittest.TestCase):
    def test_delegation_bounds_container_permissions_and_https(self):
        client, credential, generate, writer = (MagicMock() for _ in range(4))
        generate.return_value = "private-sas"
        now = datetime(2026, 10, 12, tzinfo=timezone.utc)
        result = token_store.renew("teststorage", client, credential, generate, "rwd",
                                   writer, now, "https://testvault.vault.azure.net")
        start, expiry = client.get_user_delegation_key.call_args.args
        self.assertEqual(start, now - timedelta(minutes=5))
        self.assertEqual(expiry, now + timedelta(days=5))
        self.assertLess(expiry - start, timedelta(days=7))
        self.assertEqual(generate.call_args.args, ("teststorage", "auth-tokens"))
        self.assertEqual(generate.call_args.kwargs["permission"], "rwd")
        self.assertEqual(generate.call_args.kwargs["protocol"], "https")
        self.assertEqual(writer.call_args.args[3], expiry)
        self.assertNotIn("private-sas", json.dumps(result))

    def test_failed_delegation_or_generation_never_overwrites_existing_secret(self):
        for step in ("delegation", "generation"):
            client, credential, generate, writer = (MagicMock() for _ in range(4))
            if step == "delegation":
                client.get_user_delegation_key.side_effect = RuntimeError("fail")
            else:
                generate.side_effect = RuntimeError("fail")
            with self.subTest(step=step), self.assertRaises(RuntimeError):
                token_store.renew("teststorage", client, credential, generate, "rwd", writer)
            writer.assert_not_called()

    def test_secret_put_is_fixed_named_authenticated_and_expiring(self):
        credential = MagicMock()
        credential.get_token.return_value.token = "fake-keyvault-token"
        expiry = datetime(2026, 10, 17, tzinfo=timezone.utc)
        with patch("zava_forward.orchestrator.token_store.urlopen") as open_url:
            open_url.return_value.__enter__.return_value.status = 200
            token_store.put_secret("https://testvault.vault.azure.net/", credential, "private-sas", expiry)
        request = open_url.call_args.args[0]
        self.assertEqual(request.full_url, "https://testvault.vault.azure.net/secrets/entra-token-store-sas?api-version=7.4")
        self.assertEqual(request.method, "PUT")
        payload = json.loads(request.data)
        self.assertEqual(payload["attributes"]["exp"], int(expiry.timestamp()))
        self.assertEqual(payload["tags"]["dataClassification"], "authentication-secrets")
        credential.get_token.assert_called_once_with("https://vault.azure.net/.default")

    def test_vault_must_be_a_fixed_https_azure_base_url(self):
        for url in ("http://testvault.vault.azure.net", "https://example.test", "https://testvault.vault.azure.net/secrets/other", "https://testvault.vault.azure.net?redirect=x"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                token_store.put_secret(url, MagicMock(), "secret", datetime.now(timezone.utc))
