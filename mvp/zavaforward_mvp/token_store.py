"""Renew the private EasyAuth Blob SAS without account keys or credential output."""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

CONTAINER = "auth-tokens"
SECRET = "entra-token-store-sas"


def put_secret(vault_uri, credential, value, expiry):
    parts = urlparse(vault_uri)
    if parts.scheme != "https" or not parts.hostname or not parts.hostname.endswith(".vault.azure.net") or parts.path.strip("/") or parts.query or parts.fragment:
        raise ValueError("KEY_VAULT_URI must be an Azure Key Vault base URL.")
    token = credential.get_token("https://vault.azure.net/.default").token
    body = json.dumps({
        "value": value, "contentType": "application/x-easyauth-blob-sas",
        "attributes": {"enabled": True, "exp": int(expiry.timestamp())},
        "tags": {"dataClassification": "authentication-secrets", "managedBy": "token-store-renewal"},
    }).encode()
    request = Request(vault_uri.rstrip("/") + "/secrets/" + SECRET + "?api-version=7.4",
                      data=body, method="PUT",
                      headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError("Key Vault did not accept the token-store update.")
        response.read()


def renew(account_name, client, credential, generate_sas, permission, writer=put_secret, now=None, vault_uri=None):
    now = now or datetime.now(timezone.utc)
    start, expiry = now - timedelta(minutes=5), now + timedelta(days=5)
    key = client.get_user_delegation_key(start, expiry)
    sas = generate_sas(account_name, CONTAINER, user_delegation_key=key,
                       permission=permission, start=start, expiry=expiry, protocol="https")
    writer(vault_uri, credential, f"https://{account_name}.blob.core.windows.net/{CONTAINER}?{sas}", expiry)
    return {"status": "token-store-renewed", "expiresAt": expiry.isoformat(), "container": CONTAINER}


def main():
    from azure.core.exceptions import AzureError
    from azure.identity import ManagedIdentityCredential
    from azure.storage.blob import BlobServiceClient, ContainerSasPermissions, generate_container_sas
    try:
        account = os.environ["TOKEN_STORAGE_ACCOUNT"]
        credential = ManagedIdentityCredential(client_id=os.environ["AZURE_CLIENT_ID"])
        with BlobServiceClient(f"https://{account}.blob.core.windows.net", credential=credential,
                               logging_enable=False) as client:
            result = renew(account, client, credential, generate_container_sas,
                           ContainerSasPermissions(read=True, write=True, delete=True),
                           vault_uri=os.environ["KEY_VAULT_URI"])
        print(json.dumps(result), flush=True)
    except (AzureError, URLError, OSError, ValueError, KeyError, RuntimeError):
        # SDK/HTTP exception bodies can include credential-bearing URLs.
        print('{"status":"token-store-renewal-failed","error":"Check identity permissions, network access and job configuration."}', file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
