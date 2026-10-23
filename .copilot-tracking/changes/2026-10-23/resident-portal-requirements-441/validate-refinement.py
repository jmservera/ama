"""Read-only portable custody and integration checks for the issue 441 refinement."""

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EVIDENCE = HERE / "refinement-evidence"
ENTRY = "8ada8109f9d4b7348fbd8ff76839d020dec04d4b"
SPEC = importlib.util.spec_from_file_location("resident_validation", HERE / "validate-integration.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def at_entry(path):
    return subprocess.check_output(["git", "show", f"{ENTRY}:{path}"], cwd=ROOT)


def reverse_patch(patch):
    lines = patch.splitlines(keepends=True)
    result = []
    for line in lines:
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+(?:,\d+)?) \+(\d+(?:,\d+)?) @@(.*)", line)
            assert match, line
            result.append(f"@@ -{match[2]} +{match[1]} @@{match[3]}\n")
        elif line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("-"):
            result.append("+" + line[1:])
        elif line.startswith("+"):
            result.append("-" + line[1:])
        else:
            result.append(line)
    return "".join(result).encode()


def source_bytes(record):
    current = (ROOT / record["integrated_path"]).read_bytes()
    assert v.sha(current) == record["integrated_sha256"], record["integrated_path"]
    patch = record["source_to_integrated_patch"]
    source = v.reconstruct(current, reverse_patch(patch)) if patch else current
    assert v.sha(source) == record["source_sha256"] and len(source) == record["source_bytes"]
    if patch:
        assert v.reconstruct(source, patch.encode()) == current
    return source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdownlint-cli", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads((EVIDENCE / "source-to-integrated.json").read_text())
    records = mapping["files"]
    sources = {record["source"]: source_bytes(record) for record in records}
    for name, manifest, field in [
        ("prd", "prd/output-manifest.json", "outputs"),
        ("adr", "adr/reconciliation-output-manifest.json", "files"),
    ]:
        inventory = json.loads(sources[manifest])[field]
        for record in records:
            if not record["source"].startswith(name + "/"):
                continue
            path = record["source"].removeprefix(name + "/")
            if path in inventory:
                assert inventory[path]["sha256"] == record["source_sha256"], path
    pins = {
        "prd/zava-forward-retrofit-programme-demonstrator.md": "7fb40549ba4975c2feb8d8a2a3de882e06677875c02e4a43c4b3a94ddf218343",
        "prd/output-manifest.json": "cbbcc45fde3653343115a2071793cb21dcede1c335cbf1e3800e7e41a59c46b1",
        "adr/resident-service-unregistered-proposal-reconciled.md": "8e44d6ffbfe907a5e7e8cd057d0a29e0e977e916456ed0f0d9799efe8e1a4d77",
        "adr/reconciliation-output-manifest.json": "c0b97777d015926573a320d004e38f11c45e965f0540e2e64d8e241bde4f57ce",
    }
    assert all(v.sha(sources[name]) == sha for name, sha in pins.items())
    assert v.reconstruct(at_entry(v.PRD), sources["prd/amendment.patch"]) == sources[
        "prd/zava-forward-retrofit-programme-demonstrator.md"]
    current = (ROOT / v.PRD).read_text()
    counts = {}
    for prefix in ("FR", "AC", "NFR", "CON", "GOAL", "DD", "OQ"):
        before = v.prd_definitions(at_entry(v.PRD).decode(), prefix)
        after = v.prd_definitions(current, prefix)
        assert before == after, prefix
        counts[prefix] = len(after)
    acs = v.prd_definitions(current, "AC")
    assert all(acs[f"AC-{i:03}"].endswith("| Not run |") for i in range(111, 141))
    assert len(set(re.findall(r"PR442-S\d{2}", current))) == 20
    assert len(re.findall(r"^\| PRD::FR-\d{3} \|", current, flags=re.M)) == 71
    for name in (v.BRD, "docs/case_study_48_original.md", "docs/reference/memory.md"):
        assert (ROOT / name).read_bytes() == at_entry(name), name
    assert (ROOT / "docs/reference/log.md").read_bytes().startswith(at_entry("docs/reference/log.md"))
    for name in ("resident-service-boundary.excalidraw", "resident-service-boundary.svg",
                 "resident-service-boundary.png"):
        relative = (HERE / name).relative_to(ROOT).as_posix()
        assert (HERE / name).read_bytes() == at_entry(relative), name
    archive = mapping["historical_archive"]
    assert v.sha((ROOT / archive["path"]).read_bytes()) == archive["sha256"]
    assert (ROOT / archive["path"]).read_bytes() == at_entry(
        (HERE / "resident-service-unregistered-proposal.md").relative_to(ROOT).as_posix())
    proposal = (HERE / "resident-service-unregistered-proposal.md").read_text()
    assert all(s in proposal for s in ("id: null\n", "registration_status: unregistered\n",
                                      "status: proposed\n", "supersedes: null\n", "superseded-by: null\n"))
    for number in ("005", "040", "006", "024", "041", "009", "039"):
        assert f"pr442-qual-{number}" in proposal
        assert f"pr442-qual-{number}" in sources["prd/review/reviewer-result-summary.md"].decode()
    assert all(s in proposal for s in ("FAIL / Validate BLOCKED / Finalize NOT_EVALUATED",
                                      "singular = 1 < 2", "Activation OFF.", "47-element"))
    # Source archives are inert; lint/link checks apply to every navigable derivative.
    lint, links, hashes = {}, {}, {}
    for record in records:
        path = ROOT / record["integrated_path"]
        hashes[record["integrated_path"]] = v.sha(path.read_bytes())
        if path.suffix != ".md" or record["transformation"] == "exact inert source archive":
            continue
        source = source_bytes(record)
        original = v.lint(source, args.markdownlint_cli)[2]
        result = v.lint(path.read_bytes(), args.markdownlint_cli)
        introduced = result[2] - original
        assert not introduced, (record["integrated_path"], introduced)
        lint[record["integrated_path"]] = {"source_diagnostics": sum(original.values()),
                                          "integrated_diagnostics": len(result[1]), "introduced": []}
        broken = v.broken_links(path, path.read_text())
        if path == ROOT / v.PRD:
            inherited = v.broken_links(path, at_entry(v.PRD).decode())
            assert not broken - inherited, broken - inherited
            links[record["integrated_path"]] = {"inherited": sorted(broken), "introduced": []}
        else:
            assert not broken, (record["integrated_path"], broken)
            links[record["integrated_path"]] = {"inherited": [], "introduced": []}
    readme = EVIDENCE / "README.md"
    assert not v.broken_links(readme, readme.read_text())
    assert v.lint(readme.read_bytes(), args.markdownlint_cli)[0] == 0
    v.branch_changes()
    report = {
        "status": "PASS_REFINEMENT_STATIC_NOT_QUALITY_APPROVAL",
        "entry": ENTRY, "four_owner_pins": pins,
        "portable_selected_mappings": len(records), "definitions_unchanged": counts,
        "source_patch_reconstructed": True, "all_30_resident_AC": "Not run",
        "local_stories": 20, "qualified_FR_trace_rows": 71,
        "current_quality": mapping["source_quality"],
        "source_map_sha256": v.sha((EVIDENCE / "source-to-integrated.json").read_bytes()),
        "markdownlint": lint, "links": links, "sha256": hashes,
        "limits": ["All seven current quality findings remain open, not waived",
                   "Raw archives retain original link context and are not navigable derivatives",
                   "No application execution, requirements approval, registration or live acceptance",
                   "Hosted A5/B6 score citations remain OPEN; no generated score edit"],
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(records)} portable custody mappings, exact definitions and bounded links/lint")


if __name__ == "__main__":
    main()
