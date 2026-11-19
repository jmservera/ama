---
title: Issue 203 README archive-tag fix and criterion results, 2026-11-19
description: Per-criterion results for the two unticked issue 203 criteria after the last reference violation was fixed
ms.date: 2026-11-19
---

Refs #203. Base `1dddac2e0`. Synthetic demo, desktop only.

## Results

| Criterion | Result | Evidence |
| --- | --- | --- |
| Repository search returns only intentional historical references | Proven for the documented checker scope | Before: `python3 tools/check-legacy-references.py` exit 1, one violation at `docs/reference/README.md:1359` (retired path without archive tag v0.21.0). The index row now names tag v0.21.0. After: `references: 0 violation(s); links: 0 violation(s)`; `python3 -m unittest tools.test_check_legacy_references` ran 8 tests, OK. The literal wording still relies on the exemptions recorded in the earlier 2026-11-18 notes. |
| Deployed app and CI green from `src/` | Not proven | `ca-cutover-test-demo-api` is Running (read-only `az containerapp show`) and `/health` answers 401 without credentials, so it is up but not authenticated. Image digest `sha256:5368f4e4...` has no recorded build provenance to a `src/` commit. The last 40 `main` runs contain no `Source projects CI` run (it runs on pull requests). Needs a build-to-digest link; nothing could honestly be ticked. |

No Azure resource was created or changed; no credentials were read.
