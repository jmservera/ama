"""Canonical stock keys and compact, collision-checked synthetic sensor keys."""

import base64
import hashlib

VERSION = "stock-sensor-identity-v2"


def home_key(value: object) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    try:
        units = len(value.encode("utf-16-le")) // 2
    except UnicodeEncodeError:
        return False
    return units <= 128 and all(ord(char) >= 32 and ord(char) != 127 for char in value)


def sensor_key(home_id: str) -> str:
    if not home_key(home_id):
        raise ValueError("Invalid canonical stock home ID")
    digest = hashlib.sha256(home_id.encode("utf-8")).digest()
    return "S" + base64.b32encode(digest).decode("ascii")[:10]
