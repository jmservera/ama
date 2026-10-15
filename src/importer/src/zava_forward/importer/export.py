"""One-way export of a list to CSV or Excel with history, and read-only comparison (FR-030).

Excel stays one-way and read-only: the workbook is a values-only snapshot
labelled as a copy; editing it changes nothing in the application. The history
sheet carries version, source, approval and supersession from the application
record, so it does not depend on any AI provider.
"""

import csv
import io
from collections.abc import Sequence
from dataclasses import dataclass, field

from .quarantine import BatchRecord
from .xlsx import safe_cell, write_workbook

NOTE = (
    "Read-only copy exported from Zava Forward (synthetic demo data). "
    "Changes made in this file are not "
    "imported back. Use the import preview to propose changes for human approval."
)
HISTORY_HEAD = [
    "Version",
    "Source file",
    "Source SHA-256",
    "Status",
    "Staged by",
    "Staged at",
    "Approved or decided by",
    "Decided at",
    "Superseded by version",
    "Data label",
]


def to_csv(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow([safe_cell(h) for h in headers])
    for r in rows:
        w.writerow([safe_cell(v) for v in r])
    return buf.getvalue()


def history_rows(history: Sequence[BatchRecord]) -> list[list[object]]:
    version_of = {b.batch_id: b.version for b in history}
    return [
        [
            b.version,
            b.source_name,
            b.source_sha256,
            b.status,
            b.staged_by,
            b.staged_at,
            b.decided_by or "",
            b.decided_at or "",
            version_of.get(b.superseded_by or "", ""),
            b.data_label,
        ]
        for b in history
    ]


def to_xlsx(
    sheet_name: str,
    headers: Sequence[str],
    rows: Sequence[Sequence[object]],
    history: Sequence[BatchRecord],
) -> bytes:
    return write_workbook(
        {
            "Read me": [[NOTE]],
            sheet_name[:31]: [list(headers), *[list(r) for r in rows]],
            "History": [HISTORY_HEAD, *history_rows(history)],
        }
    )


@dataclass
class Comparison:
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    changed: dict[str, dict[str, tuple[str, str]]] = field(default_factory=dict)
    unchanged: list[str] = field(default_factory=list)
    message: str = "Read-only comparison: nothing was changed in the application or the file."


def compare(current: dict[str, dict[str, str]], incoming: dict[str, dict[str, str]]) -> Comparison:
    """Compare the application rows (current) with an import (incoming) by key; never writes."""
    out = Comparison()
    for key in sorted(incoming):
        if key not in current:
            out.added.append(key)
            continue
        diff = {
            f: (current[key].get(f, ""), v)
            for f, v in incoming[key].items()
            if current[key].get(f, "") != v
        }
        if diff:
            out.changed[key] = diff
        else:
            out.unchanged.append(key)
    out.removed = sorted(k for k in current if k not in incoming)
    return out
