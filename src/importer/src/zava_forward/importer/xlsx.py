"""Minimal standard-library reader and writer for .xlsx workbooks (issue #80).

The reader opens the source file read-only and never writes to it. It reads cell
values only: formulas are not evaluated, macros are never loaded and external
links are ignored. Size limits stop oversized or zip-bomb workbooks.
"""

import io
import re
import zipfile
from collections.abc import Mapping, Sequence
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

MAX_PART_BYTES = 20 * 1024 * 1024
MAX_ROWS = 20000
MAX_COLUMNS = 200
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


class WorkbookError(ValueError):
    """The workbook cannot be read safely."""


def _part(zf: zipfile.ZipFile, name: str) -> bytes:
    info = zf.getinfo(name)
    if info.file_size > MAX_PART_BYTES:
        raise WorkbookError(f"workbook part {name} is too large")
    data = zf.read(name)
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise WorkbookError(f"workbook part {name} declares entities")
    return data


def _column_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref)
    if not letters:
        raise WorkbookError("bad cell reference")
    n = 0
    for ch in letters.group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def _text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(t.text or "" for t in node.iter(f"{{{NS['m']}}}t"))


def read_workbook(data: bytes) -> dict[str, list[list[str]]]:
    """Return sheet name -> rows of text cells from the bytes of an .xlsx file."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise WorkbookError("not a valid .xlsx file") from exc
    with zf:
        names = set(zf.namelist())
        if "xl/workbook.xml" not in names:
            raise WorkbookError("not a valid .xlsx file")
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(_part(zf, "xl/sharedStrings.xml"))
            shared = [_text(si) for si in root.findall("m:si", NS)]
        book = ET.fromstring(_part(zf, "xl/workbook.xml"))
        rels = ET.fromstring(_part(zf, "xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target", "") for r in rels.findall("pr:Relationship", NS)}
        sheets: dict[str, list[list[str]]] = {}
        for sheet in book.findall("m:sheets/m:sheet", NS):
            target = targets.get(sheet.get(f"{{{NS['r']}}}id"), "")
            path = target.lstrip("/") if target.startswith("/") else f"xl/{target}"
            if path not in names:
                continue
            sheets[sheet.get("name", "Sheet")] = _read_sheet(_part(zf, path), shared)
        return sheets


def _read_sheet(xml: bytes, shared: list[str]) -> list[list[str]]:
    root = ET.fromstring(xml)
    rows: list[list[str]] = []
    for row in root.iter(f"{{{NS['m']}}}row"):
        index = int(row.get("r", len(rows) + 1))
        if index > MAX_ROWS:
            raise WorkbookError("too many rows")
        while len(rows) < index - 1:
            rows.append([])
        cells: list[str] = []
        for c in row.findall("m:c", NS):
            col = _column_index(c.get("r", "A1"))
            if col >= MAX_COLUMNS:
                raise WorkbookError("too many columns")
            kind = c.get("t", "n")
            if kind == "s":
                v = c.find("m:v", NS)
                i = int(v.text or "0") if v is not None else 0
                value = shared[i] if i < len(shared) else ""
            elif kind == "inlineStr":
                value = _text(c.find("m:is", NS))
            else:
                v = c.find("m:v", NS)
                value = (v.text or "") if v is not None else ""
            while len(cells) < col:
                cells.append("")
            cells.append(value.strip())
        rows.append(cells)
    return rows


def safe_cell(value: object) -> str:
    """Neutralise spreadsheet formula injection in exported text."""
    text = "" if value is None else str(value)
    return "'" + text if text.startswith(FORMULA_PREFIXES) else text


def _col(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s


def write_workbook(sheets: Mapping[str, Sequence[Sequence[object]]]) -> bytes:
    """Build a values-only .xlsx (inline strings, no formulas, no macros, no links)."""
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        names = list(sheets)
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/'
            'package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.'
            'openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="'
            'application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.'
            'openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            + "".join(
                f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.'
                'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                for i in range(1, len(names) + 1)
            )
            + "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.'
            'org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.'
            'org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/workbook.xml",
            f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="{NS["m"]}" '
            f'xmlns:r="{NS["r"]}">'
            "<sheets>"
            + "".join(
                f'<sheet name="{escape(n, {chr(34): "&quot;"})}" sheetId="{i}" r:id="rId{i}"/>'
                for i, n in enumerate(names, 1)
            )
            + "</sheets></workbook>",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.'
            'org/package/2006/relationships">'
            + "".join(
                f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/'
                f'2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                for i in range(1, len(names) + 1)
            )
            + "</Relationships>",
        )
        for i, name in enumerate(names, 1):
            body = []
            for r, row in enumerate(sheets[name], 1):
                cells = "".join(
                    f'<c r="{_col(c)}{r}" t="inlineStr"><is><t xml:space="preserve">'
                    f"{escape(safe_cell(v))}</t></is></c>"
                    for c, v in enumerate(row)
                )
                body.append(f'<row r="{r}">{cells}</row>')
            zf.writestr(
                f"xl/worksheets/sheet{i}.xml",
                f'<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="{NS["m"]}"><sheetData>'
                + "".join(body)
                + "</sheetData></worksheet>",
            )
    return out.getvalue()
