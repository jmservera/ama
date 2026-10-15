"""Declared workbook structures, column mapping, conflicts and row-level preview (FR-029, SA-005).

Only declared structures are imported. Preview is pure: it reads rows already
extracted from a copy of the bytes and returns a report. The source file is
hashed before and after reading and is never opened for writing.
"""

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from zava_forward.core.doc_controls import LocalSignatureScanner

from .xlsx import WorkbookError, read_workbook

POSTCODE = re.compile(r"[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}")
SYNTHETIC = "synthetic-demo"
MAX_SOURCE_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class Field:
    name: str
    aliases: tuple[str, ...]
    required: bool = True
    pattern: re.Pattern[str] | None = None


@dataclass(frozen=True)
class Structure:
    name: str
    sheet: str
    key: str
    fields: tuple[Field, ...]


CASE_LIST = Structure(
    name="case-list",
    sheet="Cases",
    key="reference",
    fields=(
        Field("reference", ("reference", "ref", "case id", "case reference")),
        Field("address", ("address", "property", "property address")),
        Field("postcode", ("postcode", "post code", "postal code"), pattern=POSTCODE),
        Field("stage", ("stage", "workflow stage")),
        Field("status", ("status",), required=False),
        Field("owner", ("owner", "case owner"), required=False),
    ),
)
STRUCTURES = {CASE_LIST.name: CASE_LIST}


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


@dataclass
class ColumnMatch:
    field: str
    header: str | None
    column: int | None
    how: str


@dataclass
class PreviewRow:
    row: int
    values: dict[str, str]
    problems: list[str]
    lineage: dict[str, object]


@dataclass
class Preview:
    structure: str
    source_name: str
    source_sha256: str
    sheet: str
    columns: list[ColumnMatch]
    conflicts: list[str]
    rows: list[PreviewRow] = field(default_factory=list)
    unmapped_headers: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return bool(self.conflicts)

    @property
    def ready(self) -> int:
        return sum(1 for r in self.rows if not r.problems)

    @property
    def to_fix(self) -> list[PreviewRow]:
        return [r for r in self.rows if r.problems]

    message = "Your file has not been changed."


def match_columns(
    structure: Structure, headers: list[str]
) -> tuple[list[ColumnMatch], list[str], list[str]]:
    """Map headers to declared fields; report conflicts and unmapped headers."""
    normed = [_norm(h) for h in headers]
    taken: dict[int, str] = {}
    matches: list[ColumnMatch] = []
    conflicts: list[str] = []
    for f in structure.fields:
        names = [_norm(f.name), *(_norm(a) for a in f.aliases)]
        hits = [i for i, h in enumerate(normed) if h and h in names]
        if len(hits) > 1:
            conflicts.append(
                f"Several columns match {f.name}: " + ", ".join(headers[i] for i in hits)
            )
        if hits:
            i = hits[0]
            if i in taken:
                conflicts.append(f"Column {headers[i]} matches both {taken[i]} and {f.name}")
            taken[i] = f.name
            how = "exact" if normed[i] == _norm(f.name) else "alias"
            matches.append(ColumnMatch(f.name, headers[i], i, how))
        else:
            matches.append(ColumnMatch(f.name, None, None, "unmapped"))
            if f.required:
                conflicts.append(f"Required column {f.name} is missing")
    unmapped = [h for i, h in enumerate(headers) if h and i not in taken]
    return matches, conflicts, unmapped


def build_preview(
    structure: Structure, source_name: str, source_sha256: str, sheets: dict[str, list[list[str]]]
) -> Preview:
    sheet = structure.sheet if structure.sheet in sheets else next(iter(sheets), "")
    rows = sheets.get(sheet, [])
    if not rows:
        return Preview(
            structure.name,
            source_name,
            source_sha256,
            sheet,
            [],
            [f"Sheet {structure.sheet} is empty or missing"],
        )
    columns, conflicts, unmapped = match_columns(structure, rows[0])
    prev = Preview(
        structure.name,
        source_name,
        source_sha256,
        sheet,
        columns,
        conflicts,
        unmapped_headers=unmapped,
    )
    seen: dict[str, int] = {}
    by_name = {c.field: c for c in columns}
    for n, raw in enumerate(rows[1:], start=2):
        if not any(raw):
            continue
        values = {}
        for f in structure.fields:
            col = by_name[f.name].column
            values[f.name] = raw[col].strip() if col is not None and col < len(raw) else ""
        problems = [
            f"{f.name} is empty" for f in structure.fields if f.required and not values[f.name]
        ]
        for f in structure.fields:
            if f.pattern and values[f.name] and not f.pattern.fullmatch(values[f.name]):
                problems.append(f"{f.name} looks wrong")
        key = values.get(structure.key, "")
        if key:
            if key in seen:
                problems.append(f"duplicate {structure.key} (first on row {seen[key]})")
                conflicts.append(f"Duplicate {structure.key} {key} on rows {seen[key]} and {n}")
            else:
                seen[key] = n
        prev.rows.append(
            PreviewRow(
                n,
                values,
                problems,
                {
                    "source_sha256": source_sha256,
                    "source_name": source_name,
                    "sheet": sheet,
                    "row": n,
                },
            )
        )
    return prev


def preview_file(path: Path, structure: Structure = CASE_LIST) -> tuple[Preview, bytes]:
    """Scan, hash and preview a workbook; the source is read once and never written."""
    before = path.stat()
    if before.st_size > MAX_SOURCE_BYTES:
        raise WorkbookError("file is too large")
    with path.open("rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    verdict, detail = LocalSignatureScanner().scan("import", digest[:12], path.name, data, "")
    if verdict != "clean":
        raise WorkbookError(f"file did not pass the content scan: {verdict} ({detail})")
    prev = build_preview(structure, path.name, digest, read_workbook(data))
    after = path.stat()
    if (after.st_size, after.st_mtime_ns) != (before.st_size, before.st_mtime_ns):
        raise WorkbookError("the source file changed while it was being read")
    return prev, data
