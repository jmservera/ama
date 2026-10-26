"""Synthetic resident showcase domain: identity admission, demo credential, sessions and view.

Pure and dependency free by design. Adapters (the SQL reader and the HTTP server) depend on this
module, never the reverse. It is demo authentication over database-owned synthetic rows. It is not
a real resident identity, enrolment or security acceptance: one shared password is used for every
listed demo resident, so anyone who knows the password and a listed email can open that demo case.
The #444 preview harness (`safe_start`, `Grant`, `resident_view`) is not used or changed; only its
read-only text constants are reused so both surfaces say the same plain-language things.
"""

import base64
import binascii
import hashlib
import hmac
import ipaddress
import os
import re
import secrets
import time
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from . import resident_preview as _preview
from .insights import STAGE_ORDER

AUTHORITY_END = datetime(2026, 11, 1, 0, 0, tzinfo=UTC)  # exclusive: through 31 Oct UTC
MAX_MAPPINGS = 25
SESSION_SECONDS = 1800
BANNER = (
    "Synthetic demo - not a real resident service. This sign-in uses a shared demo password "
    "and does not prove who you are."
)
EMAIL_FORM = re.compile(r"[a-z0-9._+-]{1,64}@example\.com")
ROW_KEYS = frozenset(
    {
        "case_id",
        "email",
        "email_count",
        "provenance",
        "valid_from",
        "valid_to",
        "revoked",
        "address",
        "town",
        "postcode",
        "stage",
        "closed",
        "measures",
    }
)
FORBIDDEN_ENV_PREFIXES = (
    "ZF_STORE",
    "ZF_ENTRA",
    "ZF_AI",
    "AI_",
    "AZURE_OPENAI",
    "ZF_DATA",
    "ZF_STATE",
)
EXCLUSION_REASONS = (
    "provenance",
    "revoked",
    "window",
    "email_form",
    "email_duplicate",
)


class ShowcaseDenied(Exception):
    """Access denied. `code` is for tests and logs; `str` is the only text a resident sees."""

    def __init__(self, code: str):
        super().__init__("You cannot see this page.")
        self.code = code


class ShowcaseConfigError(Exception):
    """Unsafe or incomplete configuration. The message never contains a configured value."""


def canonical_email(value: Any) -> str | None:
    """Trim spaces (as SQL LTRIM/RTRIM do) and lower-case, then accept only the ASCII form."""
    if not isinstance(value, str):
        return None
    text = value.strip(" ").lower()
    return text if EMAIL_FORM.fullmatch(text) else None


@dataclass(frozen=True)
class ShowcaseRow:
    case_id: str
    email: str
    email_count: int
    provenance: str
    valid_from: datetime
    valid_to: datetime
    revoked: bool
    address: str
    town: str
    postcode: str
    stage: str
    closed: bool
    measures: tuple[str, ...]


def _aware(value: Any) -> datetime:
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise ValueError("time")
    return value


def parse_row(raw: Any) -> ShowcaseRow:
    """Strictly shape one view row; any deviation is a denied, malformed row."""
    try:
        if not isinstance(raw, Mapping) or set(raw) != ROW_KEYS:
            raise ValueError("keys")
        text_keys = ("case_id", "email", "provenance", "address", "town", "postcode", "stage")
        if not all(isinstance(raw[k], str) for k in text_keys):
            raise ValueError("text")
        if (
            type(raw["revoked"]) is not bool
            or type(raw["closed"]) is not bool
            or type(raw["email_count"]) is not int
        ):
            raise ValueError("flags")
        measures = raw["measures"]
        if not isinstance(measures, tuple) or not all(isinstance(m, str) for m in measures):
            raise ValueError("measures")
        return ShowcaseRow(
            case_id=raw["case_id"],
            email=raw["email"],
            email_count=raw["email_count"],
            provenance=raw["provenance"],
            valid_from=_aware(raw["valid_from"]),
            valid_to=_aware(raw["valid_to"]),
            revoked=raw["revoked"],
            address=raw["address"],
            town=raw["town"],
            postcode=raw["postcode"],
            stage=raw["stage"],
            closed=raw["closed"],
            measures=measures,
        )
    except (ValueError, TypeError, KeyError):
        raise ShowcaseDenied("row_shape") from None


def exclusion(row: ShowcaseRow, now: datetime) -> str | None:
    """Return why a row is not admitted, or None. Positive checks only; every one must pass."""
    if not row.case_id.strip() or not row.provenance.strip():
        return "provenance"
    if row.revoked:
        return "revoked"
    if not row.valid_from <= now < row.valid_to or now >= AUTHORITY_END:
        return "window"
    if canonical_email(row.email) != row.email:
        return "email_form"
    if row.email_count != 1:
        return "email_duplicate"
    return None


@dataclass(frozen=True)
class IdentityMap:
    """Email to case id for admitted rows, plus counts (never values) of exclusions."""

    cases: Mapping[str, str]
    excluded: Mapping[str, int]
    supplied: int

    def case_for(self, email: str) -> str | None:
        key = canonical_email(email)
        return self.cases.get(key) if key else None

    def email_for(self, case_id: str) -> str | None:
        return next((e for e, c in self.cases.items() if c == case_id), None)


def build_identity_map(rows: list[ShowcaseRow], now: datetime) -> IdentityMap:
    """Admit at most 25 rows. Too many rows or a duplicated email fails the whole map closed."""
    if len(rows) > MAX_MAPPINGS:
        raise ShowcaseConfigError("The allowlist supplies more than 25 showcase mappings.")
    cases: dict[str, str] = {}
    excluded = dict.fromkeys(EXCLUSION_REASONS, 0)
    for row in rows:
        reason = exclusion(row, now)
        if reason is None and (row.email in cases or row.case_id in cases.values()):
            reason = "email_duplicate"
        if reason is not None:
            excluded[reason] += 1
            continue
        cases[row.email] = row.case_id
    return IdentityMap(cases, excluded, len(rows))


def authorise(
    row: ShowcaseRow, now: datetime, session_case_id: str, admitted_email: str | None
) -> None:
    """Fresh, per-request authorisation of a stored row. Raises ShowcaseDenied.

    The stored email must still equal the email the identity map admitted for this case, so a
    database change cannot leave a stale email signing in or keep an old session valid.
    """
    if (
        row.case_id != session_case_id
        or admitted_email is None
        or row.email != admitted_email
        or exclusion(row, now) is not None
    ):
        raise ShowcaseDenied("not_admitted")


CLIENT_ADDRESS_MODES = ("peer", "ingress-rightmost")


def client_key(peer: str, forwarded_for: list[str], mode: str) -> str:
    """Limiter key. `peer` is the TCP peer. `ingress-rightmost` trusts only the last
    X-Forwarded-For entry, which Azure Container Apps ingress appends; earlier entries can be set
    by the client. A missing or non-IP last entry falls back to the peer, never a client value."""
    if mode != "ingress-rightmost":
        return peer
    last = ",".join(forwarded_for).rpartition(",")[2].strip()
    try:
        return str(ipaddress.ip_address(last))
    except ValueError:
        return peer


def _b64d(value: str) -> bytes:
    pad = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + pad)


def _b64e(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


class PasswordVerifier:
    """scrypt verifier `scrypt$N$r$p$salt$hash` (base64url). The plaintext is never held."""

    MIN_N, MAX_N = 2**14, 2**16

    def __init__(self, spec: str):
        try:
            tag, n, r, p, salt, digest = spec.split("$")
            self.n, self.r, self.p = int(n), int(r), int(p)
            self.salt, self.digest = _b64d(salt), _b64d(digest)
        except (ValueError, binascii.Error):
            raise ShowcaseConfigError("The demo password verifier is not well formed.") from None
        if (
            tag != "scrypt"
            or not self.MIN_N <= self.n <= self.MAX_N
            or self.n & (self.n - 1)
            or not 1 <= self.r <= 16
            or not 1 <= self.p <= 4
            or len(self.salt) < 16
            or len(self.digest) < 32
        ):
            raise ShowcaseConfigError("The demo password verifier is not well formed.")

    def verify(self, password: str) -> bool:
        if not isinstance(password, str) or not password or len(password) > 256:
            password = ""
        derived = hashlib.scrypt(
            password.encode(),
            salt=self.salt,
            n=self.n,
            r=self.r,
            p=self.p,
            maxmem=128 * self.n * self.r * 2,
            dklen=len(self.digest),
        )
        return hmac.compare_digest(derived, self.digest) and bool(password)


def make_verifier(password: str, n: int = 2**15, r: int = 8, p: int = 1) -> str:
    """Build a verifier string for a given password. Used by tests and the later gated operator
    step; it does not generate, store or print any password."""
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode(), salt=salt, n=n, r=r, p=p, maxmem=128 * n * r * 2, dklen=32
    )
    return f"scrypt${n}${r}${p}${_b64e(salt)}${_b64e(digest)}"


def verify_login(
    verifier: PasswordVerifier, identity: IdentityMap, email: Any, password: Any
) -> str | None:
    """One scrypt run for every attempt, so unknown, malformed and wrong give the same work."""
    password_ok = verifier.verify(password if isinstance(password, str) else "")
    case_id = identity.case_for(email) if isinstance(email, str) else None
    return case_id if password_ok and case_id else None


class SessionCodec:
    """Signed, expiring, process-bound session and CSRF tokens. Key rotation or restart ends all."""

    def __init__(
        self,
        key: bytes,
        expires_at: datetime,
        clock: Callable[[], float] = time.time,
        nonce: bytes | None = None,
    ):
        if len(key) < 32:
            raise ShowcaseConfigError("The session key is too short.")
        self._key, self._nonce, self._clock = key, nonce or os.urandom(16), clock
        self._end = min(expires_at, AUTHORITY_END).timestamp()
        self._revoked: dict[str, float] = {}

    def handle(self, case_id: str) -> str:
        return hmac.new(self._key, b"handle|" + case_id.encode(), "sha256").hexdigest()[:24]

    def _mac(self, purpose: bytes, body: str) -> str:
        message = purpose + b"|" + self._nonce + b"|" + body.encode()
        return _b64e(hmac.new(self._key, message, "sha256").digest())

    def issue(self, case_id: str) -> tuple[str, int]:
        now = self._clock()
        expiry = int(min(now + SESSION_SECONDS, self._end))
        body = f"{self.handle(case_id)}.{expiry}.{secrets.token_hex(8)}"
        return f"v1.{body}.{self._mac(b'session', body)}", expiry

    def verify(self, token: str | None) -> tuple[str, str] | None:
        """Return (handle, session id) for a valid, unexpired, unrevoked token, else None."""
        parts = token.split(".") if isinstance(token, str) and len(token) < 256 else []
        if len(parts) != 5 or parts[0] != "v1":
            return None
        handle, expiry, sid, mac = parts[1:]
        body = f"{handle}.{expiry}.{sid}"
        if not hmac.compare_digest(mac, self._mac(b"session", body)):
            return None
        try:
            expires = int(expiry)
        except ValueError:
            return None
        now = self._clock()
        if now >= expires or now >= self._end or sid in self._revoked:
            return None
        return handle, sid

    def revoke(self, token: str | None) -> None:
        found = self.verify(token)
        if found:
            now = self._clock()
            self._revoked = {k: v for k, v in self._revoked.items() if v > now}
            if len(self._revoked) < 4096:
                self._revoked[found[1]] = now + SESSION_SECONDS + 1

    def new_csrf(self) -> str:
        body = secrets.token_hex(16)
        return f"{body}.{self._mac(b'csrf', body)}"

    def csrf_ok(self, cookie: str | None, header: str | None) -> bool:
        if not isinstance(cookie, str) or not isinstance(header, str) or len(cookie) > 200:
            return False
        body, _, mac = cookie.partition(".")
        return (
            bool(body)
            and hmac.compare_digest(cookie, header)
            and hmac.compare_digest(mac, self._mac(b"csrf", body))
        )


class LoginLimiter:
    """Sliding-window failure counts per source and globally. In memory; a restart resets them."""

    MAX_SOURCES = 2048

    def __init__(
        self,
        per_source: int = 5,
        overall: int = 60,
        window: int = 600,
        clock: Callable[[], float] = time.time,
    ):
        self.per_source, self.overall, self.window, self._clock = per_source, overall, window, clock
        self._by_source: dict[str, deque[float]] = {}
        self._all: deque[float] = deque()

    def _prune(self, queue: deque[float], now: float) -> None:
        while queue and queue[0] <= now - self.window:
            queue.popleft()

    def retry_after(self, source: str) -> int:
        """Seconds to wait, or 0 when an attempt is allowed."""
        now = self._clock()
        self._prune(self._all, now)
        mine = self._by_source.get(source, deque())
        self._prune(mine, now)
        waits = []
        if len(self._all) >= self.overall:
            waits.append(self._all[0] + self.window - now)
        if len(mine) >= self.per_source:
            waits.append(mine[0] + self.window - now)
        return max(1, int(max(waits)) + 1) if waits else 0

    def record_failure(self, source: str) -> None:
        now = self._clock()
        self._all.append(now)
        if source not in self._by_source and len(self._by_source) >= self.MAX_SOURCES:
            self._by_source = {k: v for k, v in self._by_source.items() if v and v[-1] > now - 60}
        if len(self._by_source) < self.MAX_SOURCES or source in self._by_source:
            self._by_source.setdefault(source, deque()).append(now)


def _bounded(value: str, limit: int = 120) -> str:
    return value.strip()[:limit]


def showcase_view(row: ShowcaseRow) -> dict[str, Any]:
    """Positive allowlist, built field by field. Nothing outside these keys can reach a resident."""
    stage = row.stage
    if stage in STAGE_ORDER and stage in _preview.STAGE_TEXT:
        progress, next_step = _preview.STAGE_TEXT[stage]
    else:
        progress, next_step = _preview.UNKNOWN_PROGRESS, _preview.UNKNOWN_NEXT
    names = [_bounded(m) for m in row.measures]
    out: dict[str, Any] = dict(
        banner=BANNER,
        viewer=dict(kind="demo resident"),
        read_only=True,
        home={
            "address": _bounded(row.address),
            "town": _bounded(row.town),
            "postcode": _bounded(row.postcode),
        },
        measures=[m for m in names if m][:20],
        progress=progress,
        next_step=next_step,
        unavailable=[dict(feature=f, reason=r) for f, r in _preview.UNAVAILABLE],
        help=_preview.HELP,
    )
    if row.closed:
        out["closed"] = "This case is recorded as closed."
    return out


@dataclass(frozen=True)
class ShowcaseConfig:
    expires_at: datetime
    allowed_hosts: tuple[str, ...]
    verifier: PasswordVerifier
    session_key: bytes
    sql: Mapping[str, str]
    bind: str
    port: int
    client_address: str = "peer"


def _loopback(server: str) -> bool:
    return server in ("localhost", "127.0.0.1", "::1")


def config_from_env(env: Mapping[str, str], now: datetime | None = None) -> ShowcaseConfig:
    """Fail closed on any missing, unsafe or mixed configuration. Never echoes a value."""
    now = now or datetime.now(UTC)
    bad = sorted(k for k in env if str(k).upper().startswith(FORBIDDEN_ENV_PREFIXES))
    if bad:
        raise ShowcaseConfigError(
            "Employee, AI or staff-store settings are present (" + ", ".join(bad[:5]) + "). "
            "The resident showcase starts only from its own configuration."
        )

    def need(name: str) -> str:
        value = env.get(name, "").strip()
        if not value:
            raise ShowcaseConfigError(f"{name} is required.")
        return value

    try:
        expires = datetime.fromisoformat(need("ZF_DEMO_EXPIRES_AT").replace("Z", "+00:00"))
    except ValueError:
        raise ShowcaseConfigError("ZF_DEMO_EXPIRES_AT is not an ISO UTC time.") from None
    if expires.utcoffset() is None or expires.utcoffset().total_seconds() != 0:  # type: ignore[union-attr]
        raise ShowcaseConfigError("ZF_DEMO_EXPIRES_AT must be an explicit UTC time.")
    if expires <= now:
        raise ShowcaseConfigError("The showcase has expired.")
    if expires > AUTHORITY_END:
        raise ShowcaseConfigError("ZF_DEMO_EXPIRES_AT is later than the authorised window.")
    hosts = tuple(h.strip().lower() for h in need("ZF_DEMO_ALLOWED_HOSTS").split(",") if h.strip())
    if not hosts or any("*" in h or " " in h for h in hosts):
        raise ShowcaseConfigError("ZF_DEMO_ALLOWED_HOSTS must list exact host names.")
    verifier = PasswordVerifier(need("ZF_DEMO_PASSWORD_VERIFIER"))
    try:
        key = _b64d(need("ZF_DEMO_SESSION_KEY"))
    except (ValueError, binascii.Error):
        raise ShowcaseConfigError("ZF_DEMO_SESSION_KEY is not base64url.") from None
    if len(key) < 32:
        raise ShowcaseConfigError("The session key is too short.")
    server, database = need("ZF_SQL_SERVER"), need("ZF_SQL_DATABASE")
    auth = (env.get("ZF_SQL_AUTH") or "msi").lower()
    sql = {"server": server, "database": database, "auth": auth}
    if auth == "msi":
        sql["client_id"] = env.get("ZF_SQL_CLIENT_ID", "").strip()
    elif auth == "password":
        if not _loopback(server):
            raise ShowcaseConfigError("Password SQL sign-in is for a loopback test server only.")
        sql.update(user=need("ZF_SQL_USER"), password=need("ZF_SQL_PASSWORD"))
        sql["port"] = env.get("ZF_SQL_PORT", "1433").strip()
        sql["trust_cert"] = "1" if env.get("ZF_SQL_TRUST_CERT") == "1" else "0"
    else:
        raise ShowcaseConfigError("ZF_SQL_AUTH must be msi (or password for a loopback test).")
    try:
        port = int(env.get("PORT", "8089"))
    except ValueError:
        raise ShowcaseConfigError("PORT is not a number.") from None
    mode = (env.get("ZF_DEMO_CLIENT_ADDRESS") or "peer").strip().lower()
    if mode not in CLIENT_ADDRESS_MODES:
        raise ShowcaseConfigError("ZF_DEMO_CLIENT_ADDRESS must be peer or ingress-rightmost.")
    return ShowcaseConfig(
        expires, hosts, verifier, key, sql, env.get("ZF_DEMO_BIND", "127.0.0.1"), port, mode
    )
