"""Read-only issue 441 fresh-main recheck; writes only the requested JSON report."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT = Path(
    "/home/azureuser/.copilot/session-state/b9cc4727-b806-4e0f-a2cf-c5010d92428c/files/"
    "resident-portal-requirements-20261023"
)
CUSTODY = ROOT / (
    ".copilot-tracking/research/2026-10-23/resident-portal-requirements-441-input-custody.json"
)
BRD = ROOT / "docs/brds/agentic-retrofit-programme-brd.md"
PRD = ROOT / "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
PROPOSAL = ROOT / (
    ".copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/"
    "resident-service-unregistered-proposal.md"
)
BASE = "140d8f494482c78e84d15f3d46b9223d3c487af0"
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def check_custody():
    custody = json.loads(CUSTODY.read_text())
    result = {"base": custody["base"], "files": 0, "missing": [], "mismatch": []}
    for rel, meta in custody["files"].items():
        src = DRAFT / rel
        result["files"] += 1
        if not src.exists():
            result["missing"].append(rel)
        elif sha(src) != meta["sha256"]:
            result["mismatch"].append(rel)
    result["ok"] = not result["missing"] and not result["mismatch"]
    return result


def definitions(text, pattern):
    # Definition rows state a "shall" requirement; matrix and mapping rows do not.
    found = []
    for m in re.finditer(pattern, text, re.MULTILINE):
        if " shall " in text[m.start() : text.find("\n", m.start())]:
            found.append(m.group(1))
    return found


def check_registries():
    brd, prd = BRD.read_text(), PRD.read_text()
    out = {}
    brd_fr = definitions(brd, r"^\| (FR-\d{3}) \|")
    brd_ac = re.findall(r"\b(AC-\d{3}):", brd)
    prd_fr = definitions(prd, r"^\| (FR-\d{3}) \|")
    prd_ac = re.findall(r"\b(AC-\d{3}):", prd)
    for name, fr, ac in (("brd", brd_fr, brd_ac), ("prd", prd_fr, prd_ac)):
        out[name] = {
            "fr_rows": len(fr),
            "fr_duplicates": sorted({x for x in fr if fr.count(x) > 1}),
            "fr_max": max(fr) if fr else None,
            "ac_defs": len(ac),
            "ac_duplicates": sorted({x for x in ac if ac.count(x) > 1}),
            "ac_max": max(ac) if ac else None,
        }
    base_brd = git("show", f"{BASE}:docs/brds/agentic-retrofit-programme-brd.md")
    base_prd = git(
        "show", f"{BASE}:docs/prds/zava-forward-retrofit-programme-demonstrator.md"
    )
    out["brd_base_fr_preserved"] = set(
        definitions(base_brd, r"^\| (FR-\d{3}) \|")
    ) <= set(brd_fr)
    out["prd_base_fr_preserved"] = set(
        definitions(base_prd, r"^\| (FR-\d{3}) \|")
    ) <= set(prd_fr)
    out["brd_required_ids"] = (
        all(f"FR-{n:03d}" in brd_fr for n in range(53, 65))
        and all(f"AC-{n:03d}" in brd_ac for n in range(104, 127))
        and ("AC-084" in brd_ac)
    )
    out["prd_required_ids"] = all(
        f"FR-{n:03d}" in prd_fr for n in range(62, 74)
    ) and all(token in prd for token in ("AC-111", "AC-140", "FR-071"))
    out["ok"] = (
        out["brd_base_fr_preserved"]
        and out["prd_base_fr_preserved"]
        and out["brd_required_ids"]
        and out["prd_required_ids"]
        and not out["brd"]["fr_duplicates"]
        and not out["prd"]["fr_duplicates"]
        and not out["brd"]["ac_duplicates"]
        and not out["prd"]["ac_duplicates"]
    )
    return out


def check_policy():
    brd, prd = BRD.read_text(), PRD.read_text()
    fr044 = next(line for line in brd.splitlines() if line.startswith("| FR-044 |"))
    rule028 = next(line for line in brd.splitlines() if line.startswith("| RULE-028 |"))
    checks = {
        "fr044_names_per_output_review": "named per-output human review is required"
        in fr044,
        "fr044_exception_conditional_on_rule028": "explicitly enabled under RULE-028"
        in fr044,
        "rule028_requires_od53": "OD-53" in rule028,
        "rule028_absent_gate_means_per_message_review": (
            "named per-message human approval is required" in rule028
        ),
        "prd_mentions_per_message_default": "per-message" in prd,
        "brd_od52_55_visible": all(f"OD-{n}" in brd for n in (52, 53, 54, 55)),
        "prd_od52_55_visible": all(f"OD-{n}" in prd for n in (52, 53, 54, 55)),
    }
    checks["ok"] = all(checks.values())
    return checks


def check_formulas():
    text = BRD.read_text() + PRD.read_text()
    present = {value: value in text for value in ("-1.594", "14.74", "94.333")}
    return {"values_present": present, "ok": all(present.values())}


def check_links(paths):
    broken = []
    for path in paths:
        for target in LINK.findall(path.read_text()):
            if target.startswith(("http", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (path.parent / file_part).resolve().exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    related = [
        b for b in broken if re.search(r"resident|adrs|portal", b, re.IGNORECASE)
    ]
    return {
        "checked": [str(p.relative_to(ROOT)) for p in paths],
        "broken_resident_related": related,
        "broken_inherited_unrelated": [b for b in broken if b not in related],
        "ok": not related,
    }


def check_adr():
    branch_changes = git(
        "diff", "--name-only", "origin/main", "--", "docs/adrs"
    ).split()
    registry = sorted(p.name for p in (ROOT / "docs/adrs").glob("0*.md"))
    proposal = PROPOSAL.read_text()
    figures = sorted(
        p.name for p in PROPOSAL.parent.glob("resident-service-boundary.*")
    )
    checks = {
        "registry_is_0001_to_0006": [r[:4] for r in registry]
        == ["0001", "0002", "0003", "0004", "0005", "0006"],
        "no_adr_change_on_branch": not branch_changes,
        "no_adr_config_or_competing_registry": not (ROOT / ".adr-config.yml").exists()
        and not (ROOT / "docs/planning/adrs").exists(),
        "proposal_marked_proposed_unregistered": "proposed" in proposal.lower()
        and "unregistered" in proposal.lower(),
        "figures_present": len(figures) == 3,
        "png_chrome_wording": "Chrome" in proposal,
    }
    checks["ok"] = all(checks.values())
    checks["figure_files"] = figures
    return checks


def check_log():
    current = (ROOT / "docs/reference/log.md").read_text()
    upstream = git("show", "origin/main:docs/reference/log.md")
    entries = re.findall(r"^## \[[^\n]*\n", current, re.MULTILINE)
    last = current[current.rindex("\n## [") + 1 :]
    checks = {
        "append_only": current.startswith(upstream),
        "new_entry_is_last": current == upstream or "#441" in last,
        "entry_refs_not_closes": "Closes #441" not in current[len(upstream) :],
        "entry_keeps_gates_visible": current == upstream
        or all(t in last for t in ("OD-53", "unmet")),
        "entry_count": len(entries),
    }
    checks["ok"] = all(v for k, v in checks.items() if k != "entry_count")
    return checks


def check_freshness():
    git("fetch", "--quiet", "origin", "main")
    head = git("rev-parse", "HEAD").strip()
    origin = git("rev-parse", "origin/main").strip()
    ahead_of_origin = git("merge-base", "--is-ancestor", origin, "HEAD") == ""
    dirty = git("status", "--porcelain", "--", "docs", "src").strip()
    return {
        "head": head,
        "origin_main": origin,
        "descends_from_origin_main": ahead_of_origin,
        "dirty_docs_or_src": dirty.splitlines(),
        "ok": ahead_of_origin,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    report = {
        "freshness": check_freshness(),
        "custody": check_custody(),
        "registries": check_registries(),
        "policy": check_policy(),
        "formulas": check_formulas(),
        "links": check_links(
            [
                BRD,
                PRD,
                PROPOSAL,
                ROOT / "docs/case_study_48_addendum.md",
                ROOT / "docs/reference/README.md",
            ]
        ),
        "adr": check_adr(),
        "log": check_log(),
    }
    report["overall_ok"] = all(
        v["ok"] for v in report.values() if isinstance(v, dict) and "ok" in v
    )
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n")
    summary = {
        k: (v["ok"] if isinstance(v, dict) and "ok" in v else v)
        for k, v in report.items()
    }
    print(json.dumps(summary, indent=1))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
