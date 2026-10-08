import base64
import json
import os
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from properwarm_mvp import auth
from properwarm_mvp.server import App, make_handler
from properwarm_mvp.store import Store

TENANT = "11111111-2222-3333-4444-555555555555"
OID_SAM = "aaaaaaaa-0000-0000-0000-000000000001"
ENV = dict(PW_AUTH="trusted-proxy", PW_TRUSTED_PROXY="1", PW_ENTRA_TENANT_ID=TENANT)


def principal(roles=("ProperWarm.LiaisonOfficer",), oid=OID_SAM, tid=TENANT, typ="aad", email=None):
    claims = [dict(typ="roles", val=r) for r in roles]
    if oid:
        claims.append(dict(typ="http://schemas.microsoft.com/identity/claims/objectidentifier", val=oid))
    if tid:
        claims.append(dict(typ="http://schemas.microsoft.com/identity/claims/tenantid", val=tid))
    if email:
        claims.append(dict(typ="preferred_username", val=email))
    return base64.b64encode(json.dumps(dict(auth_typ=typ, name_typ="name", role_typ="roles", claims=claims)).encode()).decode()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = json.loads(json.dumps(test_mvp.DATA))
        d["staff"][0]["oid"] = OID_SAM
        d["staff"].append(dict(code="CON-1", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd",
                               oid="aaaaaaaa-0000-0000-0000-000000000009"))
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(d))
        self.store = Store(str(p))

    def tearDown(self):
        self.tmp.cleanup()


class TrustedProxyTests(Base):
    def prov(self, **extra):
        return auth.TrustedProxyProvider(self.store, dict(ENV, **extra))

    def who(self, header, **extra):
        return self.prov(**extra).authenticate({"X-MS-CLIENT-PRINCIPAL": header} if header is not None else {})

    def test_valid_principal_maps_role_from_app_role(self):
        u = self.who(principal())
        self.assertEqual((u["code"], u["role"]), ("RLO-01", "Resident Liaison Officer"))
        u = self.who(principal(roles=("ProperWarm.ProgrammeManager",)))
        self.assertEqual(u["role"], "Retrofit Programme Manager")
        self.assertEqual(u["code"], "RLO-01")

    def test_contractor_role_and_custom_map(self):
        u = self.who(principal(roles=("ProperWarm.Contractor",), oid="aaaaaaaa-0000-0000-0000-000000000009"))
        self.assertEqual((u["role"], u["contractor"]), ("Contractor", "Test Ltd"))
        u = self.who(principal(roles=("Warm.Coord",)), PW_ROLE_MAP=json.dumps({"Warm.Coord": "Retrofit Coordinator"}))
        self.assertEqual(u["role"], "Retrofit Coordinator")

    def test_fails_closed(self):
        self.assertIsNone(self.who(None))
        self.assertIsNone(self.who(""))
        self.assertIsNone(self.who("not base64 !!"))
        self.assertIsNone(self.who(base64.b64encode(b"[1,2]").decode()))
        self.assertIsNone(self.who(principal(typ="google")))
        self.assertIsNone(self.who(principal(tid="99999999-2222-3333-4444-555555555555")))
        self.assertIsNone(self.who(principal(tid=None)))
        self.assertIsNone(self.who(principal(roles=())))
        self.assertIsNone(self.who(principal(roles=("Unmapped.Role",))))
        self.assertIsNone(self.who(principal(roles=("ProperWarm.Contractor", "ProperWarm.ProgrammeManager"))))
        self.assertIsNone(self.who(principal(oid="not-a-provisioned-person")))
        self.assertIsNone(self.who(principal(oid=None)))
        self.assertIsNone(self.who("A" * 20000))

    def test_email_match_only_when_enabled(self):
        h = principal(oid="unknown-oid", email="sam@example.test")
        self.assertIsNone(self.who(h))
        self.assertEqual(self.who(h, PW_AUTH_EMAIL_FALLBACK="1")["code"], "RLO-01")

    def test_role_comes_from_token_not_staff_file(self):
        self.store.staff["sam@example.test"]["role"] = "Retrofit Programme Manager"
        self.assertEqual(self.who(principal())["role"], "Resident Liaison Officer")

    def test_refuses_to_start_without_tenant_or_confirmation(self):
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(self.store, dict(ENV, PW_ENTRA_TENANT_ID=""))
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(self.store, dict(ENV, PW_TRUSTED_PROXY=""))

    def test_production_refuses_password_provider(self):
        with self.assertRaises(SystemExit):
            auth.make_provider(self.store, "x", dict(PW_ENV="production"))
        self.assertEqual(auth.make_provider(self.store, "x", {}).name, "password")
        self.assertEqual(auth.make_provider(self.store, "x", dict(ENV, PW_ENV="production")).name, "trusted-proxy")


class ProxyHttpTests(Base):
    def setUp(self):
        super().setUp()
        prov = auth.TrustedProxyProvider(self.store, ENV)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, provider=prov)))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def call(self, path, headers=None, body=None):
        req = urllib.request.Request(self.base + path, json.dumps(body).encode() if body is not None else None, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_no_principal_is_401_and_password_login_is_gone(self):
        self.assertEqual(self.call("/api/me")[0], 401)
        self.assertEqual(self.call("/api/login", {}, {"email": "sam@example.test", "password": "x"})[0], 404)
        self.assertEqual(self.call("/api/cases", {"Cookie": "pw_session=anything"})[0], 401)

    def test_principal_gives_role_and_projection(self):
        code, me = self.call("/api/me", {"X-MS-CLIENT-PRINCIPAL": principal()})
        self.assertEqual((code, me["user"]["role"]), (200, "Resident Liaison Officer"))
        con = {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ProperWarm.Contractor",), oid="aaaaaaaa-0000-0000-0000-000000000009")}
        self.assertEqual(self.call("/api/stats", con)[0], 403)
        self.assertEqual(self.call("/api/cases", con)[0], 200)

    def test_post_needs_csrf_header_and_logout_redirects(self):
        h = {"X-MS-CLIENT-PRINCIPAL": principal()}
        self.assertEqual(self.call("/api/cases/PW-1/call", h, {"outcome": "Spoke"})[0], 403)
        h["X-PW-CSRF"] = "1"
        self.assertEqual(self.call("/api/cases/PW-1/call", h, {"outcome": "Spoke"})[0], 200)
        self.assertEqual(self.call("/api/logout", h, {})[1]["redirect"], "/.auth/logout")


class PasswordProviderTests(Base):
    def test_session_cookie_is_signed_stateless_and_expires(self):
        a = auth.PasswordProvider(self.store, "pw", key="k1")
        tok = a.login("sam@example.test", "pw")
        self.assertIsNone(a.login("sam@example.test", "wrong"))
        # a second process with the same key accepts the cookie: no per-process session table
        b = auth.PasswordProvider(self.store, "pw", key="k1")
        self.assertEqual(b.authenticate({"Cookie": f"pw_session={tok}"})["code"], "RLO-01")
        self.assertIsNone(auth.PasswordProvider(self.store, "pw", key="other").authenticate({"Cookie": f"pw_session={tok}"}))
        self.assertIsNone(b.authenticate({"Cookie": f"pw_session={tok[:-2]}xx"}))
        short = auth.PasswordProvider(self.store, "pw", key="k1", ttl=-1)
        self.assertIsNone(b.authenticate({"Cookie": "pw_session=" + short.login("sam@example.test", "pw")}))
        self.assertIsNone(b.authenticate({}))
