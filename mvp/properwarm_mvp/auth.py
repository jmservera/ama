"""Sign-in providers.

PasswordProvider is the development provider: one shared local password and a
signed, stateless session cookie, so it works across restarts and replicas that
share PW_SESSION_KEY. It is refused when PW_ENV=production.

TrustedProxyProvider is for Azure Container Apps built-in authentication
(Entra ID). The platform signs the user in and injects the validated principal
as the X-MS-CLIENT-PRINCIPAL header. The service trusts that header only when it
can be reached solely through that ingress, so it is opt-in and fails closed:
no principal, a principal from another tenant or identity provider, no or
several mapped app roles, or a person not provisioned in the staff list all
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

OID = ("oid", "http://schemas.microsoft.com/identity/claims/objectidentifier")
TID = ("tid", "http://schemas.microsoft.com/identity/claims/tenantid")
NAME = ("name", "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name")
EMAIL = ("preferred_username", "email", "upn", "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress")
ROLES = ("roles", "role", "http://schemas.microsoft.com/ws/2008/06/identity/claims/role")

DEFAULT_ROLE_MAP = {
    "ProperWarm.Coordinator": "Retrofit Coordinator",
    "ProperWarm.LiaisonOfficer": "Resident Liaison Officer",
    "ProperWarm.SafetyLiaison": "Building Safety Liaison",
    "ProperWarm.GrantsOfficer": "Grants and Evidence Officer",
    "ProperWarm.QualityInspector": "Quality Inspector",
    "ProperWarm.ProgrammeManager": "Retrofit Programme Manager",
    "ProperWarm.SupportOfficer": "Programme Support Officer",
    "ProperWarm.Contractor": "Contractor",
}
MAX_HEADER = 16384


def pw_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)


class PasswordProvider:
    name = "password"

    def __init__(self, store, password, key=None, ttl=28800):
        self.store, self.ttl = store, ttl
        self.salt = secrets.token_bytes(16)
        self.pw = pw_hash(password, self.salt)
        self.key = (key or os.environ.get("PW_SESSION_KEY") or secrets.token_hex(32)).encode()

    def _sign(self, payload):
        return hmac.new(self.key, payload.encode(), hashlib.sha256).hexdigest()

    def login(self, email, password):
        u = self.store.staff.get((email or "").strip().lower())
        ok = hmac.compare_digest(pw_hash(password or "", self.salt), self.pw)
        if not u or not ok:
            return None
        payload = base64.urlsafe_b64encode(json.dumps(dict(e=u["email"].lower(), x=int(time.time()) + self.ttl)).encode()).decode()
        return payload + "." + self._sign(payload)

    def authenticate(self, headers):
        from http.cookies import SimpleCookie
        m = SimpleCookie(headers.get("Cookie", "")).get("pw_session")
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
        return dict(u) if u and d.get("x", 0) > time.time() else None

    def logout_response(self):
        return {"ok": True}


class TrustedProxyProvider:
    name = "trusted-proxy"

    def __init__(self, store, env=None):
        env = os.environ if env is None else env
        self.store = store
        self.tenant = (env.get("PW_ENTRA_TENANT_ID") or "").strip().lower()
        if not self.tenant:
            raise SystemExit("PW_AUTH=trusted-proxy needs PW_ENTRA_TENANT_ID.")
        if (env.get("PW_TRUSTED_PROXY") or "") != "1":
            raise SystemExit("PW_AUTH=trusted-proxy needs PW_TRUSTED_PROXY=1, confirming the service is reachable only through the authenticating ingress.")
        self.role_map = dict(DEFAULT_ROLE_MAP)
        if env.get("PW_ROLE_MAP"):
            self.role_map.update(json.loads(env["PW_ROLE_MAP"]))
        self.email_fallback = env.get("PW_AUTH_EMAIL_FALLBACK") == "1"

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
        if not p or p.get("auth_typ") != "aad":
            return None
        tid = {t.lower() for t in self.claims(p, TID)}
        if tid != {self.tenant}:
            return None
        mapped = {self.role_map[r] for r in self.claims(p, ROLES) if r in self.role_map}
        if len(mapped) != 1:
            return None
        role = mapped.pop()
        oid = self.claims(p, OID)
        person = None
        if len(oid) == 1:
            person = next((s for s in self.store.staff.values() if s.get("oid", "").lower() == oid[0].lower()), None)
        if person is None and self.email_fallback:
            em = self.claims(p, EMAIL)
            if len(em) == 1:
                person = self.store.staff.get(em[0].lower())
        if person is None:
            return None
        return dict(person, role=role)

    def logout_response(self):
        return {"ok": True, "redirect": "/.auth/logout"}


def make_provider(store, password, env=None):
    env = os.environ if env is None else env
    kind = (env.get("PW_AUTH") or "password").lower()
    prod = (env.get("PW_ENV") or "").lower() == "production"
    if kind == "trusted-proxy":
        return TrustedProxyProvider(store, env)
    if kind != "password":
        raise SystemExit(f"Unknown PW_AUTH {kind!r}. Use password or trusted-proxy.")
    if prod:
        raise SystemExit("PW_ENV=production refuses the shared-password provider. Use PW_AUTH=trusted-proxy.")
    return PasswordProvider(store, password)
