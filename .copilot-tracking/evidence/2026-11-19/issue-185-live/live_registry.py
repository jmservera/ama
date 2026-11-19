"""Live run of the keyless IoT Hub registry adapter against a throwaway hub (#185)."""
import json, logging, sys, io
sys.path.insert(0, "src/core/tests")
from azure.identity import ManagedIdentityCredential
from test_device_identity import FakeStore, sensors
from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_registry_azure as dra

host = sys.argv[1] + ".azure-devices.net"
buf = io.StringIO()
logging.basicConfig(stream=buf, level=logging.DEBUG)
run = "live-185-demo"
sens = sensors(3)
man = di.plan(run, di.CREDENTIAL_OWNER_ROLE, sens)
spec = dra.EnrollmentSpec(run, tuple(dra.SasEnrollment(i.device_id) for i in man.identities))
out = {}
with dra.AzureIotHubRegistry(host, spec, credential=ManagedIdentityCredential()) as reg:
    store = FakeStore()
    m = di.provision(man, reg, store)
    out["provisioned"] = sorted(reg.list_run(run))
    out["owner_tag_ok"] = all(reg.run_of(i.device_id) == run for i in m.identities)
    out["one_to_one"] = len({i.device_id for i in m.identities}) == len({i.home_id for i in m.identities}) == len(m.identities)
    rcpt = di.teardown(m, reg, store)
    out["after_teardown"] = list(reg.list_run(run))
    out["receipt_zero_residual"] = rcpt.verified_zero_residual
logs = buf.getvalue()
out["log_bytes"] = len(logs)
print(json.dumps(out, indent=1))
open("/tmp/live185.log", "w").write(logs)
