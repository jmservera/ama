"""Validate native scenes, official icons, exports and source references."""
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
WORK = Path(__file__).resolve().parent
OUT = ROOT / "docs/architecture"


def check_link(path, target):
    url = urllib.parse.urlsplit(target)
    if url.scheme or target.startswith("//"):
        return
    destination = (path.parent / urllib.parse.unquote(url.path)).resolve() if url.path else path
    assert destination.exists(), f"Missing link: {path}: {target}"
    if url.fragment and destination.suffix == ".md":
        headings = re.findall(r"^#{1,6} (.+)$", destination.read_text(), re.M)
        anchors = {
            re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
            for heading in headings
        }
        assert urllib.parse.unquote(url.fragment) in anchors, f"Missing fragment: {path}: {target}"


def main():
    manifest = json.loads((WORK / "source-manifest.json").read_text())
    icons = {}
    for name, provenance in manifest["icons"].items():
        asset = OUT / f"assets/azure/{name}.svg"
        icons[name] = asset.read_bytes()
        assert hashlib.sha256(icons[name]).hexdigest() == provenance["sha256"], name
        assert asset.stat().st_mode & 0o777 == 0o644, f"Asset mode: {name}"

    results = []
    references = set()
    for expected in manifest["diagrams"]:
        name = expected["name"]
        native = OUT / f"zava-forward-{name}-architecture.excalidraw"
        scene = json.loads(native.read_text())
        elements = scene["elements"]
        by_id = {element["id"]: element for element in elements}
        assert scene["type"] == "excalidraw" and scene["version"] == 2
        assert scene["customData"]["sourceCommit"] == manifest["sourceCommit"]
        assert len(elements) == len(by_id) == expected["elements"]
        nodes = {
            element["customData"]["name"]: element
            for element in elements
            if element.get("customData", {}).get("role") == "service"
        }
        assert len(nodes) == expected["nodes"]
        artboard = elements[0]
        assert artboard["locked"]
        for element in elements:
            data = element.get("customData", {})
            for reference in data.get("sources", []):
                references.add(reference)
                check_link(ROOT / "_root.md", reference)
            if element["type"] == "arrow":
                for end, node_name in (("start", data["source"]), ("end", data["target"])):
                    node = nodes[node_name]
                    assert element[f"{end}Binding"]["elementId"] == node["id"]
                    assert {"id": element["id"], "type": "arrow"} in node["boundElements"]
                points = [(element["x"] + x, element["y"] + y) for x, y in element["points"]]
                assert all(0 <= x <= artboard["width"] and 0 <= y <= artboard["height"] for x, y in points)
            else:
                assert 0 <= element["x"] and 0 <= element["y"], element["id"]
                assert element["x"] + element["width"] <= artboard["width"], element["id"]
                assert element["y"] + element["height"] <= artboard["height"], element["id"]
            if element["type"] == "text":
                assert element["verticalAlign"] == "top"
            if element["type"] == "image":
                raw = icons[data["azureIcon"]]
                embedded = scene["files"][element["fileId"]]
                assert embedded["mimeType"] == "image/svg+xml"
                assert base64.b64decode(embedded["dataURL"].split(",", 1)[1]) == raw
                assert element["angle"] == 0 and element["scale"] == [1, 1] and element["crop"] is None
                icon = ET.fromstring(raw)
                if icon.get("viewBox"):
                    _, _, width, height = map(float, icon.get("viewBox").split())
                else:
                    width, height = float(icon.get("width")), float(icon.get("height"))
                assert abs(element["width"] / element["height"] - width / height) < 1e-8
        for node in nodes.values():
            group = node["groupIds"][0]
            members = [element for element in elements if group in element["groupIds"]]
            for role in ("title", "body"):
                labels = [element for element in members if element.get("customData", {}).get("role") == role]
                assert len(labels) == 1, f"Grouped {role}: {node['id']}"
                label = labels[0]
                assert node["x"] <= label["x"] and node["y"] <= label["y"]
                assert label["x"] + label["width"] <= node["x"] + node["width"]
                assert label["y"] + label["height"] <= node["y"] + node["height"]
        browser = json.loads((WORK / f"{name}-browser-validation.json").read_text())
        for field in ("textChanges", "overflows", "layoutFailures", "missingImages", "unboundArrows"):
            assert not browser[field], f"{name}: {field}"
        assert browser["elements"] == expected["elements"] and browser["arrows"] == expected["flows"]
        assert len(scene["files"]) == expected["icons"]
        svg_path = native.with_suffix(".svg")
        svg = ET.parse(svg_path).getroot()
        assert svg.get("role") == "img" and svg.get("aria-labelledby")
        assert svg.get("width") == str(artboard["width"]) and svg.get("height") == str(artboard["height"])
        assert len(svg.findall("{http://www.w3.org/2000/svg}title")) == 1
        assert len(svg.findall("{http://www.w3.org/2000/svg}desc")) == 1
        png = native.with_suffix(".png").read_bytes()
        assert png[:8] == b"\x89PNG\r\n\x1a\n"
        assert int.from_bytes(png[16:20], "big") == artboard["width"] * 2
        assert int.from_bytes(png[20:24], "big") == artboard["height"] * 2
        results.append({
            **expected,
            "images": browser["images"],
            "nativeIntegrity": "passed",
            "iconIntegrity": "passed",
            "browserLayout": "passed",
            "hashes": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (native, svg_path, native.with_suffix(".png"))
            },
        })

    for path in (OUT / "README.md", OUT / "assets/README.md"):
        assert path.read_text().startswith("---\n")
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            check_link(path, target)
    for relative in ("docs/reference/README.md", "docs/reference/log.md", "docs/capstone/README.md",
                     "docs/adrs/0002-pilot-readiness-architecture.md", "infra/README.md"):
        diff = subprocess.check_output(
            ["git", "diff", manifest["sourceCommit"], "--unified=0", "--", relative], cwd=ROOT, text=True
        )
        added = "\n".join(line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", added):
            check_link(ROOT / relative, target)
    old_log = subprocess.check_output(
        ["git", "show", f"{manifest['sourceCommit']}:docs/reference/log.md"], cwd=ROOT
    )
    assert (ROOT / "docs/reference/log.md").read_bytes().startswith(old_log), "Log must be append-only"
    report = {
        "sourceCommit": manifest["sourceCommit"],
        "scenes": results,
        "officialIconFiles": len(icons),
        "sourceReferences": len(references),
        "linksAndFragments": "passed",
        "knowledgeLogPrefixPreserved": True,
    }
    (WORK / "structural-validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
