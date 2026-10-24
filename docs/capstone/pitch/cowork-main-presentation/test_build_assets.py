"""Regression checks for safe notes rebuilds and interruption navigation."""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest


@pytest.fixture
def package(tmp_path):
    source = Path(__file__).resolve().parent
    target = tmp_path / "package"
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "test_*.py"))
    return target


def rebuild(package, *arguments):
    return subprocess.run(
        [sys.executable, str(package / "build_assets.py"), *arguments],
        check=True, capture_output=True, text=True,
    )


def test_given_edited_drawings_when_notes_rebuilt_then_native_and_previews_preserved(package):
    native = next((package / "diagrams").glob("*.excalidraw"))
    drawing = json.loads(native.read_text())
    drawing["author_edit"] = "Retain this native edit"
    native.write_text(json.dumps(drawing))
    svg = native.with_suffix(".svg")
    svg.write_text(svg.read_text() + "\n<!-- Author-edited preview -->\n")
    png = native.with_suffix(".png")
    png.write_bytes(b"author-owned preview")
    expected = {path: path.read_bytes() for path in (native, svg, png)}

    rebuild(package)

    assert {path: path.read_bytes() for path in expected} == expected


def test_given_explicit_reset_when_rebuilt_then_native_diagrams_reset(package):
    native = next((package / "diagrams").glob("*.excalidraw"))
    drawing = json.loads(native.read_text())
    drawing["author_edit"] = "Reset only with explicit permission"
    native.write_text(json.dumps(drawing))

    rebuild(package, "--reset-diagrams")

    assert "author_edit" not in json.loads(native.read_text())


@pytest.mark.parametrize(
    ("caller", "backup", "topic"),
    [("S01", "B15", "S16"), ("S03", "B06", "S05"),
     ("S06", "B05", "S09"), ("S15", "B15", "S16")],
)
def test_given_interruption_when_notes_generated_then_return_to_caller_not_topic(
    package, caller, backup, topic
):
    data = json.loads((package / "slides.json").read_text())
    assert backup in next(slide for slide in data["main"] if slide["id"] == caller)["interrupt"]
    assert next(slide for slide in data["backup"] if slide["id"] == backup)["return"] == topic

    rebuild(package)
    section = (package / "backup-slides.md").read_text().split(f"## {backup}:", 1)[1].split("\n## ", 1)[0]

    assert data["navigation"]["interruption_return"] == "calling-main-slide"
    assert "return to the calling main slide" in section
    assert f"Index entry only: topic destination {topic}" in section


@pytest.mark.parametrize("ident", ["S09", "S11", "B05", "B09", "B25"])
def test_given_cost_figures_removed_when_rebuilt_then_fails_before_writing(package, ident):
    path = package / "slides.json"
    data = json.loads(path.read_text())
    slide = next(slide for slide in data["main"] + data["backup"] if slide["id"] == ident)
    slide["on_slide"] = ["Cost details omitted"]
    path.write_text(json.dumps(data))
    original = (package / "speaker-script.md").read_bytes()

    with pytest.raises(subprocess.CalledProcessError, match="non-zero exit status"):
        rebuild(package)

    assert (package / "speaker-script.md").read_bytes() == original


@pytest.mark.parametrize("name,value", [
    ("tasks_per_home", "40"), ("usd_per_million_tokens", "2.00"),
    ("works_gbp_per_home", "7000"), ("conditional_grant_share", "0.40"),
])
def test_given_changed_cost_input_when_figures_stale_then_rebuild_fails(package, name, value):
    path = package / "slides.json"
    data = json.loads(path.read_text())
    data["cost_model"][name] = value
    path.write_text(json.dumps(data))

    with pytest.raises(subprocess.CalledProcessError):
        rebuild(package, "--check-only")


def test_given_current_native_deck_when_checked_then_cost_comparison_preserved(package):
    root = Path(__file__).resolve().parents[4]
    deck = root / "docs/capstone/deck/zava-forward-cowork-v2-draft.pptx"

    result = rebuild(package, "--check-only", "--check-pptx", str(deck))

    assert "Cost comparison checked" in result.stdout


@pytest.mark.parametrize("ident,qualifier", [
    ("S09", "Historical"), ("S11", "Planning scenario"),
    ("B05", "non-inference"), ("B09", "Conditional"), ("B25", "unknown"),
])
def test_given_missing_cost_qualification_when_checked_then_fails(package, ident, qualifier):
    path = package / "slides.json"
    data = json.loads(path.read_text())
    slide = next(slide for slide in data["main"] + data["backup"] if slide["id"] == ident)
    slide["on_slide"] = [line.replace(qualifier, "") for line in slide["on_slide"]]
    path.write_text(json.dumps(data))

    with pytest.raises(subprocess.CalledProcessError):
        rebuild(package, "--check-only")


@pytest.mark.parametrize("replacement", [
    b"<slide><text>Cost comparison omitted</text></slide>",
    b'<!DOCTYPE slide [<!ENTITY cost "untrusted">]><slide>&cost;</slide>',
])
def test_given_missing_or_unsafe_native_cost_slide_when_checked_then_fails(package, replacement):
    root = Path(__file__).resolve().parents[4]
    source = root / "docs/capstone/deck/zava-forward-cowork-v2-draft.pptx"
    target = package / "changed.pptx"
    with ZipFile(source) as original, ZipFile(target, "w") as changed:
        for part in original.infolist():
            content = replacement if part.filename == "ppt/slides/slide21.xml" else original.read(part)
            changed.writestr(part, content)

    with pytest.raises(subprocess.CalledProcessError):
        rebuild(package, "--check-only", "--check-pptx", str(target))
