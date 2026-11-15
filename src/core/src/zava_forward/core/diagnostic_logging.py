"""Fail-closed diagnostic log redaction (issue 146).

Diagnostic logs must not carry personal data, raw readings or chat content. Call sites write
developer-authored format strings; this module makes every record safe regardless of the
arguments they pass. It patches `Logger.makeRecord`, so every logger in the process is covered,
including `extra` fields and exception text, which are dropped. Only numbers, booleans and short
token-like strings survive as arguments; everything else becomes a placeholder. If redaction
itself fails the message is withheld. `print` output is not logging and is unchanged.
"""

from __future__ import annotations

import logging
import re
import sys
from collections.abc import Mapping
from typing import Any

WITHHELD = "<withheld>"
REDACTED = "<redacted>"
MAX_MESSAGE = 300
METER_LOGGER = "zava_forward.core.ai_consumption"
_TOKEN = re.compile(r"[A-Za-z0-9./][A-Za-z0-9._:/=-]{0,127}")
SENSITIVE = re.compile(
    r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
    r"|eyJ[\w-]{8,}\.[\w-]+"
    r"|\b(?:bearer|basic)\s+\S+"
    r"|\b\d{1,3}(?:\.\d{1,3}){3}\b"
    r"|(?<!\w)(?:\+44\s?|0)\d(?:[\s-]?\d){8,10}(?!\w)"
    r"|\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b"
    r"|\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b"
    r"|\bsk-[\w-]{16,}"
    r"|\b[0-9a-f]{32,}\b"
    r"|[A-Za-z0-9+/]{40,}={0,2}"
    r"|\b(?:api[-_ ]?key|apikey|subscription[-_]?key|account[-_]?key|access[-_]?key"
    r"|shared[-_]?access[-_]?signature"
    r"|client[-_]?secret|secret|password|passwd|pwd|token|signature|sig|sv|se|sp|srt|sas[-_]?token"
    r"|authorization|connection[-_]?string|uprn|resident[-_]?ref|household[-_]?ref|tenant[-_]?id"
    r"|resident|tenant|name|address|postcode|phone|email)\s*[=:]\s*(?:(?:bearer|basic)\s+)?\S+",
    re.IGNORECASE,
)
_TRACEBACK = re.compile(r"Traceback \(most recent call last\):.*", re.DOTALL)
_EXCEPTION_TEXT = re.compile(
    r"\b([A-Za-z_][\w.]*(?:Error|Exception))(?:\s*:[^\n]*|\((?:'[^']*'|\"[^\"]*\"|[^()'\"])*\))"
)
_QUERY = re.compile(r"(?<=\w)\?\S+")
_PAYLOAD_KEY = re.compile(
    r"\b(prompt|message|content|chat|reading|readings|body|text|answer|completion|question)"
    r"\s*[=:]\s*(\S+)",
    re.IGNORECASE,
)
_PLACEHOLDER = re.compile(r"%(\([^)]*\))?[-#0 +]*\d*(?:\.\d+)?[sdirfxXeEgG]")
_original: Any = None


def _payload(match: re.Match[str]) -> str:
    # `%.0s` still consumes the matching argument but prints nothing.
    return f"{match.group(1)}={REDACTED}{_consumed(match.group(2))}"


def _consumed(text: str) -> str:
    return "".join(f"%{p.group(1) or ''}.0s" for p in _PLACEHOLDER.finditer(text))


def _mask(match: re.Match[str]) -> str:
    return REDACTED + _consumed(match.group(0))


def _exception_text(match: re.Match[str]) -> str:
    return f"{match.group(1)}: {REDACTED}{_consumed(match.group(0))}"


def safe_text(text: str) -> str:
    """Redact identities, secrets, formatted exception text, query strings and payload pairs."""
    text = _TRACEBACK.sub(_mask, text)
    text = _EXCEPTION_TEXT.sub(_exception_text, text)
    text = SENSITIVE.sub(_mask, _QUERY.sub("", text))
    text = _PAYLOAD_KEY.sub(_payload, text)
    return text if len(text) <= MAX_MESSAGE else text[:MAX_MESSAGE] + "..."


def _safe_arg(value: Any) -> Any:
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, BaseException):
        return type(value).__name__
    if isinstance(value, str):
        token = _QUERY.sub("", value)
        if _TOKEN.fullmatch(token) and not SENSITIVE.search(token):
            return token
    return WITHHELD


def _safe_args(args: Any) -> Any:
    if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Mapping):
        args = args[0]
    if isinstance(args, Mapping):
        return {key: _safe_arg(value) for key, value in args.items()}
    if isinstance(args, tuple):
        return tuple(_safe_arg(value) for value in args)
    return args


def _exception_name(exc_info: Any) -> str | None:
    if exc_info is True:
        exc_info = sys.exc_info()
    if isinstance(exc_info, BaseException):
        return type(exc_info).__name__
    if isinstance(exc_info, tuple) and exc_info and exc_info[0] is not None:
        return str(getattr(exc_info[0], "__name__", WITHHELD))
    return None


def _make_record(
    self: logging.Logger,
    name: str,
    level: int,
    fn: str,
    lno: int,
    msg: object,
    args: Any,
    exc_info: Any,
    func: str | None = None,
    extra: Mapping[str, object] | None = None,
    sinfo: str | None = None,
) -> logging.LogRecord:
    try:
        text = safe_text(msg if isinstance(msg, str) else WITHHELD)
        safe = _safe_args(args)
        exc = _exception_name(exc_info)
        if exc:
            text += f" exc={_safe_arg(exc)}"
    except Exception:
        text, safe = WITHHELD, ()
    record: logging.LogRecord = _original(
        self, name, level, fn, lno, text, safe, None, func, None, None
    )
    return record


def install_diagnostic_redaction(*, console: bool = True) -> None:
    """Idempotently redact every log record in this process.

    With `console`, a stderr handler exists and the AI meter logger passes INFO, so the content-free
    `AI_LIMIT_BREACH` and `AI_USAGE` markers reach the container console.
    """
    global _original
    if _original is None:
        _original = logging.Logger.makeRecord
        logging.Logger.makeRecord = _make_record  # type: ignore[method-assign]
    if console:
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.WARNING, format="%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        logging.getLogger(METER_LOGGER).setLevel(logging.INFO)


def uninstall_diagnostic_redaction() -> None:
    global _original
    if _original is not None:
        logging.Logger.makeRecord = _original  # type: ignore[method-assign]
        _original = None
