"""Issue 441 criterion 9 verifier: read-only for the working tree (runs git fetch) and writes only the requested JSON report."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRD = "docs/brds/agentic-retrofit-programme-brd.md"
PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
ADD = "docs/case_study_48_addendum.md"
IDX = "docs/reference/README.md"
PROP_DIR = ".copilot-tracking/changes/2026-10-23/resident-portal-requirements-441"
PROP = f"{PROP_DIR}/resident-service-unregistered-proposal.md"
CUSTODY = ".copilot-tracking/research/2026-10-23/resident-portal-requirements-441-input-custody.json"
LINT_CONFIG = f"{PROP_DIR}/markdownlint.json"
DOCS = [BRD, PRD, ADD, IDX, PROP]
LINT_DOCS = [BRD, PRD, ADD, PROP]
BASE = "140d8f494482c78e84d15f3d46b9223d3c487af0"
PRE_1519 = "b605f78a3^"


def git(*args, check=True):
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if check and done.returncode:
        raise RuntimeError(f"git {args[0]} failed: {done.stderr.strip()}")
    return done.stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Tree:
    """Read access to the working tree or to a Git revision."""

    def __init__(self, rev=None):
        self.rev = rev
        if rev:
            self.files = set(git("ls-tree", "-r", "--name-only", rev).splitlines())
            self.dirs = {str(p) for f in self.files for p in Path(f).parents}

    def read(self, rel):
        if self.rev:
            return git("show", f"{self.rev}:{rel}")
        return (ROOT / rel).read_text()

    def exists(self, rel):
        if self.rev:
            return rel in self.files or rel in self.dirs
        return (ROOT / rel).exists()


def strip_code(lines):
    """Yield (number, line) outside fenced code with inline code spans removed."""
    fence = None
    for number, line in enumerate(lines, 1):
        marker = re.match(r"\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
            elif marker.group(1)[0] == fence:
                fence = None
            continue
        if fence is None:
            yield number, re.sub(r"`[^`]*`", "", line)


def slug(heading):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"<[^>]+>", "", text).replace("`", "").replace("*", "")
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def anchors(text):
    seen = Counter()
    found = set()
    for _, line in strip_code(text.splitlines()):
        match = re.match(r"#{1,6}\s+(.*?)\s*#*\s*$", line)
        if match:
            base = slug(match.group(1))
            count = seen[base]
            found.add(base if count == 0 else f"{base}-{count}")
            seen[base] += 1
    return found


def targets(line):
    """Return inline link targets of a line, tracking balanced parentheses."""
    out, start = [], 0
    while (at := line.find("](", start)) != -1:
        depth, i = 1, at + 2
        while i < len(line) and depth:
            depth += {"(": 1, ")": -1}.get(line[i], 0)
            i += 1
        raw = line[at + 2 : i - 1].strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1 : raw.index(">")]
        else:
            raw = raw.split(" ")[0]
        out.append(raw)
        start = i
    return out


def check_links(tree, docs):
    broken, total, external, unsupported = [], 0, 0, Counter()
    anchor_cache = {}

    def anchors_of(rel):
        if rel not in anchor_cache:
            anchor_cache[rel] = anchors(tree.read(rel))
        return anchor_cache[rel]

    for rel in docs:
        text = tree.read(rel)
        lines = text.splitlines()
        for number, line in strip_code(lines):
            if re.match(r"\[[^\]]+\]:\s", line):
                unsupported["reference_definitions"] += 1
            if re.search(r"<a\s+(id|name)=", line):
                unsupported["html_anchors"] += 1
            for target in targets(line):
                if not target:
                    continue
                if re.match(r"[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                    external += 1
                    continue
                total += 1
                path_part, _, fragment = target.partition("#")
                fragment = urllib.parse.unquote(fragment)
                if path_part:
                    dest = (
                        Path(rel).parent.as_posix()
                        + "/"
                        + urllib.parse.unquote(path_part).rstrip("/")
                    )
                    parts = []
                    for piece in dest.split("/"):
                        if piece == "..":
                            parts.pop()
                        elif piece != ".":
                            parts.append(piece)
                    dest = "/".join(parts)
                else:
                    dest = rel
                if not tree.exists(dest):
                    broken.append(f"{rel}:{number} -> {target} (missing file)")
                elif fragment:
                    if dest.endswith(".md"):
                        if fragment.lower() not in anchors_of(dest):
                            broken.append(
                                f"{rel}:{number} -> {target} (missing anchor)"
                            )
                    else:
                        unsupported["non_markdown_fragments"] += 1
    return {
        "checked_files": docs,
        "relative_links": total,
        "external_links_not_fetched": external,
        "broken": broken,
        "unsupported_constructs_not_checked": dict(unsupported),
    }


def check_freshness():
    git("fetch", "--quiet", "origin", "main")
    origin = git("rev-parse", "origin/main").strip()
    head = git("rev-parse", "HEAD").strip()
    source_diff = git("diff", "--name-only", "origin/main", "HEAD", "--", "docs", "src")
    dirty = [
        line
        for line in git(
            "status", "--porcelain=v1", "--untracked-files=all"
        ).splitlines()
        if not line[3:].startswith(".copilot-tracking/")
    ]
    return {
        "origin_main": origin,
        "head": head,
        "docs_src_diff_vs_origin_main": source_diff.split(),
        "dirty_outside_tracking": dirty,
        "ok": not source_diff.strip() and not dirty,
    }


def check_hashes():
    rels = DOCS + [
        f"{PROP_DIR}/resident-service-boundary.{ext}"
        for ext in ("excalidraw", "svg", "png")
    ]
    rows = {}
    for rel in rels:
        data = (ROOT / rel).read_bytes()
        rows[rel] = {"bytes": len(data), "sha256": sha(data)}
    return {"files": rows, "ok": True}


def check_custody():
    custody = json.loads((ROOT / CUSTODY).read_text())
    archive = ROOT / PROP_DIR / "source-evidence"
    matched, mismatched, not_archived = [], [], []
    for rel, meta in custody["files"].items():
        copy = archive / rel
        if not copy.exists():
            not_archived.append(rel)
        elif sha(copy.read_bytes()) == meta["sha256"]:
            matched.append(rel)
        else:
            mismatched.append(rel)
    return {
        "declared": len(custody["files"]),
        "base": custody["base"],
        "matched": len(matched),
        "mismatched": mismatched,
        "not_archived": not_archived,
        "ok": custody["base"] == BASE and not mismatched,
    }


def ids(text, pattern):
    return re.findall(pattern, text, re.MULTILINE)


def rng(prefix, low, high):
    return [f"{prefix}-{n:03d}" for n in range(low, high + 1)]


def check_traceability(brd, prd, base_brd, base_prd):
    brd_fr = ids(brd, r"^\| (FR-\d{3}) \|[^\n]* shall ")
    brd_ac = ids(brd, r"\b(AC-\d{3}):")
    prd_fr = ids(prd, r"^\| (FR-\d{3}) \|[^\n]* shall ")
    prd_ac = ids(prd, r"^\| (AC-\d{3}) \| Given ")
    dup = lambda xs: sorted(x for x, n in Counter(xs).items() if n > 1)
    out = {
        "brd_fr_definition_rows": len(brd_fr),
        "prd_fr_definition_rows": len(prd_fr),
        "brd_ac_definitions": len(brd_ac),
        "prd_ac_definition_rows": len(prd_ac),
        "duplicates": {
            "brd_fr": dup(brd_fr),
            "brd_ac": dup(brd_ac),
            "prd_fr": dup(prd_fr),
            "prd_ac": dup(prd_ac),
        },
    }
    out["brd_missing"] = [x for x in rng("FR", 53, 64) if x not in brd_fr] + [
        x for x in rng("AC", 104, 132) + ["AC-084"] if x not in brd_ac
    ]
    out["prd_missing"] = [x for x in rng("FR", 62, 73) if x not in prd_fr] + [
        x for x in rng("AC", 111, 140) if x not in prd_ac
    ]
    out["base_fr_preserved"] = {
        "brd": set(ids(base_brd, r"^\| (FR-\d{3}) \|[^\n]* shall ")) <= set(brd_fr),
        "prd": set(ids(base_prd, r"^\| (FR-\d{3}) \|[^\n]* shall ")) <= set(prd_fr),
    }
    # PRD criterion rows name their requirement in the third column.
    unmapped, bad_brd_refs = [], []
    for line in prd.splitlines():
        m = re.match(
            r"^\| (AC-(?:11[1-9]|1[23]\d|140)) \|.*\| ([^|]+) \| Not run \|$", line
        )
        if not m:
            continue
        if not re.search(r"\b(FR|NFR|GOAL)-\d{3}\b|GOAL-\d{3}", m.group(2)):
            unmapped.append(m.group(1))
    out["prd_ac_without_requirement"] = unmapped
    matrix = re.findall(
        r"^\| (FR-0(?:6[2-9]|7[0-3])) \| (AC-[^|]+) \| (BRD[^|]*) \|$",
        prd,
        re.MULTILINE,
    )
    out["prd_matrix_rows"] = len(matrix)
    out["prd_matrix_missing"] = [
        f for f in rng("FR", 62, 71) if f not in {m[0] for m in matrix}
    ]
    for _, _, brd_refs in matrix:
        for ref in re.findall(r"\b(FR-\d{3})\b", brd_refs):
            if ref not in brd_fr:
                bad_brd_refs.append(ref)
    out["prd_matrix_brd_refs_unresolved"] = sorted(set(bad_brd_refs))
    out["ok"] = (
        not any(out["duplicates"].values())
        and not out["brd_missing"]
        and not out["prd_missing"]
        and all(out["base_fr_preserved"].values())
        and not unmapped
        and not out["prd_matrix_missing"]
        and not out["prd_matrix_brd_refs_unresolved"]
    )
    return out


def table_row(text, label):
    for line in text.splitlines():
        if line.startswith("| ") and line[2:].startswith(label):
            cells = [c.strip() for c in line.strip("|").split("|")]
            return [float(c.replace(",", "").replace("%", "")) for c in cells[1:]]
    raise KeyError(label)


def formulas(brd):
    names = {
        "A": "New home cases/week",
        "D": "Mean elapsed active-case",
        "C": "Routine calls per active",
        "Tc": "Staff minutes per routine call",
        "E": "Separate routine email",
        "Te": "Staff minutes per email",
        "U": "Share of active cases",
        "V": "Share of those adopters",
        "R": "Additional reviews/escalations",
        "Tr": "Staff minutes per additional",
        "Q": "Additional channel reconciliation",
        "S": "Fixed recurring",
    }
    inp = {k: table_row(brd, v) for k, v in names.items()}
    inp["To"] = table_row(brd, "Staff onboarding minutes")
    for k in ("U", "V"):
        inp[k] = [x / 100 for x in inp[k]]
    rows = {
        k: []
        for k in ["W", "calls", "email", "B", "G", "H", "J", "S", "N", "O", "F", "I"]
    }
    for i in range(3):
        v = {k: inp[k][i] for k in inp}
        w = v["A"] * v["D"]
        b = w * (v["C"] * v["Tc"] + v["E"] * v["Te"]) / 60
        g = b * v["U"] * v["V"]
        h = w * v["U"] * v["R"] * v["Tr"] / 60
        j = w * v["Q"] / 60
        n = g - h - j - v["S"]
        o = v["A"] * v["U"] * v["To"] / 60
        for key, val in zip(
            rows,
            [
                w,
                w * v["C"],
                w * v["E"],
                b,
                g,
                h,
                j,
                v["S"],
                n,
                o,
                n - o,
                w * v["U"] * v["To"] / 60,
            ],
        ):
            rows[key].append(val)
    published = {
        "W": "Concurrent active home cases W",
        "calls": "Routine baseline calls/week",
        "email": "Separate email/document transactions/week",
        "B": "Routine baseline staff hours/week B",
        "G": "Gross avoided handling hours/week G",
        "H": "Additional review/escalation hours/week H",
        "J": "Reconciliation hours/week J",
        "S": "Recurring support hours/week S",
        "N": "Routine net released hours/week N",
        "O": "New-intake onboarding hours/week O",
        "F": "Net released hours/week including intake F",
        "I": "Initial active-cohort onboarding hours I",
    }
    result = {}
    for key, label in published.items():
        pub = table_row(brd, label)
        result[key] = {
            "published": pub,
            "recomputed": [round(x, 4) for x in rows[key]],
            "ok": all(abs(p - c) <= 0.005 for p, c in zip(pub, rows[key])),
        }
    return inp, rows, result


def check_formulas(brd, prd):
    inp, rows, table = formulas(brd)
    base_inp = {k: v[1] for k, v in inp.items()}
    slope = (
        rows["B"][1] * base_inp["V"]
        - rows["W"][1] * base_inp["R"] * base_inp["Tr"] / 60
        - base_inp["A"] * base_inp["To"] / 60
    )
    intercept = -(rows["J"][1] + base_inp["S"])
    breakeven_u = -intercept / slope
    breakeven_v = (rows["H"][1] + rows["J"][1] + base_inp["S"] + rows["O"][1]) / (
        rows["B"][1] * base_inp["U"]
    )
    uptake = [slope * u + intercept for u in (0.25, 0.5, 0.75)]
    prd_stated = [-1.594, 14.74, 94.333]
    checks = {
        "table_rows_x_scenarios": f"{len(table)}x3",
        "table_ok": all(r["ok"] for r in table.values()),
        "prd_combined_sensitivities": {
            "stated": prd_stated,
            "recomputed": [round(x, 3) for x in rows["F"]],
            "ok": all(abs(s - c) < 0.0006 for s, c in zip(prd_stated, rows["F"]))
            and all(
                str(s).replace("-", "-") in prd for s in ("-1.594", "14.74", "94.333")
            ),
        },
        "slope_intercept": [round(slope, 3), round(intercept, 3)],
        "slope_text_present": "F(U) = 35.4 × U − 2.96" in brd,
        "break_even_uptake": round(breakeven_u * 100, 2),
        "break_even_uptake_text_present": "**8.36%**" in brd,
        "break_even_v": round(breakeven_v * 100, 2),
        "break_even_v_text_present": "**29.90%**" in brd,
        "uptake_25_50_75": [round(x, 2) for x in uptake],
        "uptake_text_present": "5.89/14.74/23.59" in brd,
        "prd_one_off_48_present": "**48 one-off hours**" in prd,
        "prd_not_forecast_wording": "not forecasts" in prd,
    }
    checks["rows"] = table
    checks["ok"] = (
        checks["table_ok"]
        and checks["prd_combined_sensitivities"]["ok"]
        and checks["slope_text_present"]
        and checks["break_even_uptake"] == 8.36
        and checks["break_even_uptake_text_present"]
        and checks["break_even_v"] == 29.90
        and checks["break_even_v_text_present"]
        and checks["uptake_25_50_75"] == [5.89, 14.74, 23.59]
        and checks["uptake_text_present"]
        and checks["prd_one_off_48_present"]
        and checks["prd_not_forecast_wording"]
    )
    return checks


def check_policy(brd, prd):
    lines = brd.splitlines()
    fr044 = next(x for x in lines if x.startswith("| FR-044 |"))
    rule = next(x for x in lines if x.startswith("| RULE-028 |"))
    log = (ROOT / "docs/reference/log.md").read_text()
    checks = {
        "fr044_named_per_output_review": "named per-output human review is required"
        in fr044,
        "fr044_exception_conditional_on_rule028": "explicitly enabled under RULE-028"
        in fr044,
        "rule028_requires_od53": "OD-53" in rule,
        "rule028_absent_gate_per_message": "named per-message human approval is required"
        in rule,
        "brd_od52_55": all(f"OD-{n}" in brd for n in range(52, 56)),
        "prd_od52_55": all(f"OD-{n}" in prd for n in range(52, 56)),
        "prd_per_message_default": "per-message" in prd,
        "log_has_no_closes_441": not re.search(r"\bcloses #441\b", log, re.IGNORECASE),
    }
    checks["ok"] = all(checks.values())
    return checks


def check_adr():
    prop = (ROOT / PROP).read_text()
    registry = sorted(p.name for p in (ROOT / "docs/adrs").glob("0*.md"))
    checks = {
        "docs_adrs_registry": registry,
        "proposal_unregistered_and_proposed": "unregistered" in prop.lower()
        and "proposed" in prop.lower(),
        "no_resident_adr_id": not any("resident" in r for r in registry),
        "no_adr_config_or_competing_registry": not (ROOT / ".adr-config.yml").exists()
        and not (ROOT / "docs/planning/adrs").exists(),
        "png_chrome_wording": "Chrome" in prop,
        "figures": sorted(
            p.name for p in (ROOT / PROP_DIR).glob("resident-service-boundary.*")
        ),
    }
    checks["ok"] = (
        all(v for k, v in checks.items() if k not in ("docs_adrs_registry", "figures"))
        and len(checks["figures"]) == 3
    )
    return checks


def targeted_anchor_lines():
    results = {}
    for rel, number in ((PRD, 609), (ADD, 1510)):
        line = (ROOT / rel).read_text().splitlines()[number - 1]
        found = targets(line)
        sub = check_links(Tree(), [rel])
        results[f"{rel}:{number}"] = {
            "targets": found,
            "file_has_broken_links": [b for b in sub["broken"] if f":{number} " in b],
        }
    results["ok"] = all(
        not v["file_has_broken_links"] and v["targets"] for v in results.values()
    )
    return results


def lint(root_dir, docs):
    config = ROOT / LINT_CONFIG
    done = subprocess.run(
        ["npx", "--yes", "markdownlint-cli2", "--config", str(config), *docs],
        cwd=root_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    found = Counter()
    for line in (done.stdout + done.stderr).splitlines():
        m = re.match(r"(\S+?):\d+(?::\d+)? (?:error )?(MD\d+)/\S+ (.*)$", line)
        if m:
            found[(m.group(1), m.group(2), m.group(3)[:200])] += 1
    return found, done.returncode


def check_lint():
    current, code = lint(ROOT, LINT_DOCS)
    with tempfile.TemporaryDirectory(prefix="verify441-") as tmp:
        for rel in LINT_DOCS:
            if rel == PROP:
                continue
            target = Path(tmp) / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(git("show", f"{PRE_1519}:{rel}"))
        proposal = Path(tmp) / PROP
        proposal.parent.mkdir(parents=True, exist_ok=True)
        proposal.write_text(git("show", f"{PRE_1519}:{PROP}"))
        baseline, base_code = lint(Path(tmp), LINT_DOCS)
    new = current - baseline
    return {
        "tool": "npx markdownlint-cli2 with the retained 2026-10-23 config",
        "exit_current": code,
        "current_diagnostics": sum(current.values()),
        "baseline_rev": PRE_1519,
        "baseline_diagnostics": sum(baseline.values()),
        "baseline_exit": base_code,
        "new_vs_baseline": [list(k) + [v] for k, v in sorted(new.items())],
        "by_rule_current": dict(Counter(k[1] for k in current.elements())),
        "ok": not new,
    }


def check_link_comparison():
    now = check_links(Tree(), DOCS)
    old = check_links(Tree(PRE_1519), DOCS)
    strip = lambda items: {re.sub(r":\d+ ->", " ->", x) for x in items}
    return {
        "current": now,
        "pre_1519_same_method": {
            "broken": old["broken"],
            "relative_links": old["relative_links"],
        },
        "new_since_pre_1519": sorted(strip(now["broken"]) - strip(old["broken"])),
        "repaired_since_pre_1519": sorted(strip(old["broken"]) - strip(now["broken"])),
        "owned_scope_broken": [b for b in now["broken"] if not b.startswith(IDX)],
        "ok": not [b for b in now["broken"] if not b.startswith(IDX)],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    brd, prd = (ROOT / BRD).read_text(), (ROOT / PRD).read_text()
    report = {
        "freshness": check_freshness(),
        "hashes": check_hashes(),
        "custody": check_custody(),
        "traceability": check_traceability(
            brd, prd, git("show", f"{BASE}:{BRD}"), git("show", f"{BASE}:{PRD}")
        ),
        "formulas": check_formulas(brd, prd),
        "policy": check_policy(brd, prd),
        "adr": check_adr(),
        "links": check_link_comparison(),
        "targeted_anchors": targeted_anchor_lines(),
        "lint": check_lint(),
    }
    report["overall_ok"] = all(v["ok"] for v in report.values())
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {k: v["ok"] if isinstance(v, dict) else v for k, v in report.items()},
            indent=1,
        )
    )
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
