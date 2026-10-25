import base64
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

    def test_duplicate_email_in_supplied_rows_excludes_the_later_one(self) -> None:
        ident = rs.build_identity_map([row("C-1"), row("C-2")], NOW)
        self.assertEqual(ident.cases, {"a.demo@example.com": "C-1"})
        self.assertEqual(ident.excluded["email_duplicate"], 1)

    def test_twenty_five_ok_twenty_six_fails_whole_map(self) -> None:
        rows = [row(f"C-{i}", f"u{i}@example.com") for i in range(26)]
        self.assertEqual(len(rs.build_identity_map(rows[:25], NOW).cases), 25)
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
        rs.authorise(row(), NOW, "C-1")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(), NOW, "C-2")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(revoked=True), NOW, "C-1")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.authorise(row(valid_to=NOW), NOW, "C-1")


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
            "ZF_DEMO_EXPIRES_AT": "2026-10-26T12:00:00Z",
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

    def test_expiry_rules(self) -> None:
        self.refuse(ZF_DEMO_EXPIRES_AT="2026-10-26T12:00:01Z")
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
