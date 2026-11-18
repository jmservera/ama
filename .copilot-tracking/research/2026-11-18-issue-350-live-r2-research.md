# Research: issue 350 live deployed parity, re-run r2 (2026-11-18 11:37 UTC)

Research disposition: executed (re-measurement of the earlier same-day run with retained raw output). Planning Readiness: pending, set at the end of this file.

Scope: the ten unticked #350 criteria against the synthetic demo, desktop only, resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change. Prior run: [docs/reference/research/deployed-parity-live-2026-11-18.md](../../docs/reference/research/deployed-parity-live-2026-11-18.md), which did not retain raw outputs for criterion 1.

Method: Azure CLI with the existing login, Playwright Chromium at 1440x900, test sign-ins read at runtime from the owner files and never printed.
Evidence home: `docs/reference/research/deployed-parity-live-r2-2026-11-18/` and the note `docs/reference/research/deployed-parity-live-r2-2026-11-18.md`.

## Findings log

Appended as measured; see the research note for the per-criterion results.

## Result

Planning Readiness: Ready. Primary evidence: [docs/reference/research/deployed-parity-live-r2-2026-11-18.md](../../docs/reference/research/deployed-parity-live-r2-2026-11-18.md) with raw outputs, screenshots and scripts in its evidence folder.

New against run 1: raw outputs retained for the anonymous 401/302 matrix and Easy Auth config; 16 asset hashes compared (8 match, 8 differ because web files changed after the image build); ledger 1,722 entries; CSV `view=mine` 133 rows against list 16 (new defect observation); time status 500 reproduced after a fresh replica with a source-based hypothesis; five generated placeholder documents downloadable; Blob data plane blocked by network rules from this host.
No criterion is fully proven. No source change is warranted for proof; the defects are FULL-tier follow-ups.
