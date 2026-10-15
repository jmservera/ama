"""SYNTHETIC DATA ONLY. Document, form-schema and field-candidate fixtures.

Builds 120 synthetic case/building/document families from the 60,000-home
synthetic stock register: 30 tuning, 30 calibration and 60 held-out. Each
family has a survey report, EPC certificate, invoice and evidence-photo
descriptor (no image bytes, no real personal data, no street addresses), the
approved synthetic form schema, twelve gold field values, an optional seeded
defect with a fixture-owned expected result, and a dependency manifest.

Same seed and register give byte-identical output.

Usage:
    python3 zf_documents.py --seed 20260901 --out ../../../../mvp/evals/document_form_fixtures.json
"""
import argparse
import csv
import hashlib
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(HERE, "..", "stock-geography", "private-north-east-stock-register.csv")
VERSION = "document-form-fixtures-v1"
SPLITS = (("tuning", 30), ("calibration", 30), ("held-out", 60))
SCHEMA_VERSION = "SYN-FUND-FORM-1.0"
RULES_VERSION = "SYN-RULES-1.0"
TEMPLATE_VERSION = "SYN-INVOICE-TPL-1.0"
BUDGET_CEILING = 12000
FIELDS = ("home_id", "building_form", "floor_area_m2", "current_epc_band", "current_epc_score", "measure",
          "survey_date", "net_cost_gbp", "vat_gbp", "invoice_total_gbp", "match_funding_gbp", "eligibility_status")
# Fields that must be present, and the one that is only required for a given eligibility.
REQUIRED = tuple(f for f in FIELDS if f != "match_funding_gbp")
DEFECTS = {
    "duplicate-home": ("home_id", "RULE-DUP-001"),
    "missing-required": ("measure", "RULE-REQ-001"),
    "missing-conditional": ("match_funding_gbp", "RULE-COND-001"),
    "wrong-unit": ("floor_area_m2", "RULE-UNIT-001"),
    "wrong-currency": ("net_cost_gbp", "RULE-CUR-001"),
    "changed-total": ("invoice_total_gbp", "RULE-CALC-001"),
    "unknown-eligibility": ("eligibility_status", "RULE-ELIG-001"),
    "unapproved-match-budget": ("match_funding_gbp", "RULE-BUDGET-001"),
}
MEASURES = ("Loft insulation", "Cavity wall insulation", "Air source heat pump", "Solar PV", "Windows and doors")
BANDS = (("D", 55, 68), ("E", 39, 54), ("F", 21, 38), ("C", 69, 80))
FORM_AREA = {"apartments": (38, 70), "bungalow": (55, 90), "terrace": (60, 95), "semidetached_house": (70, 110),
             "detached": (90, 160)}


def load_register(path=REGISTER):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _pick_families(register, seed):
    # One home per neighbourhood cluster so related homes never straddle splits.
    rng = random.Random(f"{seed}:families")
    by_cluster = {}
    for row in sorted(register, key=lambda r: r["synthetic_home_id"]):
        by_cluster.setdefault(row["synthetic_neighbourhood_cluster_id"], []).append(row)
    clusters = sorted(by_cluster)
    rng.shuffle(clusters)
    need = sum(n for _, n in SPLITS)
    if len(clusters) < need:
        raise ValueError(f"register has {len(clusters)} clusters, {need} needed")
    return [rng.choice(by_cluster[c]) for c in clusters[:need]]


def _gold(row, rng):
    form = row["building_form_osm"]
    lo, hi = FORM_AREA.get(form, (60, 100))
    band, lo_s, hi_s = rng.choice(BANDS)
    net = rng.randrange(1500, 9500, 50)
    vat = round(net * 0.2, 2)
    return {
        "home_id": row["synthetic_home_id"], "building_form": form, "floor_area_m2": rng.randint(lo, hi),
        "current_epc_band": band, "current_epc_score": rng.randint(lo_s, hi_s), "measure": rng.choice(MEASURES),
        "survey_date": f"2026-{rng.randint(1, 9):02d}-{rng.randint(1, 28):02d}", "net_cost_gbp": float(net),
        "vat_gbp": vat, "invoice_total_gbp": round(net + vat, 2), "match_funding_gbp": float(rng.randrange(500, 3000, 50)),
        "eligibility_status": "Eligible",
    }


def _apply_defect(kind, gold, family_no, other_home):
    """Return (observed values, observed currency, expected failing result)."""
    obs = dict(gold)
    currency = "GBP"
    if kind == "duplicate-home":
        obs["home_id"] = other_home
    elif kind == "missing-required":
        obs["measure"] = None
    elif kind == "missing-conditional":
        obs["eligibility_status"] = "Eligible - match funding required"
        obs["match_funding_gbp"] = None
    elif kind == "wrong-unit":
        obs["floor_area_m2"] = round(gold["floor_area_m2"] * 10.7639, 1)
        obs["floor_area_unit"] = "sq ft"
    elif kind == "wrong-currency":
        currency = "EUR"
    elif kind == "changed-total":
        obs["invoice_total_gbp"] = round(gold["invoice_total_gbp"] + 125.0, 2)
    elif kind == "unknown-eligibility":
        obs["eligibility_status"] = "Unknown"
    elif kind == "unapproved-match-budget":
        obs["match_funding_gbp"] = float(BUDGET_CEILING + 500 + 50 * family_no)
    return obs, currency


def _expected(kind, family_id):
    field, rule = DEFECTS[kind]
    return {"defect": kind, "field": field, "rule_id": rule, "schema_version": SCHEMA_VERSION,
            "rules_version": RULES_VERSION, "expected_status": "fail", "blocks_reviewed_pack": True,
            "calculated_fields_reproducible": kind != "changed-total",
            "reported_for": family_id}


def _documents(fid, obs, currency, gold):
    label = {"is_synthetic": True, "label": "SYNTHETIC - not a real document", "family_id": fid}
    area = obs.get("floor_area_m2")
    unit = obs.get("floor_area_unit", "m2")
    return [
        dict(label, doc_id=f"{fid}-SURVEY", kind="Survey report", fields=["home_id", "building_form", "floor_area_m2",
             "measure", "survey_date"],
             text=f"Retrofit assessment report. Home {obs['home_id']} ({obs['building_form']}). "
                  f"Floor area: {area} {unit}. Recommended measure: {obs['measure']}. Surveyed {obs['survey_date']}."),
        dict(label, doc_id=f"{fid}-EPC", kind="EPC certificate", fields=["current_epc_band", "current_epc_score"],
             text=f"Energy performance certificate (synthetic). Home {gold['home_id']}. Rating "
                  f"{obs['current_epc_band']} ({obs['current_epc_score']})."),
        dict(label, doc_id=f"{fid}-INVOICE", kind="Invoice", template_version=TEMPLATE_VERSION,
             fields=["net_cost_gbp", "vat_gbp", "invoice_total_gbp", "match_funding_gbp"],
             text=f"Invoice. Net {obs['net_cost_gbp']} {currency}; VAT {obs['vat_gbp']}; Total "
                  f"{obs['invoice_total_gbp']}; match funding {obs['match_funding_gbp']}. "
                  f"Eligibility: {obs['eligibility_status']}."),
        dict(label, doc_id=f"{fid}-PHOTO", kind="Evidence photo", image_bytes=None, fields=[],
             text=f"Descriptor only: photo of {gold['measure'].lower()} location at home {gold['home_id']}; no image data."),
    ]


def _manifest(fid):
    # Fixture-owned expected stale sets (AC-051) for each single-source change.
    return [
        {"change": f"invoice template {TEMPLATE_VERSION} replaced", "changed_source": f"{fid}-INVOICE",
         "affected_fields": ["net_cost_gbp", "vat_gbp", "invoice_total_gbp", "match_funding_gbp"],
         "affected_calculations": ["invoice_total_check", "match_budget_check"],
         "unaffected_fields": [f for f in FIELDS if f not in ("net_cost_gbp", "vat_gbp", "invoice_total_gbp",
                                                              "match_funding_gbp")],
         "reviewed_export_blocked": True},
        {"change": f"EPC certificate {fid}-EPC superseded", "changed_source": f"{fid}-EPC",
         "affected_fields": ["current_epc_band", "current_epc_score"],
         "affected_calculations": ["eligibility_check"],
         "unaffected_fields": [f for f in FIELDS if f not in ("current_epc_band", "current_epc_score")],
         "reviewed_export_blocked": True},
    ]


def schema():
    return {"is_synthetic": True, "label": "SYNTHETIC placeholder schema; real funding schema unresolved (PRD OQ-015)",
            "schema_id": "SYN-FUND-FORM", "version": SCHEMA_VERSION, "rules_version": RULES_VERSION,
            "approval": {"status": "synthetic fixture only", "approved_by": None},
            "match_budget_ceiling_gbp": BUDGET_CEILING,
            "fields": [dict(name=f, required=f in REQUIRED, conditional_on=("eligibility_status contains match funding"
                       if f == "match_funding_gbp" else None)) for f in FIELDS],
            "calculations": [{"id": "invoice_total_check", "formula": "net_cost_gbp + vat_gbp == invoice_total_gbp",
                              "inputs": ["net_cost_gbp", "vat_gbp", "invoice_total_gbp"]},
                             {"id": "match_budget_check", "formula": "match_funding_gbp <= match_budget_ceiling_gbp",
                              "inputs": ["match_funding_gbp"]},
                             {"id": "eligibility_check", "formula": "eligibility_status in {Eligible}",
                              "inputs": ["eligibility_status", "current_epc_band", "current_epc_score"]}],
            "units": {"floor_area_m2": "m2", "currency": "GBP"}}


def build(register, seed):
    homes = _pick_families(register, seed)
    rng = random.Random(f"{seed}:content")
    families, i = [], 0
    for split, count in SPLITS:
        for j in range(count):
            row = homes[i]
            i += 1
            fid = f"DF-{i:03d}"
            gold = _gold(row, rng)
            kind = list(DEFECTS)[(j // 2) % len(DEFECTS)] if j % 2 == 0 else None
            other = homes[i % len(homes)]["synthetic_home_id"]
            obs, currency = _apply_defect(kind, gold, i, other) if kind else (dict(gold), "GBP")
            families.append({
                "family_id": fid, "split": split, "is_synthetic": True, "synthetic_home_id": row["synthetic_home_id"],
                "neighbourhood_cluster_id": row["synthetic_neighbourhood_cluster_id"],
                "local_authority": row["local_authority"], "gold_fields": gold, "observed_fields": obs,
                "currency": currency, "documents": _documents(fid, obs, currency, gold),
                "seeded_defect": _expected(kind, fid) if kind else None, "dependency_manifest": _manifest(fid)})
    out = {"is_synthetic": True, "generator_version": VERSION, "seed": seed, "stock_register_rows": len(register),
           "split_counts": dict(SPLITS), "form_schema": schema(), "families": families}
    out["content_sha256"] = hashlib.sha256(json.dumps(families, sort_keys=True).encode()).hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260901)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = build(load_register(), a.seed)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"wrote {a.out}: {len(out['families'])} families")


if __name__ == "__main__":
    main()
