# Research: #134 extension E2 (Source facts omission)

Date: 2026-11-11. Evidence: independent report [/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/independent-134-extension1-b2d273-1111.json](/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/independent-134-extension1-b2d273-1111.json), verdict request_changes, one High. Original C1-C5, the original High and the E1 author Review are preserved unchanged.

* Confirmed in role-screens.js lines 577-583: Technical Source facts renders the selected home's query id, source ids, values and owner. It was missing from RECORD_PANELS. Checker defect, not demonstrated product disclosure.
* Audit of the six renderer blocks (screenPanel literals) against the inventory found further selected-home panels omitted: Asset Eligibility (names the resolution owner), Technical Returns and routing and Missing references, Resident Paused or withdrawn, Linked update commitment and Service requests. Others are portfolio or static and are listed as audited-other.
* Execution defects to fix: retain full raw stdout, stderr and numeric exit for each command; record the real browser version.
* Main e691255ff7 not integrated; no overlap. Readiness: Ready, local only. R1 (A4 reading of ZF-2) stays unresolved.
