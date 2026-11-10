# Research: integrate #1258 C6 parent candidate into the #136 Blob Bicep child (Refs #136, #1258)

Date 2026-11-09. Disposition: executed (read-only git/tool inspection). Planning Readiness: Ready. Prospective: no merge, edit or check had run when written. Agent: rpi-agent, Claude Sonnet 5.5, session 62941c90-be96-4601-a097-895e310d18c1.

## Findings

* Child HEAD `fba4273a4ddc264c90e5bf4ca174e87645b52019` (tree `e6ce2c860ae7670dc2332d6ddbf91aae9c61597e`), clean, branch `feat/ranking-blob-bicep-136-1109`. It contains the prior frozen parent `9b1e2567c2d0a2173b562103cd27508f75181526` (merge base with the new parent) but NOT main `5c3b8b4be`.
* New parent candidate `99814198079c7c8fcd641497826986c706627b0f`, tree `0658fe7f883c5efa09ca286cb026be5cde16ada9`, is a local commit object, clean per the brief; independent parent Functional review `362c0bec-b992-4f6f-bb93-4a6c5506c8a6` is still RUNNING, so publication stays blocked and the pin may change (then record a refresh, preserve qualified source).
* Parent delta over the merge base is `1a84b3b`-era main advances (simulator controls, lifecycle, chat, rubric) merged at `cf8dbc285` plus C6 typing/format of the Blob tests (`99814198`). `git diff 9b1e2567c 99814198 -- infra` is empty and only `.github/rubric/scores/latest.json` changes under `.github`; the child changes only `infra/` and its records, so file overlap is nil. `git merge-tree --write-tree HEAD 99814198` is clean, predicted tree `0714b2bc260d35b7c3f09251310341b10d59684c`. Both README intents (`src/core/README.md` and `src/api/README.md` from main/parent; `infra/README.md` from the child) live in different files. Current `origin/main` is `1a84b3b0054990262a0df0625d95e3f545d2739a`, which is newer than the brief's `5c3b8b4be`; it is not merged and not imported here (the parent contains `5c3b8b4be`).
* Env contract constants `ZF_RANKING_ARCHIVE` and `ZF_RANKING_BLOB_CONTAINER` are expected unchanged by C6 (typing and format of tests); verify by grep after merge.
* Review-correction budget for this child: 1 productive cycle of 5 spent, 4 remain. Integration and evidence work does not consume a source cycle; a genuine source fix would need its own prospective plan and no automatic new grant.
* Tool versions: ruff 0.17.3 local (CI pins `ruff==0.17.1` in `.github/workflows/src-ci.yml`); Python 3.12.3; az bicep present. Formatting is checked only on files this child changed; no existing-line sweep.

## Absent, not claimed

Runtime, WORM or immutability lock, approved retention duration, folder-record migration, container-scoped role (account-scope Blob Data Contributor still permits delete), emulator or real-account behaviour, deployment. No Docker, browser, SQL, cloud what-if, identity grant, storage-account call, private credential or model call.
