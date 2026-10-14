#!/usr/bin/env bash
# Local working-candidate build only. No uv, packages, cloud or publication.
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=/home/azureuser/.copilot/session-state/1e0d58ea-7ea9-4c65-93b7-66c89c481468/files/capstone-pptx-tools
export PYTHONPATH="$PYTHONPATH:/home/azureuser/.copilot/session-state/1e0d58ea-7ea9-4c65-93b7-66c89c481468/files/capstone-icon-tools"
tools=/home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/experimental/powerpoint/scripts
python3 generate_content.py
python3 "$tools/build_deck.py" --content-dir content --style content/global/style.yaml \
  --source source/structural-24-slides.pptx \
  --slides 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 \
  --output slide-deck/zava-forward-executive-draft.pptx
python3 generate_content.py --finalise
python3 "$tools/export_slides.py" --input slide-deck/zava-forward-executive-draft.pptx \
  --output slide-deck/validation/slides.pdf
python3 "$tools/render_pdf_images.py" --input slide-deck/validation/slides.pdf \
  --output-dir slide-deck/validation --dpi 150
python3 "$tools/validate_deck.py" --input slide-deck/zava-forward-executive-draft.pptx \
  --content-dir content --output slide-deck/validation/deck-validation-results.json \
  --report slide-deck/validation/deck-validation-report.md --per-slide-dir slide-deck/validation
geometry_status=0
python3 "$tools/validate_geometry.py" --input slide-deck/zava-forward-executive-draft.pptx \
  --output slide-deck/validation/shared-geometry-results.json \
  --report slide-deck/validation/shared-geometry-report.md || geometry_status=$?
if [ "$geometry_status" -gt 1 ]; then exit "$geometry_status"; fi
python3 "$tools/export_slides.py" --input ../zava-forward-capstone-rebuild/slide-deck/zava-forward-executive-draft.pptx \
  --output reports/baseline-comparison.pdf
python3 validate_artifacts.py
