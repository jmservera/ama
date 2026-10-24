"""Sign-in providers.

PasswordProvider is the development provider: one shared local password and a
signed, stateless session cookie, so it works across restarts and replicas that
share ZF_SESSION_KEY. It is refused when ZF_ENV=production.

TrustedProxyProvider is for Azure Container Apps built-in authentication
(Entra ID). The platform signs the user in and injects the validated principal
as the X-MS-CLIENT-PRINCIPAL header. The service trusts that header only when it
can be reached solely through that ingress, so it is opt-in and fails closed:
no principal, a principal from another tenant or identity provider, no or
several staff app roles, or a malformed tenant or object id all
give no user. Roles come from the Entra app role, never from the staff file.
Nothing here validates a token signature; that is the platform's job (see the
README for what must be configured in Azure).
"""
import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import time

from zava_forward.core import identity

OID = ("oid", "http://schemas.microsoft.com/identity/claims/objectidentifier")
TID = ("tid", "http://schemas.microsoft.com/identity/claims/tenantid")
NAME = ("name", "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name")
EMAIL = ("preferred_username", "email", "upn", "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress")
ROLES = ("roles", "role", "http://schemas.microsoft.com/ws/2008/06/identity/claims/role")

DEFAULT_ROLE_MAP = {
    "ZavaForward.Coordinator": "Retrofit Coordinator",
    "ZavaForward.LiaisonOfficer": "Resident Liaison Officer",
    "ZavaForward.SafetyLiaison": "Building Safety Liaison",
    "ZavaForward.GrantsOfficer": "Grants and Evidence Officer",
    "ZavaForward.QualityInspector": "Quality Inspector",
    "ZavaForward.ProgrammeManager": "Retrofit Programme Manager",
    "ZavaForward.SupportOfficer": "Programme Support Officer",
    "ZavaForward.Contractor": "Contractor",
}
MAX_HEADER = 16384
ADMIN_ROLE = "ZavaForward.ApplicationAdmin"
ADMIN_EFFECTIVE_ROLE = "Retrofit Programme Manager"
RULE_ROLE_MAP = {
    "ZavaForward.RuleAuthor": "rule_author",
    "ZavaForward.RuleOwner": "rule_owner",
    "ZavaForward.RegulatoryChat": "regulatory_chat",
    "ZavaForward.AIRestart": "ai_restart",
}


def zf_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)


class PasswordProvider:
    name = "password"

    def __init__(self, store, password, key=None, ttl=28800):
        self.store, self.ttl = store, ttl
        self.salt = secrets.token_bytes(16)
        self.pw = zf_hash(password, self.salt)
        self.key = (key or os.environ.get("ZF_SESSION_KEY") or secrets.token_hex(32)).encode()

    def _sign(self, payload):
        return hmac.new(self.key, payload.encode(), hashlib.sha256).hexdigest()

    def login(self, email, password):
        u = self.store.staff.get((email or "").strip().lower())
        ok = hmac.compare_digest(zf_hash(password or "", self.salt), self.pw)
        if not u or not ok:
            return None
        payload = base64.urlsafe_b64encode(json.dumps(dict(e=u["email"].lower(), x=int(time.time()) + self.ttl)).encode()).decode()
        return payload + "." + self._sign(payload)

    def authenticate(self, headers):
        from http.cookies import SimpleCookie
        m = SimpleCookie(headers.get("Cookie", "")).get("zf_session")
        if not m or "." not in m.value:
            return None
        payload, sig = m.value.rsplit(".", 1)
        if not hmac.compare_digest(sig, self._sign(payload)):
            return None
        try:
            d = json.loads(base64.urlsafe_b64decode(payload.encode()))
        except (ValueError, binascii.Error):
            return None
        u = self.store.staff.get(d.get("e", ""))
        return dict(u, auth_provider=self.name, rule_roles=[]) if u and d.get("x", 0) > time.time() else None

    def account(self, headers, user):
        return {"name": user["name"], "email": user["email"], "provider": self.name}

    def logout_response(self, switch=False):
        return {"ok": True}


class TrustedProxyProvider:
    name = "trusted-proxy"

    def __init__(self, store, env=None):
        env = os.environ if env is None else env
        self.store = store
        self.tenant = identity.canonical_guid(env.get("ZF_ENTRA_TENANT_ID") or "")
        if not self.tenant:
            raise SystemExit("ZF_AUTH=trusted-proxy needs ZF_ENTRA_TENANT_ID as a tenant GUID.")
        if (env.get("ZF_TRUSTED_PROXY") or "") != "1":
            raise SystemExit("ZF_AUTH=trusted-proxy needs ZF_TRUSTED_PROXY=1, confirming the service is reachable only through the authenticating ingress.")
        self.role_map = dict(DEFAULT_ROLE_MAP)
        if env.get("ZF_ROLE_MAP"):
            self.role_map.update(json.loads(env["ZF_ROLE_MAP"]))

    @staticmethod
    def parse_principal(raw):
        if not raw or len(raw) > MAX_HEADER:
            return None
        try:
            p = json.loads(base64.b64decode(raw, validate=True))
        except (ValueError, binascii.Error):
            return None
        return p if isinstance(p, dict) and isinstance(p.get("claims"), list) else None

    @staticmethod
    def claims(p, names):
        out = []
        for c in p["claims"]:
            if isinstance(c, dict) and c.get("typ") in names and isinstance(c.get("val"), str):
                out.append(c["val"])
        return out

    def authenticate(self, headers):
        p = self.parse_principal(headers.get("X-MS-CLIENT-PRINCIPAL"))
        if not p or p.get("auth_typ") not in ("aad", "Bearer"):  # Container Apps reports Entra tokens as "aad" or "Bearer"
            return self._deny("no aad principal", p and p.get("auth_typ"))
        tid = {identity.canonical_guid(t) for t in self.claims(p, TID)}
        if tid != {self.tenant}:
            return self._deny("tenant mismatch", sorted(t for t in tid if t))
        oids = {identity.canonical_guid(o) for o in self.claims(p, OID)}
        if len(oids) != 1 or None in oids:
            return self._deny("need exactly one valid object id")
        claims = self.claims(p, ROLES)
        admin = ADMIN_ROLE in claims
        staff = {self.role_map[r] for r in claims if r in self.role_map and r not in RULE_ROLE_MAP and r != ADMIN_ROLE}
        if len(staff) > 1 or not (staff or admin):
            return self._deny("need one mapped staff role or the application admin role", sorted(set(claims)))
        staff_assigned = bool(staff)
        role = staff.pop() if staff else ADMIN_EFFECTIVE_ROLE
        if role == "Contractor":
            # A contractor's company binding is a separate approved data decision, not an Entra claim.
            return self._deny("contractor access needs a registered company binding")
        names, emails = self.claims(p, NAME), self.claims(p, EMAIL)
        return identity.principal(
            self.tenant, oids.pop(), role,
            name=names[0] if len(names) == 1 else "", email=emails[0] if len(emails) == 1 else "",
            roles=tuple(r for r in set(claims) if r in self.role_map or r in RULE_ROLE_MAP or r == ADMIN_ROLE),
            app_admin=admin, view_only=not staff_assigned) | dict(
            rule_roles=sorted({RULE_ROLE_MAP[r] for r in claims if r in RULE_ROLE_MAP}))

    @staticmethod
    def _deny(reason, detail=None):
        # Identifiers only (no names or emails), so operators can see why a signed-in user was refused.
        print(f"auth denied: {reason}: {detail}", flush=True)

    def account(self, headers, user):
        p = self.parse_principal(headers.get("X-MS-CLIENT-PRINCIPAL"))
        names, emails = self.claims(p, NAME), self.claims(p, EMAIL)
        return {"name": identity.display(names[0]) if len(names) == 1 and identity.display(names[0]) else user["name"],
                "email": identity.display(emails[0], 200) if len(emails) == 1 else "", "provider": self.name}

    def logout_response(self, switch=False):
        target = "/sign-in?switch=1" if switch else "/.auth/logout?post_logout_redirect_uri=%2F"
        return {"ok": True, "redirect": target}


def make_provider(store, password, env=None):
    env = os.environ if env is None else env
    kind = (env.get("ZF_AUTH") or "password").lower()
    prod = (env.get("ZF_ENV") or "").lower() == "production"
    if kind == "trusted-proxy":
        return TrustedProxyProvider(store, env)
    if kind != "password":
        raise SystemExit(f"Unknown ZF_AUTH {kind!r}. Use password or trusted-proxy.")
    if prod:
        raise SystemExit("ZF_ENV=production refuses the shared-password provider. Use ZF_AUTH=trusted-proxy.")
    return PasswordProvider(store, password)
