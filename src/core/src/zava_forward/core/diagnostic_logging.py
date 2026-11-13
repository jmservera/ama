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
_SENSITIVE = re.compile(
    r"[\w.+-]+@[\w-]+\.[\w.]+|eyJ[\w-]{8,}\.[\w-]+|bearer\s+\S+|\b\d{1,3}(?:\.\d{1,3}){3}\b",
    re.IGNORECASE,
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
    consumed = "".join(f"%{p.group(1) or ''}.0s" for p in _PLACEHOLDER.finditer(match.group(2)))
    return f"{match.group(1)}={REDACTED}{consumed}"


def safe_text(text: str) -> str:
    """Redact identity-like values, query strings and payload-like key/value pairs."""
    text = _SENSITIVE.sub(REDACTED, _QUERY.sub("", text))
    text = _PAYLOAD_KEY.sub(_payload, text)
    return text if len(text) <= MAX_MESSAGE else text[:MAX_MESSAGE] + "..."


def _safe_arg(value: Any) -> Any:
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, BaseException):
        return type(value).__name__
    if isinstance(value, str):
        token = _QUERY.sub("", value)
        if _TOKEN.fullmatch(token) and not _SENSITIVE.search(token):
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
