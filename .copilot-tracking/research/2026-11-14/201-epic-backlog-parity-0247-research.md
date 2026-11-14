# Research: parity matrix old-path guard (Refs #201 criterion 7)

* Disposition: executed. Planning Readiness: Ready.
* Parent 2bb30b403 guards code and workflows only.
* docs/architecture/cutover-parity-audit.tsv: 130 rows; 116 migrate and 1 rebuild (assistants.py, partial, dispatch worker not deployed) all target src/ files that exist; 12 retire and 1 archive have no target.
* mvp-to-src-parity-matrix.md 'Issues to Reopen' rows (#151, #175) dispose to M5/M3 moves into src/.
* cutover-evidence-pack.md row 7 records #113, #136, #165, #157, #149 with no open PR on old paths (timestamped 2026-10-21 observation, not completion proof).
* Limit: matrix has no per-epic column; guard is repository-wide over all rows.
