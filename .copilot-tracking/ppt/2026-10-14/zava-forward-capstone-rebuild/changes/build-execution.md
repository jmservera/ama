---
title: Native capstone build execution
ms.date: 2026-10-14
---
<!-- markdownlint-disable-file -->

## Scope and inputs

Task: build-content, build-deck, export and local validation for P01-T02.
Only this new working directory may be written. Parent owns publication.
Read the complete approved plan, details, research, 22-slide strategist
handover, YAML schema, shared PowerPoint rules and security model.
Activated powerpoint and python-foundational. No agents, cloud calls,
authentication, paid model validation, source application changes or uv.

## Execution

1. Copied current canonical 22-slide deck into `source/canonical-22-slides.pptx`.
2. Extracted all 22 slides with shared `extract_content.py --resolve-themes`
   into the new `source/extracted/`; no stale extraction existed.
3. Created `generate_content.py` to generate all 22 individual YAML layouts,
   shared style, expanded source-linked notes and native process map.
   Named title/body frames use explicit TOP anchoring and no text autosizing.
4. Preserved forest/cream/moss/warm palette and original Zava logo. Source
   masters/themes are retained through an all-slide `--source` replacement.
   Selected installed Liberation Sans explicitly; original Aptos fonts are
   absent locally. Native PowerPoint font inspection remains a human gate.

## Build/export/repair record

5. Generated all 22 YAML files and source-linked notes with `generate_content.py`.
6. Shared `build_deck.py --source source/canonical-22-slides.pptx --slides 1,…,22`
   rebuilt the full presentation in place, retaining 22 slides.
7. Shared `export_slides.py` produced a full LibreOffice PDF;
   `render_pdf_images.py --dpi 150` produced all 22 individual JPGs.
8. Initial actual-image review and rendered-word bounds checks found map OFF
   labels wrapping, assessor-owner overflow, decision-panel overflow and
   options-header overflow. Shared source-clear also retained the old slide-22
   `graphicFrame` table. Fixed generator copy/geometry, added the narrowly
   scoped safe slide-22 cleanup hook and re-exported the whole deck.
9. Added native frame-intersection checking; moved slide-18 closing restriction
   upward to remove its frame-only overlap with the footer/counter.
10. Executed `bash rebuild.sh` as the final complete reproduction run. It ran
    all 22 source rebuilds, full PDF/JPG export, shared notes/count checks,
    shared default geometry and strict local validations.

## Final results

* Final working PPTX SHA-256:
  `7b25fd7e77d1ed7d9aa908cf3da429bcfeae104beadea5ac90c1e97dbc71fbb4`.
* Canonical/source copy SHA-256 unchanged:
  `d089b54ff3d905c58020dfe26828d7786dac424ed4310a7547d082175f701d8e`.
* 22 slides; 22 correct relationship-resolved notes; all topic/source/YAML
  checks pass. Map still correctly uses `notesSlide22.xml`.
* 477 total shapes; map 60 shapes, 43 native textboxes, 12 backgrounds,
  four native connectors, one identified branding image, zero diagram pictures.
* 311 nonempty text frames TOP/NONE; all rendered words within frames;
  56 peer rows exact equality; zero out-of-bounds shapes or text intersections.
* All original masters/layouts/themes byte-identical.
* Shared `validate_deck.py`: zero issues across 22 slides.
* Shared geometry default heuristic: 180 findings (154 warnings/26 info),
  zero errors. Raw nonzero result retained, not called clean. All findings
  individually classified in `reports/shared-geometry-dispositions.json`;
  actual native/rendered checks and image review found no unresolved blocker.
* Inspected all slides in fresh contact sheets and individual dense/control/
  proof/map/cash/measurement/options images. Details in visual-inspection report.
* Planned 795s main +105s discussion/contingency; not rehearsed.
* No SDK/model vision validation attempted. No uv, dependencies, cloud/auth,
  source application changes, staging or publication.

## Finalization

Complete file/path/hash/command handover is `../build-handover.md`.
Parent owns final inspection, byte-identical canonical publication and index/
README/log/#68 changes. No builder-blocking issue or clarification remains.
