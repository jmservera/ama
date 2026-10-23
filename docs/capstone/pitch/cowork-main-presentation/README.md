---
title: Zava Forward Cowork Main Presentation Handoff
description: Portable executive-first script, diagrams, demo, Tokenomics and question-led appendix for a 30-minute presentation plus a 10-minute demo
ms.date: 2026-10-23
ms.topic: reference
---

## Start Here

Give Cowork **this entire folder**, then use [COWORK-BRIEF.md](./COWORK-BRIEF.md)
as the opening instruction. It contains a complete authoring job, not just an
outline. No repository access, private stock data or credentials are needed
to build the proposed presentation.

The central story is: **more homes ready, with control intact**. Lead with the
customer outcome and proposed decision, explain the operating model, then
progressively reveal AI placement, architecture and delivery technique.
The original five business responsibilities survive; five autonomous managers
are not the proposed operating model.

| File or folder | Purpose |
| --- | --- |
| [slides.json](./slides.json) | Authoritative content contract: 18 main slides and 27 question-led backups, with copy, notes, timing, evidence and return routes |
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
PPTX. That deck remains at `docs/capstone/deck/zava-forward-executive-draft.pptx`
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
observation, partial metering and unknown accepted-outcome cost.
Monetary budgets and per-request/depth bounds remain proposals, not
implemented controls. No internal Microsoft presentation content is included.

## Rebuild and Portability

From any working directory:

```bash
python3 /path/to/cowork-main-presentation/build_assets.py
```

This regenerates `.excalidraw`, `.svg`, the main script and backup notes using
only Python's standard library and the bundled icon bytes. It checks timing,
source IDs and source geometry. PNG previews and the validation report are
separate rendered artifacts; regenerate them after diagram edits using an
SVG renderer and repeat the visual checks. It does not build a PPTX.

Relative links inside this package are portable. Source paths in the evidence
register are citations against the pinned repository baseline, not files Cowork
must open. The evidence summaries are included for offline authoring.
