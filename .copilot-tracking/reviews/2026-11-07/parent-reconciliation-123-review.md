<!-- markdownlint-disable-file -->
# Review: discovery parent reconciliation (#123), 2026-11-07

Single author review, executed once; not independent. Independent exact-head assessment and hosted checks remain separate and required.

## Outcome

CLEAN for the bounded reconciliation as far as local light evidence goes, with ONE BLOCKED gate (below). This is not an approval of #128, #440 or #123, and not main acceptance.

## Verified

* Ancestry: `dec700c7`, parent `9bacb87d` and main `b284d0d3` are ancestors of the candidate; ordinary merges, no rebase, reset, amend or force. Planning commit `fd78de2f` precedes the merges.
* Conflict handling: the only conflict (evidence pack tail) retains both sides in full and order; historical lines of main, parent, log and pack are preserved (README differs only by main's own tokenomics row).
* Scope: non-tracking changes against main are the evidence pack, KB index, log, core README, `paired_equity.py` and `test_paired_equity.py`; no infrastructure, SQL, finance, security or deployment implementation. `fairness_evidence=False` and `activation_allowed=False` unchanged.
* Current light checks on the integrated tree (exit 0): 74 coupled tests, core Ruff, format check, configured mypy with declared 0.17.1 and 2.4.0, 26 JSON files parsed, 50 added links, `git diff --check`.

## BLOCKED: repository default focused gate not run

`python3 tools/rpi-checks.py --changed` was NOT run. Its own selection logic (read-only, no group executed) for base `b284d0d3` selects: `preflight`, `project-core`, `project-agents`, `project-api`, `project-orchestrator`, `project-importer`, `namespace`, `static`, `image-api`, `image-agents`, `image-orchestrator`, `image-importer` and `logo-0600`. The inherited `src/core/src/.../paired_equity.py` change is a core runtime path, which selects all projects and the four image builds plus the logo build. The admission excludes image-building and unrelated heavy work and says to stop before excluded groups, so no lock was acquired, no output directory was created and no receipt exists. No skip token, fabricated result or fallback was used. Needed decision: the coordinator either admits those image groups for this exact head or directs a different gate scope; the tier text (FOCUSED) is unchanged by this finding but the tool's selection exceeds the stated focused admission.

## Remaining gates

* Coordinator decision on the blocked gate; then a native partial receipt verified with `--required-scope partial --base b284d0d3`.
* Independent exact-head review, hosted checks, guarded merge, offline requirement and design traces (known design-check blocker is unchanged and not a pass).
* Whole #123 AC1 and AC2, #440 C7 and C8, human, legal, accessibility and actual-model criteria stay unproven.

## Routed later work

Gate-scope admission; independent review; named human decisions as already recorded.
