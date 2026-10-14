---
title: Excalidraw Architecture Validation
description: Source, native editing, browser export, geometry and icon evidence for the two PR 68 architecture views
ms.date: 2026-10-14
ms.topic: reference
---

## Scope and Outcome

The executive and technical drawings describe the same PR #68 source
baseline, `062434a1fedbf6a87d1374c767c2bf0a11491ab6`.
Both passed the bounded authoring/export checks below. This is not a fresh
Azure inventory, production acceptance, a new architectural decision or
independent audience/panel approval.

| View | Native elements | Service/person cards | Bound arrows | Embedded icons | SVG canvas | PNG pixels |
| --- | --- | --- | --- | --- | --- | --- |
| Executive | 57 | 7 | 6 | 5 | 1920 x 1260 | 3840 x 2520 |
| Technical | 194 | 24 | 27 | 26 | 2850 x 2870 | 5700 x 5740 |

## Source and Content Checks

Read the original case, addendum, reference index/memory, housing-association
primer, complete capstone assessment guide, ADRs 0001/0002, infrastructure
entry point/modules, MVP handover and relevant runtime implementations.

The public [handover](../../../../docs/architecture/README.md) retains the
interaction/source matrix and distinguishes the current single-API five
assistants from deferred worker images. It also preserves the development
public-network exceptions, conditional M365 connections, unproven full
application tracing, unimplemented external audit digest anchor and the
absence of standing five-assistant authority/proactive operation.

The complete 20-criterion guide check is a contribution/gap assessment,
not a rubric score or clearance of any section floor.
No cloud, tenant, token, model or deployment operation was performed.
The deck, original case, owner memory, regulatory snapshots and runtime
remain unchanged.

## Native Editing and Export

Scenes were generated using `generate.py`, existing isolated Pillow and the
Linux Liberation Sans regular font for Arial/Helvetica-compatible region
measurement. Official SVG bytes came from
`Azure_Public_Service_Icons_V24.zip`; `source-manifest.json` identifies
the 20 selected entries and their SHA-256 hashes.

Both were loaded into the actual Excalidraw editor running on loopback,
not merely inspected as JSON. Session-only tool dependencies were
Excalidraw 0.18.1, React/React DOM 18.3.1 and Vite 8.3.4 on Node 24.21.0.
The editor used `restoreElements`, native scene files, `exportToSvg`
and `exportToBlob` with a 2x PNG scale. No scene was uploaded to an
external drawing service.

In the technical editor, selected the API service's five-element native
group and pressed `ArrowRight`. Every grouped element moved exactly one
pixel; all five outgoing bound arrows changed geometry while retaining
their API binding. Reloaded the pristine source before final export.
The paper artboard is locked against accidental movement; service boxes,
text and arrows remain native editable objects. Additional monitoring/model
icons belong to their service groups.

Both browser reports have empty `textChanges`, `overflows`,
`layoutFailures`, `missingImages` and `unboundArrows` arrays.
The executive and technical final PNGs were inspected directly. Corrected
the executive capability caption, environment-header crossing, own-photo
label location and public-edge/private-backend wording before these exports.
Opaque route labels are layered above all connectors so later token/Teams
routes do not cross earlier captions.
Peer card titles and bodies use fixed top-aligned regions rather than
shrink-to-fit typography.

SVG previews include a title, full textual description, `role="img"` and
ARIA association. The public handover supplies Mermaid text equivalents;
both parsed successfully using the actual browser Mermaid 11.17.2 parser.
The technical node was renamed `msgraph` to avoid Mermaid's reserved
`graph` token. The initial Node-only parse attempt could not initialize
DOMPurify without a browser DOM; browser parsing resolved that tooling
limitation rather than bypassing the parser.

## Structural Checks and Reuse

`validate.py` checks unique native IDs, canvas bounds, grouped titles/body
regions, reciprocal arrow bindings, local source files/fragments, embedded
image bytes, unmodified icon aspect ratios/crop/rotation/flip, public asset
modes, browser reports, SVG accessibility metadata and exact SVG/PNG
dimensions. It also checks new documentation links and that the prior
knowledge-base log remains a byte-identical prefix.

All checks passed: 20 official asset files, 30 unique source references,
both native scenes and all six delivery assets.
`structural-validation.json` records the final delivery SHA-256 hashes;
`executive-browser-validation.json` and
`technical-browser-validation.json` retain the browser results.
`git diff --check` passed.

From the repository root, regenerate native scenes with Pillow available
and the official downloaded pack:

```bash
python3 .copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/generate.py \
  --icon-pack /path/to/Azure_Public_Service_Icons_V24.zip
```

Open the resulting `.excalidraw` files locally to edit/export previews.
The generator records the current source commit; a later rebuild must
review whether the topology and dated handover still match.
After exporting matching SVG/PNG and updating browser reports, run:

```bash
python3 .copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/validate.py
```

The local editor/export harness was session-only. The published native
scenes are the editing authority; manual Excalidraw exports require
preserving or reapplying the SVG title/description accessibility metadata.
