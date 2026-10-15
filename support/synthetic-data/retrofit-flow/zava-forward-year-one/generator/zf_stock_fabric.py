"""SYNTHETIC DATA ONLY. Fabric attributes for the 60,000-home stock register and
the case-to-stock link report. Every distribution below is a modelling
assumption chosen for the exercise, not a Zava North Homes fact. Output depends
only on the seed and the home ID, so it is reproducible."""
import csv
import json
import os
import random
import sys
from collections import Counter

from zf_manifest import generator_revision

VERSION = "stock-fabric-v1"
SEED = 4820260930
LABEL = "Synthetic assumption; not a company fact, survey result or EPC record."
FIELDS = ["synthetic_home_id", "build_year", "age_band", "dwelling_type", "construction", "heating",
          "fabric_is_synthetic", "fabric_version"]

# Assumed locality mix of age bands (cumulative choice weights), by locality letter.
AGE_BANDS = {
    "pre-1919": (1880, 1918), "1919-1944": (1919, 1944), "1945-1964": (1945, 1964),
    "1965-1980": (1965, 1980), "1981-1999": (1981, 1999), "2000 or later": (2000, 2024),
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
    "A": (("Mains gas boiler", 0.84), ("Electric storage", 0.08), ("Communal or district", 0.06), ("Air source heat pump", 0.02)),
    "B": (("Mains gas boiler", 0.88), ("Electric storage", 0.07), ("Communal or district", 0.02), ("Air source heat pump", 0.03)),
    "C": (("Mains gas boiler", 0.62), ("Electric storage", 0.20), ("Oil boiler", 0.12), ("Air source heat pump", 0.06)),
}
FORM_TO_DWELLING = {
    "apartments": "Flat", "bungalow": "Bungalow", "terrace": "Terraced house",
    "semidetached_house": "Semi-detached house", "detached": "Detached house",
}
ASSUMPTIONS = {
    "age_band_weights_by_locality": {k: dict(zip(AGE_BANDS, v)) for k, v in AGE_WEIGHTS.items()},
    "construction_weights_by_age_band": {k: dict(v) for k, v in CONSTRUCTION.items()},
    "heating_weights_by_locality": {k: dict(v) for k, v in HEATING.items()},
    "dwelling_type": "Mapped from the OSM building form; untagged or generic forms are drawn as house types "
                     "(Terraced 35%, Semi-detached 40%, Detached 15%, Bungalow 10%).",
}


def _pick(rng, choices):
    r, acc = rng.random(), 0.0
    for value, weight in choices:
        acc += weight
        if r < acc:
            return value
    return choices[-1][0]


def locality_letter(theme):
    return (theme.split()[1] if theme.startswith("Locality ") else "B")[:1]


def fabric(row, seed=SEED):
    rng = random.Random(f"{seed}-{VERSION}-{row['synthetic_home_id']}")
    loc = locality_letter(row.get("locality_theme", ""))
    loc = loc if loc in AGE_WEIGHTS else "B"
    band = _pick(rng, list(zip(AGE_BANDS, AGE_WEIGHTS[loc])))
    lo, hi = AGE_BANDS[band]
    dwelling = FORM_TO_DWELLING.get(row.get("building_form_osm", "")) or _pick(
        rng, (("Terraced house", 0.35), ("Semi-detached house", 0.40), ("Detached house", 0.15), ("Bungalow", 0.10)))
    return dict(synthetic_home_id=row["synthetic_home_id"], build_year=rng.randint(lo, hi), age_band=band,
                dwelling_type=dwelling, construction=_pick(rng, CONSTRUCTION[band]),
                heating=_pick(rng, HEATING[loc]), fabric_is_synthetic=True, fabric_version=VERSION)


def fabric_rows(register, seed=SEED):
    return [fabric(r, seed) for r in register]


def link_report(cases, register):
    """Resolve every case to exactly one stock home ID, or list it as unlinked."""
    ids = {r["synthetic_home_id"] for r in register}
    linked, unlinked, per_anchor = {}, [], Counter()
    for c in cases:
        anchor = c.get("synthetic_stock_anchor_id")
        if anchor in ids:
            linked[c["id"]] = anchor
            per_anchor[anchor] += 1
        else:
            unlinked.append(c["id"])
    return dict(is_synthetic=True, cases=len(cases), linked_cases=len(linked), unlinked_cases=len(unlinked),
                unlinked_case_ids=sorted(unlinked), distinct_stock_homes=len(per_anchor),
                stock_homes_shared_by_cases=sum(1 for n in per_anchor.values() if n > 1),
                stock_register_rows=len(register),
                note="Flats in one building share a stock anchor, so distinct homes are fewer than cases.")


def summary(rows, seed=SEED):
    out = dict(is_synthetic=True, label=LABEL, version=VERSION, seed=seed, generator_revision=generator_revision(),
               homes=len(rows), assumptions=ASSUMPTIONS)
    for k in ("age_band", "dwelling_type", "construction", "heating"):
        out[f"{k}_counts"] = dict(sorted(Counter(r[k] for r in rows).items()))
    return out


def main(argv=None):
    import argparse
    here = os.path.dirname(os.path.abspath(__file__))
    geo = os.path.join(here, "..", "stock-geography")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--register", default=os.path.join(geo, "private-north-east-stock-register.csv"))
    ap.add_argument("--out", default=os.path.join(geo, "private-north-east-stock-fabric.csv"))
    ap.add_argument("--summary", default=os.path.join(geo, "private-stock-fabric-summary.json"))
    a = ap.parse_args(argv)
    with open(a.register, encoding="utf-8-sig", newline="") as f:
        rows = fabric_rows(list(csv.DictReader(f)), a.seed)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(a.summary, "w", encoding="utf-8") as f:
        json.dump(summary(rows, a.seed), f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"wrote {len(rows)} fabric rows", file=sys.stderr)


if __name__ == "__main__":
    main()
