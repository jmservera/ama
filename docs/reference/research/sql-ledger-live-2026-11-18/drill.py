"""DH-005 drill steps run inside the VNet against a throwaway Azure SQL database (issue #114, 2026-11-18).

usage: python drill.py erase     (erase one synthetic case on the drill database, write the register entry)
       python drill.py cleanup  (delete the throwaway blob container)
       python drill.py restored  (on the PITR-restored database: show state before and after reapply_deletions)
The database and blob container come from ZF_SQL_DATABASE and ZF_BLOB_CONTAINER; nothing here names live data.
Prints case ids, counts and booleans only; no personal data and no secrets.
"""

import json
import sys

from zava_forward.core import recovery
from zava_forward.core.factory import open_store

mode = sys.argv[1]
if mode in ("erase", "cleanup"):
    import os
    from azure.identity import ManagedIdentityCredential
    from azure.storage.blob import BlobServiceClient

    svc = BlobServiceClient(
        os.environ["ZF_BLOB_ACCOUNT_URL"],
        credential=ManagedIdentityCredential(client_id=os.environ["ZF_BLOB_CLIENT_ID"]),
    )
    if mode == "cleanup":
        svc.delete_container(os.environ["ZF_BLOB_CONTAINER"])
        print(json.dumps({"step": "drill-container-deleted"}))
        sys.exit(0)
    if os.environ["ZF_BLOB_CONTAINER"] != "evidence":
        try:
            svc.create_container(os.environ["ZF_BLOB_CONTAINER"])
        except Exception as error:
            print(json.dumps({"step": "container", "note": type(error).__name__}))
s = open_store()
case_id = sorted(s.cases)[0]


def state(label):
    c = s._case(case_id)
    r = c["resident"]
    erased = all(r.get(k) in (recovery.REDACTED, "", None) for k in recovery.PERSONAL if k in r)
    print(
        json.dumps(
            {"step": label, "case": case_id, "resident_erased": erased, "ledger": s.verify_ledger()}
        )
    )


if mode == "erase":
    state("before-erasure")
    entry = recovery.erase_resident(
        s, {"email": "drill-114@zava.invalid"}, case_id, "DH-005 drill 2026-11-18"
    )
    print(json.dumps({"step": "register-entry-written", "entry": entry}))
    state("after-erasure")
elif mode == "restored":
    state("restored-before-reapply")
    print(json.dumps({"step": "register-entries", "count": len(recovery.read_register(s))}))
    print(json.dumps({"step": "reapplied", "cases": recovery.reapply_deletions(s)}))
    state("restored-after-reapply")
    rep = s.verify_ledger_before_reliance(current_year=2026, seal_past_years=False)
    print(
        json.dumps(
            {
                "step": "per-year-reliance-check",
                "reliance_allowed": rep.get("reliance_allowed"),
                "years": sorted(rep.get("years", {})),
                "problems": sorted({p["code"] for p in rep.get("problems", [])}),
            }
        )
    )
