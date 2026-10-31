---
title: Native Cowork Recovery Reproduction
description: Pinned original input and external-output Build, Verify and native PowerPoint Render commands
ms.date: 2026-10-24
ms.topic: how-to
---

## Inputs and Authority

The [promoted script](../../../../../tools/cowork-native-recovery/Invoke-Recovery.ps1)
and [manifest](../../../../../tools/cowork-native-recovery/content/recovery.json)
apply six cost-slide revisions to the preserved 54-slide
[original PPTX](./baseline/original.pptx). They do not reconstruct the full deck
from the original-route 18-slide inventory. The baseline SHA-256 is:

```text
d41acc969efb1687cfdd0103b753a62ea697005652760b1579a8e6de955cf447
```

Every action checks this baseline before writing output. Missing or wrong
baseline fails closed; the delivered deck is never a fallback. Every Build
starts from the pinned original, not a previous candidate. Only six slides
and their six notes change. Verify checks all other parts, 54 nonempty notes,
preserved timing, 27 caller actions and a single added shape 70001 on slide 32.

## Commands

From the repository root, choose one external output directory per run and
reuse it for Build, Verify and Render. The script resolves the manifest from
its own directory and requires explicit `RepoRoot` and `OutputDir` parameters.
Output paths inside the repository or traversing links are refused.

```bash
OUTPUT="$HOME/.local/share/ama/cowork-native-runs/new-run"
pwsh -NoProfile -File tools/cowork-native-recovery/Invoke-Recovery.ps1 -Action Build -RepoRoot "$PWD" -OutputDir "$OUTPUT"
pwsh -NoProfile -File tools/cowork-native-recovery/Invoke-Recovery.ps1 -Action Verify -RepoRoot "$PWD" -OutputDir "$OUTPUT"
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/capstone/pitch/cowork-main-presentation/build_assets.py --check-only --check-pptx "$OUTPUT/zava-forward-cowork-v2-draft.pptx"
```

Render requires real Windows PowerPoint COM. From WSL, convert both paths:

```bash
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$(wslpath -w "$PWD/tools/cowork-native-recovery/Invoke-Recovery.ps1")" -Action Render -RepoRoot "$(wslpath -w "$PWD")" -OutputDir "$(wslpath -w "$OUTPUT")"
```

On Windows, supply native absolute paths directly. If Windows PowerPoint is
unavailable, record Render as Not run, not as visual acceptance. Build/Verify
use PowerShell and .NET ZIP/XML support. Render exports a 54-slide PDF and
18 changed/adjacent previews beneath the same external directory; it does not
overwrite canonical delivery. Compare repeated builds by ZIP member names and
uncompressed bytes, not ZIP ordering, timestamps or whole-package hash alone.

## Evidence and Limits

The [sanitised promotion and validation receipt](../../../../reference/resources/tracking-retention-promotion.json)
retains source/copy hashes, native Build/Verify/Render results, package counts,
canonical delivery hashes and archive accounting. The canonical PPTX/PDF and
this receipt are the durable review inputs, not a promise that historical
relative output paths resolve beside the copied narrative.

The [historical build narrative](../../../deck/cowork-generated/native-recovery-build-2026-10-24.md)
is preserved byte-for-byte, with its original command/path context. Use the
commands above for the promoted builder. The original tracking builder,
baseline PPTX/PDF, 89 current build entries and current delivery pair remain.
No extra durable original PDF is copied.

Heavy native PNG previews and full per-slide validator exports remain local
working evidence, not published portable assets. Their existing paths and
limitations are historical; regenerate them into external output with Render
when required. The verified local archive preserves their original bytes,
but is not publicly accessible or guaranteed to exist on another machine.

Read the [cost evidence](../evidence/ai-cost-evidence.md#recovered-council-comparison-2026-10-24)
and [retention policy](../../../../reference/method/tracking-retention-policy.md).
Arithmetic and native export checks do not establish current primary prices,
Finance/funder approval, measured benefits, independent presentation review,
accessibility conformance or publication clearance.
