"""CSV export of an application list for Excel (FR-030, issue 80).

The file is a values-only, one-way copy: editing it changes nothing in the
application, and nothing here reads a file back. The rows are exactly what the
matching list endpoint returned to the signed-in role, so the export never
widens what that role can already see; contractors get no export. It uses no AI provider.
"""

import csv
import io
import json
from collections.abc import Mapping, Sequence
from typing import Any

FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value: object) -> str:
    """Render one cell as text, neutralising spreadsheet formula injection."""
    if value is None:
        text = ""
    elif isinstance(value, bool):
        text = "Yes" if value else "No"
    elif isinstance(value, Mapping | list | tuple):
        text = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    else:
        text = str(value)
    return "'" + text if text.startswith(FORMULA_PREFIXES) else text


def to_csv(rows: Sequence[Mapping[str, Any]]) -> str:
    """Return CSV text for a list of row dicts; the columns are the keys in first-seen order."""
    headers: list[str] = []
    for row in rows:
        headers.extend(k for k in row if k not in headers)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([safe_cell(h) for h in headers])
    for row in rows:
        writer.writerow([safe_cell(row.get(h)) for h in headers])
    return buf.getvalue()
