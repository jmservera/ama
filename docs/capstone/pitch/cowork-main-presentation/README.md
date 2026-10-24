---
title: Zava Forward Cowork Main Presentation Handoff
description: Portable executive-first script, diagrams, demo, Tokenomics and question-led appendix for a 30-minute presentation plus a 10-minute demo
ms.date: 2026-10-24
ms.topic: reference
---

## Start Here

The owner's 2026-10-24 cost recovery is in the
[calculation evidence](./evidence/ai-cost-evidence.md#recovered-council-comparison-2026-10-24),
source S09/S11 and backups B05/B09/B25. It restores the USD 0.44 planned-home
inference scenario, GBP 6,082 works benchmark and conditional GBP 3,041/home
grant illustration, not measured accepted-outcome economics or guaranteed
funding. The [native revision map](./COWORK-BRIEF.md#owner-requested-cost-recovery-2026-10-24)
identifies the six revised v2 pages. The current
[PPTX](../../deck/zava-forward-cowork-v2-draft.pptx) and
[native PowerPoint PDF](../../deck/zava-forward-cowork-v2-draft.pdf) now include
this recovery. The [build record](../../deck/cowork-generated/native-recovery-build-2026-10-24.md)
records 54 slides/notes, 27 native caller returns, exact-part preservation,
native previews and remaining independent review/approval gates.
The [evidence guide](./native-recovery/README.md#evidence-and-limits) links the
retained validation receipt and identifies preview exports as local-only,
regenerable evidence rather than portable published assets.

Use the [native recovery guide](./native-recovery/README.md) for the durable
builder, pinned baseline and explicit external-output commands. The copied
build record retains its historical commands and paths unchanged.

For the current presentation, apply the
[IoT and optional-resident-portal refinement](../../deck/cowork-generated/refinement-2026-10-23/README.md)
and the dated revision direction in [COWORK-BRIEF.md](./COWORK-BRIEF.md).
The owner-selected native v2 deck has 54 slides. The 18-slide inventory below
is the original authoring contract; its updated copy is reusable but does
not reconstruct the complete later Cowork v2 layout. IoT now belongs in the
main narrative, and the optional portal is under assessment in issue #441,
not excluded, implemented or measured as a saving.

Choose the authoring mode before handing over files:

* Current-v2 revision: give Cowork this entire folder **and** the current
	[54-slide PPTX](../../deck/zava-forward-cowork-v2-draft.pptx), its
	[current PDF](../../deck/zava-forward-cowork-v2-draft.pdf), the
	[refinement folder](../../deck/cowork-generated/refinement-2026-10-23/README.md)
	including its five previews, and the
	[dated correction record](../../deck/cowork-generated/review-corrections-2026-10-24.md).
	Preserve their relative paths or provide an explicit file map. The native
	deck owns v2 slide order, layouts, media, notes and navigation; this folder
	alone cannot reconstruct it.
* Original-route offline authoring: this folder alone supplies the original
	18-slide main route and 27 backups. That is a separate authoring mode, not a
	rebuild or replacement of the owner-selected 54-slide v2 deck.

Use [COWORK-BRIEF.md](./COWORK-BRIEF.md) as the opening instruction and retain
the mode distinction. Neither mode needs private stock data or credentials.

The central story is: **more homes ready, with control intact**. Lead with the
customer outcome and proposed decision, explain the operating model, then
progressively reveal AI placement, architecture and delivery technique.
The original five business responsibilities survive; five autonomous managers
are not the proposed operating model.

| File or folder | Purpose |
| --- | --- |
| [slides.json](./slides.json) | Original-route content contract: 18 main slides and 27 backups, plus reusable cost inputs; not authority for all native-v2 slide order or layouts |
| [speaker-script.md](./speaker-script.md) | Complete first-person main-route script and interruption cues |
| [backup-slides.md](./backup-slides.md) | Appendix copy, answers, visual instructions and source IDs |
| [demo-runbook.md](./demo-runbook.md) | Separate ten-minute demo, preflight, live/evidence routes and recovery |
| [audience-and-delivery.md](./audience-and-delivery.md) | CXO archetype strategy, timing variants, objection handling and delivery coaching |
| [diagrams/README.md](./diagrams/README.md) | Seven progressive 16:9 architecture/economics views, text alternatives and animation plan |
| `diagrams/*.excalidraw` | Editable native boxes, text, arrows and embedded official Azure SVG icons |
| `diagrams/*.svg`, `diagrams/*.png` | Portable slide-ready vector and raster previews; the Excalidraw source is editing authority |
| [evidence/sources.json](./evidence/sources.json) | Source IDs, pinned repository paths, claim classifications and limitations |
| [evidence/README.md](./evidence/README.md) | Portable evidence policy and source baseline |
| [evidence/ai-cost-evidence.md](./evidence/ai-cost-evidence.md) | Verified AI, cost and merged Tokenomics detail |
| [evidence/delivery-method-evidence.md](./evidence/delivery-method-evidence.md) | HVE, prototypes, original backlog and complete assessment criteria/gaps |
| [tokenomics-worksheet.csv](./tokenomics-worksheet.csv) | Human-readable observation/unknown/proposal ledger, not an invented calculator result |
| [validation.md](./validation.md) | Checks performed and remaining authoring, PowerPoint and human gates |
| [build_assets.py](./build_assets.py) | Rebuild generated notes and deterministic source-based diagrams |

## Timing and Status

The proposed route has 24 minutes of narration, six minutes for interruptions
inside the 30-minute presentation, and a separate ten-minute demo.
The final 30-second decision slide follows the demo but is included in the
presentation's 24-minute narration. The clock budget is therefore 40 minutes
overall, not 40 minutes plus Q&A. Appendix slides are optional answers, not
an additional scheduled talk.

This supersedes the older 15-minute limit **for this requested package only**.
It does not rewrite owner memory or replace the current 24-slide executive
PPTX. That historical deck is retained under
[deck/draft](../../deck/draft/zava-forward-executive-draft.pptx)
until the new deck is authored and validated. Publish the eventual executive
delivery only in `docs/capstone/deck/`, never over the separate mentor deck.

This folder is an authoring handoff, not a final PowerPoint, observed rehearsal,
fresh live demo, customer endorsement, measured benefit or passed capstone
assessment. Its scripts describe proposed delivery, not conversations already
held.

## Latest Main and Tokenomics

The working presentation branch incorporates `origin/main` commit
`140d8f4` (PR #433), pulled at the owner's request on 2026-10-23.
Tokenomics is explicit in main slide S11, diagram 07, backups B25-B27 and
the worksheet. The main slide states the historical 6,884-token/five-run
observation and a separately labelled recovered inference planning scenario;
partial metering and unknown accepted-outcome cost remain explicit.
Monetary budgets and per-request/depth bounds remain proposals, not
implemented controls. No internal Microsoft presentation content is included.

## Rebuild and Portability

From any working directory:

```bash
python3 /path/to/cowork-main-presentation/build_assets.py
```

The default rebuild updates the main script, backup notes and board HTML.
It leaves all native Excalidraw sources and SVG/PNG previews untouched,
including author edits. Native sources remain the editing authority.

The recovered costs are a required rebuild contract, not optional slide copy.
The `cost_model` in [slides.json](./slides.json) retains dated E21 inputs;
the builder recalculates them using decimal arithmetic and rejects missing or
stale figures and caveats before writing notes. Input changes require matching
evidence, source copy, notes and native-slide changes, not silent omission.
Current-price and grant verification remain separate from arithmetic.

Every future PowerPoint build must also pass the
[cost preservation gate](./COWORK-BRIEF.md#required-cost-preservation-on-every-rebuild).
From the repository root, substitute the new candidate path when appropriate:

```bash
.venv/bin/python docs/capstone/pitch/cowork-main-presentation/build_assets.py --check-only --check-pptx docs/capstone/deck/zava-forward-cowork-v2-draft.pptx
.venv/bin/python -m pytest docs/capstone/pitch/cowork-main-presentation/test_build_assets.py -q
```

Only to discard native edits and restore the hard-coded diagram templates:

```bash
python3 /path/to/cowork-main-presentation/build_assets.py --reset-diagrams
```

`--reset-diagrams` is a destructive reset of all seven `.excalidraw` and
`.svg` files, not an export of edited drawings. It does not refresh PNGs;
render and inspect fresh previews after any reset or native-source change.
The builder checks timing, source IDs, source geometry and required costs;
`--check-pptx` also checks the native cost pages without rendering or editing
them. It does not build a PPTX or validate viewer navigation. Backup interruptions return to
the calling main slide; recorded topic returns apply only to index entry.

Relative links inside this package are portable. Source paths in the evidence
register are citations against the pinned repository baseline, not files Cowork
must open. The evidence summaries are included for offline authoring.
