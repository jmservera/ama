"""Match canonical asset suffixes across release queries and version directories."""

import re


def asset_url(path: str, base: str | None = None) -> re.Pattern[str]:
    origin = re.escape(base) if base is not None else r"(?:https?://[^/?#]+)?"
    return re.compile(rf"^{origin}(?:/[^/?#]+)*{re.escape(path)}(?:\?[^#]*)?(?:#.*)?$")
