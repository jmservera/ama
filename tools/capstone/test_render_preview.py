# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
"""Regression checks for fixed slide-jump preservation in Linux PDF previews."""

from pathlib import Path
import zipfile

import pymupdf
import pytest

from render_preview import SlideJump, read_slide_jumps, restore_slide_links

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
RELS = "http://schemas.openxmlformats.org/package/2006/relationships"


def make_deck(
    directory: Path,
    action: str = "ppaction://hlinksldjump",
    target: str = "slide2.xml",
    overlapping_target: str | None = None,
) -> Path:
    deck = directory / "deck.pptx"
    extra_shape = ""
    extra_relationship = ""
    if overlapping_target is not None:
        extra_shape = (
            '<p:sp><p:nvSpPr><p:cNvPr id="2">'
            '<a:hlinkClick action="ppaction://hlinksldjump" r:id="extra"/>'
            "</p:cNvPr></p:nvSpPr><p:spPr><a:xfrm>"
            '<a:off x="150" y="75"/><a:ext cx="300" cy="100"/>'
            "</a:xfrm></p:spPr></p:sp>"
        )
        extra_relationship = (
            f'<Relationship Id="extra" Target="{overlapping_target}" Type="{R}/slide"/>'
        )
    with zipfile.ZipFile(deck, "w") as archive:
        archive.writestr(
            "ppt/presentation.xml",
            f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst><p:sldId r:id="r1"/>'
            '<p:sldId r:id="r2"/></p:sldIdLst><p:sldSz cx="1000" cy="500"/></p:presentation>',
        )
        archive.writestr(
            "ppt/_rels/presentation.xml.rels",
            f'<Relationships xmlns="{RELS}"><Relationship Id="r1" Target="slides/slide1.xml" Type="{R}/slide"/>'
            f'<Relationship Id="r2" Target="slides/slide2.xml" Type="{R}/slide"/></Relationships>',
        )
        archive.writestr(
            "ppt/slides/slide1.xml",
            f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:sp>'
            f'<p:nvSpPr><p:cNvPr id="1"><a:hlinkClick action="{action}" r:id="jump"/></p:cNvPr></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="100" y="50"/><a:ext cx="300" cy="100"/></a:xfrm></p:spPr>'
            f"</p:sp>{extra_shape}</p:spTree></p:cSld></p:sld>",
        )
        archive.writestr(
            "ppt/slides/slide2.xml",
            f'<p:sld xmlns:p="{P}"><p:cSld><p:spTree/></p:cSld></p:sld>',
        )
        archive.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            f'<Relationships xmlns="{RELS}"><Relationship Id="jump" Target="{target}" Type="{R}/slide"/>{extra_relationship}</Relationships>',
        )
    return deck


def make_pdf(directory: Path, pages: int = 2) -> Path:
    path = directory / "rendered.pdf"
    with pymupdf.open() as document:
        for _ in range(pages):
            document.new_page(width=720, height=360)
        if pages > 1:
            document[0].insert_link(
                {
                    "kind": pymupdf.LINK_GOTO,
                    "from": pymupdf.Rect(0, 0, 20, 20),
                    "page": 0,
                }
            )
        document.save(path)
    return path


def test_given_fixed_jump_when_parsed_then_order_and_fractional_bounds_are_preserved(
    tmp_path,
):
    count, jumps = read_slide_jumps(make_deck(tmp_path))

    assert (count, jumps) == (2, [SlideJump(0, 1, (0.1, 0.1, 0.3, 0.2))])


def test_given_dropped_or_wrong_pdf_link_when_restored_then_source_target_and_hit_region_match(
    tmp_path,
):
    output = tmp_path / "linked.pdf"

    result = restore_slide_links(make_deck(tmp_path), make_pdf(tmp_path), output)

    with pymupdf.open(output) as document:
        links = document[0].get_links()
        assert len(links) == result["fixed_slide_jumps"] == 1
        assert links[0]["page"] == 1
        assert tuple(links[0]["from"]) == (72, 36, 288, 108)


@pytest.mark.parametrize("target", ["missing.xml", "../../../outside.xml"])
def test_given_missing_or_escaping_destination_when_parsed_then_refused(
    tmp_path, target
):
    with pytest.raises(ValueError, match="destination|escapes"):
        read_slide_jumps(make_deck(tmp_path, target=target))


def test_given_history_action_when_parsed_then_not_misrepresented_as_fixed_jump(
    tmp_path,
):
    with pytest.raises(ValueError, match="Unsupported navigation"):
        read_slide_jumps(
            make_deck(tmp_path, action="ppaction://hlinkshowjump?jump=lastslideviewed")
        )


def test_given_different_page_count_when_restoring_then_refused(tmp_path):
    with pytest.raises(ValueError, match="slide counts differ"):
        restore_slide_links(
            make_deck(tmp_path), make_pdf(tmp_path, pages=1), tmp_path / "linked.pdf"
        )


def test_given_existing_output_when_restoring_then_not_overwritten(tmp_path):
    output = tmp_path / "existing.pdf"
    output.write_bytes(b"keep")

    with pytest.raises(ValueError, match="already exists"):
        restore_slide_links(make_deck(tmp_path), make_pdf(tmp_path), output)

    assert output.read_bytes() == b"keep"


def test_given_overlapping_different_targets_when_restoring_then_refused_before_saving(
    tmp_path,
):
    output = tmp_path / "linked.pdf"

    with pytest.raises(
        ValueError, match="Overlapping slide-jump hit regions on slide 1"
    ):
        restore_slide_links(
            make_deck(tmp_path, overlapping_target="slide1.xml"),
            make_pdf(tmp_path),
            output,
        )

    assert not output.exists()


def test_given_overlapping_same_target_when_restoring_then_both_links_preserved(
    tmp_path,
):
    result = restore_slide_links(
        make_deck(tmp_path, overlapping_target="slide2.xml"),
        make_pdf(tmp_path),
        tmp_path / "linked.pdf",
    )

    assert result["fixed_slide_jumps"] == 2
