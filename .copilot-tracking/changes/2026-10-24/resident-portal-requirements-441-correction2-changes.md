---
title: Resident manifest verification correction changes
description: Prospective bounded correction, independent critique completed before edits
ms.date: 2026-10-24
---

## Implementation opening

Task jmservera/ama#441, native59f31558, declared scope P01 implementation,
followed by owner-requested P02 Review/commit handoff. Research executed Ready;
one independent final-candidate critique Complete / Pass, no PC findings.
No production source/test or bot integration occurred before critique.
Existing history/custody adverse evidence retained. P01-T01 starts with
ref/clean-owned-file guard then authorized verified bot fast-forward.
P01-T02/03 source correction and focused checks pending. No heavy gate
authorized or queued; no source/score/product approval implied.

## P01-T01 - Verified bot preservation

Fresh refs unchanged immediately before fast-forward. HEADf902/mainf1e2/
topic816eea7a exact; parentf902 and single changed score path checked.
Tracked/index clean; only this run's five new dated RPI artifacts present.
git merge --ff-only origin/docs/resident-portal-requirements-441 succeeded.
Bot inherited unchanged, SHA256
d86b99ff1aae894dbe6be4faa4f5350201a27ef48ef1f57f2f21d74588634427.
No manual score edit or history rewriting. Pre-edit critique remains original.

## P01-T02 - Production correction

Only validate-refinement.py and its existing test_validate_refinement.py change.
manifest_inventory normalizes real ADR list/PRD dictionary into keyed entries,
explicitly rejects malformed/empty shapes, bad path/entry/hash/byte fields and
duplicate list paths. verify_manifest_sources is called directly from main
for both manifests, compares SHA256 and byte count with contextual ValueError.
Unknown selected omissions reject; exact self manifests and original capstone
boundary are the documented narrow exclusions when absent. Listed exceptions
still compare. No broad skip, catch, fallback or immutable manifest rewrite.
Existing four fixed pins/mapping reconstruction remain. No dependencies.

SHA256 of implemented validator:
90a39010ce6ade5f35339d8eaef9adfe740bc959a642ce4c828d744e2970dbfb.
Test module:
4fcb1873f8aed65edc58772359a1eeff784c58fbec61a4e715a860401d62356c.

## P01-T03 - Actual Focused Validation

All Python calls set PYTHONDONTWRITEBYTECODE=1. P is the existing
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441 package.
CLI is the already-installed external markdownlint CLI from correction1.
OUT is this native session's external files area, not a repository working
link. Exact commands/outputs also retained in session-only handoff.

```bash
python3 -m unittest discover -s "$P" -p 'test_validate*.py' -v
python3 "$P/validate-refinement.py" \
  --markdownlint-cli "$CLI" --out "$OUT/441-correction2-refinement-report.json"
python3 "$P/validate-integration.py" \
  --markdownlint-cli "$CLI" --out "$OUT/441-correction2-integration-report.json"
```

* 15tests PASS exit0, ten retained and five new. Covers both real manifests,
  hash/byte mismatch in both shapes, malformed/duplicate/unknown selection
  rejection and listed/unlisted exception boundaries, plus actual-main caller.
* Actual-main regression changes only in-memory SOURCE mapping via reversible
  patch, source hash/length; source_bytes() still proves consistent unchanged
  integrated bytes. Before fix actual main accepted it exit0. After fix the
  identical research reproduction exits1 specifically:
  adr/reconciliation-output-manifest.json: source hash mismatch for
  requirement-map-reconciled.json. Not a downstream hash/pin/lint proxy.
* Refinement validator exit0:18mappings, exact definitions, source patch,
  quality/trace/assets/links/lint. Status
  PASS_REFINEMENT_STATIC_NOT_QUALITY_APPROVAL, not lifecycle approval.
* Original integration validator exit0:22artifact hashes, formulas, scope,
  protected history and inherited-diagnostic checks. Status
  PASS_FOCUSED_STATIC_NOT_APPROVAL. Correction1 validator/tests unchanged.
* Protected git diff vs816eea7a exit0 for docs, source evidence/mapping,
  proposal, correction1 sources and score. Existing custody and output hashes
  remain, including PRD0c53fdfef and proposal51b8a6dc.
* New-artifact Markdown initially FAILED27diagnostics:26table MD013 plus one
  bare URL. Reflowed research/critique tables to plain text/list, made hosted
  URL an ordinary link. Independent critic prose/verdict/zero findings
  unchanged; exact original external SHA
  9b892dd531e5ab898507ee4e7fccf9b9e4c760c1a09fb07c25a5610dc8770eb0.
  Re-run of all five new Markdown artifacts exit0. No lint suppression.
* Correction-only git diff --check exit0. All-branch main-to-candidate check
  FAILED exit2 with52historical diagnostics:12refinement plus40earlier source
  patch-context diagnostics. Actual text byte-identical before current edits.
  The required twelve failures remain; no broad PASS, suppression or rewrite.
* PR442 read-only check OPEN/non-draft/@jmservera, issue441 OPEN. Complete
  current issue text inspected; stale decisions in issue do not override
  later explicit owner directions. No shared product edits/overlap introduced.

## External Evidence Hashes

Session basenames, not committed working links:

* 441-correction2-reproduction.log:
  a7a58cfc4018fbdf3c13f6d429b4b3c81245912d4ac42b96c0c332b49f0c5cd1.
* 441-correction2-reproduction-after.log:
  8725d326c9e49b32b8e0d7b3fe1f19807a4e07c25b1c50efc400a1593bab560c.
* 441-correction2-regressions.log:
  d4d246bf05cb0ff13098676e4c77c2d6498944aafc201f3a047cd4a9bd97e053.
* 441-correction2-refinement-report.json:
  6dd403c6fd47b8edc712d7821ce9c3636b93afff202f28883abdba3d5aac37d3.
* 441-correction2-integration-report.json:
  52c6717166d5cda6e5400d07776dd332305013696ccbcac1ff2b8183f74612b1.

## Reconciliation and Handoff

P01 Complete; P02 Review and commit/handoff pending. No material divergence,
scope change or second critique. Ordinary implementation judgment added
explicit membership/byte-boundary enforcement per accepted plan. Markdown-only
research/critique formatting preserved independent substance, not new review.
No source changes planned after Review. If a defect remains, stop and report.
Final pre-Review check confirms all five new Markdown artifacts lint/link
clean and the prospective state JSON parses with all six existing paths
resolved, no review pointer invented. P01 markers/details/changes agree.
P02 Review and future commit remain accurately pending in immutable snapshot;
Review record and external final handoff own their actual completion evidence.

All current PRD FAIL/Validate BLOCKED/seven findings and unsigned/live gates,
30Notrun/routineOFF, OD52-55/OQ28-31/NFRprecedence and id:null/unregistered
deferral remain. A5/B6 remain OPEN; old validator4364803620 resolved per hosted
review, this cycle addresses4365410759 only. Historical receipt67057df2 and
97filef902assessment are not new-candidate evidence. No heavy gate started or
queued and no publication/approval claimed. Coordinator owns later admission.
