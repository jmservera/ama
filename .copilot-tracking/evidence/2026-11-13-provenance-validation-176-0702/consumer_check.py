"""Fresh constructed outputs (new generator_revision key) through existing production consumers.

Reads only public registered payloads copied to a temp root; no private register, no SQLite store.
"""

import copy
import json
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "src/importer/tests"))
sys.path.insert(0, str(ROOT / "src/core/tests"))
sys.path.insert(0, str(ROOT / "src/api/tests"))
import dataset  # noqa: E402
import test_document_form_fixtures as t  # noqa: E402
from zava_forward.core.store import Store  # noqa: E402
from zava_forward.core.synthetic import privacy  # noqa: E402

docs = t.gen.build(t.register(), 20260901)
ctrl = t.controls.build(t.register(), 20260901)
assert "generator_revision" in docs and "generator_revision" in ctrl
print("docs_revision", docs["generator_revision"])
print("ctrl_revision", ctrl["generator_revision"])

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp) / "public"
    for source in [ROOT / privacy.PACK, *sorted((ROOT / "src").glob("*/evals"))]:
        dest = root / source.relative_to(ROOT)
        dest.mkdir(parents=True)
        for p in source.iterdir():
            if p.suffix in {".csv", ".json"}:
                shutil.copyfile(p, dest / p.name)
    print("baseline_public_issues", privacy.public_issues(root))
    (root / "src/importer/evals/document_form_fixtures.json").write_text(json.dumps(docs))
    (root / "src/core/evals/document_control_fixtures.json").write_text(json.dumps(ctrl))
    print("fresh_public_issues", privacy.public_issues(root))
    broken = copy.deepcopy(ctrl)
    del broken["cases"][0]["is_synthetic"]
    (root / "src/core/evals/document_control_fixtures.json").write_text(json.dumps(broken))
    print("negative_control_issues", [i for i in privacy.public_issues(root) if "document_control" in i])

    # Mirror of the API ScanTests body over fresh output, with the JSON Store only.
    def payload(kind, scan_class):
        magic = b"\x89PNG\r\n\x1a\n" if kind == "Photo" else b"%PDF-1.4 "
        if scan_class == "test-marker":
            from zava_forward.core.doc_controls import TEST_MARKER

            return magic + TEST_MARKER
        if scan_class == "type-mismatch":
            return b"plain text pretending to be a file"
        return magic + b"synthetic body"

    p = Path(tmp) / "zavaforward.json"
    p.write_text(json.dumps(dataset.DATA))
    st = Store(str(p))
    sam = dataset.DATA["staff"][0]
    seen, ok, refused = set(), 0, 0
    assert date.fromisoformat(ctrl["as_of"])
    for fx in ctrl["cases"]:
        for u in fx["uploads"]:
            data = payload(u["kind"], u["scan_class"])
            md = dataset.change_metadata(st, "ZF-1")
            if u["scan_class"] == "clean":
                st.add_document(sam, "ZF-1", u["name"], u["kind"], data, metadata=md)
                ok += 1
            else:
                try:
                    st.add_document(sam, "ZF-1", u["name"], u["kind"], data, metadata=md)
                except ValueError:
                    refused += 1
                else:
                    raise SystemExit("expected refusal")
            seen.add(u["scan_class"])
    print("cases", len(ctrl["cases"]), "clean_accepted", ok, "refused", refused, "classes", sorted(seen))
    print("all_clean", all(d["scan"]["status"] == "clean" for d in st.detail("ZF-1")["documents"]))
