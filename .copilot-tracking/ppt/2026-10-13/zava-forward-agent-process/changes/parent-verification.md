<!-- markdownlint-disable-file -->
---
title: Parent verification and capstone publication
ms.date: 2026-10-13
status: Validated canonical copy
---

## Result

The installed PowerPoint Builder completed the requested supplied-content
handoff. Its original result is preserved in `powerpoint-agent-result.md`;
the parent's final output supersedes its output hash and full-slide placement.
The agent's transient CLI logs, original/staging copies and intermediate
exports remain local working artifacts, not additional delivery copies.

The parent resolved all nine new-slide edge-margin warnings by insetting the
diagram to 10.667 x 6 inches at (1.333, 0.5), putting the footer at y=6.8 and
moving the branding to 0.5-inch top/right margins. The footer now uses
Liberation Sans, matching the diagram and avoiding new Aptos substitution.
Only slide 13 was rebuilt from YAML with `build_deck.py --source --slides 13`.
The shared builder ignores the YAML `alt_text` field. `build_agent_slide.py`
therefore runs that partial build, then embeds its exact YAML description into
the built image nonvisual properties. The published description was read back
from the actual PPTX and matched against YAML, not inferred from configuration.

## Independent verification

* Final slide count 22; process map 13; original AI boundary 12; CFO example 14.
* Original 21 shapes compared by canonical detached XML, permitting only nine
  moved footer counter updates, including both original whitespace formats.
  Original notes XML and image bytes are exact. Notes backlinks correctly
  point to their moved slide parts; masters/layouts/themes remain unchanged.
* Deck property checks: zero errors/warnings, one expected partial-content info.
* Slide 13 geometry: zero issues at default 0.5-inch margins/0.3-inch gap.
  This is a changed-slide check, not a clean geometry claim for the old deck.
* Fresh LibreOffice full-deck export and pdftoppm slides 12/13/14 inspected:
  new slide readable, with clear card alignment, title, branding and footer,
  no clipping/overlap, consistent palette. Original Aptos substitution remains.
* PyMuPDF-filtered export was unavailable; full export plus pdftoppm page
  selection produced the actual final images without installing dependencies.
* All 22 notes are populated. Diagram alt text, full text equivalent, sources,
  proactive/deployment caveats and proposed value tests are retained.

## Deferred or unavailable, not passed

Model-SDK vision lane, real PowerPoint/Aptos rendering, staff/usability/accessibility
acceptance, calibrated capability/value proof and pitch rehearsal timing.
The suggested 45-60-second talk track is not measured rehearsal evidence.

## Rebuild boundary

Use `build_agent_slide.py --builder <powerpoint-skill>/scripts/build_deck.py`
with the existing Python dependencies. Its default source is the published
22-slide canonical PPTX, and output is this root's `slide-deck/`. It uses `content/`
and `content/global/style.yaml`, and `--slides 13` to rebuild the new slide.
Never use `--template` for this partial rebuild. The 2026-10-11 full YAML set
is historical 21-slide content, not an up-to-date full-deck regeneration source.
Retain existing Python dependencies; company policy forbids uv.

## Hashes

* Starting canonical source: `6ae671851a456b3f1482b0b24af09be2b836900c1d8eccc5a13fa929c1c268da`.
* Final working and canonical output: `d089b54ff3d905c58020dfe26828d7786dac424ed4310a7547d082175f701d8e`.
