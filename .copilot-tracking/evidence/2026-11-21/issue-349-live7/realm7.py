"""Redacted realm discovery for the two test accounts (no identifiers printed)."""
import json, os, urllib.request
from urllib.parse import urlparse
out = {}
for label, f in (("test", "~/.ama-test-user"), ("resident", "~/.ama-resident-test-user")):
    lines = [l.strip() for l in open(os.path.expanduser(f)) if l.strip()]
    req = urllib.request.Request("https://login.microsoftonline.com/common/GetCredentialType",
        data=json.dumps({"Username": lines[0]}).encode(), headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    ep = d.get("Credentials", {}).get("FederationRedirectUrl", "")
    out[label] = {"IfExistsResult": d.get("IfExistsResult"), "fed_host": urlparse(ep).netloc,
                  "has_password": d.get("Credentials", {}).get("HasPassword")}
print(json.dumps(out, indent=1))
