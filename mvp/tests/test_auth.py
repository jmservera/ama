import base64
import json
import os
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from zavaforward_mvp import auth
from zavaforward_mvp.server import App, make_handler
from zavaforward_mvp.store import Store

TENANT = "11111111-2222-3333-4444-555555555555"
OID_SAM = "aaaaaaaa-0000-0000-0000-000000000001"
ENV = dict(ZF_AUTH="trusted-proxy", ZF_TRUSTED_PROXY="1", ZF_ENTRA_TENANT_ID=TENANT)


def principal(roles=("ZavaForward.LiaisonOfficer",), oid=OID_SAM, tid=TENANT, typ="aad", email=None):
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
        p = Path(self.tmp.name) / "zavaforward.json"
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
        u = self.who(principal(roles=("ZavaForward.ProgrammeManager",)))
        self.assertEqual(u["role"], "Retrofit Programme Manager")
        self.assertEqual(u["code"], "RLO-01")

    def test_contractor_role_and_custom_map(self):
        u = self.who(principal(roles=("ZavaForward.Contractor",), oid="aaaaaaaa-0000-0000-0000-000000000009"))
        self.assertEqual((u["role"], u["contractor"]), ("Contractor", "Test Ltd"))
        u = self.who(principal(roles=("Warm.Coord",)), ZF_ROLE_MAP=json.dumps({"Warm.Coord": "Retrofit Coordinator"}))
        self.assertEqual(u["role"], "Retrofit Coordinator")

    def test_fails_closed(self):
        self.assertIsNone(self.who(None))
        self.assertIsNone(self.who(""))
        self.assertIsNone(self.who("not base64 !!"))
        self.assertIsNone(self.who(base64.b64encode(b"[1,2]").decode()))
        self.assertIsNone(self.who(principal(typ="google")))
        self.assertIsNotNone(self.who(principal(typ="Bearer")))
        self.assertIsNone(self.who(principal(tid="99999999-2222-3333-4444-555555555555")))
        self.assertIsNone(self.who(principal(tid=None)))
        self.assertIsNone(self.who(principal(roles=())))
        self.assertIsNone(self.who(principal(roles=("Unmapped.Role",))))
        self.assertIsNone(self.who(principal(roles=("ZavaForward.Contractor", "ZavaForward.ProgrammeManager"))))
        self.assertIsNone(self.who(principal(oid="not-a-provisioned-person")))
        self.assertIsNone(self.who(principal(oid=None)))
        self.assertIsNone(self.who("A" * 20000))

    def test_email_match_only_when_enabled(self):
        h = principal(oid="unknown-oid", email="sam@example.test")
        self.assertIsNone(self.who(h))
        self.assertEqual(self.who(h, ZF_AUTH_EMAIL_FALLBACK="1")["code"], "RLO-01")

    def test_role_comes_from_token_not_staff_file(self):
        self.store.staff["sam@example.test"]["role"] = "Retrofit Programme Manager"
        self.assertEqual(self.who(principal())["role"], "Resident Liaison Officer")

    def test_refuses_to_start_without_tenant_or_confirmation(self):
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(self.store, dict(ENV, ZF_ENTRA_TENANT_ID=""))
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(self.store, dict(ENV, ZF_TRUSTED_PROXY=""))

    def test_production_refuses_password_provider(self):
        with self.assertRaises(SystemExit):
            auth.make_provider(self.store, "x", dict(ZF_ENV="production"))
        self.assertEqual(auth.make_provider(self.store, "x", {}).name, "password")
        self.assertEqual(auth.make_provider(self.store, "x", dict(ENV, ZF_ENV="production")).name, "trusted-proxy")


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
        self.assertEqual(self.call("/api/cases", {"Cookie": "zf_session=anything"})[0], 401)

    def test_principal_gives_role_and_projection(self):
        code, me = self.call("/api/me", {"X-MS-CLIENT-PRINCIPAL": principal()})
        self.assertEqual((code, me["user"]["role"]), (200, "Resident Liaison Officer"))
        con = {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Contractor",), oid="aaaaaaaa-0000-0000-0000-000000000009")}
        self.assertEqual(self.call("/api/stats", con)[0], 403)
        self.assertEqual(self.call("/api/cases", con)[0], 200)

    def test_post_needs_csrf_header_and_logout_redirects(self):
        h = {"X-MS-CLIENT-PRINCIPAL": principal()}
        self.assertEqual(self.call("/api/cases/ZF-1/call", h, {"outcome": "Spoke"})[0], 403)
        h["X-ZF-CSRF"] = "1"
        self.assertEqual(self.call("/api/cases/ZF-1/call", h, {"outcome": "Spoke"})[0], 200)
        self.assertEqual(self.call("/api/logout", h, {})[1]["redirect"], "/.auth/logout?post_logout_redirect_uri=%2F")
        self.assertEqual(self.call("/api/logout", h, {"switchAccount": True})[1]["redirect"], "/sign-in?switch=1")

    def test_account_selection_uses_only_fixed_explicit_flag(self):
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        opener = urllib.request.build_opener(NoRedirect())
        normal = "/.auth/login/aad?post_login_redirect_uri=%2Fapp"
        for query, target in (
            ("switch=1", normal + "&prompt=select_account"),
            ("switch=1&return=https%3A%2F%2Fexample.invalid&prompt=none", normal + "&prompt=select_account"),
            ("", normal), ("switch=0", normal), ("switch=", normal),
            ("switch=1&switch=1", normal), ("switch=1&switch=", normal),
            ("switch=&switch=1", normal), ("prompt=select_account", normal),
        ):
            with self.subTest(query=query), self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(self.base + "/sign-in?" + query)
            self.assertEqual(error.exception.code, 302)
            self.assertEqual(error.exception.headers["Location"], target)
            self.assertEqual(error.exception.headers["Cache-Control"], "no-store")

    def test_auth_flow_events_are_fixed_and_require_authorized_success(self):
        h = {"X-MS-CLIENT-PRINCIPAL": principal(), "X-ZF-CSRF": "1"}
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        opener = urllib.request.build_opener(NoRedirect())
        with patch("builtins.print") as output:
            for path in ("/sign-in", "/sign-in?switch=1&token=synthetic-secret"):
                with self.assertRaises(urllib.error.HTTPError):
                    opener.open(self.base + path)
            self.call("/api/logout", h, {"switchAccount": True})
            self.call("/api/logout", h, {})
            req = urllib.request.Request(self.base + "/app", headers=h)
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status, 200)
            self.assertEqual(output.call_args_list, [
                unittest.mock.call("auth flow: sign-in-started", flush=True),
                unittest.mock.call("auth flow: account-picker-started", flush=True),
                unittest.mock.call("auth flow: account-switch-requested", flush=True),
                unittest.mock.call("auth flow: sign-out-requested", flush=True),
                unittest.mock.call("auth flow: workbench-entered", flush=True),
            ])
            output.reset_mock()
            self.assertEqual(self.call("/api/logout", {}, {"switchAccount": True})[0], 401)
            self.assertEqual(self.call("/api/logout", {"X-MS-CLIENT-PRINCIPAL": principal()},
                                       {"switchAccount": True})[0], 403)
            req = urllib.request.Request(self.base + "/app",
                                         headers={"X-MS-CLIENT-PRINCIPAL": principal(oid="unknown")})
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(req)
            self.assertEqual(error.exception.code, 403)
            self.assertFalse(any(str(call.args[0]).startswith("auth flow:") for call in output.call_args_list))

    def test_password_sign_in_and_switch_do_not_invoke_microsoft(self):
        app = App(self.store, "pw")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        try:
            opener = urllib.request.build_opener(NoRedirect())
            with patch("builtins.print") as output:
                for query in ("", "?switch=1"):
                    with self.assertRaises(urllib.error.HTTPError) as error:
                        opener.open(f"http://127.0.0.1:{httpd.server_address[1]}/sign-in{query}")
                    self.assertEqual(error.exception.headers["Location"], "/app")
                self.assertEqual(app.provider.logout_response(switch=True), {"ok": True})
                output.assert_not_called()
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_welcome_is_public_and_workbench_is_protected(self):
        with urllib.request.urlopen(self.base + "/") as response:
            text = response.read().decode()
            self.assertIn("Sign in to the workbench", text)
            self.assertNotIn("app.js", text)
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        opener = urllib.request.build_opener(NoRedirect())
        for path, target in (("/app", "/sign-in"), ("/sign-in", "/.auth/login/aad?post_login_redirect_uri=%2Fapp")):
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(self.base + path)
            self.assertEqual(error.exception.code, 302)
            self.assertEqual(error.exception.headers["Location"], target)
        req = urllib.request.Request(self.base + "/app", headers={"X-MS-CLIENT-PRINCIPAL": principal()})
        with urllib.request.urlopen(req) as response:
            self.assertIn('data-auth-provider="trusted-proxy"', response.read().decode())

    def test_current_account_claims_do_not_change_staff_records(self):
        p = json.loads(base64.b64decode(principal(email="signed-in@example.test")))
        p["claims"].append({"typ": "name", "val": "Signed In Person"})
        header = base64.b64encode(json.dumps(p).encode()).decode()
        code, me = self.call("/api/me", {"X-MS-CLIENT-PRINCIPAL": header})
        self.assertEqual(code, 200)
        self.assertEqual(me["account"]["name"], "Signed In Person")
        self.assertEqual(me["account"]["email"], "signed-in@example.test")
        self.assertEqual(self.store.staff["sam@example.test"]["name"], "Sam Example")

    def test_photo_requires_current_user_and_contractor_is_allowed_own_photo(self):
        self.assertEqual(self.call("/api/account/photo")[0], 401)
        con = {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Contractor",), oid="aaaaaaaa-0000-0000-0000-000000000009")}
        with patch("zavaforward_mvp.profile.own_photo") as photo:
            from zavaforward_mvp.profile import PhotoError
            photo.side_effect = PhotoError(404, "No Microsoft profile photo has been set.")
            self.assertEqual(self.call("/api/account/photo", con)[0], 404)
            self.assertEqual(self.call("/api/me", con)[1]["staff"], [])
            photo.assert_called_once_with(None)

    def test_photo_binary_response_is_private_and_does_not_expose_platform_token(self):
        from zavaforward_mvp.server import WEB
        raw = (WEB / "zava-logo.png").read_bytes()
        headers = {"X-MS-CLIENT-PRINCIPAL": principal(),
                   "X-MS-TOKEN-AAD-ACCESS-TOKEN": "synthetic-platform-token"}
        with patch("zavaforward_mvp.profile.own_photo", return_value=(raw, "image/png")) as photo:
            req = urllib.request.Request(self.base + "/api/account/photo", headers=headers)
            with urllib.request.urlopen(req) as response:
                body = response.read()
                self.assertEqual(response.headers["Content-Type"], "image/png")
                self.assertEqual(response.headers["Cache-Control"], "no-store")
                self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            self.assertEqual(body, raw)
            self.assertNotIn(b"synthetic-platform-token", body)
            photo.assert_called_once_with("synthetic-platform-token")


class PasswordProviderTests(Base):
    def test_session_cookie_is_signed_stateless_and_expires(self):
        a = auth.PasswordProvider(self.store, "pw", key="k1")
        tok = a.login("sam@example.test", "pw")
        self.assertIsNone(a.login("sam@example.test", "wrong"))
        # a second process with the same key accepts the cookie: no per-process session table
        b = auth.PasswordProvider(self.store, "pw", key="k1")
        self.assertEqual(b.authenticate({"Cookie": f"zf_session={tok}"})["code"], "RLO-01")
        self.assertIsNone(auth.PasswordProvider(self.store, "pw", key="other").authenticate({"Cookie": f"zf_session={tok}"}))
        self.assertIsNone(b.authenticate({"Cookie": f"zf_session={tok[:-2]}xx"}))
        short = auth.PasswordProvider(self.store, "pw", key="k1", ttl=-1)
        self.assertIsNone(b.authenticate({"Cookie": "zf_session=" + short.login("sam@example.test", "pw")}))
        self.assertIsNone(b.authenticate({}))


class TileConfigTests(Base):
    def test_blob_sources_are_allowed_only_for_images(self):
        app = App(self.store, "pw")
        directives = {}
        for directive in app.csp.split(";"):
            name, *sources = directive.strip().split()
            directives[name] = sources
        self.assertIn("blob:", directives["img-src"])
        for name, sources in directives.items():
            if name != "img-src":
                self.assertNotIn("blob:", sources)

    def test_default_dev_uses_osm_and_csp_allows_only_it(self):
        from zavaforward_mvp.server import tile_config
        t = tile_config({})
        self.assertIn("tile.openstreetmap.org", t["url"])

    def test_production_without_url_has_no_tiles(self):
        from zavaforward_mvp.server import tile_config
        t = tile_config({"ZF_ENV": "production"})
        self.assertEqual((t["url"], t["host"]), (None, None))

    def test_custom_provider_and_validation(self):
        from zavaforward_mvp.server import tile_config
        t = tile_config({"ZF_TILE_URL": "https://{s}.tiles.example.org/{z}/{x}/{y}.png", "ZF_TILE_ATTRIBUTION": "Example"})
        self.assertEqual(t["host"], "https://a.tiles.example.org")
        with self.assertRaises(SystemExit):
            tile_config({"ZF_TILE_URL": "http://insecure.example.org/{z}/{x}/{y}.png"})

    def test_csp_header_and_me_payload_follow_config(self):
        import zavaforward_mvp.server as srv
        old = os.environ.get("ZF_TILE_URL"), os.environ.get("ZF_ENV")
        os.environ["ZF_TILE_URL"] = "https://tiles.example.org/{z}/{x}/{y}.png"
        try:
            app = App(self.store, "pw")
        finally:
            for k, v in zip(("ZF_TILE_URL", "ZF_ENV"), old):
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            with urllib.request.urlopen(base + "/") as r:
                csp = r.headers["Content-Security-Policy"]
            self.assertIn("img-src 'self' data: blob: https://tiles.example.org;", csp)
            self.assertNotIn("openstreetmap", csp)
            tok = app.provider.login("sam@example.test", "pw")
            req = urllib.request.Request(base + "/api/me", headers={"Cookie": f"zf_session={tok}"})
            with urllib.request.urlopen(req) as r:
                self.assertEqual(json.loads(r.read())["map"]["tiles"], "https://tiles.example.org/{z}/{x}/{y}.png")
        finally:
            httpd.shutdown()
            httpd.server_close()
