"""SYNTHETIC DATA ONLY. Fabric attributes for the 60,000-home stock register and
the case-to-stock link report. Every distribution below is a modelling
assumption chosen for the exercise, not a Zava North Homes fact. Output depends
only on the seed and the home ID, so it is reproducible."""

import csv
import json
import random
import sys
from collections import Counter
from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Literal, TypedDict

from zava_forward.core.synthetic import output_dir, provenance

VERSION = "stock-fabric-v1"
SEED = 4820260930
LABEL = "Synthetic assumption; not a company fact, survey result or EPC record."
FIELDS = [
    "synthetic_home_id",
    "build_year",
    "age_band",
    "dwelling_type",
    "construction",
    "heating",
    "fabric_is_synthetic",
    "fabric_version",
    "is_synthetic",
]
LINK_SCOPE = "Source register anchor only; not verified stock-unit identity."

# Assumed locality mix of age bands (cumulative choice weights), by locality letter.
AGE_BANDS = {
    "pre-1919": (1880, 1918),
    "1919-1944": (1919, 1944),
    "1945-1964": (1945, 1964),
    "1965-1980": (1965, 1980),
    "1981-1999": (1981, 1999),
    "2000 or later": (2000, 2024),
}
AGE_WEIGHTS = {
    "A": (0.18, 0.14, 0.22, 0.24, 0.12, 0.10),
    "B": (0.30, 0.17, 0.22, 0.15, 0.10, 0.06),
    "C": (0.15, 0.10, 0.20, 0.25, 0.18, 0.12),
}
CONSTRUCTION = {
    "pre-1919": (("Solid brick", 0.85), ("Stone", 0.15)),
    "1919-1944": (("Solid brick", 0.40), ("Cavity brick", 0.60)),
    "1945-1964": (("Cavity brick", 0.85), ("Non-traditional (precast concrete)", 0.15)),
    "1965-1980": (("Cavity brick", 0.90), ("Timber frame", 0.10)),
    "1981-1999": (("Cavity brick, partial fill", 0.80), ("Timber frame", 0.20)),
    "2000 or later": (("Cavity brick, full fill", 0.70), ("Timber frame", 0.30)),
}
HEATING = {
    "A": (
        ("Mains gas boiler", 0.84),
        ("Electric storage", 0.08),
        ("Communal or district", 0.06),
        ("Air source heat pump", 0.02),
    ),
    "B": (
        ("Mains gas boiler", 0.88),
        ("Electric storage", 0.07),
        ("Communal or district", 0.02),
        ("Air source heat pump", 0.03),
    ),
    "C": (
        ("Mains gas boiler", 0.62),
        ("Electric storage", 0.20),
        ("Oil boiler", 0.12),
        ("Air source heat pump", 0.06),
    ),
}
FORM_TO_DWELLING = {
    "apartments": "Flat",
    "bungalow": "Bungalow",
    "terrace": "Terraced house",
    "semidetached_house": "Semi-detached house",
    "detached": "Detached house",
}
ASSUMPTIONS = {
    "age_band_weights_by_locality": {
        k: dict(zip(AGE_BANDS, v, strict=True)) for k, v in AGE_WEIGHTS.items()
    },
    "construction_weights_by_age_band": {k: dict(v) for k, v in CONSTRUCTION.items()},
    "heating_weights_by_locality": {k: dict(v) for k, v in HEATING.items()},
    "dwelling_type": "Mapped from the OSM building form; generic forms are drawn as house types "
    "(Terraced 35%, Semi-detached 40%, Detached 15%, Bungalow 10%).",
}


class StockFabric(TypedDict):
    synthetic_home_id: str
    build_year: int
    age_band: str
    dwelling_type: str
    construction: str
    heating: str
    fabric_is_synthetic: bool
    fabric_version: str
    is_synthetic: bool


class CaseLink(TypedDict):
    case_id: str
    stock_home_id: str | None
    status: Literal["linked", "unlinked"]
    reason: str | None
    shared_anchor: bool
    scope: str
    is_synthetic: bool


def _pick(rng: random.Random, choices: Sequence[tuple[str, float]]) -> str:
    r, acc = rng.random(), 0.0
    for value, weight in choices:
        acc += weight
        if r < acc:
            return value
    return choices[-1][0]


def locality_letter(theme: str) -> str:
    parts = theme.split()
    return parts[1][:1] if len(parts) > 1 and parts[0] == "Locality" else "B"


def _valid_id(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _home_id(row: Mapping[str, object]) -> str:
    value = row.get("synthetic_home_id")
    if not isinstance(value, str) or not _valid_id(value):
        raise ValueError("synthetic_home_id must be a nonblank string without outer whitespace")
    return value


def fabric(row: Mapping[str, object], seed: int = SEED) -> StockFabric:
    home_id = _home_id(row)
    rng = random.Random(f"{seed}-{VERSION}-{home_id}")
    theme = row.get("locality_theme", "")
    form = row.get("building_form_osm", "")
    if not isinstance(theme, str) or not isinstance(form, str):
        raise ValueError("locality_theme and building_form_osm must be strings")
    loc = locality_letter(theme)
    loc = loc if loc in AGE_WEIGHTS else "B"
    band = _pick(rng, list(zip(AGE_BANDS, AGE_WEIGHTS[loc], strict=True)))
    lo, hi = AGE_BANDS[band]
    dwelling = FORM_TO_DWELLING.get(form) or _pick(
        rng,
        (
            ("Terraced house", 0.35),
            ("Semi-detached house", 0.40),
            ("Detached house", 0.15),
            ("Bungalow", 0.10),
        ),
    )
    return StockFabric(
        synthetic_home_id=home_id,
        build_year=rng.randint(lo, hi),
        age_band=band,
        dwelling_type=dwelling,
        construction=_pick(rng, CONSTRUCTION[band]),
        heating=_pick(rng, HEATING[loc]),
        fabric_is_synthetic=True,
        fabric_version=VERSION,
        is_synthetic=True,
    )


def fabric_rows(register: Sequence[Mapping[str, object]], seed: int = SEED) -> list[StockFabric]:
    ids = [_home_id(row) for row in register]
    if len(ids) != len(set(ids)):
        raise ValueError(
            "Duplicate synthetic_home_id; cannot generate an unambiguous fabric snapshot"
        )
    return [fabric(r, seed) for r in register]


def resolve_cases(
    cases: Sequence[Mapping[str, object]], register: Sequence[Mapping[str, object]]
) -> list[CaseLink]:
    """Match exact register references, never infer a unit from shared geography."""
    ids = Counter(
        row["synthetic_home_id"] for row in register if _valid_id(row.get("synthetic_home_id"))
    )
    case_ids: set[str] = set()
    anchors = Counter(
        c["synthetic_stock_anchor_id"]
        for c in cases
        if _valid_id(c.get("synthetic_stock_anchor_id"))
    )
    links: list[CaseLink] = []
    for c in cases:
        cid = c.get("id")
        if not isinstance(cid, str) or not _valid_id(cid) or cid in case_ids:
            raise ValueError("Case IDs must be unique nonblank strings without outer whitespace")
        case_ids.add(cid)
        anchor = c.get("synthetic_stock_anchor_id")
        if anchor is None or anchor == "":
            reason = "missing_stock_anchor"
        elif not isinstance(anchor, str) or not _valid_id(anchor):
            reason = "invalid_stock_anchor"
        elif ids[anchor] == 0:
            reason = "stock_anchor_not_found"
        elif ids[anchor] != 1:
            reason = "ambiguous_stock_anchor"
        else:
            reason = None
        matched = anchor if isinstance(anchor, str) and reason is None else None
        links.append(
            CaseLink(
                case_id=cid,
                stock_home_id=matched,
                status="linked" if matched else "unlinked",
                reason=reason,
                shared_anchor=matched is not None and anchors[matched] > 1,
                scope=LINK_SCOPE,
                is_synthetic=True,
            )
        )
    return links


def link_report(
    cases: Sequence[Mapping[str, object]], register: Sequence[Mapping[str, object]]
) -> dict[str, object]:
    links = resolve_cases(cases, register)
    per_anchor = Counter(link["stock_home_id"] for link in links if link["status"] == "linked")
    unlinked = [link["case_id"] for link in links if link["status"] == "unlinked"]
    return dict(
        is_synthetic=True,
        cases=len(cases),
        linked_cases=len(cases) - len(unlinked),
        unlinked_cases=len(unlinked),
        unlinked_case_ids=sorted(unlinked),
        distinct_stock_homes=len(per_anchor),
        stock_homes_shared_by_cases=sum(n > 1 for n in per_anchor.values()),
        stock_register_rows=len(register),
        resolutions=sorted(links, key=lambda link: link["case_id"]),
        scope=LINK_SCOPE,
        note="Legacy home counters count source anchors, not verified dwellings. "
        "Shared anchors do not establish shared unit identity.",
    )


def attach_fabric(
    cases: Sequence[MutableMapping[str, object]],
    register: Sequence[Mapping[str, object]],
    seed: int = SEED,
) -> dict[str, Mapping[str, object]]:
    """Attach source-anchor assumptions; leave operational fields and decisions alone."""
    links = resolve_cases(cases, register)
    counts = Counter(
        row["synthetic_home_id"] for row in register if _valid_id(row.get("synthetic_home_id"))
    )
    unique = {
        _home_id(row): row
        for row in register
        if _valid_id(row.get("synthetic_home_id")) and counts[row["synthetic_home_id"]] == 1
    }
    additions: list[tuple[CaseLink, StockFabric | None]] = [
        (link, fabric(unique[link["stock_home_id"]], seed) if link["stock_home_id"] else None)
        for link in links
    ]
    for case, (link, attrs) in zip(cases, additions, strict=True):
        case["stock_link"] = link
        case.pop("stock_fabric", None)
        case.pop("stock_epc", None)
        if attrs is not None:
            case["stock_fabric"] = {
                key: value for key, value in attrs.items() if key != "synthetic_home_id"
            }
    return unique


def revision_sources() -> tuple[Path, ...]:
    return (Path(__file__), Path(provenance.__file__), Path(__file__).with_name("__init__.py"))


def summary(rows: Sequence[StockFabric], seed: int = SEED) -> dict[str, object]:
    out: dict[str, object] = dict(
        is_synthetic=True,
        label=LABEL,
        version=VERSION,
        seed=seed,
        generator_revision=provenance.source_revision(revision_sources()),
        homes=len(rows),
        assumptions=ASSUMPTIONS,
    )
    for k in ("age_band", "dwelling_type", "construction", "heating"):
        out[f"{k}_counts"] = dict(sorted(Counter(r[k] for r in rows).items()))
    return out


def _records(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, list) or not all(
        isinstance(row, dict) and all(isinstance(key, str) for key in row) for row in value
    ):
        raise ValueError(f"{label} must be a list of objects")
    return value


def _destination(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    # Installed CLI may run outside a checkout; reject checkout destinations when present.
    roots = [p for p in Path(__file__).resolve().parents if (p / ".git").exists()]
    roots.extend(p for p in (Path.cwd(), *Path.cwd().parents) if (p / ".git").exists())
    # Include existing ancestors even when the requested snapshot does not exist yet.
    roots.extend(p for p in (path, *path.parents) if (p / ".git").exists())
    if any(path.is_relative_to(root) for root in roots):
        raise ValueError("Private stock output must be outside the repository")
    if Path(value).expanduser().is_symlink():
        raise ValueError("Refusing symlink output")
    return path


def main(argv: Sequence[str] | None = None) -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument(
        "--register", type=Path, default=output_dir("private-north-east-stock-register.csv")
    )
    ap.add_argument(
        "--cases", type=Path, help="Optional case seed JSON, preserved with link evidence"
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=output_dir("stock-fabric"),
        help="New/empty snapshot directory outside the repository",
    )
    a = ap.parse_args(argv)
    try:
        out = _destination(a.out)
        with a.register.open(encoding="utf-8-sig", newline="") as f:
            register: list[Mapping[str, object]] = list(csv.DictReader(f))
        if not register:
            raise ValueError("Stock register must contain at least one home")
        rows = fabric_rows(register, a.seed)
        report = summary(rows, a.seed)
        data = None
        if a.cases:
            data = json.loads(a.cases.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Case seed must be an object")
            cases = _records(data.get("cases"), "cases")
            attach_fabric(cases, register, a.seed)
            data["stock_link"] = link_report(cases, register)
            data["stock_fabric_seed"] = a.seed
        out = provenance.prepare_output(out)
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    with (out / "stock-fabric.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    if data is not None:
        (out / "linked-cases.json").write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    report["file_sha256"] = provenance.file_hashes(p for p in out.iterdir() if p.is_file())
    with (out / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"wrote {len(rows)} fabric rows", file=sys.stderr)


if __name__ == "__main__":
    main()
