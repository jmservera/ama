"""SYNTHETIC DATA ONLY. EPC, survey and assessment records for the 60,000-home
stock register, derived from the stock fabric attributes so the two reconcile,
plus a manifest of seeded EPC conflicts. Every distribution is a modelling
assumption for the exercise, not a Zava North Homes fact, survey result or
lodged EPC. Output depends only on the seed and the home ID."""
import csv
import json
import os
import random
import sys
from collections import Counter
from datetime import date, timedelta

import zf_stock_fabric as fab
from zf_model import band_from_sap

VERSION = "stock-epc-v1"
SEED = 4820261015
LABEL = "Synthetic assumption; not a lodged EPC, a survey result or a company fact."
FIELDS = ["synthetic_home_id", "epc_band", "epc_sap", "epc_lodged", "epc_expires", "epc_status",
          "epc_build_age_band", "epc_dwelling_type", "epc_construction", "epc_heating",
          "survey_status", "survey_date", "survey_type", "surveyed_sap", "surveyed_band",
          "surveyed_build_age_band", "surveyed_construction", "surveyed_heating",
          "conflict_type", "epc_is_synthetic", "epc_version"]
CONFLICT_FIELDS = ["synthetic_home_id", "conflict_type", "epc_value", "surveyed_value", "description"]

SURVEY_RATE = 0.35
CONFLICT_RATE = 0.08
SAP_BASE = {"pre-1919": 42, "1919-1944": 48, "1945-1964": 54, "1965-1980": 59, "1981-1999": 65, "2000 or later": 74}
SAP_CONSTRUCTION = {"Solid brick": -4, "Stone": -6, "Timber frame": 1, "Cavity brick": 0}
SAP_HEATING = {"Mains gas boiler": 0, "Electric storage": -8, "Oil boiler": -5,
               "Communal or district": 3, "Air source heat pump": 8}
SAP_DWELLING = {"Flat": 3, "Terraced house": 1, "Bungalow": -1, "Semi-detached house": -1, "Detached house": -4}
CONFLICT_TYPES = {
    "band_differs": "Lodged EPC band differs from the band implied by the survey SAP.",
    "heating_differs": "Lodged EPC main heating differs from the surveyed main heating.",
    "construction_differs": "Lodged EPC wall construction differs from the surveyed construction.",
    "age_band_differs": "Lodged EPC build age band differs from the surveyed build age band.",
}
CONFLICT_WEIGHTS = (("band_differs", 0.55), ("heating_differs", 0.20), ("construction_differs", 0.15),
                    ("age_band_differs", 0.10))
SURVEY_TYPES = (("Retrofit assessment", 0.5), ("Condition survey", 0.3), ("Pre-works survey", 0.2))
SURVEY_START, SURVEY_END = date(2022, 1, 1), date(2026, 9, 30)
EPC_START, EPC_END = date(2010, 1, 1), date(2026, 9, 30)
AS_OF = date(2026, 10, 15)
ASSUMPTIONS = dict(
    survey_rate=SURVEY_RATE, conflict_rate_of_surveyed=CONFLICT_RATE, conflict_type_weights=dict(CONFLICT_WEIGHTS),
    sap_model="Base SAP by age band plus offsets for construction, heating and dwelling type, with bounded noise; "
              "the EPC band is derived from the SAP with the standard A-G cut-offs.",
    reconciliation="Without a seeded conflict, EPC and survey age band, dwelling type, construction and heating "
                   "equal the stock fabric attributes, and the EPC and surveyed SAP agree within 3 points.",
)


def _wall(construction):
    return next((v for k, v in SAP_CONSTRUCTION.items() if construction.startswith(k)), 0)


def _rand_date(rng, lo, hi):
    return lo + timedelta(days=rng.randint(0, (hi - lo).days))


def _alt(rng, options, current):
    return rng.choice([o for o in options if o != current])


def epc_record(row, seed=SEED, fabric_row=None):
    """Build one EPC and survey record for a register row."""
    f = fabric_row or fab.fabric(row)
    rng = random.Random(f"{seed}-{VERSION}-{row['synthetic_home_id']}")
    sap = (SAP_BASE[f["age_band"]] + _wall(f["construction"]) + SAP_HEATING[f["heating"]]
           + SAP_DWELLING[f["dwelling_type"]] + rng.randint(-5, 5))
    sap = max(5, min(95, sap))
    lodged = _rand_date(rng, max(EPC_START, date(f["build_year"], 1, 1)), EPC_END)
    expires = lodged + timedelta(days=3652)
    rec = dict(synthetic_home_id=row["synthetic_home_id"], epc_band=band_from_sap(sap), epc_sap=sap,
               epc_lodged=lodged.isoformat(), epc_expires=expires.isoformat(),
               epc_status="Expired" if expires < AS_OF else "Valid",
               epc_build_age_band=f["age_band"], epc_dwelling_type=f["dwelling_type"],
               epc_construction=f["construction"], epc_heating=f["heating"],
               survey_status="Not surveyed", survey_date="", survey_type="", surveyed_sap="", surveyed_band="",
               surveyed_build_age_band="", surveyed_construction="", surveyed_heating="", conflict_type="",
               epc_is_synthetic=True, epc_version=VERSION)
    if rng.random() >= SURVEY_RATE:
        return rec
    ssap = max(5, min(95, sap + rng.randint(-3, 3)))
    rec.update(survey_status="Surveyed", survey_date=_rand_date(rng, SURVEY_START, SURVEY_END).isoformat(),
               survey_type=fab._pick(rng, SURVEY_TYPES), surveyed_sap=ssap, surveyed_band=band_from_sap(ssap),
               surveyed_build_age_band=f["age_band"], surveyed_construction=f["construction"],
               surveyed_heating=f["heating"])
    if rng.random() < CONFLICT_RATE:
        kind = fab._pick(rng, CONFLICT_WEIGHTS)
        if kind == "band_differs":
            # The survey finds a materially different SAP, so the band moves.
            while True:
                ssap = max(5, min(95, sap + rng.choice((-1, 1)) * rng.randint(8, 18)))
                if band_from_sap(ssap) != rec["epc_band"]:
                    break
            rec.update(surveyed_sap=ssap, surveyed_band=band_from_sap(ssap))
        elif kind == "heating_differs":
            rec["epc_heating"] = _alt(rng, SAP_HEATING, f["heating"])
        elif kind == "construction_differs":
            rec["epc_construction"] = _alt(rng, [c for v in fab.CONSTRUCTION.values() for c, _ in v], f["construction"])
        else:
            rec["epc_build_age_band"] = _alt(rng, fab.AGE_BANDS, f["age_band"])
        rec["conflict_type"] = kind
    return rec


def epc_rows(register, seed=SEED):
    return [epc_record(r, seed) for r in register]


def conflict_manifest(rows):
    pairs = dict(band_differs=("epc_band", "surveyed_band"), heating_differs=("epc_heating", "surveyed_heating"),
                 construction_differs=("epc_construction", "surveyed_construction"),
                 age_band_differs=("epc_build_age_band", "surveyed_build_age_band"))
    out = []
    for r in rows:
        k = r["conflict_type"]
        if k:
            a, b = pairs[k]
            out.append(dict(synthetic_home_id=r["synthetic_home_id"], conflict_type=k, epc_value=r[a],
                            surveyed_value=r[b], description=CONFLICT_TYPES[k]))
    return out


def summary(rows, seed=SEED):
    conflicts = conflict_manifest(rows)
    return dict(is_synthetic=True, label=LABEL, version=VERSION, seed=seed, homes=len(rows),
                surveyed_homes=sum(1 for r in rows if r["survey_status"] == "Surveyed"),
                seeded_conflicts=len(conflicts),
                conflict_type_counts=dict(sorted(Counter(c["conflict_type"] for c in conflicts).items())),
                epc_band_counts=dict(sorted(Counter(r["epc_band"] for r in rows).items())),
                epc_status_counts=dict(sorted(Counter(r["epc_status"] for r in rows).items())),
                conflict_types=CONFLICT_TYPES, assumptions=ASSUMPTIONS)


def main(argv=None):
    import argparse
    here = os.path.dirname(os.path.abspath(__file__))
    geo = os.path.join(here, "..", "stock-geography")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--register", default=os.path.join(geo, "private-north-east-stock-register.csv"))
    ap.add_argument("--out", default=os.path.join(geo, "private-north-east-stock-epc.csv"))
    ap.add_argument("--manifest", default=os.path.join(geo, "private-stock-epc-conflict-manifest.csv"))
    ap.add_argument("--summary", default=os.path.join(geo, "private-stock-epc-summary.json"))
    a = ap.parse_args(argv)
    with open(a.register, encoding="utf-8-sig", newline="") as f:
        rows = epc_rows(list(csv.DictReader(f)), a.seed)
    for path, fields, data in ((a.out, FIELDS, rows), (a.manifest, CONFLICT_FIELDS, conflict_manifest(rows))):
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fields, lineterminator="\n")
            w.writeheader()
            w.writerows(data)
    with open(a.summary, "w", encoding="utf-8") as f:
        json.dump(summary(rows, a.seed), f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"wrote {len(rows)} EPC rows", file=sys.stderr)


if __name__ == "__main__":
    main()
