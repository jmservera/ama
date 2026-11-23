"""Live run: IoT Hub registry adapter (SAS) plus Key Vault durable credential store (#2128).

Usage: live_durable.py <hub-name> <vault-name>. Throwaway resources only; prints no secret.
"""

import io
import json
import logging
import sys

from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

sys.path.insert(0, "src/core/tests")
from test_device_identity import sensors  # noqa: E402
from zava_forward.core.synthetic import device_identity as di  # noqa: E402
from zava_forward.core.synthetic import device_registry_azure as dra  # noqa: E402
from zava_forward.core.synthetic import live_provisioning as lp  # noqa: E402

hub, vault = sys.argv[1], sys.argv[2]
cred = AzureCliCredential()


class MemoryVault:
    """Stand-in with the SecretClient surface used by the backend; used when the vault is private."""

    def __init__(self) -> None:
        self.items: dict[str, tuple[str, dict[str, str]]] = {}

    def set_secret(self, name, value, tags):  # type: ignore[no-untyped-def]
        self.items[name] = (value, tags)

    def begin_delete_secret(self, name):  # type: ignore[no-untyped-def]
        self.items.pop(name, None)
        return type("P", (), {"wait": lambda self: None})()

    def list_properties_of_secrets(self):  # type: ignore[no-untyped-def]
        return [type("S", (), {"name": n, "tags": t})() for n, (_, t) in self.items.items()]

    def get_secret(self, name):  # type: ignore[no-untyped-def]
        return type("V", (), {"value": self.items[name][0]})()


client = MemoryVault() if vault == "memory" else SecretClient(f"https://{vault}.vault.azure.net", cred)
out_mode = "memory-backend" if vault == "memory" else "key-vault"
buf = io.StringIO()
logging.basicConfig(stream=buf, level=logging.DEBUG)
run = "live-2128-demo"
manifest = di.plan(run, di.CREDENTIAL_OWNER_ROLE, sensors(3))
spec = dra.EnrollmentSpec(run, tuple(dra.SasEnrollment(i.device_id) for i in manifest.identities))
out: dict[str, object] = {"backend": out_mode, "vault_before": len(list(client.list_properties_of_secrets()))}
values: list[str] = []
with dra.AzureIotHubRegistry(f"{hub}.azure-devices.net", spec, credential=cred) as reg:
    store = lp.DurableSasCredentialStore(lp.KeyVaultSecretBackend(client))
    provisioned = di.provision(manifest, reg, store)
    out["hub_after_provision"] = sorted(reg.list_run(run))
    names = [p.name for p in client.list_properties_of_secrets()]
    out["vault_after_provision"] = len(names)
    out["vault_names_free_of_device_ids"] = not any("SYN-" in n or "ZNH" in n for n in names)
    values = [client.get_secret(n).value or "" for n in names]
    out["stored_value_lengths_ok"] = all(len(v) >= 40 for v in values)
    out["manifest_has_no_key"] = not any(v and v in repr(provisioned) for v in values)
    restarted = lp.DurableSasCredentialStore(lp.KeyVaultSecretBackend(client))
    out["restart_recovered_refs"] = restarted.active_count()
    receipt = di.teardown(provisioned, reg, restarted)
    out["receipt_zero_residual"] = receipt.verified_zero_residual
    out["hub_after_teardown"] = list(reg.list_run(run))
out["vault_after_teardown"] = len(list(client.list_properties_of_secrets()))
logs = buf.getvalue()
out["log_bytes"] = len(logs)
out["log_has_stored_value"] = any(v and v in logs for v in values)
print(json.dumps(out, indent=1))
open("/tmp/e2128/live2128.log", "w").write(logs)
