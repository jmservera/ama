"""Diagnose which identity keys differ between signed-in principal and roster (values hashed)."""
import hashlib
from playwright.sync_api import sync_playwright
from common import *
h=lambda v: (hashlib.sha256(str(v).encode()).hexdigest()[:8] if v else "<empty>")
with sync_playwright() as p:
    b,pg=session(p)
    s,me=call(pg,"GET","/api/me")
    print("me keys",sorted(me.keys()) if isinstance(me,dict) else me)
    print({k:h(me.get(k)) for k in ("email","code","oid","upn","name","role") if isinstance(me,dict)})
    s,d=call(pg,"GET","/api/cases/ZF-2025-0331")
    for o in d["nomination_permissions"]["staff_owners"]:
        print("owner keys",sorted(o.keys()),{k:h(o.get(k)) for k in ("email","code","oid")})
    u=me["user"]; print("user keys",sorted(u.keys()),{k:h(u.get(k)) for k in ("email","code","oid","name","role")})
    print("staff", str(me["staff"])[:200].replace("@","[at]"))
    r=[x for x in me["staff"] if x.get("email")==u.get("email")]
    print("roster rows for user",len(r),[sorted(x.keys()) for x in r],[{k:h(x.get(k)) for k in ("code","name","role")} for x in r])
    print("owner==user email", [o["email"].lower()==str(u.get("email")).lower() for o in d["nomination_permissions"]["staff_owners"]])
    b.close()
