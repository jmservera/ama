#!/usr/bin/env bash
# Rebuild and validate only the bounded, generated working artifacts.
set -eu
cd /home/azureuser/source/ama-wt-zava-challenge
export PYTHONPATH=/home/azureuser/.copilot/session-state/1e0d58ea-7ea9-4c65-93b7-66c89c481468/files/capstone-pptx-tools
work=.copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild
tools=/home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/experimental/powerpoint/scripts
canonical_before=$(python3 -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("docs/capstone/deck/zava-forward-executive-draft.pptx").read_bytes()).hexdigest())')
python3 "$work/generate_content.py"
python3 "$tools/build_deck.py" \
  --content-dir "$work/content" \
  --style "$work/content/global/style.yaml" \
  --source "$work/source/canonical-22-slides.pptx" \
  --slides 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22 \
  --output "$work/slide-deck/zava-forward-executive-draft.pptx"
python3 "$tools/export_slides.py" \
  --input "$work/slide-deck/zava-forward-executive-draft.pptx" \
  --output "$work/slide-deck/validation/slides.pdf"
python3 "$tools/render_pdf_images.py" \
  --input "$work/slide-deck/validation/slides.pdf" \
  --output-dir "$work/slide-deck/validation" --dpi 150
python3 "$tools/validate_deck.py" \
  --input "$work/slide-deck/zava-forward-executive-draft.pptx" \
  --content-dir "$work/content" \
  --output "$work/slide-deck/validation/deck-validation-results.json" \
  --report "$work/slide-deck/validation/deck-validation-report.md" \
  --per-slide-dir "$work/slide-deck/validation"
# The shared default heuristic reports intentional brand/footer/compact spacing.
# Preserve its nonzero warning result; never present it as a clean pass.
geometry_status=0
python3 "$tools/validate_geometry.py" \
  --input "$work/slide-deck/zava-forward-executive-draft.pptx" \
  --output "$work/slide-deck/validation/shared-geometry-results.json" \
  --report "$work/slide-deck/validation/shared-geometry-report.md" || geometry_status=$?
if [ "$geometry_status" -gt 1 ]; then
  exit "$geometry_status"
fi
python3 "$work/validate_artifacts.py" --expected-canonical-sha "$canonical_before"
