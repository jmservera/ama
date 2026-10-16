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
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler
from zava_forward.core.store import Store
from zava_forward.core.lawstore import LawStore
from zava_forward.core.rulecards import SEED_CARDS

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

    def test_rule_capabilities_require_unique_object_binding(self):
        roles = ("ZavaForward.LiaisonOfficer", "ZavaForward.RuleAuthor", "ZavaForward.RuleOwner")
        self.store.staff["sam@example.test"]["rule_roles"] = ["forged"]
        user = self.who(principal(roles=roles, email="someone-else@example.test"))
        self.assertEqual(user["email"], "sam@example.test")
        self.assertEqual(user["rule_roles"], ["rule_author", "rule_owner"])
        self.assertEqual(self.who(principal())["rule_roles"], [])
        for oid in ("unknown", None):
            user = self.who(principal(roles=roles, oid=oid, email="sam@example.test"), ZF_AUTH_EMAIL_FALLBACK="1")
            self.assertEqual(user["rule_roles"], [])
        p = json.loads(base64.b64decode(principal(roles=roles, email="sam@example.test")))
        p["claims"].append(dict(typ="oid", val="another"))
        header = base64.b64encode(json.dumps(p).encode()).decode()
        self.assertEqual(self.who(header, ZF_AUTH_EMAIL_FALLBACK="1")["rule_roles"], [])
        self.store.staff["duplicate@example.test"] = dict(self.store.staff["sam@example.test"])
        self.assertEqual(self.who(principal(roles=roles, email="sam@example.test"), ZF_AUTH_EMAIL_FALLBACK="1")["rule_roles"], [])
        self.assertIsNone(self.who(principal(roles=roles)))

    def test_reserved_rule_claim_cannot_be_mapped_to_staff_role(self):
        for role in ("ZavaForward.RuleAuthor", "ZavaForward.RuleOwner"):
            self.assertIsNone(self.who(principal(roles=(role,)), ZF_ROLE_MAP=json.dumps({role: "Retrofit Programme Manager"})))

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


class RuleHttpTests(Base):
    def setUp(self):
        super().setUp()
        self.store.staff["pam@example.test"]["oid"] = "synthetic-owner-oid"
        self.law = LawStore(str(Path(self.tmp.name) / "law.sqlite"), Path(self.tmp.name) / "blobs")
        self.app = App(self.store, provider=auth.TrustedProxyProvider(self.store, ENV), law=self.law)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join()
        self.law.close()
        super().tearDown()

    def headers(self, who="author", capabilities=None):
        capabilities = capabilities if capabilities is not None else ("ZavaForward.RuleAuthor",) if who == "author" else ("ZavaForward.RuleOwner",)
        oid = OID_SAM if who == "author" else "synthetic-owner-oid"
        return {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.LiaisonOfficer", *capabilities), oid=oid), "X-ZF-CSRF": "1"}

    def call(self, path="/api/law/cards", headers=None, body=None):
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode() if body is not None else None,
                                         headers=self.headers() if headers is None else headers)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                raw = response.read()
                return response.status, json.loads(raw) if raw.startswith(b"{") else raw.decode()
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def draft(self, **kw):
        return dict(SEED_CARDS[0], approver="pam@example.test", **kw)

    def transition(self, action, headers=None, body=None, version=2):
        return self.call(f"/api/law/cards/hazard-awareness-clock/{version}/{action}",
                         self.headers("owner") if headers is None else headers, {} if body is None else body)

    def test_running_local_app_full_lifecycle_and_retained_versions(self):
        self.assertEqual(self.call("/healthz")[0], 200)
        self.assertEqual(self.call("/app")[0], 200)
        cards = self.call()[1]["cards"]
        self.assertEqual(len(cards), 2)
        self.assertTrue(all(c["state"] == "draft" and "EXERCISE CARD" in c["label"] and c["approved_by"] is None for c in cards))
        self.assertEqual(self.call(body=self.draft())[0], 201)
        for action in ("approve", "activate", "hold", "release", "retire"):
            code, result = self.transition(action, body={"note": "Synthetic owner hold"} if action == "hold" else {})
            self.assertEqual(code, 200, result)
        history = self.call("/api/law/cards/hazard-awareness-clock")[1]["versions"]
        self.assertEqual([c["state"] for c in history], ["draft", "retired"])
        self.assertEqual(history[-1]["author"], "sam@example.test")
        self.assertEqual(history[-1]["approved_by"], "pam@example.test")
        self.assertTrue(history[-1]["approved_on"])
        self.assertTrue(all(e["simulated"] for e in history[-1]["events"]))
        before = self.law.rules.history("hazard-awareness-clock")
        self.law.rules.source_changed("awaabs-law-regulations-2025", 2)
        self.assertEqual(self.law.rules.history("hazard-awareness-clock"), before)
        self.assertEqual(len(self.call("/api/law/cards/reviews")[1]["reviews"]), 1)
        self.law.close()
        self.law = LawStore(str(Path(self.tmp.name) / "law.sqlite"), Path(self.tmp.name) / "blobs")
        self.app.law = self.law
        self.assertEqual(self.call("/api/law/cards/hazard-awareness-clock")[1]["versions"], before)

    def test_body_cannot_supply_authority_or_dates(self):
        for key, value in (("author", "pam@example.test"), ("role", "rule_owner"), ("actor", "pam@example.test"),
                           ("today", "2020-01-01"), ("exercise", False)):
            self.assertEqual(self.call(body=dict(self.draft(), **{key: value}))[0], 400)
        self.assertEqual(len(self.law.rules.history("hazard-awareness-clock")), 1)
        self.assertEqual(self.call(body=self.draft())[0], 201)
        for key in ("role", "actor", "today", "approved_on"):
            self.assertEqual(self.transition("approve", body={key: "forged"})[0], 400)
        self.assertIsNone(self.law.rules.history("hazard-awareness-clock")[-1]["approved_by"])

    def test_every_owner_transition_denies_wrong_capability_or_named_owner(self):
        self.assertEqual(self.call(body=self.draft())[0], 201)
        before = self.law.rules.history("hazard-awareness-clock")
        wrong_owner = self.headers("author", ("ZavaForward.RuleOwner",))
        for action in ("approve", "activate", "hold", "release", "retire"):
            self.assertEqual(self.transition(action, self.headers())[0], 403)
            self.assertEqual(self.transition(action, wrong_owner)[0], 409)
            self.assertEqual(self.law.rules.history("hazard-awareness-clock"), before)
        self.assertEqual(self.transition("activate")[0], 409)
        self.assertEqual(self.transition("approve")[0], 200)
        self.assertEqual(self.transition("activate")[0], 200)
        self.assertEqual(self.transition("hold")[0], 409)
        self.assertEqual(self.transition("hold", body={"note": "Synthetic hold"})[0], 200)
        self.assertIsNone(self.law.rules.is_active("hazard-awareness-clock"))

    def test_dual_roles_do_not_allow_self_approval(self):
        fields = self.draft()
        fields["approver"] = "sam@example.test"
        dual = self.headers(capabilities=("ZavaForward.RuleAuthor", "ZavaForward.RuleOwner"))
        self.assertEqual(self.call(headers=dual, body=fields)[0], 201)
        self.assertEqual(self.transition("approve", dual)[0], 409)
        self.assertEqual(self.transition("approve", version=1)[0], 409)

    def test_untrusted_fallback_agent_and_contractor_cannot_write(self):
        self.assertEqual(self.call(headers={}, body=self.draft())[0], 401)
        h = self.headers()
        h.pop("X-ZF-CSRF")
        self.assertEqual(self.call(headers=h, body=self.draft())[0], 403)
        self.store.staff["sam@example.test"]["rule_roles"] = ["rule_author", "rule_owner"]
        self.assertEqual(self.call(headers=self.headers(capabilities=()), body=self.draft())[0], 403)
        for roles in (("agent",), ("ZavaForward.RuleAuthor",), ("ZavaForward.LiaisonOfficer", "ZavaForward.ProgrammeManager", "ZavaForward.RuleAuthor")):
            h = {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles), "X-ZF-CSRF": "1"}
            self.assertEqual(self.call(headers=h, body=self.draft())[0], 401)
        self.app.provider = auth.TrustedProxyProvider(self.store, dict(ENV, ZF_AUTH_EMAIL_FALLBACK="1"))
        h = {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.LiaisonOfficer", "ZavaForward.RuleAuthor"),
                                              oid="unknown", email="sam@example.test"), "X-ZF-CSRF": "1"}
        self.assertEqual(self.call(headers=h, body=self.draft())[0], 403)
        con = {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Contractor", "ZavaForward.RuleOwner", "ZavaForward.RuleAuthor"),
                                                oid="aaaaaaaa-0000-0000-0000-000000000009"), "X-ZF-CSRF": "1"}
        for path in ("/api/law/cards", "/api/law/cards/reviews", "/api/law/cards/hazard-awareness-clock"):
            self.assertEqual(self.call(path, con)[0], 403)
            self.assertEqual(self.call(path, con, {})[0], 403)
        self.app.provider = auth.PasswordProvider(self.store, "synthetic")
        cookie = self.app.provider.login("sam@example.test", "synthetic")
        self.assertEqual(self.call(headers={"Cookie": f"zf_session={cookie}"}, body=self.draft())[0], 403)
        self.assertEqual(len(self.law.rules.history("hazard-awareness-clock")), 1)

    def test_errors_for_unavailable_store_missing_routes_and_malformed_fields(self):
        self.assertEqual(self.call("/api/law/cards/missing")[0], 404)
        for changes in (dict(provisions="not a list"), dict(effective="bad"), dict(title=123),
                        dict(retirement="2020-01-01"), dict(approver="unknown@example.test")):
            fields = dict(self.draft(), **changes)
            self.assertIn(self.call(body=fields)[0], (400, 409))
        self.assertEqual(self.transition("approve", version="bad")[0], 400)
        self.assertEqual(self.transition("unknown")[0], 404)
        self.assertEqual(self.call(body=dict(self.draft(), card_id="reviews"))[0], 409)
        code, card = self.call(body=dict(self.draft(), card_id="  synthetic-trimmed  "))
        self.assertEqual(code, 201)
        self.assertEqual(card["versions"][0]["card_id"], "synthetic-trimmed")
        self.app.law = None
        self.assertEqual(self.call()[0], 503)
        self.assertEqual(self.call(body=self.draft())[0], 503)


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
        with patch("zava_forward.core.profile.own_photo") as photo:
            from zava_forward.core.profile import PhotoError
            photo.side_effect = PhotoError(404, "No Microsoft profile photo has been set.")
            self.assertEqual(self.call("/api/account/photo", con)[0], 404)
            self.assertEqual(self.call("/api/me", con)[1]["staff"], [])
            photo.assert_called_once_with(None)

    def test_photo_binary_response_is_private_and_does_not_expose_platform_token(self):
        from zava_forward.api.server import WEB
        raw = (WEB / "zava-logo.png").read_bytes()
        headers = {"X-MS-CLIENT-PRINCIPAL": principal(),
                   "X-MS-TOKEN-AAD-ACCESS-TOKEN": "synthetic-platform-token"}
        with patch("zava_forward.core.profile.own_photo", return_value=(raw, "image/png")) as photo:
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
        from zava_forward.api.server import tile_config
        t = tile_config({})
        self.assertIn("tile.openstreetmap.org", t["url"])

    def test_production_without_url_has_no_tiles(self):
        from zava_forward.api.server import tile_config
        t = tile_config({"ZF_ENV": "production"})
        self.assertEqual((t["url"], t["host"]), (None, None))

    def test_custom_provider_and_validation(self):
        from zava_forward.api.server import tile_config
        t = tile_config({"ZF_TILE_URL": "https://{s}.tiles.example.org/{z}/{x}/{y}.png", "ZF_TILE_ATTRIBUTION": "Example"})
        self.assertEqual(t["host"], "https://a.tiles.example.org")
        with self.assertRaises(SystemExit):
            tile_config({"ZF_TILE_URL": "http://insecure.example.org/{z}/{x}/{y}.png"})

    def test_csp_header_and_me_payload_follow_config(self):
        import zava_forward.api.server as srv
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
