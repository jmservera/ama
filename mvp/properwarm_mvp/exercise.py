"""Public fictional fixtures; no private seed, live service or startup side effects."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import io
import posixpath
import re
import zipfile
from collections.abc import Iterator, Sequence
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

FIXTURE_VERSION = "properwarm-exercise-1"
AS_OF = "2026-10-10"
MANIFEST_PATH = Path(__file__).resolve().parents[1] / "evals" / "exercise_manifest.json"
DATA_VERSION = "exercise-data-1"
DATA_FIELDS = ("coordination_note", "task_due_date")
WORKBOOK_FIELDS = ("case_id", *DATA_FIELDS)
MAX_WORKBOOK_BYTES = 5 * 1024 * 1024
_SHEET_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def data_fingerprint(case: dict) -> str:
    """Hash the complete case version, excluding persisted preview bookkeeping."""
    snapshot = copy.deepcopy(case)
    snapshot.get("exercise", {}).pop("data_previews", None)
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_data_changes(changes: dict) -> list[str]:
    """Validate only nonconsequential coordination metadata; never infer defaults."""
    errors = []
    if not isinstance(changes, dict) or not changes:
        return ["Choose at least one permitted field explicitly."]
    for field, value in changes.items():
        if field not in DATA_FIELDS:
            errors.append(f"{field}: immutable or controlled field; use individual authorised controls.")
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"{field}: supply an explicit nonempty text value.")
        elif field == "coordination_note" and len(value) > 300:
            errors.append("coordination_note: maximum 300 characters.")
        elif field == "task_due_date":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError
                date.fromisoformat(value)
            except ValueError:
                errors.append("task_due_date: use a valid YYYY-MM-DD date, not an Excel serial.")
    return errors


def _workbook_xml(raw: bytes) -> ET.Element:
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper() or b"\x00" in raw:
        raise ValueError("Workbook XML DTD/entities or non-UTF-8 encodings are unsupported.")
    try:
        return ET.fromstring(raw)
    except ET.ParseError as error:
        raise ValueError("Malformed workbook XML; repair the source copy manually.") from error


def read_case_updates(raw: bytes) -> dict:
    """Read a frozen Case updates XLSX in memory with bounded ZIP/XML expansion.

    No source workbook writes or formula evaluation occur. Invalid cells retain
    their physical row locator and require manual correction and a new preview.
    """
    if not isinstance(raw, bytes) or len(raw) > MAX_WORKBOOK_BYTES:
        raise ValueError("Workbook must be XLSX bytes of at most 5 MiB.")
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            names = [entry.filename for entry in entries]
            if (len(entries) > 20 or sum(entry.file_size for entry in entries) > 20 * 1024 * 1024
                    or len(names) != len(set(names))):
                raise ValueError("Workbook exceeds 20 entries/20 MiB expansion or contains duplicate ZIP entries.")
            xml = {}
            for entry in entries:
                if entry.flag_bits & 1 or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise ValueError("Encrypted or unsupported ZIP compression.")
                if entry.filename.endswith((".xml", ".rels")):
                    xml[entry.filename] = _workbook_xml(archive.read(entry))
            workbook = xml.get("xl/workbook.xml")
            relationships = xml.get("xl/_rels/workbook.xml.rels")
            if workbook is None or relationships is None:
                raise ValueError("Required XLSX workbook/sheet relationships are missing.")
            sheets = [sheet for sheet in workbook.findall(f"{_SHEET_NS}sheets/{_SHEET_NS}sheet")
                      if sheet.get("name") == "Case updates"]
            if len(sheets) != 1:
                raise ValueError("Declare exactly one sheet named Case updates.")
            rid = sheets[0].get(f"{_REL_NS}id")
            links = [link for link in relationships if link.get("Id") == rid]
            if len(links) != 1 or links[0].get("TargetMode") == "External":
                raise ValueError("Case updates must reference one internal worksheet.")
            target = links[0].get("Target", "")
            path = posixpath.normpath(target.lstrip("/") if target.startswith("/")
                                     else posixpath.join("xl", target))
            if not path.startswith("xl/worksheets/") or path not in xml:
                raise ValueError("Case updates worksheet path is invalid.")
            shared = []
            if "xl/sharedStrings.xml" in xml:
                shared = ["".join(node.text or "" for node in si.iter(f"{_SHEET_NS}t"))
                          for si in xml["xl/sharedStrings.xml"].findall(f"{_SHEET_NS}si")]
            physical = xml[path].findall(f"{_SHEET_NS}sheetData/{_SHEET_NS}row")
            if len(physical) > 501:
                raise ValueError("Case updates supports at most 500 data rows.")
            parsed = []
            seen_rows = set()
            for row in physical:
                number = row.get("r", "")
                if not number.isdigit() or int(number) < 1 or number in seen_rows:
                    raise ValueError("Rows require unique positive physical row numbers.")
                seen_rows.add(number)
                cells, errors = {}, []
                for cell in row.findall(f"{_SHEET_NS}c"):
                    ref = cell.get("r", "")
                    match = re.fullmatch(r"([A-Z]{1,3})([1-9]\d*)", ref)
                    if not match or match[2] != number or match[1] in cells:
                        raise ValueError("Cell reference does not match its row or is duplicated.")
                    column = match[1]
                    value = cell.findtext(f"{_SHEET_NS}v", "")
                    kind = cell.get("t")
                    if cell.find(f"{_SHEET_NS}f") is not None:
                        errors.append(f"{ref}: formulas unsupported; enter a manual literal value.")
                        value = ""
                    elif kind == "s":
                        if not value.isdigit() or int(value) >= len(shared):
                            errors.append(f"{ref}: invalid shared string index.")
                            value = ""
                        else:
                            value = shared[int(value)]
                    elif kind == "inlineStr":
                        inline = cell.find(f"{_SHEET_NS}is")
                        value = "".join(node.text or "" for node in inline.iter(f"{_SHEET_NS}t")) if inline is not None else ""
                    elif kind not in (None, "str", "d"):
                        errors.append(f"{ref}: unsupported cell type; enter text manually.")
                    cells[column] = value
                parsed.append((int(number), cells, errors))
    except (zipfile.BadZipFile, KeyError, RuntimeError, NotImplementedError, OSError) as error:
        raise ValueError("Invalid XLSX archive; provide a supported Case updates workbook.") from error
    if not parsed or parsed[0][0] != 1 or parsed[0][2]:
        raise ValueError("Case updates requires a literal header at physical row 1.")
    headers = parsed[0][1]
    if (len(headers.values()) != len(set(headers.values()))
            or any(field not in headers.values() for field in WORKBOOK_FIELDS)):
        raise ValueError("Required unique mapping: case_id, coordination_note, task_due_date.")
    rows = []
    for number, cells, errors in parsed[1:]:
        values = {headers[column]: value for column, value in cells.items() if column in headers}
        errors.extend(f"{column}{number}: unmapped cell." for column in cells if column not in headers)
        errors.extend(f"{field}: immutable or controlled column." for field in headers.values()
                      if field not in WORKBOOK_FIELDS)
        rows.append(dict(row=number, case_id=values.pop("case_id", ""), values=values, errors=errors))
    if not rows:
        raise ValueError("Case updates has no data rows.")
    return dict(source_sha256=hashlib.sha256(raw).hexdigest(), sheet="Case updates",
                mapping=headers, rows=rows, parser_version=DATA_VERSION, source_unchanged=True)

STAFF_ROLES: tuple[tuple[str, str], ...] = (
    ("EX-PM-01", "Retrofit Programme Manager"),
    ("EX-PM-02", "Retrofit Programme Manager"),
    ("EX-PSO-01", "Programme Support Officer"),
    ("EX-PSO-02", "Programme Support Officer"),
    ("EX-RLO-01", "Resident Liaison Officer"),
    ("EX-RC-01", "Retrofit Coordinator"),
    ("EX-RC-02", "Retrofit Coordinator"),
    ("EX-QI-01", "Quality Inspector"),
    ("EX-QI-02", "Quality Inspector"),
    ("EX-BSL-01", "Building Safety Liaison"),
    ("EX-GEO-01", "Grants and Evidence Officer"),
    ("EX-CON-01", "Contractor"),
)


def manifest() -> dict[str, object]:
    """Read a fresh public manifest; callers may mutate their copy independently."""
    with MANIFEST_PATH.open(encoding="utf-8") as source:
        return json.load(source)


def forecast_input(scenario: str = "steady") -> dict[str, object]:
    """Copy the manifest's four-week input and apply one declared scenario only."""
    public = manifest()
    scenarios = public["forecast_scenarios"]
    if scenario not in scenarios:
        raise ValueError(f"Unknown exercise scenario {scenario!r}; use a declared manifest scenario.")
    inputs = copy.deepcopy(public["forecast_input"])
    for key, value in scenarios[scenario].items():
        if key == "omit_source":
            inputs["sources"].pop(value)
        else:
            inputs[key] = copy.deepcopy(value)
    inputs["scenario"] = scenario
    return inputs


def _staff() -> list[dict[str, object]]:
    people = [
        {"code": code, "name": f"Fictional Colleague {index:02d}",
         "email": f"{code.lower()}@example.test", "role": role}
        for index, (code, role) in enumerate(STAFF_ROLES, 1)
    ]
    people[-1]["contractor"] = "Imaginary Retrofit Ltd"
    return people


def _case(home_id: str, index: int, *, population: str, state: str,
          building_id: str, fixture_version: str = FIXTURE_VERSION) -> dict[str, object]:
    return {
        "id": home_id, "wave": "Fictional exercise", "closed": False,
        "stage": "Contacting resident", "stage_since": AS_OF, "days_in_stage": 0,
        "waiting_on": "Fictional Colleague 05", "reason": "to record an independent resident choice",
        "owner_code": "EX-RLO-01", "owner": "Fictional Colleague 05",
        "owner_role": "Resident Liaison Officer",
        "resident": {
            "title": "Mx", "name": f"Fictional Resident {population} {index:05d}",
            "formal": f"Mx Fictional {index:05d}", "phone": "01632 960000",
            "email": f"{home_id.lower()}@example.test", "preferred": "Phone",
            "adjustment": "None", "priority_support": False, "unavailable": "",
            "representative": None,
        },
        "home": {
            "address": f"Flat {index}, Imaginary {population} Court",
            "town": "Fictional Example Borough", "postcode": "ZZ1 1ZZ",
            "area": "Fictional exercise area", "type": "Flat", "built": 1970,
            "epc": "Unknown" if population == "story" else "D",
            "tenure": "Social rent", "lat": 0, "lon": 0,
        },
        "measures": "Loft insulation",
        "contractor": {"name": "Imaginary Retrofit Ltd", "phone": "01632 960001",
                       "scope": "Fictional loft insulation", "contact": "Fictional Colleague 12"},
        "decision": {"status": "Not yet asked", "by": None, "at": None},
        "funding_ok": False, "contacts": [], "appointments": [], "hazards": [], "history": [],
        "exercise": {
            "fixture_version": fixture_version, "as_of": AS_OF, "fictional": True,
            "population": population, "building_id": building_id,
            "property_register_id": f"exercise-property:{home_id}",
            "field_authority_version": "exercise-field-authority-1",
            "scheme": {"id": "proper-warm-exercise-fund", "version": "exercise-fund-1"},
            "forecast_state": state,
            "readiness_note": "Analytical scenario prerequisite assumption only; not a service approval.",
            "source_candidates": [], "unknowns": [],
        },
    }


def dataset() -> dict[str, object]:
    """Return 2 story and 16 cohort cases, 12 staff, and the frozen as-of date.

    All approvals/consent/funding remain absent. The cohort's 12 ready and four
    held states are separate analytical assumptions, not Store release gates.
    Arbitrary metadata lives inside each case so SqlStore preserves it.
    """
    public = manifest()
    cases = [
        _case(f"EX-HOME-{index:03d}", index, population="story", state="unknown",
              building_id="EX-BUILDING-001")
        for index in (1, 2)
    ]
    for case in cases:
        metadata = case["exercise"]
        metadata["package_id"] = "EX-PACKAGE-001"
        metadata["package_applicability"] = "Not reviewed independently"
        metadata["contract"] = copy.deepcopy(public["lead_contract"])
        metadata["unknowns"] = ["Resident choice", "Independent technical reviews", "Funding evidence"]
        metadata["source_candidates"] = [
            dict(copy.deepcopy(source), sha256=hashlib.sha256(source["raw_text"].encode()).hexdigest(),
                 as_of=AS_OF, fictional=True)
            for source in public["sources"] if source["home_id"] == case["id"]
        ]
        cid = case["id"]
        metadata["lifecycle"] = "Intake"
        metadata["evidence"] = [
            {"id": f"{cid}-IDENTITY", "version": "1", "authority": "technical",
             "media_type": "text/plain", "raw_text": f'home_ids: ["{cid}"]\n',
             "field_ids": ["home_ids"], "by": "Fictional property register", "at": AS_OF},
            {"id": f"{cid}-FUND", "version": "1", "authority": "funding", "media_type": "text/plain",
             "raw_text": "eligibility: eligible\nnarrative: Fictional loft insulation programme.\nallocation_reference: EX-ALLOCATION\naward_reference: EX-AWARD\nawarded_amount: 7500 GBP\n",
             "field_ids": ["eligibility", "narrative", "allocation_reference", "award_reference", "awarded_amount"],
             "by": "Fictional fund evidence", "at": AS_OF},
            {"id": f"{cid}-FINANCE", "version": "1", "authority": "finance", "media_type": "text/plain",
             "raw_text": "eligible_cost: 16000 GBP\ntotal_cost: 20000 GBP\nco_funding: 12500 GBP\nclaim_amount: 7500 GBP\ninvoice_reference: EX-INVOICE\n",
             "field_ids": ["eligible_cost", "total_cost", "co_funding", "claim_amount", "invoice_reference"],
             "by": "Fictional finance evidence", "at": AS_OF},
            {"id": f"{cid}-HUMAN", "version": "1", "authority": "human", "media_type": "text/plain",
             "raw_text": "Evidence reference for separately entered exercise human statements; not a signature or approval.",
             "field_ids": ["match_budget_approved", "declaration", "signature", "certification", "controlled_approval"],
             "by": "Exercise human evidence reference", "at": AS_OF},
            {"id": f"{cid}-COMPLETION", "version": "1", "authority": "technical", "media_type": "text/plain",
             "raw_text": "completed: true\nfloor_area: 65 m2\nassessment_notes: Fictional supplied survey, not a site observation.\n",
             "field_ids": ["completed", "floor_area", "assessment_notes"], "by": "Fictional survey", "at": AS_OF},
        ]
        for source in metadata["source_candidates"]:
            value = "E" if source["id"] == "EX-EPC-B" else "C" if "SIBLING" in source["id"] else "D"
            metadata["evidence"].append({
                "id": source["id"], "version": source["version"], "authority": "survey",
                "media_type": "text/plain", "raw_text": f"epc_band: {value}\n",
                "field_ids": ["epc_band"], "by": "Fictional EPC source", "at": AS_OF,
            })
    cases[0]["exercise"]["unknowns"].append("Conflicting EPC D/E")
    cases[0]["resident"]["adjustment"] = "Officer-assisted contact; give notice and a named contact"
    cases[0]["exercise"]["safe_contact"] = "Phone or officer-assisted letter; no live sending"
    cases[1]["resident"]["preferred"] = "Letter"
    for row in public["forecast_input"]["homes"]:
        index = row["priority"]
        case = _case(row["id"], index, population="forecast", state=row["state"],
                     building_id=f"EX-COHORT-BUILDING-{(index + 1) // 2:03d}")
        case["exercise"].update(
            cohort_id="EX-COHORT-16", priority=index,
            source_versions={key: value["version"] for key, value in public["forecast_input"]["sources"].items()},
        )
        if row["state"] == "held":
            case["exercise"].update(hold_reason=row["hold_reason"], release_week=None,
                                    unknowns=[row["hold_reason"], "Hold release date"])
        cases.append(case)
    return {"staff": _staff(), "cases": cases, "as_of": AS_OF}


def iter_scale_homes(*, home_count: int = 60_000) -> Iterator[dict[str, object]]:
    """Stream distinct scale-only fictional cases without allocating the workload."""
    if type(home_count) is not int or home_count < 1:
        raise ValueError("home_count must be a positive integer.")
    for index in range(1, home_count + 1):
        yield _case(f"EX-SCALE-HOME-{index:06d}", index, population="scale", state="unknown",
                    building_id=f"EX-SCALE-BUILDING-{(index + 1) // 2:06d}",
                    fixture_version="properwarm-scale-1")


def iter_scale_events(*, home_count: int = 60_000,
                      events_per_home: int = 10) -> Iterator[dict[str, object]]:
    """Stream 600,000 uniquely identified events by default; not a load result."""
    if any(type(value) is not int or value < 1 for value in (home_count, events_per_home)):
        raise ValueError("home_count and events_per_home must be positive integers.")
    for index in range(1, home_count + 1):
        for sequence in range(1, events_per_home + 1):
            yield {
                "id": f"EX-SCALE-EVENT-{index:06d}-{sequence:03d}",
                "home_id": f"EX-SCALE-HOME-{index:06d}", "sequence": sequence,
                "at": f"{AS_OF}T00:00:00+00:00", "kind": "fictional_trace",
                "fixture_version": "properwarm-scale-1", "fictional": True,
                "note": "Scale-shaped trace, not an approval, resident outcome or cash event",
            }


def create_seed(output: str | Path, *, overwrite: bool = False) -> Path:
    """Write only the named seed in an existing caller-provided state directory."""
    target = Path(output)
    resolved = target.resolve()
    if any(resolved == path or path in resolved.parents for path in (Path("/tmp"), Path("/var/tmp"))):
        raise ValueError("Use an explicit non-temporary caller state directory.")
    if not target.parent.is_dir():
        raise FileNotFoundError("Create the caller state directory before writing its exercise seed.")
    if target.is_symlink():
        raise ValueError("Exercise seed output must not be a symlink.")
    with target.open("w" if overwrite else "x", encoding="utf-8") as destination:
        json.dump(dataset(), destination, indent=2, ensure_ascii=True)
        destination.write("\n")
    return target


def main(argv: Sequence[str] | None = None) -> int:
    """Generate an explicit seed; never open a database or start a server."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        create_seed(arguments.output, overwrite=arguments.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
