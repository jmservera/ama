---
description: Source-format requirements and local publication boundaries
ms.date: 2026-11-25
---

# Task Research: arXiv release package

## Executive Summary

The paper can be packaged as a compilation-only ZIP and tar.gz, preserving
relative paths. Its embedded bibliography needs neither BibTeX nor a BBL.
Research is complete for this bounded tool; arXiv service acceptance remains
outside local validation.

## What You May Not Know

The current paper revision lives on an unmerged branch. Its publication notes
retain outstanding exact-byte author approval and employer-clearance conditions.
Producing an archive must not imply either approval.

## Findings

### Package only reachable compilation inputs

Q1 is answered by C1 and W1-W2. Eight TeX sources, three literal prompt files
and eleven PNG figures form the current compilation closure. The TeX root
must remain the archive root. Logs, the compiled main PDF, unused figures,
editable diagrams and research correspondence are not compilation inputs.
This is an evidence-backed finding, with high confidence for the inspected
literal commands; arbitrary TeX macro expansion is not a supported parser.

### Validate the archive, not the working directory

Q2 is answered by W2 and C2. arXiv compiles from the submission root, without
on-demand figure conversion. An extracted-bundle PDFLaTeX build can reveal
missing dependencies. It cannot certify arXiv acceptance, scientific quality,
license selection or author approval.

### Publication needs an explicit committed revision

Q3 is answered by C2 and W3. Use a clean Git snapshot, a new create-only tag
at its full SHA, and upload assets to a draft before publishing. Failed upload
must leave an explicit error and an inspectable draft, never an overwritten
release or a success-shaped fallback.

## Recommendation and Alternatives

Use a paper-local standard-library Python script alongside the existing
authoring tools. Discover literal input dependencies, stage only those files,
write deterministic archives, extract and compile one, then optionally publish.

| Option | Benefit | Cost or risk | Disposition |
| --- | --- | --- | --- |
| Reachable inputs | Small, auditable submission | Literal commands only | Selected |
| Whole-directory archive | Little discovery code | Includes unrelated evidence and build outputs | Rejected, W2 |
| Hardcoded 22-file list | Predictable | Silently becomes stale after new inputs | Rejected |
| GitHub Action | Hosted execution | Contradicts local-only request | Excluded |

## Scope and Questions

Owner-facing local tooling for the attached paper only. No manuscript changes,
source cleanup, automatic approval, arXiv upload or release execution.

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What files and archive layout does arXiv need? | Answered |
| Q2 | What can local compilation prove? | Answered |
| Q3 | How can publication avoid mismatched or partial releases? | Answered |

## Decisions and Feedback

| Group | Decision or feedback item | Status | Owner | Evidence |
| --- | --- | --- | --- | --- |
| D1 | End-to-end automatic progression | Confirmed | User | Working-mode form |
| D2 | Explicit package-only default and opt-in release | Confirmed | Agent | User requested a script, not its execution |
| D3 | Use original document-review branch | Confirmed | User | Explicit 2026-11-25 correction |
| D4 | No customization artifact | Confirmed | Agent | Executable scope does not fit HVE Builder artifact types |

## Risks and Open Questions

Publication clearance remains a human obligation. Recheck arXiv requirements
when submitting. Failed release publication may require manual recovery of
the new tag or draft; the tool must report that state rather than delete it.

## Planning Readiness and Next Step

| Field | Record |
| --- | --- |
| Research disposition | Executed |
| Decision participation | Agent-owned, automatic, user selected end-to-end |
| Planning Readiness | Ready, Q1-Q3 answered |
| Research depth and helpers | Wider, Deeper and Contrarian completed directly |
| Blockers | None for implementation; no publication authorized |
| Output mode and planning support | Convergence; supports planning |
| Continuation owner | Automatic RPI parent |
| Required gates or confirmations | Source review and local tests pending |
| Next action | Plan script, tests and usage instructions |
| Primary evidence file | .copilot-tracking/research/2026-11-25/arxiv-release-package-research.md |

## Research Record

### Method and Boundaries

Focused posture because the caller named one paper and one local tool.
Evidence date follows the user's 2026-11-25 timestamp. Default evidence root
is .copilot-tracking/research. The paper README's earlier manual archive is
prior knowledge, not evidence that the new script works.

### Extensions and Participation

Repository branch, source-exclusion, publication and plain-prose rules apply.
HVE Builder was loaded as requested but does not authorize inventing an agent.
RPI Research applies to source gathering; no domain experiment design is needed.
No helpers were used. Routine choices are agent-owned under D1.

### Research Cycle Log

* Wider: read official submission overview and the paper's preparation section.
  Reflection: source-only archives are required; a whole-directory export is wrong.
* Deeper: inspect reachable TeX, graphics and literal listings; inspect GitHub CLI
  create/edit options. Reflection: preserve paths and publish through a draft.
* Contrarian: compare hardcoded manifests and full-directory archives; inspect
  unmerged source ancestry and pending human publication gates. Reflection:
  reject stale manifests and automatic release execution.
* Synthesis: accept literal dependency traversal with extracted-bundle compilation.
  No material format question remains; another research cycle is not warranted.

### Evidence Log

| ID | Source and location | Claim or finding |
| --- | --- | --- |
| C1 | docs/capstone/thought-leadership/everything-but-the-software/main.tex; input/includegraphics/lstinputlisting in its reachable anc sources | Current literal dependency graph |
| C2 | docs/capstone/thought-leadership/everything-but-the-software/README.md, arXiv preparation; PR 2368 and git log origin/main..HEAD | Existing compilation-only scope, pending approval, unmerged current paper |
| W1 | https://info.arxiv.org/help/submit/index.html, retrieved 2026-11-25 | ZIP/tar.gz, filenames, figures, author submission |
| W2 | https://info.arxiv.org/help/submit_tex.html, preparation/bibliography sections retrieved 2026-11-25 | Root compilation, exclude outputs, embed bibliography |
| W3 | gh release create --help; gh release edit --help, inspected 2026-11-25 | Draft upload, verify-tag and draft=false publication |

Self-check: questions answered, all three waves recorded, limits explicit.
The TeX guidance response was truncated after the relevant preparation and
bibliography sections; later sections are not claimed as inspected.
