<!-- markdownlint-disable-file -->
# Tracking Retention and PR 438 Research

Task ID: tracking-retention-pr438
Research disposition: reused audit, with focused review-thread refresh.
Planning Readiness: Ready for P01; cleanup selections require explicit preservation inventory before P02/P03.

## User Direction
* Continue all three recommendations: promote durable sources/evidence, archive retired outputs, establish retention policy.
* Owner selected continuing on docs/capstone-cowork-story, not a child branch or separate worktree.
* Also address review comments on PR 438. No commit, push, merge, deployment or live inference requested.

## Evidence
* C1: Read-only inventory: 2,414 files, 2,325 tracked, 89 untracked, 80.02 MiB logical / approximately 88 MiB allocated. Presentation files account for 60.49 MiB logical. Existing source and document summaries are not interchangeable.
* C2: SHA-256 comparison with docs found six exact duplicate files totalling 8.5 MiB. Preview folders contain 134 images / 31.72 MiB, not all independently verified disposable.
* C3: Current docs/GitHub Markdown links resolve to 24 tracking targets. RAI baseline report, original PRD challenges and historical validation provenance are unique and must survive any relocation. Historical log entries remain unchanged; compatibility pointers may be necessary.
* C4: Latest untracked presentation directory contains the sole six-page native builder, manifest, original baseline and validation records. Preserve before moving or deleting. Current canonical PPTX/PDF and cost guards are protected.
* C5: PR 438 is OPEN, head docs/capstone-cowork-story at baf35acf; branch starts clean except the above untracked folder. User explicitly selected this branch for the cleanup.
* C6: PR review API lists six unresolved threads: destructive diagram rebuild; caller return navigation; exact deck registry/size; LIVE status labels; deck-selection test; missing current-v2 inputs/authority in portable handoff. The first five have apparent existing corrections; verify rather than repeat. Correct the last in README and COWORK-BRIEF.

## Investigation and Counter-Evidence
* Wider: prior inventory, hashes, document links and current source-code references establish the folder is not application runtime data.
* Deeper: source builder depends on original.pptx; mentor YAML/content and historical original reviews are not reconstructed from published PPTX or prose summaries.
* Contrarian: do not interpret age, lack of an inbound link, byte duplication or a green test as sufficient deletion authority. Build output copies can remain inputs to Verify/Render. Tracked deletion does not shrink Git history; untracked deletion is not Git-recoverable.

## Selected Approach and Limits
Use one verified external archive plus per-path checksums before pruning. Promote reusable native-slide tooling and important report sources, update active links, preserve historical-link compatibility and original adverse findings. Select generated or retired presentation artifacts explicitly; retain unknown active RPI work and original reviews unless their preservation and replacement are established. Do not archive secrets or inspect private datasets. Keep current task artifacts in tracking.
