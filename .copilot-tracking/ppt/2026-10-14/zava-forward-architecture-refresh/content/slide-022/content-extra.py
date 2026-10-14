"""Remove stale source graphic frames omitted by the shared source-clear helper."""

from pathlib import Path

from pptx.slide import Slide


def render(slide: Slide, style: dict, content_dir: Path) -> None:
    """Remove only retained graphicFrames; all replacement cells are YAML textboxes."""
    tree = slide.shapes._spTree
    for child in list(tree):
        if child.tag.endswith("}graphicFrame"):
            tree.remove(child)
