import base64
import sys
import threading
import unittest
from datetime import UTC, datetime, timedelta
from typing import Any

from zava_forward.core import resident_preview as preview
from zava_forward.core import resident_showcase as rs
from zava_forward.core.insights import STAGE_ORDER

FAKE_PASSWORD = "FAKE-TEST-FIXTURE-ONLY-not-a-real-demo-password"
NOW = datetime(2026, 10, 25, 12, 0, tzinfo=UTC)
FAKE_KEY = base64.urlsafe_b64encode(b"fake-session-key-for-tests-only!").rstrip(b"=").decode()


def row(case_id: str = "C-1", email: str = "a.demo@example.com", **kw: Any) -> rs.ShowcaseRow:
    base: dict[str, Any] = dict(
        case_id=case_id,
        email=email,
        email_count=1,
        provenance="owner-approved test fixture",
        valid_from=NOW - timedelta(days=1),
        valid_to=NOW + timedelta(days=1),
        revoked=False,
        address="1 Test Street",
        town="Testtown",
        postcode="TE1 1ST",
        stage="Survey",
        closed=False,
        measures=("Loft insulation",),
    )
    base.update(kw)
    return rs.ShowcaseRow(**base)


def raw(r: rs.ShowcaseRow) -> dict[str, Any]:
    return {k: getattr(r, k) for k in rs.ROW_KEYS}


class Clock:
    def __init__(self, now: float = 1_000_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


class AdmissionTests(unittest.TestCase):
    def test_canonical_email_accepts_only_ascii_example_com(self) -> None:
        self.assertEqual(rs.canonical_email("  A.Demo@Example.COM "), "a.demo@example.com")
        for bad in (
            "a@example.org",
            "a@sub.example.com",
            "a b@example.com",
            "ａ@example.com",
            "@example.com",
            "a@example.com\n",
            None,
            7,
            "a@@example.com",
        ):
            self.assertIsNone(rs.canonical_email(bad), bad)

    def test_admits_clean_row_and_reports_counts_only(self) -> None:
        ident = rs.build_identity_map([row()], NOW)
        self.assertEqual(ident.case_for("A.DEMO@example.com"), "C-1")
        self.assertEqual(ident.supplied, 1)
        self.assertEqual(sum(ident.excluded.values()), 0)

    def test_each_exclusion_reason_fails_closed(self) -> None:
        cases = {
            "provenance": row(provenance="  "),
            "revoked": row(revoked=True),
            "window": row(valid_to=NOW - timedelta(seconds=1)),
            "window ": row(valid_from=NOW + timedelta(seconds=1)),
            "email_form": row(email="a@example.org"),
            "email_duplicate": row(email_count=2),
        }
        for name, r in cases.items():
            ident = rs.build_identity_map([r], NOW)
            self.assertEqual(ident.cases, {}, name)
            self.assertEqual(sum(ident.excluded.values()), 1, name)

    def test_window_never_extends_past_authority_end(self) -> None:
        late = rs.AUTHORITY_END + timedelta(seconds=1)
        r = row(valid_from=rs.AUTHORITY_END - timedelta(days=1), valid_to=late + timedelta(days=9))
        self.assertIsNotNone(rs.exclusion(r, late))
        self.assertIsNone(rs.exclusion(r, rs.AUTHORITY_END - timedelta(seconds=1)))

    def test_january_authority_supersedes_old_cutoffs_but_remains_exclusive(self) -> None:
        r = row(valid_from=NOW, valid_to=rs.AUTHORITY_END)
        for moment in (
            datetime(2026, 11, 1, tzinfo=UTC),
            datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC),
            datetime(2027, 1, 31, 23, 59, 59, 999999, tzinfo=UTC),
        ):
            self.assertIsNone(rs.exclusion(r, moment))
        self.assertEqual(rs.exclusion(r, rs.AUTHORITY_END), "window")
        self.assertEqual(rs.exclusion(r, rs.AUTHORITY_END + timedelta(seconds=1)), "window")

    def test_duplicate_email_in_supplied_rows_excludes_the_later_one(self) -> None:
        ident = rs.build_identity_map([row("C-1"), row("C-2")], NOW)
        self.assertEqual(ident.cases, {"a.demo@example.com": "C-1"})
        self.assertEqual(ident.excluded["email_duplicate"], 1)

    def test_cap_ok_one_over_fails_whole_map(self) -> None:
        rows = [row(f"C-{i}", f"u{i}@example.com") for i in range(rs.MAX_MAPPINGS + 1)]
        self.assertEqual(len(rs.build_identity_map(rows[:-1], NOW).cases), rs.MAX_MAPPINGS)
        with self.assertRaises(rs.ShowcaseConfigError):
            rs.build_identity_map(rows, NOW)

    def test_parse_row_is_strict(self) -> None:
        good = raw(row())
        self.assertEqual(rs.parse_row(good).case_id, "C-1")
        for mutate in (
            lambda d: d.pop("email"),
            lambda d: d.update(extra="x"),
            lambda d: d.update(revoked=1),
            lambda d: d.update(email_count="1"),
            lambda d: d.update(measures=["list"]),
            lambda d: d.update(valid_to=datetime(2026, 1, 1)),
            lambda d: d.update(stage=None),
        ):
            data = dict(good)
            mutate(data)  # type: ignore[no-untyped-call]
            with self.assertRaises(rs.ShowcaseDenied):
                rs.parse_row(data)
        with self.assertRaises(rs.ShowcaseDenied):
            rs.parse_row([1, 2])

    def test_authorise_requires_same_case_and_current_admission(self) -> None:
        rs.authorise(row(), NOW, "C-1", "a.demo@example.com")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(), NOW, "C-2", "a.demo@example.com")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(revoked=True), NOW, "C-1", "a.demo@example.com")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(valid_to=NOW), NOW, "C-1", "a.demo@example.com")

    def test_stale_email_denied_and_unchanged_email_admitted(self) -> None:
        identity = rs.build_identity_map([row()], NOW)
        self.assertEqual(identity.email_for("C-1"), "a.demo@example.com")
        self.assertIsNone(identity.email_for("C-9"))
        rs.authorise(row(), NOW, "C-1", identity.email_for("C-1"))
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(
                row(email="changed.demo@example.com"), NOW, "C-1", identity.email_for("C-1")
            )
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(), NOW, "C-1", None)


class ClientKeyTests(unittest.TestCase):
    peer = "10.0.0.7"

    def key(self, headers: list[str], mode: str = "ingress-rightmost") -> str:
        return rs.client_key(self.peer, headers, mode)

    def test_default_mode_ignores_every_header(self) -> None:
        self.assertEqual(self.key(["203.0.113.5"], "peer"), self.peer)

    def test_rightmost_entry_is_used_and_client_prefix_is_ignored(self) -> None:
        self.assertEqual(self.key(["1.2.3.4, 9.9.9.9, 203.0.113.5"]), "203.0.113.5")
        self.assertEqual(self.key(["198.51.100.1", "203.0.113.5"]), "203.0.113.5")
        self.assertEqual(self.key(["1.2.3.4, 2001:db8::1"]), "2001:db8::1")
        self.assertEqual(self.key(["1.2.3.4, 2001:DB8:0:0:0:0:0:1"]), "2001:db8::1")

    def test_bad_missing_or_decorated_last_entry_falls_back_to_the_peer(self) -> None:
        for headers in (
            [],
            [""],
            ["1.2.3.4,"],
            ["1.2.3.4, x"],
            ["203.0.113.5:443"],
            ["[2001:db8::1]"],
        ):
            self.assertEqual(self.key(headers), self.peer, headers)


class PasswordTests(unittest.TestCase):
    spec: str
    verifier: rs.PasswordVerifier

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = rs.make_verifier(FAKE_PASSWORD, n=2**14)
        cls.verifier = rs.PasswordVerifier(cls.spec)

    def test_verify(self) -> None:
        self.assertTrue(self.verifier.verify(FAKE_PASSWORD))
        bad: Any
        for bad in ("", FAKE_PASSWORD + "x", "x" * 300, None, 5):
            self.assertFalse(self.verifier.verify(bad))

    def test_spec_validation(self) -> None:
        for bad in (
            "",
            "scrypt$1$1$1$a$b",
            "bcrypt" + self.spec[6:],
            self.spec.replace("$16384$", "$16385$"),
            self.spec.rsplit("$", 1)[0],
        ):
            with self.assertRaises(rs.ShowcaseConfigError):
                rs.PasswordVerifier(bad)

    def test_login_same_outcome_for_unknown_wrong_and_right(self) -> None:
        ident = rs.build_identity_map([row()], NOW)
        self.assertEqual(
            rs.verify_login(self.verifier, ident, "a.demo@example.com", FAKE_PASSWORD), "C-1"
        )
        self.assertEqual(
            rs.verify_login(self.verifier, ident, "A.DEMO@EXAMPLE.COM ", FAKE_PASSWORD), "C-1"
        )
        self.assertIsNone(rs.verify_login(self.verifier, ident, "a.demo@example.com", "wrong"))
        self.assertIsNone(
            rs.verify_login(self.verifier, ident, "nobody@example.com", FAKE_PASSWORD)
        )
        self.assertIsNone(rs.verify_login(self.verifier, ident, 5, FAKE_PASSWORD))
        self.assertIsNone(rs.verify_login(self.verifier, ident, "a.demo@example.com", None))


class SessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = Clock(NOW.timestamp())
        self.key = b"k" * 32
        self.codec = rs.SessionCodec(self.key, rs.AUTHORITY_END, self.clock)

    def test_round_trip_and_handle_is_opaque(self) -> None:
        token, expiry = self.codec.issue("C-1")
        self.assertNotIn("C-1", token)
        self.assertEqual((self.codec.verify(token) or ("", ""))[0], self.codec.handle("C-1"))
        self.assertEqual(expiry, int(NOW.timestamp()) + rs.SESSION_SECONDS)

    def test_tamper_expiry_and_garbage_denied(self) -> None:
        token, _ = self.codec.issue("C-1")
        parts = token.split(".")
        forged = ".".join(parts[:2] + [str(int(parts[2]) + 999999)] + parts[3:])
        bad: Any
        for bad in (forged, token[:-2] + "xx", "", "v1.a.b", None, 5, "v2" + token[2:], "x" * 400):
            self.assertIsNone(self.codec.verify(bad))
        self.clock.now += rs.SESSION_SECONDS
        self.assertIsNone(self.codec.verify(token))

    def test_restart_and_key_change_invalidate(self) -> None:
        token, _ = self.codec.issue("C-1")
        self.assertIsNone(rs.SessionCodec(self.key, rs.AUTHORITY_END, self.clock).verify(token))
        same_nonce = rs.SessionCodec(
            self.key, rs.AUTHORITY_END, self.clock, nonce=self.codec._nonce
        )
        self.assertIsNotNone(same_nonce.verify(token))
        other = rs.SessionCodec(b"z" * 32, rs.AUTHORITY_END, self.clock, nonce=self.codec._nonce)
        self.assertIsNone(other.verify(token))

    def test_logout_revokes_only_that_session(self) -> None:
        a, _ = self.codec.issue("C-1")
        b, _ = self.codec.issue("C-1")
        self.codec.revoke(a)
        self.assertIsNone(self.codec.verify(a))
        self.assertIsNotNone(self.codec.verify(b))

    def test_concurrent_logouts_do_not_lose_revocations(self) -> None:
        tokens = [self.codec.issue(f"C-{i}")[0] for i in range(40)]
        old = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            for _ in range(3):
                threads = [threading.Thread(target=self.codec.revoke, args=(t,)) for t in tokens]
                for th in threads:
                    th.start()
                for th in threads:
                    th.join()
                self.assertTrue(all(self.codec.verify(t) is None for t in tokens))
                tokens = [self.codec.issue(f"C-{i}")[0] for i in range(40)]
        finally:
            sys.setswitchinterval(old)

    def test_full_revocation_store_still_ends_the_logging_out_session(self) -> None:
        first, _ = self.codec.issue("C-1")
        other, _ = self.codec.issue("C-2")
        for index in range(4096):
            self.codec._revoked[f"s{index}"] = NOW.timestamp() + 10_000
        self.codec.revoke(first)
        self.assertIsNone(self.codec.verify(first))
        self.assertIsNone(self.codec.verify(other))  # fail closed: every session ends
        fresh, _ = self.codec.issue("C-1")
        self.assertIsNotNone(self.codec.verify(fresh))

    def test_never_outlives_showcase_expiry(self) -> None:
        end = NOW + timedelta(seconds=60)
        codec = rs.SessionCodec(self.key, end, self.clock)
        token, expiry = codec.issue("C-1")
        self.assertEqual(expiry, int(end.timestamp()))
        self.clock.now = end.timestamp()
        self.assertIsNone(codec.verify(token))

    def test_short_key_refused(self) -> None:
        with self.assertRaises(rs.ShowcaseConfigError):
            rs.SessionCodec(b"short", rs.AUTHORITY_END)

    def test_csrf(self) -> None:
        token = self.codec.new_csrf()
        self.assertTrue(self.codec.csrf_ok(token, token))
        self.assertFalse(self.codec.csrf_ok(token, token + "x"))
        self.assertFalse(self.codec.csrf_ok(token, None))
        self.assertFalse(self.codec.csrf_ok(None, token))
        forged = "abc.def"
        self.assertFalse(self.codec.csrf_ok(forged, forged))


class LimiterTests(unittest.TestCase):
    def test_per_source_then_window_expires(self) -> None:
        clock = Clock()
        lim = rs.LoginLimiter(per_source=3, overall=100, window=600, clock=clock)
        for _ in range(3):
            self.assertEqual(lim.retry_after("a"), 0)
            lim.record_failure("a")
        self.assertGreater(lim.retry_after("a"), 0)
        self.assertEqual(lim.retry_after("b"), 0)
        clock.now += 601
        self.assertEqual(lim.retry_after("a"), 0)

    def test_global_window(self) -> None:
        lim = rs.LoginLimiter(per_source=5, overall=4, window=600, clock=Clock())
        for i in range(4):
            lim.record_failure(f"s{i}")
        self.assertGreater(lim.retry_after("new"), 0)

    def test_source_table_is_bounded(self) -> None:
        lim = rs.LoginLimiter(per_source=5, overall=10**6, clock=Clock())
        for i in range(rs.LoginLimiter.MAX_SOURCES + 500):
            lim.record_failure(f"s{i}")
        self.assertLessEqual(len(lim._by_source), rs.LoginLimiter.MAX_SOURCES)


class ViewTests(unittest.TestCase):
    def test_view_is_exact_allowlist(self) -> None:
        view = rs.showcase_view(row())
        self.assertEqual(
            set(view),
            {
                "banner",
                "viewer",
                "read_only",
                "home",
                "measures",
                "sensors",
                "progress",
                "next_step",
                "unavailable",
                "help",
            },
        )
        self.assertEqual(set(view["home"]), {"address", "town", "postcode"})
        self.assertTrue(view["banner"].startswith("Synthetic demo"))

    def test_view_never_carries_identity_or_internal_fields(self) -> None:
        text = repr(
            rs.showcase_view(
                row(
                    case_id="CASE-CANARY",
                    email="canary@example.com",
                    provenance="PROVENANCE-CANARY",
                )
            )
        )
        for canary in ("CASE-CANARY", "canary@example.com", "PROVENANCE-CANARY"):
            self.assertNotIn(canary, text)

    def test_bounds_closed_and_unknown_stage(self) -> None:
        long = "x" * 500
        view = rs.showcase_view(
            row(
                measures=tuple(f"m{i}" for i in range(40)) + ("",),
                address=long,
                stage="not-a-stage",
                closed=True,
            )
        )
        self.assertEqual(len(view["measures"]), 20)
        self.assertEqual(len(view["home"]["address"]), 120)
        self.assertEqual(view["progress"], preview.UNKNOWN_PROGRESS)
        self.assertIn("closed", view)

    def test_known_stage_uses_plain_language_text(self) -> None:
        stage = next(s for s in STAGE_ORDER if s in preview.STAGE_TEXT)
        view = rs.showcase_view(row(stage=stage))
        self.assertEqual((view["progress"], view["next_step"]), preview.STAGE_TEXT[stage])


class ConfigTests(unittest.TestCase):
    def env(self, **over: Any) -> dict[str, str]:
        base = {
            "ZF_DEMO_EXPIRES_AT": "2027-02-01T00:00:00Z",
            "ZF_DEMO_ALLOWED_HOSTS": "demo.example.invalid",
            "ZF_DEMO_PASSWORD_VERIFIER": rs.make_verifier(FAKE_PASSWORD, n=2**14),
            "ZF_DEMO_SESSION_KEY": FAKE_KEY,
            "ZF_SQL_SERVER": "sql.example.invalid",
            "ZF_SQL_DATABASE": "retrofit",
        }
        base.update(over)
        return {k: v for k, v in base.items() if v is not None}

    def refuse(self, **over: Any) -> str:
        with self.assertRaises(rs.ShowcaseConfigError) as ctx:
            rs.config_from_env(self.env(**over), NOW)
        return str(ctx.exception)

    def test_valid_config(self) -> None:
        cfg = rs.config_from_env(self.env(), NOW)
        self.assertEqual(cfg.sql["auth"], "msi")
        self.assertEqual(cfg.bind, "127.0.0.1")
        self.assertEqual(cfg.expires_at, rs.AUTHORITY_END)

    def test_client_address_mode_defaults_to_peer_and_rejects_unknown(self) -> None:
        self.assertEqual(rs.config_from_env(self.env(), NOW).client_address, "peer")
        cfg = rs.config_from_env(self.env(ZF_DEMO_CLIENT_ADDRESS="ingress-rightmost"), NOW)
        self.assertEqual(cfg.client_address, "ingress-rightmost")
        for value in ("x-forwarded-for", "forwarded", "*"):
            self.refuse(ZF_DEMO_CLIENT_ADDRESS=value)

    def test_missing_required_values_fail(self) -> None:
        for name in (
            "ZF_DEMO_EXPIRES_AT",
            "ZF_DEMO_ALLOWED_HOSTS",
            "ZF_DEMO_PASSWORD_VERIFIER",
            "ZF_DEMO_SESSION_KEY",
            "ZF_SQL_SERVER",
            "ZF_SQL_DATABASE",
        ):
            self.refuse(**{name: None})

    def test_config_accepts_inclusive_cap_but_stops_serving_at_expiry(self) -> None:
        self.assertEqual(rs.AUTHORITY_END, datetime(2027, 2, 1, tzinfo=UTC))
        for expires in (
            "2026-11-01T00:00:00Z",
            "2026-12-31T23:59:59Z",
            "2027-01-31T23:59:59Z",
            "2027-02-01T00:00:00Z",
        ):
            cfg = rs.config_from_env(self.env(ZF_DEMO_EXPIRES_AT=expires), NOW)
            self.assertEqual(cfg.expires_at.isoformat().replace("+00:00", "Z"), expires)
        with self.assertRaises(rs.ShowcaseConfigError):
            rs.config_from_env(self.env(), rs.AUTHORITY_END)
        far = row(
            valid_from=rs.AUTHORITY_END - timedelta(days=2),
            valid_to=rs.AUTHORITY_END + timedelta(days=2),
        )
        self.assertIsNone(rs.exclusion(far, rs.AUTHORITY_END - timedelta(seconds=1)))
        self.assertIsNotNone(rs.exclusion(far, rs.AUTHORITY_END))

    def test_expiry_rules(self) -> None:
        self.refuse(ZF_DEMO_EXPIRES_AT="2027-02-01T00:00:01Z")
        self.refuse(ZF_DEMO_EXPIRES_AT="2027-02-01T00:00:00.001Z")
        self.refuse(ZF_DEMO_EXPIRES_AT="2026-10-25T11:59:59Z")
        self.refuse(ZF_DEMO_EXPIRES_AT="2026-10-26T11:00:00")
        self.refuse(ZF_DEMO_EXPIRES_AT="2026-10-26T13:00:00+01:00")
        self.refuse(ZF_DEMO_EXPIRES_AT="never")

    def test_mixed_composition_and_short_key_and_hosts(self) -> None:
        for name in ("ZF_STORE", "ZF_ENTRA_TENANT", "AI_ENDPOINT", "AZURE_OPENAI_KEY", "ZF_DATA"):
            self.assertIn(name, self.refuse(**{name: "x"}))
        self.refuse(ZF_DEMO_SESSION_KEY=base64.urlsafe_b64encode(b"short").decode())
        self.refuse(ZF_DEMO_ALLOWED_HOSTS="*.example.invalid")
        self.refuse(ZF_DEMO_PASSWORD_VERIFIER="scrypt$bad")

    def test_sql_auth_rules_and_no_value_echo(self) -> None:
        self.refuse(ZF_SQL_AUTH="password", ZF_SQL_USER="u", ZF_SQL_PASSWORD="SECRET-CANARY")
        self.refuse(ZF_SQL_AUTH="token")
        message = self.refuse(
            ZF_SQL_AUTH="password", ZF_SQL_USER="u", ZF_SQL_PASSWORD="SECRET-CANARY"
        )
        self.assertNotIn("SECRET-CANARY", message)
        cfg = rs.config_from_env(
            self.env(
                ZF_SQL_SERVER="127.0.0.1",
                ZF_SQL_AUTH="password",
                ZF_SQL_USER="u",
                ZF_SQL_PASSWORD="p",
            ),
            NOW,
        )
        self.assertEqual(cfg.sql["auth"], "password")


class BoundaryTests(unittest.TestCase):
    def test_module_does_not_touch_444_guard(self) -> None:
        with open(rs.__file__, encoding="utf-8") as handle:
            source = handle.read()
        for forbidden in ("safe_start", "resolve_grant", "resident_view", "open_store", "Grant("):
            self.assertNotIn(
                forbidden, source.split('"""', 2)[2].replace("`" + forbidden + "`", "")
            )


if __name__ == "__main__":
    unittest.main()
